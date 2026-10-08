"""
app.py
Main Flask Application for AI-Based Student Career Guidance System.
Integrates HTML/Bootstrap Frontend, Python AI Recommendation Engine, and SQLite Database.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
import re
import database as db
import recommendation_engine as engine

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "fai_career_guidance_secret_key_2026_xyz")

# Initialize database schema on startup
with app.app_context():
    db.init_db()

# Helper function to get current student or None
def get_current_student():
    student_id = session.get("student_id")
    if not student_id:
        return None
    return db.get_student(student_id)

# ------------------------------------------------------------------------------
# 1. HOME ROUTE
# ------------------------------------------------------------------------------
@app.route("/")
def index():
    student = get_current_student()
    return render_template("index.html", student=student)

# ------------------------------------------------------------------------------
# 2. PROFILE ROUTES
# ------------------------------------------------------------------------------
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        age_str = request.form.get("age", "").strip()
        email = request.form.get("email", "").strip()
        education = request.form.get("education", "").strip()
        course = request.form.get("course", "").strip()
        academic_year = request.form.get("academic_year", "").strip()
        favorite_subjects = request.form.get("favorite_subjects", "").strip()
        interests = request.form.get("interests", "").strip()

        # Validation
        errors = []
        if not name or len(name) < 2:
            errors.append("Please enter a valid student name.")
        
        try:
            age = int(age_str)
            if age < 12 or age > 70:
                errors.append("Please enter a valid age between 12 and 70.")
        except (ValueError, TypeError):
            errors.append("Please enter a numeric age.")

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not email or not re.match(email_regex, email):
            errors.append("Please enter a valid email address.")

        valid_educations = ["10th", "12th", "Diploma", "Undergraduate", "Postgraduate", "Other"]
        if education not in valid_educations:
            errors.append("Please select a valid education level.")

        if not favorite_subjects:
            errors.append("Please enter your favorite subjects.")
        if not interests:
            errors.append("Please enter your main areas of interest.")

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("profile.html", form_data=request.form)

        # Store in SQLite
        student_id = db.create_student(
            name=name,
            age=age,
            email=email,
            education=education,
            course=course,
            academic_year=academic_year,
            favorite_subjects=favorite_subjects,
            interests=interests
        )

        # Save student_id in session
        session["student_id"] = student_id
        flash(f"Welcome, {name}! Your profile has been created. Please complete the career assessment.", "success")
        return redirect(url_for("assessment"))

    # GET request
    student = get_current_student()
    return render_template("profile.html", student=student)

# ------------------------------------------------------------------------------
# 3. ASSESSMENT ROUTES
# ------------------------------------------------------------------------------
@app.route("/assessment")
def assessment():
    student = get_current_student()
    if not student:
        flash("Please fill in your student profile before taking the assessment.", "warning")
        return redirect(url_for("profile"))

    # Fetch any existing responses if resuming
    existing_responses = db.get_assessment_responses(student["id"])

    return render_template(
        "assessment.html",
        student=student,
        categories=engine.ASSESSMENT_CATEGORIES,
        questions=engine.ASSESSMENT_QUESTIONS,
        existing_responses=existing_responses
    )

@app.route("/submit-assessment", methods=["POST"])
def submit_assessment():
    student = get_current_student()
    if not student:
        flash("Your session has expired. Please create your profile again.", "warning")
        return redirect(url_for("profile"))

    responses = {}
    missing_questions = []

    # Validate all 30 questions
    for q in engine.ASSESSMENT_QUESTIONS:
        qid = q["id"]
        val = request.form.get(f"q{qid}")
        if not val or not val.strip():
            missing_questions.append(qid)
        else:
            responses[qid] = val.strip()

    if missing_questions:
        flash(f"Please answer all 30 questions. You have unanswered questions: Q{', Q'.join(str(x) for x in missing_questions[:5])}{'...' if len(missing_questions) > 5 else ''}", "danger")
        return render_template(
            "assessment.html",
            student=student,
            categories=engine.ASSESSMENT_CATEGORIES,
            questions=engine.ASSESSMENT_QUESTIONS,
            existing_responses=responses
        )

    # Save responses in SQLite
    db.save_assessment_responses(student["id"], responses)

    # Run AI Career Recommendation Engine
    career_evaluations = engine.evaluate_career_compatibility(student, responses)

    # Save career recommendations in SQLite
    db.save_career_results(student["id"], career_evaluations)

    flash("Assessment successfully analyzed! Here are your personalized career recommendations.", "success")
    return redirect(url_for("results"))

# ------------------------------------------------------------------------------
# 4. RESULTS DASHBOARD
# ------------------------------------------------------------------------------
@app.route("/results")
def results():
    student = get_current_student()
    if not student:
        flash("Please complete your profile and assessment to view career results.", "warning")
        return redirect(url_for("profile"))

    responses = db.get_assessment_responses(student["id"])
    if not responses or len(responses) < 30:
        flash("Please complete the 30-question assessment first.", "warning")
        return redirect(url_for("assessment"))

    # Fetch career evaluations from DB or recompute
    career_results = db.get_career_results(student["id"])
    if not career_results:
        career_evaluations = engine.evaluate_career_compatibility(student, responses)
        db.save_career_results(student["id"], career_evaluations)
        career_results = db.get_career_results(student["id"])

    # Top 3 to 5 recommendations
    top_careers = career_results[:5]

    # Enrich with catalog details (skills, roles, description)
    enriched_top = []
    for c in top_careers:
        cat_info = engine.CAREER_CATALOG.get(c["career"], {})
        enriched_top.append({
            "career": c["career"],
            "score": c["score"],
            "explanation": c["explanation"],
            "category": cat_info.get("category", "General"),
            "description": cat_info.get("description", ""),
            "required_skills": cat_info.get("required_skills", []),
            "possible_roles": cat_info.get("possible_roles", []),
            "work_type": cat_info.get("work_type", ""),
            "education": cat_info.get("education", "")
        })

    # Compute Skill Profile for Chart.js Radar Chart
    skill_profile = engine.calculate_skill_profile(responses)

    # Data for Career Compatibility Bar Chart (Top 6 careers)
    all_evaluations = engine.evaluate_career_compatibility(student, responses)
    chart_careers = [c["career"] for c in all_evaluations[:6]]
    chart_scores = [c["score"] for c in all_evaluations[:6]]

    return render_template(
        "results.html",
        student=student,
        top_careers=enriched_top,
        skill_profile=skill_profile,
        chart_careers=chart_careers,
        chart_scores=chart_scores,
        strongest_skill=responses.get(10, "Problem Solving"),
        strongest_subject=responses.get(23, student.get("favorite_subjects", "N/A"))
    )

# ------------------------------------------------------------------------------
# 5. CAREER COMPARISON ROUTE
# ------------------------------------------------------------------------------
@app.route("/comparison")
def comparison():
    student = get_current_student()
    if not student:
        flash("Please complete your assessment first.", "warning")
        return redirect(url_for("profile"))

    career_results = db.get_career_results(student["id"])
    if not career_results:
        flash("No assessment results found. Please take the assessment first.", "warning")
        return redirect(url_for("assessment"))

    # Compare top 4 careers
    comparison_list = []
    for c in career_results[:4]:
        info = engine.CAREER_CATALOG.get(c["career"], {})
        comparison_list.append({
            "career": c["career"],
            "score": c["score"],
            "category": info.get("category", ""),
            "main_skills": ", ".join(info.get("required_skills", [])[:4]),
            "work_type": info.get("work_type", "Standard"),
            "education": info.get("education", "Bachelor's Degree"),
            "growth_outlook": info.get("growth_outlook", "Steady"),
            "explanation": c["explanation"]
        })

    return render_template("comparison.html", student=student, comparisons=comparison_list)

# ------------------------------------------------------------------------------
# 6. SKILL GAP ANALYSIS ROUTE
# ------------------------------------------------------------------------------
@app.route("/skill-gap")
def skill_gap():
    student = get_current_student()
    if not student:
        flash("Please complete your assessment first.", "warning")
        return redirect(url_for("profile"))

    responses = db.get_assessment_responses(student["id"])
    if not responses:
        flash("Please complete your assessment first.", "warning")
        return redirect(url_for("assessment"))

    career_results = db.get_career_results(student["id"])
    top_career_name = career_results[0]["career"] if career_results else "Software Developer"

    # Allow user to toggle career via query parameter
    selected_career = request.args.get("career", top_career_name)
    if selected_career not in engine.CAREER_CATALOG:
        selected_career = top_career_name

    gap_data = engine.get_skill_gap_analysis(selected_career, student, responses)

    # Top recommended career names for dropdown selector
    available_careers = [c["career"] for c in career_results[:5]] if career_results else list(engine.CAREER_CATALOG.keys())[:5]

    return render_template(
        "skill_gap.html",
        student=student,
        gap_data=gap_data,
        selected_career=selected_career,
        available_careers=available_careers
    )

# ------------------------------------------------------------------------------
# 7. PERSONALIZED ROADMAP ROUTE
# ------------------------------------------------------------------------------
@app.route("/roadmap")
def roadmap():
    student = get_current_student()
    if not student:
        flash("Please complete your assessment first.", "warning")
        return redirect(url_for("profile"))

    career_results = db.get_career_results(student["id"])
    top_career_name = career_results[0]["career"] if career_results else "Software Developer"

    selected_career = request.args.get("career", top_career_name)
    if selected_career not in engine.CAREER_CATALOG:
        selected_career = top_career_name

    roadmap_steps = engine.get_career_roadmap(selected_career)
    career_info = engine.CAREER_CATALOG.get(selected_career, {})

    available_careers = [c["career"] for c in career_results[:5]] if career_results else list(engine.CAREER_CATALOG.keys())[:5]

    return render_template(
        "roadmap.html",
        student=student,
        roadmap_steps=roadmap_steps,
        selected_career=selected_career,
        career_info=career_info,
        available_careers=available_careers
    )

# ------------------------------------------------------------------------------
# 8. AI CAREER ASSISTANT ROUTE
# ------------------------------------------------------------------------------
@app.route("/assistant", methods=["GET", "POST"])
def assistant():
    student = get_current_student()
    if not student:
        flash("Please complete your profile to enable personalized career assistance.", "warning")
        return redirect(url_for("profile"))

    career_results = db.get_career_results(student["id"])
    responses = db.get_assessment_responses(student["id"])

    response_text = None
    query_text = ""

    if request.method == "POST":
        query_text = request.form.get("query", "").strip()
        if query_text:
            response_text = engine.generate_ai_assistant_response(query_text, student, career_results, responses)

    sample_questions = [
        "Which career is best for me?",
        "What skills should I learn?",
        "How can I become a Data Scientist?",
        "What should I study after 12th?",
        "Which career matches my interests?",
        "What skills should I improve?",
        "What is the roadmap for becoming a Software Developer?"
    ]

    return render_template(
        "assistant.html",
        student=student,
        query_text=query_text,
        response_text=response_text,
        sample_questions=sample_questions,
        top_career=career_results[0]["career"] if career_results else "Software Developer"
    )

@app.route("/assistant/query", methods=["POST"])
def assistant_query():
    """Asynchronous JSON endpoint for real-time chat with the AI Assistant."""
    student = get_current_student()
    if not student:
        return jsonify({"success": False, "error": "Session expired. Please refresh."}), 401

    data = request.get_json() or {}
    query_text = data.get("query", "").strip()

    if not query_text:
        return jsonify({"success": False, "error": "Query cannot be empty."}), 400

    career_results = db.get_career_results(student["id"])
    responses = db.get_assessment_responses(student["id"])

    ai_reply = engine.generate_ai_assistant_response(query_text, student, career_results, responses)
    return jsonify({"success": True, "reply": ai_reply})

# ------------------------------------------------------------------------------
# 9. STUDENT FEEDBACK ROUTES
# ------------------------------------------------------------------------------
@app.route("/feedback", methods=["GET"])
def feedback():
    student = get_current_student()
    existing_feedback = db.get_feedback(student["id"]) if student else None
    return render_template("feedback.html", student=student, existing_feedback=existing_feedback)

@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    student = get_current_student()
    student_id = student["id"] if student else None

    usefulness = request.form.get("usefulness", "").strip()
    satisfaction = request.form.get("satisfaction", "").strip()
    interest_match = request.form.get("interest_match", "").strip()
    ease_of_use = request.form.get("ease_of_use", "").strip()
    positive_feedback = request.form.get("positive_feedback", "").strip()
    improvement_feedback = request.form.get("improvement_feedback", "").strip()

    errors = []
    if not usefulness:
        errors.append("Please rate how useful the career assessment was.")
    if not satisfaction:
        errors.append("Please rate your satisfaction with the recommendations.")
    if not interest_match:
        errors.append("Please indicate whether recommendations matched your interests.")
    if not ease_of_use:
        errors.append("Please rate the ease of understanding the assessment.")

    if errors:
        for err in errors:
            flash(err, "danger")
        return render_template("feedback.html", student=student, form_data=request.form)

    # Save to SQLite
    db.save_feedback(
        student_id=student_id,
        usefulness=usefulness,
        satisfaction=satisfaction,
        interest_match=interest_match,
        ease_of_use=ease_of_use,
        positive_feedback=positive_feedback,
        improvement_feedback=improvement_feedback
    )

    return render_template("feedback.html", student=student, submitted=True)

# ------------------------------------------------------------------------------
# 10. SESSION RESET / RESTART
# ------------------------------------------------------------------------------
@app.route("/reset")
def reset():
    session.clear()
    flash("Session reset. You can start a fresh assessment now.", "info")
    return redirect(url_for("profile"))

# ------------------------------------------------------------------------------
# 11. ERROR HANDLERS
# ------------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template("base.html", error_title="404 - Page Not Found", error_message="The page you requested could not be located."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("base.html", error_title="500 - Application Error", error_message="An unexpected system error occurred. Please try again."), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
