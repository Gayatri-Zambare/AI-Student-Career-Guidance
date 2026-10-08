# AI-Based Student Career Guidance System

An intelligent, explainable, and full-featured academic mini-project designed to help students discover and navigate their optimal career paths based on their **interests, skills, personality, academic performance, work preferences, and long-term career goals**.

---

## 1. Project Objective

Choosing a suitable career path is one of the most critical challenges facing high school, diploma, and undergraduate students. Traditional career counseling often relies on subjective advice or is restricted to a narrow set of conventional options.

The **AI-Based Student Career Guidance System** solves this by providing:
* A structured, holistic **30-question multi-dimensional assessment**.
* A transparent, explainable **Python AI recommendation engine** covering 16 modern career domains.
* Dynamic compatibility percentage scoring (e.g., *Software Developer — 88% Match*).
* Detailed rationale explaining *why* each career is recommended.
* **Competency Gap Analysis** comparing current abilities with industry requirements.
* Personalized **6-step career execution roadmaps**.
* An **AI Career Assistant** offering real-time contextual advice.
* A structured **student feedback and audit mechanism** stored in SQLite.

---

## 2. Technologies Used

### Frontend
* **HTML5**: Semantic document structure and accessibility.
* **CSS3**: Custom minimalist **Black and White theme** with clean borders, cards, and smooth transitions.
* **JavaScript (ES6+)**: Dynamic 30-question wizard pagination, progress tracking, form validation, and asynchronous AI chat queries.
* **Bootstrap 5.3.3**: Responsive mobile-first grid system, navigation, cards, and utility classes.

### Backend
* **Python 3.14**: Core backend language.
* **Flask**: Lightweight web framework managing routing, sessions, templates, and REST/JSON endpoints.

### Database
* **SQLite (`database.db`)**: Local embedded relational database storing students, assessment responses, career results, and feedback.

### Visualization
* **Chart.js 4.4.2**: Dynamic monochrome data visualizations:
  * Horizontal/Vertical Bar Chart for career compatibility match scores.
  * Radar Chart for the 6-dimension candidate skill aptitude profile.

### AI / Recommendation Engine
* **Transparent Python Scoring Model**: Multi-factor weighted alignment algorithm calculating fit across 6 assessment categories and student profile traits, with zero external paid API dependencies.

---

## 3. Project Architecture & Structure

```text
AI-Career-Guidance-System/
│
├── app.py                      # Main Flask application & routes
├── recommendation_engine.py    # AI recommendation logic, questions, career catalog & roadmap
├── database.py                 # SQLite database initialization & helper functions
├── database.db                 # SQLite database file (generated automatically)
├── requirements.txt            # Python dependencies (Flask)
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Master layout, navbar, footer & CDN assets
│   ├── index.html              # Landing page, hero, how it works, features & about
│   ├── profile.html            # Student registration & academic profile form
│   ├── assessment.html         # 30-question assessment wizard across 6 categories
│   ├── results.html            # Results dashboard with top 3-5 careers & Chart.js charts
│   ├── comparison.html         # Side-by-side comparison matrix of top careers
│   ├── skill_gap.html          # Current vs. required skill gap matrix & improvement actions
│   ├── roadmap.html            # Tailored 6-step roadmap with milestones & certifications
│   ├── assistant.html          # AI Career Assistant Q&A interface with suggestion chips
│   └── feedback.html           # 6-question student feedback & rating survey
│
├── static/
│   ├── css/
│   │   └── style.css           # Professional Black and White design system
│   └── js/
│       └── script.js           # Assessment wizard logic, Chart.js setup, dynamic AI assistant
│
└── README.md                   # Complete documentation and viva guide
```

---

## 4. Complete Project Flow

```text
+-------------------+
|     Home Page     |  (/)
+---------+---------+
          |
          v
+-------------------+
|  Student Profile  |  (/profile) -> Name, Age, Email, Education, Interests
+---------+---------+
          |
          v
+-------------------+
| 30-Q Assessment   |  (/assessment) -> 6 Categories (Interests, Skills, Personality, etc.)
+---------+---------+
          |
          v
+-------------------+
| Python AI Engine  |  Transparent weighted matching across 16 career profiles
+---------+---------+
          |
          v
+-------------------+
| Results Dashboard |  (/results) -> Top 3-5 Careers, Match %, AI Rationale, Chart.js
+---------+---------+
          |
          +-------------------> Career Comparison   (/comparison)
          +-------------------> Skill Gap Analysis  (/skill-gap)
          +-------------------> Career Roadmap      (/roadmap)
          +-------------------> AI Career Assistant (/assistant)
          +-------------------> Student Feedback    (/feedback)
```

