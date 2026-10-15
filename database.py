import sqlite3
import os
import shutil
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, 'database.db')

# In Vercel or serverless environments with a read-only filesystem, use tempdir
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    DATABASE_PATH = os.path.join(tempfile.gettempdir(), "database.db")
    if not os.path.exists(DATABASE_PATH) and os.path.exists(DEFAULT_DB_PATH):
        try:
            shutil.copy2(DEFAULT_DB_PATH, DATABASE_PATH)
        except Exception:
            pass
else:
    DATABASE_PATH = os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH)

def get_db():
    """Get a database connection with dict-like row access, timeout, and WAL mode."""
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.execute("PRAGMA journal_mode = WAL")
    except Exception:
        pass
    return conn

def init_db():
    """Initialize SQLite database tables with proper constraints and relationships."""
    conn = get_db()
    try:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL,
            education TEXT NOT NULL,
            course TEXT,
            academic_year TEXT,
            favorite_subjects TEXT,
            interests TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessment_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            career TEXT NOT NULL,
            score INTEGER NOT NULL,
            explanation TEXT NOT NULL,
            rank INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            usefulness TEXT NOT NULL,
            satisfaction TEXT NOT NULL,
            interest_match TEXT NOT NULL,
            ease_of_use TEXT NOT NULL,
            positive_feedback TEXT,
            improvement_feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE SET NULL
        )
        """)

        # Create indexes for fast querying
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_assessment_student ON assessment_responses(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_career_results_student ON career_results(student_id)")

        conn.commit()
    finally:
        conn.close()

def create_student(name, age, email, education, course, academic_year, favorite_subjects, interests):
    """Insert a new student profile and return the student id."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO students (name, age, email, education, course, academic_year, favorite_subjects, interests)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, age, email, education, course, academic_year, favorite_subjects, interests))
        student_id = cursor.lastrowid
        conn.commit()
        return student_id
    finally:
        conn.close()

def get_student(student_id):
    """Retrieve student information by ID."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def save_assessment_responses(student_id, responses_dict):
    """Store or update 30 assessment question responses."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        # Delete old responses for this student if re-taking
        cursor.execute("DELETE FROM assessment_responses WHERE student_id = ?", (student_id,))
        for q_id, ans in responses_dict.items():
            cursor.execute("""
                INSERT INTO assessment_responses (student_id, question_id, answer)
                VALUES (?, ?, ?)
            """, (student_id, int(q_id), str(ans).strip()))
        conn.commit()
    finally:
        conn.close()

def get_assessment_responses(student_id):
    """Retrieve all assessment responses for a student as {q_num: answer}."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question_id, answer FROM assessment_responses
            WHERE student_id = ? ORDER BY question_id ASC
        """, (student_id,))
        rows = cursor.fetchall()
        return {row["question_id"]: row["answer"] for row in rows}
    finally:
        conn.close()

def save_career_results(student_id, results_list):
    """Store top career recommendation scores and explanations."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM career_results WHERE student_id = ?", (student_id,))
        for idx, item in enumerate(results_list, start=1):
            cursor.execute("""
                INSERT INTO career_results (student_id, career, score, explanation, rank)
                VALUES (?, ?, ?, ?, ?)
            """, (student_id, item["career"], item["score"], item["explanation"], idx))
        conn.commit()
    finally:
        conn.close()

def get_career_results(student_id):
    """Retrieve saved career recommendations for a student."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM career_results WHERE student_id = ? ORDER BY rank ASC
        """, (student_id,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def save_feedback(student_id, usefulness, satisfaction, interest_match, ease_of_use, positive_feedback, improvement_feedback):
    """Record student feedback in SQLite."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO feedback (student_id, usefulness, satisfaction, interest_match, ease_of_use, positive_feedback, improvement_feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_id, usefulness, satisfaction, interest_match, ease_of_use, positive_feedback, improvement_feedback))
        feedback_id = cursor.lastrowid
        conn.commit()
        return feedback_id
    finally:
        conn.close()

def get_feedback(student_id):
    """Retrieve submitted feedback for a student."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback WHERE student_id = ? ORDER BY id DESC LIMIT 1", (student_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

