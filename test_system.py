"""
test_system.py
Comprehensive automated test suite for the AI-Based Student Career Guidance System.
Verifies Profile A, Profile B, Profile C, Recommendation Engine scoring,
Database operations, and all Flask routes.
"""

import unittest
import json
import os
import sqlite3
from app import app
import database as db
import recommendation_engine as engine

class TestCareerGuidanceSystem(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test_secret_key"
        self.client = app.test_client()
        with app.app_context():
            db.init_db()

    def test_database_tables_exist(self):
        """Verify all required SQLite tables and indexes are created."""
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("students", tables)
        self.assertIn("assessment_responses", tables)
        self.assertIn("career_results", tables)
        self.assertIn("feedback", tables)
        print("[OK] Database tables verified: students, assessment_responses, career_results, feedback")

    def test_profile_a_technology(self):
        """Profile A: Strong technology + mathematics + logical reasoning."""
        student_profile = {
            "name": "Alex Tech",
            "age": 20,
            "email": "alex@tech.edu",
            "education": "Undergraduate",
            "course": "Computer Science",
            "academic_year": "3rd Year",
            "favorite_subjects": "Mathematics, Computer Science, Algorithms",
            "interests": "Coding, machine learning, robotics, solving algorithms"
        }
        student_id = db.create_student(**student_profile)
        self.assertIsNotNone(student_id)

        # Profile A answers: heavy tech/math/logic
        responses = {
            1: "Solving technical problems",
            2: "Computer/IT",
            3: "Coding or experimenting with technology",
            4: "Technical problems",
            5: "Very interested",
            6: "Very confident",
            7: "Excellent",
            8: "Good",
            9: "Very comfortable",
            10: "Technical skills",
            11: "Very good",
            12: "Working independently",
            13: "Logic and facts",
            14: "Comfortable",
            15: "Analyze it step-by-step",
            16: "Analytical",
            17: "Comfortable",
            18: "Technology/IT",
            19: "Working with computers",
            20: "Challenging and competitive",
            21: "Yes",
            22: "80–100%",
            23: "Computer Science",
            24: "Languages",
            25: "Daily",
            26: "Career growth",
            27: "Software/IT",
            28: "Interested",
            29: "Technical professional",
            30: "Very confident"
        }

        db.save_assessment_responses(student_id, responses)
        evals = engine.evaluate_career_compatibility(student_profile, responses)
        top_careers = [e["career"] for e in evals[:3]]

        print(f"Profile A Top 3: {evals[0]['career']} ({evals[0]['score']}%), {evals[1]['career']} ({evals[1]['score']}%), {evals[2]['career']} ({evals[2]['score']}%)")
        self.assertTrue(any(c in top_careers for c in ["Software Developer", "Data Scientist", "AI/ML Engineer"]))
        self.assertGreaterEqual(evals[0]["score"], 80)
        self.assertTrue(len(evals[0]["explanation"]) > 20)

    def test_profile_b_creative_design(self):
        """Profile B: Strong creativity + communication + design interest."""
        student_profile = {
            "name": "Maya Design",
            "age": 19,
            "email": "maya@design.art",
            "education": "Undergraduate",
            "course": "Visual Arts",
            "academic_year": "2nd Year",
            "favorite_subjects": "Arts/Humanities, Design, English",
            "interests": "Drawing, UX prototyping, graphic illustrations, typography"
        }
        student_id = db.create_student(**student_profile)

        # Profile B answers: heavy design/creativity/visual
        responses = {
            1: "Designing or creating things",
            2: "Arts/Humanities",
            3: "Drawing/designing",
            4: "Creative problems",
            5: "Interested",
            6: "Average",
            7: "Good",
            8: "Excellent",
            9: "Comfortable",
            10: "Creativity",
            11: "Good",
            12: "Combination of both",
            13: "Creativity and ideas",
            14: "Comfortable",
            15: "Try creative solutions",
            16: "Creative",
            17: "Very comfortable",
            18: "Creative environment",
            19: "Creating/designing",
            20: "Flexible and creative",
            21: "Yes",
            22: "70–79%",
            23: "Languages",
            24: "Mathematics",
            25: "4–5 days a week",
            26: "Creativity",
            27: "Design",
            28: "Maybe",
            29: "Creative professional",
            30: "Somewhat confident"
        }

        db.save_assessment_responses(student_id, responses)
        evals = engine.evaluate_career_compatibility(student_profile, responses)
        top_careers = [e["career"] for e in evals[:3]]

        print(f"Profile B Top 3: {evals[0]['career']} ({evals[0]['score']}%), {evals[1]['career']} ({evals[1]['score']}%), {evals[2]['career']} ({evals[2]['score']}%)")
        self.assertIn("UI/UX Designer", top_careers)
        self.assertGreaterEqual(evals[0]["score"], 75)

    def test_profile_c_leadership_business(self):
        """Profile C: Strong leadership + business interest + entrepreneurship."""
        student_profile = {
            "name": "Liam Leader",
            "age": 21,
            "email": "liam@business.org",
            "education": "Undergraduate",
            "course": "Business Administration",
            "academic_year": "Final Year",
            "favorite_subjects": "Commerce, Economics, Marketing",
            "interests": "Startups, public speaking, event organizing, corporate leadership"
        }
        student_id = db.create_student(**student_profile)

        # Profile C answers: heavy management/business/entrepreneurship
        responses = {
            1: "Managing or organizing activities",
            2: "Commerce/Economics",
            3: "Organizing events",
            4: "Business problems",
            5: "Interested",
            6: "Good",
            7: "Good",
            8: "Excellent",
            9: "Comfortable",
            10: "Leadership",
            11: "Very good",
            12: "Working with a team",
            13: "Logic and facts",
            14: "Very comfortable",
            15: "Try creative solutions",
            16: "Enterprising",
            17: "Very comfortable",
            18: "Office/Corporate",
            19: "Managing projects",
            20: "Challenging and competitive",
            21: "Yes",
            22: "80–100%",
            23: "Commerce",
            24: "Science",
            25: "Daily",
            26: "Leadership opportunities",
            27: "Business/Management",
            28: "Very interested",
            29: "Entrepreneur",
            30: "Very confident"
        }

        db.save_assessment_responses(student_id, responses)
        evals = engine.evaluate_career_compatibility(student_profile, responses)
        top_careers = [e["career"] for e in evals[:3]]

        print(f"Profile C Top 3: {evals[0]['career']} ({evals[0]['score']}%), {evals[1]['career']} ({evals[1]['score']}%), {evals[2]['career']} ({evals[2]['score']}%)")
        self.assertTrue(any(c in top_careers for c in ["Business Manager", "Entrepreneur"]))
        self.assertGreaterEqual(evals[0]["score"], 80)

    def test_flask_routes_and_assistant(self):
        """Test Flask web routes, session handling, AI query, and feedback."""
        # 1. Home page
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"AI-Based Student Career Guidance System", res.data)

        # 2. Profile post
        profile_data = {
            "name": "Sarah Connor",
            "age": "20",
            "email": "sarah@cyber.net",
            "education": "Undergraduate",
            "course": "IT & Security",
            "academic_year": "2nd Year",
            "favorite_subjects": "Computer Networks, Math",
            "interests": "Cybersecurity, penetration testing, network defense"
        }
        res = self.client.post("/profile", data=profile_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Career Assessment", res.data)

        # 3. Assessment submit (all 30 questions)
        assessment_form = {
            "q1": "Solving technical problems",
            "q2": "Computer/IT",
            "q3": "Coding or experimenting with technology",
            "q4": "Technical problems",
            "q5": "Very interested",
            "q6": "Very confident",
            "q7": "Excellent",
            "q8": "Good",
            "q9": "Very comfortable",
            "q10": "Technical skills",
            "q11": "Very good",
            "q12": "Working independently",
            "q13": "Logic and facts",
            "q14": "Comfortable",
            "q15": "Analyze it step-by-step",
            "q16": "Analytical",
            "q17": "Comfortable",
            "q18": "Technology/IT",
            "q19": "Working with computers",
            "q20": "Challenging and competitive",
            "q21": "Yes",
            "q22": "80–100%",
            "q23": "Computer Science",
            "q24": "Languages",
            "q25": "Daily",
            "q26": "Career growth",
            "q27": "Software/IT",
            "q28": "Interested",
            "q29": "Technical professional",
            "q30": "Very confident"
        }

        res = self.client.post("/submit-assessment", data=assessment_form, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Personalized Career Results Dashboard", res.data)

        # 4. Results page
        res = self.client.get("/results")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Top AI Career Recommendations", res.data)

        # 5. Comparison page
        res = self.client.get("/comparison")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Career Comparison Matrix", res.data)

        # 6. Skill Gap page
        res = self.client.get("/skill-gap")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Competency Comparison Matrix", res.data)

        # 7. Roadmap page
        res = self.client.get("/roadmap")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Personalized Career Roadmap", res.data)

        # 8. AI Assistant query
        res = self.client.post("/assistant/query", json={"query": "Which career is best for me?"})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertIn("compatibility match", data["reply"].lower())

        # 9. Feedback submit
        feedback_data = {
            "usefulness": "Very useful",
            "satisfaction": "Very satisfied",
            "interest_match": "Yes",
            "ease_of_use": "Very easy",
            "positive_feedback": "Accurate career scores and comprehensive roadmap steps.",
            "improvement_feedback": "None, perfect system."
        }
        res = self.client.post("/submit-feedback", data=feedback_data, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Thank you! Your feedback has been successfully submitted.", res.data)
        print("[OK] All Flask routes and interactive features verified successfully!")

if __name__ == "__main__":
    unittest.main()
