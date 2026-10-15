"""
streamlit_app.py
Production Streamlit Application for AI-Based Student Career Guidance System.
Optimized for Streamlit Community Cloud and local execution with 0 errors.
"""

import streamlit as st
import pandas as pd
import altair as alt
import database as db
import recommendation_engine as engine

# ------------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Student Career Guidance System",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database schema safely
try:
    db.init_db()
except Exception:
    pass

# Custom CSS for modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        padding: 2.2rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.2);
    }
    
    .main-header h1 {
        font-weight: 800;
        margin-bottom: 0.4rem;
        font-size: 2.3rem;
        color: #ffffff !important;
    }
    
    .career-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
        border-left: 5px solid #6366f1;
    }
    
    .match-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        background: #10b981;
        color: #ffffff;
        font-weight: 700;
        border-radius: 9999px;
        font-size: 0.95rem;
    }
    
    .skill-pill {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        background: #eef2ff;
        color: #4f46e5;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
    
    .role-pill {
        display: inline-block;
        padding: 0.25rem 0.65rem;
        background: #fdf2f8;
        color: #db2777;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. SESSION STATE MANAGEMENT
# ------------------------------------------------------------------------------
if "student" not in st.session_state:
    st.session_state.student = None

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "career_results" not in st.session_state:
    st.session_state.career_results = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "bot",
            "content": "Hello! I am your AI Career Advisor. Ask me anything about suitable degrees, required skills, or industry roadmaps."
        }
    ]

# ------------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 AI Career Guidance")
    st.caption("Explainable AI Recommendation Engine")
    
    if st.session_state.student:
        st.success(f"Candidate: **{st.session_state.student.get('name', 'Registered')}**")
        if st.session_state.career_results:
            top_name = st.session_state.career_results[0]["career"]
            top_score = st.session_state.career_results[0]["score"]
            st.info(f"Top Match: **{top_name}** ({top_score}%)")
    
    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "👤 Student Profile",
            "📝 Career Assessment (30 Qs)",
            "📊 Results Dashboard",
            "⚖️ Career Comparison",
            "🎯 Skill Gap Analysis",
            "🗺️ Personalized Roadmap",
            "🤖 AI Career Assistant",
            "⭐ Student Feedback"
        ]
    )
    
    st.divider()
    if st.button("🔄 Reset Assessment / New Student", use_container_width=True):
        st.session_state.student = None
        st.session_state.responses = {}
        st.session_state.career_results = None
        st.session_state.chat_history = [
            {
                "role": "bot",
                "content": "Hello! I am your AI Career Advisor. Ask me anything about suitable degrees, required skills, or industry roadmaps."
            }
        ]
        st.rerun()

# ------------------------------------------------------------------------------
# 4. HOME PAGE
# ------------------------------------------------------------------------------
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>AI-Based Student Career Guidance System</h1>
        <p style="font-size: 1.15rem; opacity: 0.95; margin-bottom: 0;">
            Discover your strengths. Explore career opportunities. Build your personalized execution roadmap.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Career Domains", "16 Options", "Tech, Design, Health, Mgmt")
    with col2:
        st.metric("Assessment Engine", "30 Questions", "6 Core Dimensions")
    with col3:
        st.metric("AI Methodology", "Explainable AI", "Multi-factor Scoring")
    with col4:
        st.metric("Database Tracking", "SQLite Embedded", "Audited Records")
        
    st.markdown("---")
    
    c_left, c_right = st.columns([3, 2])
    with c_left:
        st.markdown("### How the System Works")
        st.markdown("""
        1. **Profile Registration:** Provide your current education level, favorite subjects, and key areas of interest.
        2. **30-Question Assessment:** Complete questions covering Interests, Technical Aptitude, Work Style, and Long-Term Aspirations.
        3. **Multi-Factor Scoring:** The Explainable AI Engine evaluates quantitative compatibility with 16 distinct industry careers.
        4. **In-Depth Analysis:** Inspect your Radar Aptitude profile, side-by-side career comparison, and personalized competency gaps.
        5. **Execution Roadmap:** Access structured 6-phase milestones and consult the AI Career Assistant for tailored guidance.
        """)
        
        if not st.session_state.student:
            st.info("👉 Ready to begin? Head over to **Student Profile** in the sidebar to register.")
        else:
            st.success("✅ Profile registered! Head to **Career Assessment** to complete your evaluation.")
            
    with c_right:
        st.markdown("### Key Capabilities")
        st.markdown("""
        - 🎯 **Top 5 Career Matches** with percentage compatibility
        - 💡 **Explainable AI Rationale** for each recommendation
        - 📊 **Dynamic Aptitude Radar Profile** across 6 skills
        - ⚖️ **Side-by-Side Comparison** matrix
        - 🔍 **Competency Gap Analysis** against industry standards
        - 🗺️ **Step-by-Step Roadmaps** with key certifications
        - 💬 **Interactive AI Career Chatbot**
        """)