---

## 5. Main Features

1. **AI-Based Career Recommendation**: Transparent matching of candidate responses against 16 career profiles.
2. **Interest Analysis**: Scrutinizes activities, hobbies, and favorite subjects.
3. **Skill Analysis**: Assesses problem-solving, technical aptitude, logic, and learning speed.
4. **Personality Analysis**: Evaluates decision-making, autonomy, leadership comfort, and team collaboration.
5. **Work Preferences**: Factors in corporate, research, outdoor, or tech environments.
6. **Academic Analysis**: Weights current academic marks, strong subjects, and weak areas.
7. **Career Compatibility Score**: Computes individual percentage scores (e.g., 88%, 82%, 74%) sorted by fit.
8. **Explainable AI Rationale**: Generates custom explanations identifying the exact factors driving each recommendation.
9. **Interactive Visualizations**: Radar chart for student skill strengths + bar chart for career scores.
10. **Career Comparison**: Multi-column comparison matrix covering skills, education, work type, and growth outlook.
11. **Skill Gap Analysis**: Compares current self-assessed levels against required industry benchmarks.
12. **Personalized 6-Step Roadmap**: Clear milestones, tools, and certifications from foundation to industry entry.
13. **AI Career Assistant**: Rule-based conversational advisor utilizing student profile context for real-time answers.
14. **Student Feedback System**: Stores user ratings, satisfaction, and qualitative suggestions in SQLite.

---

## 6. Supported Career Paths (16 Profiles)

1. **Software Developer**
2. **Data Scientist**
3. **AI/ML Engineer**
4. **Cybersecurity Analyst**
5. **Web Developer**
6. **UI/UX Designer**
7. **Mechanical Engineer**
8. **Civil Engineer**
9. **Electrical Engineer**
10. **Doctor/Healthcare Professional**
11. **Business Manager**
12. **Entrepreneur**
13. **Financial Analyst**
14. **Teacher/Educator**
15. **Researcher**
16. **Government/Public Service Professional**

---

## 7. How to Run the Application

### Prerequisites
* Python 3.8 or higher installed on your system.

### Step 1: Install Dependencies
Open your terminal in the project directory and install Flask:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Flask Application
Execute the following command:

```bash
python app.py
```

### Step 3: Open in Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000/
```

The database (`database.db`) will be automatically initialized on first launch.

---

## 8. Verification & Test Profiles

To demonstrate explainability during viva or presentation testing, verify these three distinct candidate profiles:

### Profile A: Technology & Mathematics Focus
* **Student Interests:** Coding, Computer/IT, solving technical problems.
* **Skills:** Excellent logical reasoning, high math confidence, technical comfort.
* **Goals:** Technical professional, Software/IT or AI.
* **Expected Outcome:** High compatibility for **Software Developer (85-95%)**, **Data Scientist**, and **AI/ML Engineer**.

### Profile B: Creative & Design Focus
* **Student Interests:** Designing or creating things, Arts/Humanities, drawing/designing.
* **Skills:** Strong creativity, good communication.
* **Work Style:** Flexible and creative environment.
* **Expected Outcome:** High compatibility for **UI/UX Designer (80-92%)**, **Web Developer**, and **Creative Careers**.

### Profile C: Leadership & Entrepreneurial Focus
* **Student Interests:** Managing or organizing activities, Commerce/Economics, organizing events.
* **Skills:** Strong leadership, communication, very comfortable taking responsibility.
* **Goals:** High interest in starting own business, 5-10 year vision as Manager/Entrepreneur.
* **Expected Outcome:** High compatibility for **Business Manager (82-94%)** and **Entrepreneur**.

---

## 9. Viva & Presentation Highlights

* **Explainable AI (XAI)**: Unlike opaque black-box neural networks, our system generates human-readable justifications explaining *why* a career matches, fostering trust.
* **Zero Paid API Requirement**: Fully self-contained Python architecture runs anywhere without external network dependencies or token costs.
* **Relational SQLite Schema**: Parameterized SQL queries ensure data integrity, privacy, and prevention of SQL injection.
* **Responsive Monochrome Theme**: Delivers a crisp, distraction-free aesthetic highlighting actionable career metrics.