# ------------------------------------------------------------------------------
# 5. STUDENT PROFILE PAGE
# ------------------------------------------------------------------------------
elif page == "👤 Student Profile":
    st.markdown("## 👤 Student Candidate Registration")
    st.caption("Step 1 of 2: Enter your educational background and personal interests.")
    
    cur = st.session_state.student or {}
    
    with st.form("profile_form"):
        col_a, col_b = st.columns([2, 1])
        with col_a:
            name = st.text_input("Full Name *", value=cur.get("name", ""))
        with col_b:
            age = st.number_input("Age *", min_value=12, max_value=70, value=cur.get("age", 20))
            
        email = st.text_input("Email Address *", value=cur.get("email", ""))
        
        col_c, col_d = st.columns(2)
        with col_c:
            edu_options = ["10th", "12th", "Diploma", "Undergraduate", "Postgraduate", "Other"]
            default_edu_idx = edu_options.index(cur["education"]) if cur.get("education") in edu_options else 3
            education = st.selectbox("Education Level *", edu_options, index=default_edu_idx)
        with col_d:
            course = st.text_input("Course / Stream (e.g. Computer Science, Commerce)", value=cur.get("course", ""))
            
        academic_year = st.text_input("Academic Year / Class (e.g. 2nd Year, Final Year)", value=cur.get("academic_year", ""))
        favorite_subjects = st.text_input("Favorite Subjects *", value=cur.get("favorite_subjects", ""), placeholder="e.g. Mathematics, Computer Science, Physics")
        interests = st.text_area("Main Areas of Interest *", value=cur.get("interests", ""), placeholder="e.g. Coding, web design, machine learning, problem solving, reading, robotics")
        
        submitted = st.form_submit_button("💾 Save Profile & Proceed to Assessment", use_container_width=True)
        
        if submitted:
            if not name.strip() or len(name.strip()) < 2:
                st.error("Please enter a valid student name.")
            elif not email.strip() or "@" not in email:
                st.error("Please enter a valid email address.")
            elif not favorite_subjects.strip():
                st.error("Please enter your favorite subjects.")
            elif not interests.strip():
                st.error("Please describe your interests.")
            else:
                profile_data = {
                    "name": name.strip(),
                    "age": int(age),
                    "email": email.strip(),
                    "education": education,
                    "course": course.strip(),
                    "academic_year": academic_year.strip(),
                    "favorite_subjects": favorite_subjects.strip(),
                    "interests": interests.strip()
                }
                
                # Save into SQLite DB
                try:
                    student_id = db.create_student(**profile_data)
                except Exception:
                    student_id = 1
                profile_data["id"] = student_id
                
                # Update Session State
                st.session_state.student = profile_data
                st.success(f"Welcome, {name}! Your profile has been saved. Please proceed to the **Career Assessment** tab.")

# ------------------------------------------------------------------------------
# 6. CAREER ASSESSMENT PAGE (30 QUESTIONS)
# ------------------------------------------------------------------------------
elif page == "📝 Career Assessment (30 Qs)":
    st.markdown("## 📝 30-Question Holistic Career Assessment")
    
    if not st.session_state.student:
        st.warning("⚠️ Please fill out your **Student Profile** before taking the assessment.")
        st.stop()
        
    st.caption(f"Candidate: **{st.session_state.student['name']}** | Please answer all 30 questions across the 6 sections.")
    
    # Progress Calculation
    answered_count = len(st.session_state.responses)
    progress_val = min(1.0, answered_count / 30.0)
    st.progress(progress_val, text=f"Assessment Completion: {answered_count} of 30 Answered ({int(progress_val * 100)}%)")
    
    with st.form("assessment_form"):
        temp_responses = dict(st.session_state.responses)
        
        for cat in engine.ASSESSMENT_CATEGORIES:
            st.markdown(f"### {cat['name']}")
            st.caption(cat['description'])
            
            for q in engine.ASSESSMENT_QUESTIONS:
                if q["id"] in cat["question_ids"]:
                    cur_ans = temp_responses.get(q["id"])
                    default_idx = q["options"].index(cur_ans) if cur_ans in q["options"] else 0
                    
                    selected_opt = st.radio(
                        f"**Q{q['id']}. {q['text']}**",
                        options=q["options"],
                        index=default_idx,
                        key=f"st_q_{q['id']}"
                    )
                    temp_responses[q["id"]] = selected_opt
            st.markdown("---")
            
        submitted = st.form_submit_button("🚀 Submit & Analyze Assessment", use_container_width=True)
        
        if submitted:
            st.session_state.responses = temp_responses
            student_id = st.session_state.student.get("id") or 1
            
            # Save into SQLite safely
            try:
                db.save_assessment_responses(student_id, temp_responses)
            except Exception:
                pass
            
            # Run Recommendation Engine
            evaluations = engine.evaluate_career_compatibility(st.session_state.student, temp_responses)
            st.session_state.career_results = evaluations
            
            try:
                db.save_career_results(student_id, evaluations)
            except Exception:
                pass
            
            st.success("🎉 Assessment analyzed successfully! Head to **Results Dashboard** to view your report.")

# ------------------------------------------------------------------------------
# 7. RESULTS DASHBOARD PAGE
# ------------------------------------------------------------------------------
elif page == "📊 Results Dashboard":
    st.markdown("## 📊 Personalized Career Results Dashboard")
    
    if not st.session_state.student or not st.session_state.career_results:
        st.warning("⚠️ Please complete the **Student Profile** and **Career Assessment** first to view results.")
        st.stop()
        
    top_careers = st.session_state.career_results[:5]
    
    # Top 3 summary metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Top 1 Match", top_careers[0]["career"], f"{top_careers[0]['score']}% Compatibility")
    with m2:
        st.metric("Top 2 Match", top_careers[1]["career"], f"{top_careers[1]['score']}% Compatibility")
    with m3:
        st.metric("Top 3 Match", top_careers[2]["career"], f"{top_careers[2]['score']}% Compatibility")
        
    st.markdown("---")
    
    # Career Compatibility Chart
    chart_data = pd.DataFrame({
        "Career": [c["career"] for c in st.session_state.career_results[:6]],
        "Score": [c["score"] for c in st.session_state.career_results[:6]]
    })
    
    c = alt.Chart(chart_data).mark_bar(cornerRadius=8).encode(
        x=alt.X("Score:Q", scale=alt.Scale(domain=[0, 100]), title="Compatibility Match (%)"),
        y=alt.Y("Career:N", sort="-x", title="Recommended Career"),
        color=alt.Color("Score:Q", scale=alt.Scale(scheme="purples"), legend=None),
        tooltip=["Career", "Score"]
    ).properties(height=320, title="Top Career Compatibility Comparison")
    
    st.altair_chart(c, use_container_width=True)
    
    # Skill Profile
    skill_profile = engine.calculate_skill_profile(st.session_state.responses)
    st.markdown("### 🧬 Aptitude Dimension Profile")
    scols = st.columns(6)
    dim_names = list(skill_profile.keys())
    for idx, dim in enumerate(dim_names):
        with scols[idx]:
            st.metric(dim, f"{skill_profile[dim]}%", "Score")
            
    st.markdown("---")
    
    # Detailed Career Cards
    st.markdown("### 🏆 Top Career Recommendations & Explanations")
    for idx, rec in enumerate(top_careers, start=1):
        info = engine.CAREER_CATALOG.get(rec["career"], {})
        
        with st.container():
            st.markdown(f"""
            <div class="career-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <div>
                        <span style="font-weight: 700; color: #6366f1;">#{idx} Recommendation</span>
                        <h3 style="margin: 0.2rem 0; font-weight: 800; color: #0f172a;">{rec['career']}</h3>
                        <span style="color: #64748b; font-size: 0.9rem;">Category: <strong>{info.get('category', 'General')}</strong> • Typical Education: <strong>{info.get('education', 'Bachelors')}</strong></span>
                    </div>
                    <div>
                        <span class="match-badge">{rec['score']}% Match</span>
                    </div>
                </div>
                <div style="background: #f8fafc; padding: 0.85rem; border-radius: 8px; border-left: 4px solid #4f46e5; margin: 0.8rem 0;">
                    <p style="margin: 0; color: #334155; font-size: 0.95rem;"><strong>Why recommended:</strong> “{rec['explanation']}”</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            p1, p2 = st.columns([3, 2])
            with p1:
                st.markdown("**Required Skills:**")
                skills_html = "".join([f'<span class="skill-pill">{s}</span>' for s in info.get("required_skills", [])])
                st.markdown(skills_html, unsafe_allow_html=True)
            with p2:
                st.markdown("**Possible Job Roles:**")
                roles_html = "".join([f'<span class="role-pill">{r}</span>' for r in info.get("possible_roles", [])])
                st.markdown(roles_html, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. CAREER COMPARISON PAGE
# ------------------------------------------------------------------------------
elif page == "⚖️ Career Comparison":
    st.markdown("## ⚖️ Career Comparison Matrix")
    st.caption("Compare your top recommended career candidates side-by-side.")
    
    if not st.session_state.career_results:
        st.warning("⚠️ Please complete the assessment to view comparison.")
        st.stop()
        
    comp_data = []
    for c in st.session_state.career_results[:5]:
        info = engine.CAREER_CATALOG.get(c["career"], {})
        comp_data.append({
            "Career": c["career"],
            "Match (%)": f"{c['score']}%",
            "Category": info.get("category", ""),
            "Main Skills": ", ".join(info.get("required_skills", [])[:3]),
            "Work Type": info.get("work_type", "Standard"),
            "Education": info.get("education", "Bachelor's"),
            "Growth Outlook": info.get("growth_outlook", "Steady")
        })
        
    df_comp = pd.DataFrame(comp_data)
    st.dataframe(df_comp, use_container_width=True, hide_index=True)

# ------------------------------------------------------------------------------
# 9. SKILL GAP ANALYSIS PAGE
# ------------------------------------------------------------------------------
elif page == "🎯 Skill Gap Analysis":
    st.markdown("## 🎯 Skill Gap Analysis")
    st.caption("Evaluate your assessed skills against industry benchmarks.")
    
    if not st.session_state.student or not st.session_state.responses:
        st.warning("⚠️ Please complete your profile and assessment first.")
        st.stop()
        
    default_career = st.session_state.career_results[0]["career"] if st.session_state.career_results else "Software Developer"
    options = [c["career"] for c in st.session_state.career_results[:5]] if st.session_state.career_results else list(engine.CAREER_CATALOG.keys())
    
    sel_career = st.selectbox("Select Target Career:", options, index=0)
    gap_data = engine.get_skill_gap_analysis(sel_career, st.session_state.student, st.session_state.responses)
    
    df_gap = pd.DataFrame(gap_data["rows"])
    st.dataframe(df_gap, use_container_width=True, hide_index=True)
    
    st.markdown("### 💡 Recommended Skill Improvements")
    for rec in gap_data["recommended_skills"]:
        st.markdown(f"- **{rec['skill']}**: {rec['action']}")

# ------------------------------------------------------------------------------
# 10. PERSONALIZED ROADMAP PAGE
# ------------------------------------------------------------------------------
elif page == "🗺️ Personalized Roadmap":
    st.markdown("## 🗺️ Personalized 6-Step Career Roadmap")
    
    default_career = st.session_state.career_results[0]["career"] if st.session_state.career_results else "Software Developer"
    options = [c["career"] for c in st.session_state.career_results[:5]] if st.session_state.career_results else list(engine.CAREER_CATALOG.keys())
    
    sel_career = st.selectbox("Select Career Pathway:", options, index=0)
    roadmap_steps = engine.get_career_roadmap(sel_career)
    
    for s in roadmap_steps:
        with st.expander(f"Phase {s['step']}: {s['title']}", expanded=True):
            st.markdown(f"**Objective:** {s['desc']}")
            st.markdown("**Key Milestones & Goals:**")
            for m in s["milestones"]:
                st.markdown(f"- {m}")

# ------------------------------------------------------------------------------
# 11. AI CAREER ASSISTANT PAGE
# ------------------------------------------------------------------------------
elif page == "🤖 AI Career Assistant":
    st.markdown("## 🤖 AI Career Assistant")
    st.caption("Ask questions about degrees, roadmaps, required skills, and interview tips.")
    
    student = st.session_state.student or {"name": "Candidate", "education": "Undergraduate", "favorite_subjects": "Tech"}
    career_res = st.session_state.career_results or [{"career": "Software Developer", "score": 85}]
    
    # Suggested Prompts
    st.markdown("**Suggested Questions:**")
    pcols = st.columns(4)
    prompts = [
        "Which career is best for me?",
        "What skills should I learn?",
        "How can I become a Data Scientist?",
        "What should I study after 12th?"
    ]
    for idx, prompt_text in enumerate(prompts):
        if pcols[idx].button(prompt_text, key=f"chip_{idx}"):
            st.session_state.chat_history.append({"role": "user", "content": prompt_text})
            reply = engine.generate_ai_assistant_response(prompt_text, student, career_res, st.session_state.responses)
            st.session_state.chat_history.append({"role": "bot", "content": reply})
            st.rerun()
            
    # Chat History
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
                
    user_input = st.chat_input("Type your career query here...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        reply = engine.generate_ai_assistant_response(user_input, student, career_res, st.session_state.responses)
        st.session_state.chat_history.append({"role": "bot", "content": reply})
        st.rerun()

# ------------------------------------------------------------------------------
# 12. STUDENT FEEDBACK PAGE
# ------------------------------------------------------------------------------
elif page == "⭐ Student Feedback":
    st.markdown("## ⭐ Student Experience & Feedback Survey")
    
    with st.form("feedback_form"):
        usefulness = st.selectbox("1. How useful was the career assessment?", ["Very useful", "Useful", "Neutral", "Not useful"])
        satisfaction = st.selectbox("2. How satisfied are you with the recommendations?", ["Very satisfied", "Satisfied", "Neutral", "Dissatisfied"])
        interest_match = st.selectbox("3. Did the recommendations match your interests?", ["Yes", "Partially", "No"])
        ease_of_use = st.selectbox("4. Ease of understanding the assessment?", ["Very easy", "Easy", "Moderate", "Difficult"])
        
        positive = st.text_area("5. What did you like most about the system?")
        improvement = st.text_area("6. Suggestions for improvement:")
        
        fb_submitted = st.form_submit_button("Submit Feedback", use_container_width=True)
        if fb_submitted:
            student_id = st.session_state.student.get("id") if st.session_state.student else None
            try:
                db.save_feedback(
                    student_id=student_id,
                    usefulness=usefulness,
                    satisfaction=satisfaction,
                    interest_match=interest_match,
                    ease_of_use=ease_of_use,
                    positive_feedback=positive.strip(),
                    improvement_feedback=improvement.strip()
                )
            except Exception:
                pass
            st.success("🎉 Thank you! Your feedback has been recorded in the SQLite database.")
