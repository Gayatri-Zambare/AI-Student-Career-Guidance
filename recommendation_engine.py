"""
recommendation_engine.py
AI-Based Student Career Guidance Recommendation Engine.
Provides transparent, explainable scoring, skill profile calculation,
skill-gap evaluation, personalized roadmaps, and rule-based AI assistance.
"""

# ==============================================================================
# 1. 30 ASSESSMENT QUESTIONS SPECIFICATION
# ==============================================================================

ASSESSMENT_CATEGORIES = [
    {
        "id": "interests",
        "name": "Interests",
        "description": "Explores activities, subjects, and hobbies that motivate and energize you.",
        "icon": "bi-compass",
        "question_ids": [1, 2, 3, 4, 5]
    },
    {
        "id": "skills",
        "name": "Skills",
        "description": "Evaluates your self-assessed strengths, technical aptitude, and problem-solving skills.",
        "icon": "bi-tools",
        "question_ids": [6, 7, 8, 9, 10, 11]
    },
    {
        "id": "personality",
        "name": "Personality",
        "description": "Analyzes how you think, collaborate, make decisions, and communicate.",
        "icon": "bi-person-badge",
        "question_ids": [12, 13, 14, 15, 16, 17]
    },
    {
        "id": "work_preferences",
        "name": "Work Preferences",
        "description": "Identifies the environment, culture, and nature of work you thrive in.",
        "icon": "bi-briefcase",
        "question_ids": [18, 19, 20, 21]
    },
    {
        "id": "academic_performance",
        "name": "Academic Performance",
        "description": "Reviews your academic standing, strongest subjects, and learning discipline.",
        "icon": "bi-mortarboard",
        "question_ids": [22, 23, 24, 25]
    },
    {
        "id": "career_goals",
        "name": "Career Goals",
        "description": "Uncovers your long-term aspirations, priorities, and industry inclinations.",
        "icon": "bi-flag",
        "question_ids": [26, 27, 28, 29, 30]
    }
]

ASSESSMENT_QUESTIONS = [
    # INTERESTS (Q1 - Q5)
    {
        "id": 1,
        "category": "Interests",
        "text": "Which type of activity do you enjoy most?",
        "options": [
            "Solving technical problems",
            "Designing or creating things",
            "Helping and communicating with people",
            "Analyzing information",
            "Managing or organizing activities"
        ]
    },
    {
        "id": 2,
        "category": "Interests",
        "text": "Which subjects do you enjoy the most?",
        "options": [
            "Mathematics",
            "Science",
            "Computer/IT",
            "Commerce/Economics",
            "Arts/Humanities",
            "Biology/Healthcare"
        ]
    },
    {
        "id": 3,
        "category": "Interests",
        "text": "What do you prefer doing in your free time?",
        "options": [
            "Coding or experimenting with technology",
            "Drawing/designing",
            "Reading/researching",
            "Communicating with others",
            "Organizing events",
            "Building or repairing things"
        ]
    },
    {
        "id": 4,
        "category": "Interests",
        "text": "Which type of problem interests you most?",
        "options": [
            "Technical problems",
            "Business problems",
            "Social problems",
            "Scientific problems",
            "Creative problems"
        ]
    },
    {
        "id": 5,
        "category": "Interests",
        "text": "How interested are you in learning new technology?",
        "options": [
            "Very interested",
            "Interested",
            "Neutral",
            "Slightly interested",
            "Not interested"
        ]
    },

    # SKILLS (Q6 - Q11)
    {
        "id": 6,
        "category": "Skills",
        "text": "How confident are you in solving mathematical problems?",
        "options": [
            "Very confident",
            "Confident",
            "Average",
            "Need improvement"
        ]
    },
    {
        "id": 7,
        "category": "Skills",
        "text": "How would you rate your logical reasoning?",
        "options": [
            "Excellent",
            "Good",
            "Average",
            "Needs improvement"
        ]
    },
    {
        "id": 8,
        "category": "Skills",
        "text": "How would you rate your communication skills?",
        "options": [
            "Excellent",
            "Good",
            "Average",
            "Needs improvement"
        ]
    },
    {
        "id": 9,
        "category": "Skills",
        "text": "How comfortable are you with computers and technology?",
        "options": [
            "Very comfortable",
            "Comfortable",
            "Average",
            "Beginner"
        ]
    },
    {
        "id": 10,
        "category": "Skills",
        "text": "Which skill is your strongest?",
        "options": [
            "Problem solving",
            "Communication",
            "Creativity",
            "Leadership",
            "Analytical thinking",
            "Technical skills",
            "Teamwork"
        ]
    },
    {
        "id": 11,
        "category": "Skills",
        "text": "How good are you at learning new concepts?",
        "options": [
            "Very good",
            "Good",
            "Average",
            "Need improvement"
        ]
    },

    # PERSONALITY (Q12 - Q17)
    {
        "id": 12,
        "category": "Personality",
        "text": "When working on a project, what do you prefer?",
        "options": [
            "Working independently",
            "Working with a team",
            "Combination of both"
        ]
    },
    {
        "id": 13,
        "category": "Personality",
        "text": "How do you make important decisions?",
        "options": [
            "Logic and facts",
            "Creativity and ideas",
            "Advice from others",
            "Personal experience"
        ]
    },
    {
        "id": 14,
        "category": "Personality",
        "text": "How comfortable are you taking responsibility?",
        "options": [
            "Very comfortable",
            "Comfortable",
            "Neutral",
            "Uncomfortable"
        ]
    },
    {
        "id": 15,
        "category": "Personality",
        "text": "How do you react to a difficult problem?",
        "options": [
            "Analyze it step-by-step",
            "Try creative solutions",
            "Ask someone for help",
            "Avoid it initially"
        ]
    },
    {
        "id": 16,
        "category": "Personality",
        "text": "Which describes you best?",
        "options": [
            "Analytical",
            "Creative",
            "Social",
            "Organized",
            "Enterprising",
            "Practical"
        ]
    },
    {
        "id": 17,
        "category": "Personality",
        "text": "How comfortable are you speaking in front of others?",
        "options": [
            "Very comfortable",
            "Comfortable",
            "Average",
            "Uncomfortable"
        ]
    },

    # WORK PREFERENCES (Q18 - Q21)
    {
        "id": 18,
        "category": "Work Preferences",
        "text": "What work environment do you prefer?",
        "options": [
            "Technology/IT",
            "Laboratory/Research",
            "Office/Corporate",
            "Healthcare",
            "Creative environment",
            "Field/Outdoor work"
        ]
    },
    {
        "id": 19,
        "category": "Work Preferences",
        "text": "What type of work do you prefer?",
        "options": [
            "Working with computers",
            "Working with people",
            "Working with data",
            "Working with machines",
            "Creating/designing",
            "Managing projects"
        ]
    },
    {
        "id": 20,
        "category": "Work Preferences",
        "text": "Which work style suits you?",
        "options": [
            "Fixed and structured",
            "Flexible and creative",
            "Challenging and competitive",
            "Collaborative and team-oriented"
        ]
    },
    {
        "id": 21,
        "category": "Work Preferences",
        "text": "Would you prefer a career involving continuous learning?",
        "options": [
            "Yes",
            "Maybe",
            "No"
        ]
    },

    # ACADEMIC PERFORMANCE (Q22 - Q25)
    {
        "id": 22,
        "category": "Academic Performance",
        "text": "What is your approximate academic performance?",
        "options": [
            "80–100%",
            "70–79%",
            "60–69%",
            "50–59%",
            "Below 50%"
        ]
    },
    {
        "id": 23,
        "category": "Academic Performance",
        "text": "Which subject area is your strongest?",
        "options": [
            "Mathematics",
            "Science",
            "Computer Science",
            "Commerce",
            "Biology",
            "Languages",
            "Social Sciences"
        ]
    },
    {
        "id": 24,
        "category": "Academic Performance",
        "text": "Which subject area needs improvement?",
        "options": [
            "Mathematics",
            "Science",
            "Computer Science",
            "Commerce",
            "Biology",
            "Languages",
            "Social Sciences"
        ]
    },
    {
        "id": 25,
        "category": "Academic Performance",
        "text": "How regularly do you study?",
        "options": [
            "Daily",
            "4–5 days a week",
            "2–3 days a week",
            "Occasionally"
        ]
    },

    # CAREER GOALS (Q26 - Q30)
    {
        "id": 26,
        "category": "Career Goals",
        "text": "What is most important to you in a future career?",
        "options": [
            "High salary",
            "Job security",
            "Creativity",
            "Social impact",
            "Career growth",
            "Work-life balance",
            "Leadership opportunities"
        ]
    },
    {
        "id": 27,
        "category": "Career Goals",
        "text": "Which career area interests you most?",
        "options": [
            "Software/IT",
            "Artificial Intelligence/Data Science",
            "Engineering",
            "Medicine/Healthcare",
            "Business/Management",
            "Finance",
            "Design",
            "Education",
            "Research",
            "Government/Public Services"
        ]
    },
    {
        "id": 28,
        "category": "Career Goals",
        "text": "Are you interested in starting your own business?",
        "options": [
            "Very interested",
            "Interested",
            "Maybe",
            "Not interested"
        ]
    },
    {
        "id": 29,
        "category": "Career Goals",
        "text": "Where do you see yourself in the next 5–10 years?",
        "options": [
            "Technical professional",
            "Manager/Leader",
            "Entrepreneur",
            "Researcher",
            "Creative professional",
            "Public service professional",
            "Healthcare professional"
        ]
    },
    {
        "id": 30,
        "category": "Career Goals",
        "text": "How confident are you about your current career choice?",
        "options": [
            "Very confident",
            "Somewhat confident",
            "Not sure",
            "Completely confused"
        ]
    }
]

# Quick lookup dictionary for questions
QUESTIONS_BY_ID = {q["id"]: q for q in ASSESSMENT_QUESTIONS}

# ==============================================================================
# 2. CAREER KNOWLEDGE BASE (16 CAREERS)
# ==============================================================================

CAREER_CATALOG = {
    "Software Developer": {
        "title": "Software Developer",
        "category": "Information Technology",
        "description": "Designs, builds, and maintains software applications, operating systems, and computer software solutions using modern programming languages and architecture.",
        "required_skills": ["Programming (Python/Java/C++)", "Problem Solving", "Data Structures & Algorithms", "Databases & SQL", "Software Architecture", "Version Control (Git)"],
        "possible_roles": ["Software Developer", "Software Engineer", "Full Stack Developer", "Application Developer", "Systems Programmer"],
        "work_type": "Working with computers & code",
        "education": "B.Tech / B.E. in CS/IT, BCA/MCA, or relevant STEM Degree",
        "growth_outlook": "High Demand (25% projected global growth)",
        "skill_benchmarks": {
            "Programming": "High",
            "Problem Solving": "High",
            "Logical Reasoning": "High",
            "Data Structures": "High",
            "Communication": "Medium",
            "Teamwork": "Medium"
        },
        "target_traits": {
            "q1": ["Solving technical problems"],
            "q2": ["Computer/IT", "Mathematics"],
            "q3": ["Coding or experimenting with technology", "Building or repairing things"],
            "q4": ["Technical problems"],
            "q10": ["Problem solving", "Technical skills", "Analytical thinking"],
            "q16": ["Analytical", "Practical"],
            "q18": ["Technology/IT"],
            "q19": ["Working with computers"],
            "q23": ["Computer Science", "Mathematics"],
            "q27": ["Software/IT"],
            "q29": ["Technical professional"]
        }
    },
    "Data Scientist": {
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Extracts actionable insights and predictive patterns from complex structured and unstructured data using statistics, machine learning, and data visualization.",
        "required_skills": ["Python / R", "Statistics & Probability", "Machine Learning", "SQL & Big Data", "Data Visualization", "Critical Thinking"],
        "possible_roles": ["Data Scientist", "Data Analyst", "Business Intelligence Specialist", "Quantitative Researcher", "Analytics Consultant"],
        "work_type": "Working with data, algorithms & statistics",
        "education": "B.Tech / B.Sc in Data Science, Computer Science, Statistics, or Math",
        "growth_outlook": "Very High (35% projected growth, top emerging role)",
        "skill_benchmarks": {
            "Mathematics & Statistics": "High",
            "Programming (Python/R)": "High",
            "Data Analysis": "High",
            "Problem Solving": "High",
            "Communication": "Medium",
            "Business Acumen": "Medium"
        },
        "target_traits": {
            "q1": ["Analyzing information", "Solving technical problems"],
            "q2": ["Mathematics", "Computer/IT", "Science"],
            "q3": ["Reading/researching", "Coding or experimenting with technology"],
            "q4": ["Technical problems", "Scientific problems", "Business problems"],
            "q10": ["Analytical thinking", "Problem solving", "Technical skills"],
            "q16": ["Analytical", "Practical"],
            "q18": ["Technology/IT", "Laboratory/Research", "Office/Corporate"],
            "q19": ["Working with data", "Working with computers"],
            "q23": ["Mathematics", "Computer Science", "Science"],
            "q27": ["Artificial Intelligence/Data Science", "Software/IT"],
            "q29": ["Technical professional", "Researcher"]
        }
    },
    "AI/ML Engineer": {
        "title": "AI/ML Engineer",
        "category": "Artificial Intelligence",
        "description": "Designs and develops deep learning architectures, neural networks, and self-learning intelligent agents that automate complex cognitive tasks.",
        "required_skills": ["Machine Learning & Deep Learning", "Python / PyTorch / TensorFlow", "Linear Algebra & Calculus", "Data Modeling", "Algorithm Optimization", "Cloud AI Deployment"],
        "possible_roles": ["AI Engineer", "Machine Learning Engineer", "NLP Specialist", "Computer Vision Engineer", "AI Research Scientist"],
        "work_type": "Developing intelligent algorithms & neural models",
        "education": "B.Tech / M.Tech in AI, Data Science, Computer Science, or Mathematics",
        "growth_outlook": "Exceptional Growth (AI sector expanding exponentially)",
        "skill_benchmarks": {
            "Machine Learning": "High",
            "Advanced Mathematics": "High",
            "Programming": "High",
            "Analytical Thinking": "High",
            "Continuous Learning": "High",
            "Research Aptitude": "Medium"
        },
        "target_traits": {
            "q1": ["Solving technical problems", "Analyzing information"],
            "q2": ["Computer/IT", "Mathematics", "Science"],
            "q3": ["Coding or experimenting with technology", "Reading/researching"],
            "q4": ["Technical problems", "Scientific problems"],
            "q10": ["Technical skills", "Analytical thinking", "Problem solving"],
            "q16": ["Analytical", "Creative"],
            "q18": ["Technology/IT", "Laboratory/Research"],
            "q19": ["Working with computers", "Working with data"],
            "q23": ["Computer Science", "Mathematics"],
            "q27": ["Artificial Intelligence/Data Science"],
            "q29": ["Technical professional", "Researcher"]
        }
    },
    "Cybersecurity Analyst": {
        "title": "Cybersecurity Analyst",
        "category": "Information Security",
        "description": "Protects digital systems, networks, and confidential information assets against cyber threats, vulnerabilities, intrusions, and security breaches.",
        "required_skills": ["Network Security", "Ethical Hacking & Penetration Testing", "Security Auditing", "Cryptography", "Incident Response", "Linux & Shell Scripting"],
        "possible_roles": ["Cybersecurity Analyst", "Security Engineer", "Ethical Hacker", "Information Security Consultant", "SOC Analyst"],
        "work_type": "Defending computer networks and digital infrastructure",
        "education": "B.Tech in IT / Cybersecurity / Computer Science, or Security Certifications",
        "growth_outlook": "Critical Global Demand (32% annual expansion)",
        "skill_benchmarks": {
            "Network Security": "High",
            "Problem Solving": "High",
            "Logical Reasoning": "High",
            "Risk Assessment": "High",
            "Programming / Scripting": "Medium",
            "Attention to Detail": "High"
        },
        "target_traits": {
            "q1": ["Solving technical problems", "Analyzing information"],
            "q2": ["Computer/IT", "Mathematics"],
            "q3": ["Coding or experimenting with technology", "Building or repairing things"],
            "q4": ["Technical problems"],
            "q10": ["Problem solving", "Technical skills", "Analytical thinking"],
            "q16": ["Analytical", "Practical", "Organized"],
            "q18": ["Technology/IT", "Office/Corporate"],
            "q19": ["Working with computers", "Working with data"],
            "q23": ["Computer Science", "Mathematics"],
            "q27": ["Software/IT"],
            "q29": ["Technical professional"]
        }
    },
    "Web Developer": {
        "title": "Web Developer",
        "category": "Software Engineering",
        "description": "Builds and deploys dynamic, interactive websites and browser-based software applications with modern client-server architectures.",
        "required_skills": ["HTML5/CSS3/JavaScript", "Frontend Frameworks (React/Vue)", "Backend APIs (Node/Python)", "Responsive Design", "Git & Deployment", "Web Performance"],
        "possible_roles": ["Web Developer", "Frontend Developer", "Backend Developer", "Full Stack Web Engineer", "Web Consultant"],
        "work_type": "Creating web applications and digital interfaces",
        "education": "B.Tech / BCA / B.Sc in Computer Science or Web Development Bootcamp",
        "growth_outlook": "Strong Sustained Growth across all industry sectors",
        "skill_benchmarks": {
            "Web Technologies (HTML/CSS/JS)": "High",
            "API Integration": "High",
            "Creativity & Design Sense": "Medium",
            "Problem Solving": "Medium",
            "Communication": "Medium",
            "Continuous Learning": "Medium"
        },
        "target_traits": {
            "q1": ["Designing or creating things", "Solving technical problems"],
            "q2": ["Computer/IT"],
            "q3": ["Coding or experimenting with technology", "Drawing/designing"],
            "q4": ["Technical problems", "Creative problems"],
            "q10": ["Technical skills", "Creativity", "Problem solving"],
            "q16": ["Practical", "Creative"],
            "q18": ["Technology/IT", "Creative environment"],
            "q19": ["Working with computers", "Creating/designing"],
            "q23": ["Computer Science"],
            "q27": ["Software/IT", "Design"],
            "q29": ["Technical professional", "Creative professional"]
        }
    },
    "UI/UX Designer": {
        "title": "UI/UX Designer",
        "category": "Design & User Experience",
        "description": "Researches user behavior and crafts intuitive, accessible, and visually stunning digital product interfaces, wireframes, and prototypes.",
        "required_skills": ["UI Design & Wireframing (Figma/Adobe XD)", "User Research & Usability Testing", "Information Architecture", "Design Systems", "Prototyping", "Visual Communication"],
        "possible_roles": ["UI/UX Designer", "Product Designer", "User Experience Researcher", "Interaction Designer", "Visual Designer"],
        "work_type": "Designing user experiences, wireframes & interfaces",
        "education": "Bachelor of Design (B.Des), Fine Arts, HCI, or related field",
        "growth_outlook": "High Demand (Digital product-first economy)",
        "skill_benchmarks": {
            "UI/UX Prototyping (Figma)": "High",
            "Creativity & Aesthetic Sense": "High",
            "User Empathy & Research": "High",
            "Communication": "High",
            "Problem Solving": "Medium",
            "Basic Technical Understanding": "Medium"
        },
        "target_traits": {
            "q1": ["Designing or creating things", "Helping and communicating with people"],
            "q2": ["Arts/Humanities", "Computer/IT"],
            "q3": ["Drawing/designing", "Reading/researching"],
            "q4": ["Creative problems", "Social problems"],
            "q10": ["Creativity", "Communication", "Problem solving"],
            "q16": ["Creative", "Social"],
            "q18": ["Creative environment", "Technology/IT"],
            "q19": ["Creating/designing", "Working with people", "Working with computers"],
            "q23": ["Languages", "Computer Science", "Social Sciences"],
            "q27": ["Design", "Software/IT"],
            "q29": ["Creative professional"]
        }
    },
    "Mechanical Engineer": {
        "title": "Mechanical Engineer",
        "category": "Core Engineering",
        "description": "Designs, analyzes, manufactures, and tests mechanical systems, robotics, thermal devices, automotive components, and industrial machinery.",
        "required_skills": ["CAD/CAM (SolidWorks/AutoCAD)", "Thermodynamics & Fluid Mechanics", "Materials Science", "Robotics & Automation", "Manufacturing Processes", "Structural Analysis"],
        "possible_roles": ["Mechanical Engineer", "Design Engineer", "Automotive Engineer", "Robotics Specialist", "HVAC / Thermal Engineer"],
        "work_type": "Working with machines, physical mechanisms & blueprints",
        "education": "B.Tech / B.E. in Mechanical Engineering",
        "growth_outlook": "Steady Growth (Robotics, Electric Vehicles & Clean Energy)",
        "skill_benchmarks": {
            "Mechanical Design (CAD)": "High",
            "Physics & Mechanics": "High",
            "Mathematics": "High",
            "Problem Solving": "High",
            "Practical Execution": "High",
            "Teamwork": "Medium"
        },
        "target_traits": {
            "q1": ["Solving technical problems", "Designing or creating things"],
            "q2": ["Science", "Mathematics"],
            "q3": ["Building or repairing things", "Drawing/designing"],
            "q4": ["Technical problems", "Scientific problems"],
            "q10": ["Problem solving", "Technical skills", "Analytical thinking"],
            "q16": ["Practical", "Analytical"],
            "q18": ["Field/Outdoor work", "Laboratory/Research", "Technology/IT"],
            "q19": ["Working with machines", "Working with computers"],
            "q23": ["Science", "Mathematics"],
            "q27": ["Engineering"],
            "q29": ["Technical professional"]
        }
    },
    "Civil Engineer": {
        "title": "Civil Engineer",
        "category": "Core Engineering & Infrastructure",
        "description": "Plans, designs, supervises, and manages the construction and maintenance of building structures, transportation systems, bridges, and public utilities.",
        "required_skills": ["Structural Analysis (ETABS/STAAD.Pro)", "AutoCAD & BIM", "Surveying & Geotechnical Analysis", "Project Management", "Construction Safety", "Cost Estimation"],
        "possible_roles": ["Civil Engineer", "Structural Engineer", "Site Engineer", "Transportation Planner", "Project Construction Manager"],
        "work_type": "Planning infrastructure, on-site execution & structural design",
        "education": "B.Tech / B.E. in Civil Engineering",
        "growth_outlook": "Consistent Demand (Global infrastructure modernization)",
        "skill_benchmarks": {
            "Structural Design": "High",
            "Mathematics & Physics": "High",
            "Project Management": "High",
            "Problem Solving": "Medium",
            "Teamwork & Leadership": "High",
            "Field Supervision": "High"
        },
        "target_traits": {
            "q1": ["Managing or organizing activities", "Designing or creating things"],
            "q2": ["Science", "Mathematics"],
            "q3": ["Building or repairing things", "Organizing events"],
            "q4": ["Technical problems", "Business problems"],
            "q10": ["Problem solving", "Leadership", "Teamwork"],
            "q16": ["Practical", "Organized"],
            "q18": ["Field/Outdoor work", "Office/Corporate"],
            "q19": ["Working with machines", "Managing projects"],
            "q23": ["Science", "Mathematics"],
            "q27": ["Engineering", "Government/Public Services"],
            "q29": ["Technical professional", "Manager/Leader"]
        }
    },
    "Electrical Engineer": {
        "title": "Electrical Engineer",
        "category": "Core Engineering & Electronics",
        "description": "Develops, tests, and oversees electrical systems, power generation networks, microelectronics, renewable energy grids, and embedded circuits.",
        "required_skills": ["Circuit Design & Simulation (MATLAB/SPICE)", "Power Systems & Renewable Energy", "Embedded Systems (Arduino/ARM)", "Control Systems", "Signal Processing", "Safety Standards"],
        "possible_roles": ["Electrical Engineer", "Electronics Engineer", "Power Systems Engineer", "Embedded Hardware Engineer", "Control Systems Specialist"],
        "work_type": "Working with electrical circuits, power grids & hardware",
        "education": "B.Tech / B.E. in Electrical or Electronics Engineering",
        "growth_outlook": "High Growth (Electric Mobility, Renewable Power & IoT)",
        "skill_benchmarks": {
            "Circuit Analysis & Design": "High",
            "Mathematics & Electromagnetics": "High",
            "Problem Solving": "High",
            "Technical Skills": "High",
            "Analytical Thinking": "High",
            "Practical Execution": "Medium"
        },
        "target_traits": {
            "q1": ["Solving technical problems"],
            "q2": ["Science", "Mathematics"],
            "q3": ["Building or repairing things", "Coding or experimenting with technology"],
            "q4": ["Technical problems", "Scientific problems"],
            "q10": ["Technical skills", "Problem solving", "Analytical thinking"],
            "q16": ["Analytical", "Practical"],
            "q18": ["Technology/IT", "Laboratory/Research", "Field/Outdoor work"],
            "q19": ["Working with machines", "Working with computers"],
            "q23": ["Science", "Mathematics"],
            "q27": ["Engineering"],
            "q29": ["Technical professional"]
        }
    },
    "Doctor/Healthcare Professional": {
        "title": "Doctor/Healthcare Professional",
        "category": "Healthcare & Medicine",
        "description": "Diagnoses, treats, and cares for patients, prevents illnesses, and champions public health and medical clinical excellence.",
        "required_skills": ["Clinical Diagnosis", "Human Anatomy & Physiology", "Patient Communication & Empathy", "Critical Care & First Aid", "Medical Ethics", "Pharmacology"],
        "possible_roles": ["Medical Doctor (Physician)", "Surgeon", "Medical Researcher", "Clinical Specialist", "Public Health Officer"],
        "work_type": "Direct patient care, clinical examination & healthcare",
        "education": "MBBS, BDS, MD, or relevant professional medical degree",
        "growth_outlook": "Invaluable & High Demand (Global healthcare focus)",
        "skill_benchmarks": {
            "Medical Sciences & Biology": "High",
            "Empathy & Patient Care": "High",
            "Critical Decision Making": "High",
            "Communication Skills": "High",
            "Emotional Resilience": "High",
            "Continuous Learning": "High"
        },
        "target_traits": {
            "q1": ["Helping and communicating with people", "Analyzing information"],
            "q2": ["Biology/Healthcare", "Science"],
            "q3": ["Reading/researching", "Communicating with others"],
            "q4": ["Social problems", "Scientific problems"],
            "q10": ["Communication", "Problem solving", "Analytical thinking"],
            "q16": ["Social", "Analytical", "Practical"],
            "q18": ["Healthcare", "Laboratory/Research"],
            "q19": ["Working with people"],
            "q23": ["Biology", "Science"],
            "q27": ["Medicine/Healthcare"],
            "q29": ["Healthcare professional"]
        }
    },
    "Business Manager": {
        "title": "Business Manager",
        "category": "Management & Corporate Leadership",
        "description": "Oversees business operations, organizational strategy, team productivity, financial budgets, and client relations to achieve strategic goals.",
        "required_skills": ["Strategic Planning", "Leadership & Team Management", "Financial Acumen & Budgeting", "Negotiation & Communication", "Process Optimization", "Risk Management"],
        "possible_roles": ["Operations Manager", "Business Development Manager", "Project Manager", "General Manager", "Management Consultant"],
        "work_type": "Managing projects, corporate teams & business operations",
        "education": "BBA, MBA, Commerce, or Management Degree",
        "growth_outlook": "Strong Demand across all corporate and industrial sectors",
        "skill_benchmarks": {
            "Leadership": "High",
            "Communication": "High",
            "Strategic Thinking": "High",
            "Problem Solving": "Medium",
            "Financial Literacy": "Medium",
            "Teamwork & Delegation": "High"
        },
        "target_traits": {
            "q1": ["Managing or organizing activities", "Helping and communicating with people"],
            "q2": ["Commerce/Economics"],
            "q3": ["Organizing events", "Communicating with others"],
            "q4": ["Business problems"],
            "q10": ["Leadership", "Communication", "Teamwork"],
            "q16": ["Enterprising", "Organized", "Social"],
            "q18": ["Office/Corporate"],
            "q19": ["Managing projects", "Working with people"],
            "q23": ["Commerce", "Social Sciences"],
            "q27": ["Business/Management"],
            "q29": ["Manager/Leader"]
        }
    },
    "Entrepreneur": {
        "title": "Entrepreneur",
        "category": "Venture Building & Innovation",
        "description": "Identifies market opportunities, conceives innovative solutions, secures capital, and scales disruptive commercial ventures.",
        "required_skills": ["Business Modeling & Innovation", "Sales & Pitching", "Fundraising & Capital Allocation", "Resilience & Decision-Making", "Product Strategy", "Leadership"],
        "possible_roles": ["Founder / Co-Founder", "Startup CEO", "Venture Partner", "Product Innovator", "Business Accelerator"],
        "work_type": "Building innovative products, businesses & leading teams",
        "education": "Degree in Any Field + Strong Entrepreneurial Drive & Business Sense",
        "growth_outlook": "High Potential (Rapid global startup & technology ecosystem)",
        "skill_benchmarks": {
            "Leadership & Vision": "High",
            "Resilience & Risk Tolerance": "High",
            "Creativity & Innovation": "High",
            "Networking & Pitching": "High",
            "Strategic Problem Solving": "High",
            "Financial Management": "Medium"
        },
        "target_traits": {
            "q1": ["Managing or organizing activities", "Designing or creating things"],
            "q2": ["Commerce/Economics", "Computer/IT"],
            "q3": ["Organizing events", "Coding or experimenting with technology"],
            "q4": ["Business problems", "Creative problems"],
            "q10": ["Leadership", "Creativity", "Problem solving"],
            "q16": ["Enterprising", "Creative", "Practical"],
            "q18": ["Office/Corporate", "Creative environment", "Technology/IT"],
            "q19": ["Managing projects", "Creating/designing"],
            "q23": ["Commerce", "Computer Science"],
            "q27": ["Business/Management", "Software/IT"],
            "q28": ["Very interested", "Interested"],
            "q29": ["Entrepreneur", "Manager/Leader"]
        }
    },
    "Financial Analyst": {
        "title": "Financial Analyst",
        "category": "Finance & Economics",
        "description": "Evaluates financial statements, investment opportunities, market trends, and economic indicators to guide strategic wealth and investment decisions.",
        "required_skills": ["Financial Modeling (Excel)", "Corporate Finance", "Investment Valuation", "Data Analysis & Statistics", "Accounting Standards", "Risk Modeling"],
        "possible_roles": ["Financial Analyst", "Investment Banking Analyst", "Portfolio Manager", "Equity Research Associate", "Corporate Finance Specialist"],
        "work_type": "Analyzing numbers, financial models & market trends",
        "education": "B.Com, BBA Finance, Economics, CFA, or MBA Finance",
        "growth_outlook": "Robust (Expanding global fintech and investment banking)",
        "skill_benchmarks": {
            "Financial Modeling & Excel": "High",
            "Quantitative Analysis": "High",
            "Accounting & Economics": "High",
            "Logical Reasoning": "High",
            "Communication": "Medium",
            "Risk Assessment": "High"
        },
        "target_traits": {
            "q1": ["Analyzing information", "Solving technical problems"],
            "q2": ["Commerce/Economics", "Mathematics"],
            "q3": ["Reading/researching", "Organizing events"],
            "q4": ["Business problems"],
            "q10": ["Analytical thinking", "Problem solving"],
            "q16": ["Analytical", "Organized"],
            "q18": ["Office/Corporate"],
            "q19": ["Working with data", "Working with computers"],
            "q23": ["Commerce", "Mathematics"],
            "q27": ["Finance", "Business/Management"],
            "q29": ["Technical professional", "Manager/Leader"]
        }
    },
    "Teacher/Educator": {
        "title": "Teacher/Educator",
        "category": "Education & Academic Instruction",
        "description": "Inspires, instructs, and mentors students, develops curriculum, and empowers future generations with knowledge and life skills.",
        "required_skills": ["Pedagogy & Teaching Methodologies", "Verbal Communication & Public Speaking", "Empathy & Mentorship", "Curriculum Design", "Classroom Management", "Educational Technology"],
        "possible_roles": ["School Teacher", "College Professor / Lecturer", "Instructional Designer", "Academic Mentor", "Corporate Trainer"],
        "work_type": "Teaching, mentoring & communicating with students",
        "education": "Bachelor's / Master's degree in subject area + B.Ed / M.Ed or Ph.D.",
        "growth_outlook": "Evergreen Stability (Education & EdTech growing worldwide)",
        "skill_benchmarks": {
            "Subject Mastery": "High",
            "Communication & Presentation": "High",
            "Empathy & Patience": "High",
            "Curriculum Planning": "High",
            "Leadership & Mentorship": "Medium",
            "Active Listening": "High"
        },
        "target_traits": {
            "q1": ["Helping and communicating with people"],
            "q2": ["Arts/Humanities", "Science", "Mathematics"],
            "q3": ["Communicating with others", "Reading/researching"],
            "q4": ["Social problems", "Scientific problems"],
            "q10": ["Communication", "Leadership", "Teamwork"],
            "q16": ["Social", "Organized"],
            "q18": ["Office/Corporate", "Creative environment"],
            "q19": ["Working with people"],
            "q23": ["Languages", "Science", "Social Sciences"],
            "q27": ["Education"],
            "q29": ["Researcher", "Public service professional"]
        }
    },
    "Researcher": {
        "title": "Researcher",
        "category": "Scientific Research & Academia",
        "description": "Investigates fundamental scientific, technological, or social phenomena to discover new principles, publish academic discoveries, and advance human knowledge.",
        "required_skills": ["Research Methodology", "Critical & Hypothesis-Driven Thinking", "Academic Writing & Publication", "Statistical Data Analysis", "Literature Review", "Laboratory/Experimentation"],
        "possible_roles": ["Research Scientist", "Academic Scholar / Postdoc", "R&D Specialist", "Policy Researcher", "Scientific Consultant"],
        "work_type": "Scientific experimentation, academic discovery & research papers",
        "education": "Master's Degree / Ph.D. in specialized science or humanities field",
        "growth_outlook": "High Strategic Value (Government, Biotech, R&D labs)",
        "skill_benchmarks": {
            "Analytical Thinking": "High",
            "Scientific Methodology": "High",
            "Critical Inquiry": "High",
            "Written Communication": "High",
            "Patience & Perseverance": "High",
            "Mathematics / Statistics": "Medium"
        },
        "target_traits": {
            "q1": ["Analyzing information", "Solving technical problems"],
            "q2": ["Science", "Mathematics", "Biology/Healthcare"],
            "q3": ["Reading/researching"],
            "q4": ["Scientific problems"],
            "q10": ["Analytical thinking", "Problem solving"],
            "q16": ["Analytical"],
            "q18": ["Laboratory/Research"],
            "q19": ["Working with data", "Working with computers"],
            "q23": ["Science", "Mathematics", "Biology"],
            "q27": ["Research"],
            "q29": ["Researcher"]
        }
    },
    "Government/Public Service Professional": {
        "title": "Government/Public Service Professional",
        "category": "Public Administration & Governance",
        "description": "Formulates and implements public policy, manages civic infrastructure, delivers citizen services, and upholds public order and law.",
        "required_skills": ["Public Administration", "Constitutional Law & Governance", "Policy Analysis", "Crisis Management", "Public Communication", "Integrity & Ethics"],
        "possible_roles": ["Civil Services Officer", "Public Policy Analyst", "Government Administrator", "Diplomat / Foreign Service", "Urban Planning Officer"],
        "work_type": "Public welfare, policy administration & civic governance",
        "education": "Bachelor's Degree in any discipline + Civil Services / Public exams",
        "growth_outlook": "Very High Prestige, Job Security and Significant Social Impact",
        "skill_benchmarks": {
            "Leadership & Public Trust": "High",
            "Policy & Legal Knowledge": "High",
            "Communication & Diplomacy": "High",
            "Decision Making": "High",
            "Integrity & Ethics": "High",
            "Social Awareness": "High"
        },
        "target_traits": {
            "q1": ["Managing or organizing activities", "Helping and communicating with people"],
            "q2": ["Arts/Humanities", "Commerce/Economics"],
            "q3": ["Organizing events", "Reading/researching", "Communicating with others"],
            "q4": ["Social problems", "Business problems"],
            "q10": ["Leadership", "Communication", "Problem solving"],
            "q16": ["Organized", "Enterprising", "Social"],
            "q18": ["Office/Corporate", "Field/Outdoor work"],
            "q19": ["Managing projects", "Working with people"],
            "q23": ["Social Sciences", "Languages"],
            "q26": ["Social impact", "Job security", "Leadership opportunities"],
            "q27": ["Government/Public Services"],
            "q29": ["Public service professional", "Manager/Leader"]
        }
    }
}

# ==============================================================================
# 3. TAILORED ROADMAPS (6 STEPS PER CAREER)
# ==============================================================================

CAREER_ROADMAPS = {
    "Software Developer": [
        {"step": 1, "title": "Build Foundation", "desc": "Master computer science basics, binary logic, and fundamentals of Python or C++.", "milestones": ["Learn Variables, Loops & Functions", "Understand Memory & Object-Oriented Programming (OOP)", "Practice basic command line and Git fundamentals"]},
        {"step": 2, "title": "Develop Skills", "desc": "Deep dive into Data Structures and Algorithms (DSA) and relational databases.", "milestones": ["Master Arrays, Linked Lists, Trees & Graphs", "Learn SQL & schema design (PostgreSQL/MySQL)", "Study clean code principles and design patterns"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Develop end-to-end full stack software applications solving real problems.", "milestones": ["Build a CLI task automation tool", "Create a CRUD application with RESTful APIs", "Solve 100+ algorithmic problems on LeetCode/HackerRank"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Document your code on GitHub, create live hosted web demos and write technical articles.", "milestones": ["Create an impressive GitHub profile with READMEs", "Deploy 2 production-ready projects on Render/AWS", "Write technical articles on dev.to or Hashnode"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Contribute to open source projects, participate in hackathons and secure junior software internships.", "milestones": ["Make 3 open-source pull requests", "Participate in national/college hackathons", "Acquire a 3-6 month software development internship"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Excel in technical coding interviews and land a full-time software engineering role.", "milestones": ["Prepare for System Design & Behavioral interviews", "Apply for Software Engineer / Associate Developer roles", "Establish continuous learning in cloud and DevOps"]}
    ],
    "Data Scientist": [
        {"step": 1, "title": "Build Foundation", "desc": "Solidify mathematics, probability, calculus, and programming in Python.", "milestones": ["Master Python basics, NumPy, and Pandas", "Review Linear Algebra, Calculus & Descriptive Statistics", "Learn data cleaning and Exploratory Data Analysis (EDA)"]},
        {"step": 2, "title": "Develop Skills", "desc": "Learn statistical inference, machine learning algorithms and SQL for data queries.", "milestones": ["Study Supervised & Unsupervised Machine Learning", "Master SQL queries, joins, and aggregations", "Learn data visualization with Matplotlib, Seaborn, and Tableau"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Work on real-world datasets from Kaggle to build predictive models.", "milestones": ["Complete 3 Kaggle prediction competitions", "Build an end-to-end customer churn prediction pipeline", "Deploy ML models via Flask/FastAPI microservices"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Publish documented Jupyter notebooks and interactive Streamlit data dashboards.", "milestones": ["Build an interactive portfolio dashboard with Streamlit", "Write comprehensive case studies explaining business insights", "Share predictive modeling insights on LinkedIn"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Work on analytics research projects and seek Data Analyst / Data Science internships.", "milestones": ["Apply for Junior Data Analyst or BI Intern roles", "Engage with the local data science and AI community", "Learn basic Big Data tools like Apache Spark"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Target Data Scientist or Machine Learning Analyst roles across technology and finance.", "milestones": ["Practice take-home data challenges and ML interviews", "Secure Data Scientist / Analytics Consultant role", "Keep up to date with generative AI and LLM evaluation"]}
    ],
    "AI/ML Engineer": [
        {"step": 1, "title": "Build Foundation", "desc": "Learn advanced Python, vector calculus, matrix operations, and classical ML algorithms.", "milestones": ["Master PyTorch or TensorFlow fundamentals", "Learn optimization algorithms (Gradient Descent, Adam)", "Implement linear regression and neural nets from scratch"]},
        {"step": 2, "title": "Develop Skills", "desc": "Specialize in Deep Learning architectures: CNNs, Transformers, and LLM fine-tuning.", "milestones": ["Train Computer Vision and Natural Language Processing models", "Understand Hugging Face ecosystem and model architectures", "Learn ML operations (MLOps) and model quantization"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Build and evaluate custom AI applications integrating neural models.", "milestones": ["Train a domain-specific conversational AI or RAG pipeline", "Build an image classification/detection system", "Optimize inference latency using ONNX and Docker"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Showcase deployed AI microservices, research replications, and Hugging Face spaces.", "milestones": ["Host live interactive AI demos on Hugging Face Spaces", "Write blog posts explaining model architecture breakdowns", "Create a benchmark evaluation comparing foundational models"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Collaborate in AI research labs or join early-stage AI engineering teams.", "milestones": ["Intern as an AI/ML developer at a startup or lab", "Contribute to open-source AI frameworks", "Attend AI conferences and meetups"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Interview for ML Engineer / AI Specialist roles with focus on scalable deployment.", "milestones": ["Master system design for machine learning systems", "Secure role as AI/ML Engineer in high-impact tech", "Continue exploring multimodal architectures and agents"]}
    ],
    "UI/UX Designer": [
        {"step": 1, "title": "Build Foundation", "desc": "Understand visual design fundamentals, typography, color theory, and Gestalt principles.", "milestones": ["Study hierarchy, contrast, balance, and white space", "Master Figma interface, auto-layout, and components", "Learn the fundamentals of Design Thinking"]},
        {"step": 2, "title": "Develop Skills", "desc": "Master user research methodologies, user personas, wireframing, and interactive prototyping.", "milestones": ["Conduct user interviews and create empathy maps", "Build low-fidelity wireframes and high-fidelity mockups", "Create interactive micro-animations and clickable prototypes"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Redesign existing problematic interfaces and build comprehensive product case studies.", "milestones": ["Redesign a complex mobile app and document user pain points", "Create a complete cross-platform design system in Figma", "Perform usability testing sessions with real users"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Assemble a Behance or web portfolio detailing 3 comprehensive end-to-end case studies.", "milestones": ["Document the problem, process, research, and final solution", "Publish polished designs on Behance and Dribbble", "Create a personal design portfolio website"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Join digital design agencies or tech product teams as a UI/UX intern.", "milestones": ["Complete a design internship collaborating with developers", "Present designs in design crits and receive feedback", "Learn basic HTML/CSS to collaborate effectively"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Land a Product Designer or UI/UX Designer role at a product-led company.", "milestones": ["Prepare for portfolio walkthrough and design challenge interviews", "Join as a full-time UI/UX or Product Designer", "Expand into Design Leadership and Design Operations"]}
    ],
    "Web Developer": [
        {"step": 1, "title": "Build Foundation", "desc": "Master semantic HTML5, modern CSS3 (Flexbox & Grid), and modern JavaScript (ES6+).", "milestones": ["Build 5 responsive static website layouts", "Understand DOM manipulation and asynchronous JavaScript", "Learn Git workflow for version control"]},
        {"step": 2, "title": "Develop Skills", "desc": "Learn frontend frameworks (React/Vue) and backend technologies (Node.js/Python/Flask).", "milestones": ["Build component-driven single-page applications", "Create REST APIs and handle HTTP status codes", "Work with relational (SQLite/PostgreSQL) and NoSQL databases"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Create full-stack web applications with authentication, databases, and third-party APIs.", "milestones": ["Build an e-commerce or community portal with user login", "Implement payment gateway or external API integrations", "Ensure cross-browser compatibility and accessibility (a11y)"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Host live web applications on Vercel, Netlify, or Render with custom domains.", "milestones": ["Launch a personal developer portfolio featuring live links", "Optimize Lighthouse scores (performance, SEO, best practices)", "Maintain clean, well-commented code repositories"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Work as a junior web developer intern or freelance web contractor.", "milestones": ["Complete web development client projects or internships", "Collaborate on team repos using pull requests and code reviews", "Participate in local web dev communities"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Begin career as a Full Stack Web Developer or Frontend Specialist.", "milestones": ["Prepare for frontend and backend technical assessments", "Secure a role at a tech company or digital agency", "Explore cloud architectures (AWS/GCP) and CI/CD pipelines"]}
    ],
    "Cybersecurity Analyst": [
        {"step": 1, "title": "Build Foundation", "desc": "Master computer networking fundamentals (TCP/IP, OSI model, DNS) and Linux systems.", "milestones": ["Understand network routing, subnets, and firewalls", "Master Linux terminal commands and shell scripting", "Learn fundamentals of cryptography and hashing"]},
        {"step": 2, "title": "Develop Skills", "desc": "Learn ethical hacking methodologies, vulnerability assessment, and security auditing.", "milestones": ["Use Wireshark, Nmap, and Burp Suite for network analysis", "Study OWASP Top 10 web application vulnerabilities", "Obtain foundational certifications like CompTIA Security+"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Solve security challenges on TryHackMe, Hack The Box, and build home security labs.", "milestones": ["Complete 30+ virtual machines on Hack The Box", "Configure a home lab with Snort or Suricata IDS", "Conduct vulnerability scans and write formal remediation reports"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Document penetration testing writeups and security research on a public blog/GitHub.", "milestones": ["Publish detailed walkthroughs of resolved CTF challenges", "Demonstrate automated Python security audit scripts", "Showcase certifications and badge credentials"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Seek Security Operations Center (SOC) Tier 1 analyst roles or security internships.", "milestones": ["Join a Security Operations Center as an intern/analyst", "Participate in collegiate Cyber Defense Competitions", "Network with infosec professionals on LinkedIn and Twitter"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Advance to Cybersecurity Analyst or Incident Responder.", "milestones": ["Prepare for technical security scenarios and triage interviews", "Earn advanced credentials like CEH, OSCP, or CISSP", "Specialize in cloud security, red teaming, or digital forensics"]}
    ],
    "Business Manager": [
        {"step": 1, "title": "Build Foundation", "desc": "Understand principles of management, organizational behavior, and microeconomics.", "milestones": ["Learn foundational business economics and marketing basics", "Develop strong written and spoken business communication", "Master Microsoft Excel and business presentation tools"]},
        {"step": 2, "title": "Develop Skills", "desc": "Study financial accounting, team leadership, operations management, and data-driven decision making.", "milestones": ["Learn to read balance sheets, P&L statements, and cash flows", "Study agile project management (Scrum, Kanban)", "Practice conflict resolution and interpersonal negotiation"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Lead student organizations, organize major campus initiatives, and solve corporate case competitions.", "milestones": ["Lead a team in organizing an inter-college conference", "Win or place in national management case study challenges", "Create an operational turnaround proposal for a simulated company"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Document leadership milestones, project outcomes, and analytical business reports.", "milestones": ["Build a professional LinkedIn profile highlighting leadership", "Publish case analysis decks and strategic business breakdowns", "Earn project management credentials (CAPM, Google Project Management)"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Secure management internships in operations, consulting, or project management.", "milestones": ["Complete a management training internship in a corporate setting", "Shadow senior executives and understand P&L ownership", "Build a network of industry alumni and mentors"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Join as an Associate Project Manager, Operations Lead, or Management Trainee.", "milestones": ["Excel in behavioral case interviews and assessment centers", "Join top-tier management rotation or consulting firms", "Consider an executive MBA or specialization after 2-3 years"]}
    ],
    "Entrepreneur": [
        {"step": 1, "title": "Build Foundation", "desc": "Cultivate growth mindset, understand business models, unit economics, and customer discovery.", "milestones": ["Read foundational startup literature (Lean Startup, Zero to One)", "Learn how to calculate CAC, LTV, and profit margins", "Observe industry trends and identify real customer pain points"]},
        {"step": 2, "title": "Develop Skills", "desc": "Master Rapid Prototyping, minimum viable product (MVP) design, and sales pitching.", "milestones": ["Conduct 20+ customer problem validation interviews", "Build a no-code or low-code MVP to test market demand", "Design a compelling 10-slide pitch deck for investors"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Launch a small-scale venture, campus service, or digital product to acquire paying customers.", "milestones": ["Acquire your first 10 paying customers or users", "Iterate product features based on direct user feedback", "Establish formal company registration and accounting structure"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Showcase measurable traction, product-market fit metrics, and founder storytelling.", "milestones": ["Document MRR (Monthly Recurring Revenue) or active user growth", "Pitch in collegiate and regional startup incubator competitions", "Build strong visibility across entrepreneurship forums"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Work closely inside an early-stage startup or join an incubator/accelerator program.", "milestones": ["Gain acceptance into an incubator (Y Combinator, Techstars, or university cell)", "Connect with angel investors and industry advisors", "Learn fundraising, hiring, and legal compliance"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Scale your startup full-time or lead innovation as a Venture Lead / Intrapreneur.", "milestones": ["Close a pre-seed or seed funding round / achieve self-sustainability", "Scale operations, hire key team leads, and expand markets", "Build lasting value and industry-defining impact"]}
    ],
    "Financial Analyst": [
        {"step": 1, "title": "Build Foundation", "desc": "Master accounting principles, corporate finance, and intermediate macroeconomics.", "milestones": ["Learn the Three Financial Statements and their interconnections", "Master Excel formulas, pivot tables, and lookup functions", "Understand interest rates, inflation, and capital markets"]},
        {"step": 2, "title": "Develop Skills", "desc": "Build Discounted Cash Flow (DCF) models, comparative company analysis, and sensitivity tables.", "milestones": ["Learn 3-statement financial modeling in Excel", "Study company valuation techniques (DCF, Multiples, Precedents)", "Learn Python for finance or SQL for data queries"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Write comprehensive equity research reports analyzing publicly traded companies.", "milestones": ["Analyze an annual 10-K report and publish an equity valuation report", "Participate in CFA Institute Research Challenge or finance competitions", "Backtest an algorithmic trading strategy using historical data"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Maintain a financial model repository and insightful market analysis reports.", "milestones": ["Publish valuation teardowns of major corporate earnings", "Pass CFA Level 1 or relevant licensing exams", "Share concise financial commentary on LinkedIn"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Intern at equity research desks, corporate treasury, or investment banks.", "milestones": ["Secure an internship in financial planning & analysis (FP&A)", "Network with CFA charterholders and finance alumni", "Learn terminal tools like Bloomberg or FactSet"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Begin as an Analyst in Investment Banking, Equity Research, or Corporate Finance.", "milestones": ["Prepare for technical finance interviews (valuation & accounting)", "Start full-time role as Financial Analyst", "Target CFA / CPA completion to accelerate career trajectory"]}
    ],
    "Mechanical Engineer": [
        {"step": 1, "title": "Build Foundation", "desc": "Solidify engineering physics, calculus, thermodynamics, and engineering graphics.", "milestones": ["Master statics, dynamics, and strength of materials", "Learn standard engineering drawing conventions and GD&T", "Get familiar with workshop tools and basic fabrication"]},
        {"step": 2, "title": "Develop Skills", "desc": "Master 3D CAD modeling (SolidWorks/Creo) and Finite Element Analysis (ANSYS).", "milestones": ["Create parametric 3D CAD assemblies in SolidWorks", "Run structural and thermal FEA simulations in ANSYS", "Learn manufacturing processes (machining, CNC, 3D printing)"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Design and fabricate physical mechanical prototypes or participate in Formula Student / SAE.", "milestones": ["Participate in college BAJA SAE, Formula Student, or robotics team", "Build an automated mechanical mechanism from scratch", "Perform fatigue analysis and optimize design weight"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Compile a detailed mechanical design portfolio showing drawings, FEA results, and prototypes.", "milestones": ["Create a PDF engineering portfolio with rendered CAD models", "Showcase simulation validations and physical test comparisons", "Document hands-on fabrication and assembly experience"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Intern at automotive, aerospace, or manufacturing manufacturing plants.", "milestones": ["Complete industrial training in a manufacturing or design facility", "Learn quality control standards (Six Sigma, ISO 9001)", "Shadow plant engineers and maintenance teams"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Start as a Mechanical Design Engineer, Automotive Specialist, or Robotics Engineer.", "milestones": ["Prepare for core technical interviews on materials and mechanics", "Secure role in automotive, aerospace, or machinery design", "Pursue professional engineering license or higher specialization"]}
    ],
    "Civil Engineer": [
        {"step": 1, "title": "Build Foundation", "desc": "Master engineering mechanics, surveying, building materials, and fluid mechanics.", "milestones": ["Learn plane and geodetic surveying with Total Station", "Understand properties of concrete, steel, and soil mechanics", "Learn drafting in AutoCAD"]},
        {"step": 2, "title": "Develop Skills", "desc": "Master structural analysis software (STAAD.Pro, ETABS) and BIM tools (Revit).", "milestones": ["Model multistory building frames in ETABS", "Learn reinforced concrete and steel structure design codes", "Study environmental engineering and hydrological modeling"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Conduct structural designs for real architectural plans and estimate bills of quantities.", "milestones": ["Design a G+4 residential building structural layout", "Prepare complete quantity estimation and costing sheets", "Conduct geotechnical soil test experiments in labs"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Present engineering drawings, structural analysis reports, and site project logs.", "milestones": ["Assemble a civil portfolio with AutoCAD drawings and ETABS reports", "Certify in Revit Architecture / BIM modeling", "Highlight project management software skills (Primavera/MS Project)"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Work as a site engineer intern on active residential or commercial construction projects.", "milestones": ["Gain hands-on site supervision experience for 3+ months", "Learn bar-bending schedule checking and concrete quality assurance", "Connect with local chapters of Civil Engineering associations"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Begin as a Structural Engineer, Site Engineer, or Project Construction Coordinator.", "milestones": ["Prepare for technical interviews on concrete and structural theory", "Secure role in consulting, infrastructure, or construction firms", "Prepare for government civil examinations or master's degrees"]}
    ],
    "Electrical Engineer": [
        {"step": 1, "title": "Build Foundation", "desc": "Master circuit theory, electromagnetics, differential equations, and signal systems.", "milestones": ["Understand Kirchhoff's laws, AC circuits, and power factor", "Study semiconductor physics and analog electronics", "Learn MATLAB and circuit simulation in SPICE"]},
        {"step": 2, "title": "Develop Skills", "desc": "Study electrical machines, power systems, microcontroller programming, and PCB design.", "milestones": ["Design single and multi-layer PCBs using KiCad/Altium", "Program microcontrollers (STM32/ESP32) in C/C++", "Simulate power grids, transformers, and switchgear in MATLAB/Simulink"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Build embedded electronics hardware or clean energy conversion systems.", "milestones": ["Build a functional solar MPPT charge controller or EV motor driver", "Implement an IoT hardware sensor monitoring device", "Analyze power system stability and fault protections"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Document schematics, soldered PCB prototypes, firmware repos, and simulation results.", "milestones": ["Showcase PCB fabrication photos and circuit schematics on GitHub", "Document firmware architectures and test logs", "Obtain certifications in Embedded Systems or Renewable Energy"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Intern at power utility companies, electronics manufacturers, or EV tech firms.", "milestones": ["Work in hardware testing, power generation, or embedded R&D", "Learn compliance standards (EMI/EMC, safety regulations)", "Network with IEEE members and industry engineers"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Join as an Electrical Engineer, Hardware Design Specialist, or Power Systems Engineer.", "milestones": ["Ace technical circuit analysis and system troubleshooting interviews", "Secure positions in clean energy, automotive, or automation sectors", "Explore high-voltage engineering or VLSI specialization"]}
    ],
    "Doctor/Healthcare Professional": [
        {"step": 1, "title": "Build Foundation", "desc": "Master pre-medical sciences: Human Anatomy, Physiology, Biochemistry, and Cell Biology.", "milestones": ["Excel in pre-medical entrance exams (NEET/MCAT)", "Understand anatomical structures and organ systems", "Master laboratory biological techniques and sterile protocols"]},
        {"step": 2, "title": "Develop Skills", "desc": "Study Pathology, Pharmacology, Microbiology, and fundamentals of Clinical Diagnosis.", "milestones": ["Understand disease mechanisms and pharmaceutical therapeutics", "Learn patient history taking and thorough physical examinations", "Develop active empathetic listening and clinical etiquette"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Undergo clinical hospital rotations across internal medicine, surgery, pediatrics, and emergency care.", "milestones": ["Participate in bedside clinical rounds and patient case discussions", "Practice basic surgical suturing, CPR, and triage protocols", "Shadow senior attending consultants and chief residents"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Engage in clinical audits, medical case study presentations, and academic healthcare research.", "milestones": ["Present a medical case study at a regional medical conference", "Participate in community health camps and vaccination drives", "Maintain immaculate clinical training logbooks"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Complete the mandatory 1-year clinical rotating internship at a teaching hospital.", "milestones": ["Complete emergency medicine, casualty, and rural postings", "Handle independent preliminary patient assessments under supervision", "Build mentorship bonds with leading medical specialists"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Obtain medical license, practice as a physician, or clear postgraduate residency exams.", "milestones": ["Clear medical licensing examinations (USMLE / PLAB / NEXT)", "Enter medical residency in your desired clinical specialty", "Dedicate to lifelong learning and patient-centered service"]}
    ],
    "Teacher/Educator": [
        {"step": 1, "title": "Build Foundation", "desc": "Attain comprehensive subject mastery in your chosen academic discipline.", "milestones": ["Complete bachelor's degree in your chosen subject with honors", "Read educational psychology and childhood/adult learning theories", "Develop articulate public speaking and expressive storytelling"]},
        {"step": 2, "title": "Develop Skills", "desc": "Complete formal pedagogical training (B.Ed / Teaching Certification) and lesson planning.", "milestones": ["Learn diverse instructional strategies and differentiated teaching", "Master classroom management and student engagement techniques", "Incorporate modern EdTech tools (Google Classroom, interactive boards)"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Complete student teaching practicums and design comprehensive curriculum units.", "milestones": ["Deliver 50+ supervised practice lessons to diverse student groups", "Design creative assessment rubrics and interactive learning games", "Provide structured one-on-one student tutoring and remedial help"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Assemble a Teaching Portfolio with sample lesson plans, student feedback, and teaching philosophy.", "milestones": ["Draft a clear statement of your educational philosophy", "Compile video excerpts of successful teaching sessions", "Obtain state/national teacher eligibility qualifications (TET / CTET)"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Work as an apprentice teacher or assistant lecturer in a respected educational institution.", "milestones": ["Gain full semester co-teaching experience", "Participate in parent-teacher conferences and staff development", "Join professional teacher associations and subject communities"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Secure a full-time teaching appointment or university lecturer position.", "milestones": ["Excel in teaching demonstration and interview panels", "Establish a caring, intellectually vibrant classroom community", "Continuously innovate through pedagogical research and workshops"]}
    ],
    "Researcher": [
        {"step": 1, "title": "Build Foundation", "desc": "Build deep expertise in your field, master research methodology, and statistical analysis.", "milestones": ["Complete advanced undergraduate and master's degree courses", "Learn hypothesis formulation and scientific inquiry ethics", "Master statistical tools (R, Python, SPSS, or MATLAB)"]},
        {"step": 2, "title": "Develop Skills", "desc": "Master scientific literature review, experimental design, and academic writing.", "milestones": ["Read and critique 100+ peer-reviewed papers in your niche", "Design reproducible experimental setups or surveys", "Learn academic paper structure and reference management (Zotero)"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Conduct original empirical or theoretical investigations under faculty supervision.", "milestones": ["Formulate a novel research question and execute experiments", "Draft an original scientific manuscript or thesis chapter", "Present preliminary findings at department colloquiums"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Publish peer-reviewed conference or journal articles and share pre-prints on arXiv.", "milestones": ["Submit first-author paper to an indexed journal/conference", "Present poster or oral talk at international research conferences", "Create Google Scholar and ResearchGate research profiles"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Work as a research fellow in premier national/international laboratories or universities.", "milestones": ["Gain research fellowship (CSIR, UGC, NSF, or DAAD)", "Collaborate with international research teams", "Learn grant proposal writing and funding application protocols"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Earn your Ph.D. and progress to Postdoctoral Fellow, Principal Investigator, or R&D Scientist.", "milestones": ["Defend doctoral dissertation successfully", "Secure postdoctoral fellowship or corporate R&D position", "Lead dedicated research initiatives that expand the frontiers of science"]}
    ],
    "Government/Public Service Professional": [
        {"step": 1, "title": "Build Foundation", "desc": "Study constitutional framework, national history, political science, geography, and current affairs.", "milestones": ["Thoroughly understand constitutional rights and administrative structures", "Read national newspapers daily and analyze editorial perspectives", "Build broad general knowledge across socioeconomic issues"]},
        {"step": 2, "title": "Develop Skills", "desc": "Master analytical essay writing, ethics, public policy decision making, and quantitative aptitude.", "milestones": ["Write structured answers on complex socio-economic policies", "Study case studies in administrative ethics and public integrity", "Practice logical reasoning, reading comprehension, and mental aptitude"]},
        {"step": 3, "title": "Practice & Projects", "desc": "Engage in local governance initiatives, civil society internships, or extensive mock examinations.", "milestones": ["Volunteer with grassroots NGOs or civic improvement groups", "Take 50+ timed full-length competitive mock examinations", "Analyze government policy papers and budget speeches"]},
        {"step": 4, "title": "Build Portfolio", "desc": "Excel in competitive civil service exams (UPSC / State PSC / SSC / Public Service boards).", "milestones": ["Clear the preliminary competitive screening exam", "Clear comprehensive written mains examination with high marks", "Prepare a comprehensive biodata and record of extracurricular service"]},
        {"step": 5, "title": "Internship & Networking", "desc": "Undergo personality interviews and specialized academy administrative training.", "milestones": ["Excel in the board personality interview with confidence and poise", "Enter the National Academy of Administration for foundation training", "Undergo district attachments and practical field training"]},
        {"step": 6, "title": "Career & Industry Entry", "desc": "Assume official administrative duties as an officer or public policy executive.", "milestones": ["Take charge of district or sub-divisional administrative responsibilities", "Oversee welfare schemes, infrastructure, and citizen services", "Provide selfless, ethical public leadership to advance society"]}
    ]
}

# ==============================================================================
# 4. RECOMMENDATION ENGINE & SCORING LOGIC
# ==============================================================================

def calculate_skill_profile(responses):
    """
    Computes a 6-dimension skill profile (0-100) from assessment responses.
    Dimensions: Technical, Analytical, Communication, Creativity, Leadership, Teamwork.
    """
    # Raw score accumulators and maximum possible values
    scores = {
        "Technical": 10,
        "Analytical": 10,
        "Communication": 10,
        "Creativity": 10,
        "Leadership": 10,
        "Teamwork": 10
    }
    max_scores = {
        "Technical": 60,
        "Analytical": 60,
        "Communication": 60,
        "Creativity": 60,
        "Leadership": 60,
        "Teamwork": 60
    }

    # Helper to check answer
    def get(qid):
        return responses.get(qid, "")

    # Q1: Enjoyed activity
    q1 = get(1)
    if q1 == "Solving technical problems":
        scores["Technical"] += 10
        scores["Analytical"] += 8
    elif q1 == "Designing or creating things":
        scores["Creativity"] += 10
        scores["Technical"] += 4
    elif q1 == "Helping and communicating with people":
        scores["Communication"] += 10
        scores["Teamwork"] += 8
    elif q1 == "Analyzing information":
        scores["Analytical"] += 10
        scores["Technical"] += 5
    elif q1 == "Managing or organizing activities":
        scores["Leadership"] += 10
        scores["Teamwork"] += 8

    # Q2: Enjoyed subjects
    q2 = get(2)
    if q2 == "Computer/IT":
        scores["Technical"] += 8
    elif q2 in ["Mathematics", "Science"]:
        scores["Analytical"] += 8
        scores["Technical"] += 5
    elif q2 == "Arts/Humanities":
        scores["Creativity"] += 8
        scores["Communication"] += 5
    elif q2 == "Commerce/Economics":
        scores["Analytical"] += 6
        scores["Leadership"] += 5

    # Q5: Tech interest
    q5 = get(5)
    if q5 == "Very interested":
        scores["Technical"] += 10
    elif q5 == "Interested":
        scores["Technical"] += 7
    elif q5 == "Neutral":
        scores["Technical"] += 4

    # Q6: Math confidence
    q6 = get(6)
    if q6 == "Very confident":
        scores["Analytical"] += 10
    elif q6 == "Confident":
        scores["Analytical"] += 7
    elif q6 == "Average":
        scores["Analytical"] += 4

    # Q7: Logical reasoning
    q7 = get(7)
    if q7 == "Excellent":
        scores["Analytical"] += 10
    elif q7 == "Good":
        scores["Analytical"] += 7
    elif q7 == "Average":
        scores["Analytical"] += 4

    # Q8: Communication
    q8 = get(8)
    if q8 == "Excellent":
        scores["Communication"] += 10
    elif q8 == "Good":
        scores["Communication"] += 7
    elif q8 == "Average":
        scores["Communication"] += 4

    # Q9: Tech comfort
    q9 = get(9)
    if q9 == "Very comfortable":
        scores["Technical"] += 10
    elif q9 == "Comfortable":
        scores["Technical"] += 7
    elif q9 == "Average":
        scores["Technical"] += 4

    # Q10: Strongest skill
    q10 = get(10)
    if q10 == "Problem solving":
        scores["Analytical"] += 10
        scores["Technical"] += 5
    elif q10 == "Communication":
        scores["Communication"] += 12
    elif q10 == "Creativity":
        scores["Creativity"] += 12
    elif q10 == "Leadership":
        scores["Leadership"] += 12
    elif q10 == "Analytical thinking":
        scores["Analytical"] += 12
    elif q10 == "Technical skills":
        scores["Technical"] += 12
    elif q10 == "Teamwork":
        scores["Teamwork"] += 12

    # Q12: Working preference
    q12 = get(12)
    if q12 == "Working with a team":
        scores["Teamwork"] += 10
        scores["Communication"] += 4
    elif q12 == "Combination of both":
        scores["Teamwork"] += 7
        scores["Leadership"] += 4
    elif q12 == "Working independently":
        scores["Analytical"] += 4

    # Q14: Responsibility
    q14 = get(14)
    if q14 == "Very comfortable":
        scores["Leadership"] += 10
    elif q14 == "Comfortable":
        scores["Leadership"] += 7

    # Q16: Describes best
    q16 = get(16)
    if q16 == "Analytical":
        scores["Analytical"] += 10
    elif q16 == "Creative":
        scores["Creativity"] += 10
    elif q16 == "Social":
        scores["Communication"] += 10
        scores["Teamwork"] += 6
    elif q16 == "Organized":
        scores["Leadership"] += 6
        scores["Analytical"] += 4
    elif q16 == "Enterprising":
        scores["Leadership"] += 10
        scores["Creativity"] += 5

    # Q17: Public speaking
    q17 = get(17)
    if q17 == "Very comfortable":
        scores["Communication"] += 10
        scores["Leadership"] += 6
    elif q17 == "Comfortable":
        scores["Communication"] += 7

    # Q20: Work style
    q20 = get(20)
    if q20 == "Flexible and creative":
        scores["Creativity"] += 8
    elif q20 == "Collaborative and team-oriented":
        scores["Teamwork"] += 8
        scores["Communication"] += 4
    elif q20 == "Challenging and competitive":
        scores["Leadership"] += 6

    # Normalize to 0 - 100 range with realistic baseline minimum of 20
    normalized = {}
    for key, val in scores.items():
        pct = int(min(100, max(20, round((val / max_scores[key]) * 100))))
        normalized[key] = pct

    return normalized

def evaluate_career_compatibility(student_profile, responses):
    """
    Transparent Python AI Recommendation Engine.
    Evaluates student profile and 30 assessment questions against all 16 careers.
    Returns sorted list of careers with dynamic percentage compatibility and explainable reasons.
    """
    results = []

    # Extract student self-rated attributes
    fav_subjects = (student_profile.get("favorite_subjects") or "").lower()
    interests_text = (student_profile.get("interests") or "").lower()
    education_level = student_profile.get("education") or ""

    skill_profile = calculate_skill_profile(responses)

    # Question answer shortcuts
    q1 = responses.get(1, "")
    q2 = responses.get(2, "")
    q3 = responses.get(3, "")
    q4 = responses.get(4, "")
    q5 = responses.get(5, "")
    q6 = responses.get(6, "")
    q7 = responses.get(7, "")
    q8 = responses.get(8, "")
    q9 = responses.get(9, "")
    q10 = responses.get(10, "")
    q11 = responses.get(11, "")
    q12 = responses.get(12, "")
    q13 = responses.get(13, "")
    q14 = responses.get(14, "")
    q15 = responses.get(15, "")
    q16 = responses.get(16, "")
    q17 = responses.get(17, "")
    q18 = responses.get(18, "")
    q19 = responses.get(19, "")
    q20 = responses.get(20, "")
    q21 = responses.get(21, "")
    q22 = responses.get(22, "")
    q23 = responses.get(23, "")
    q24 = responses.get(24, "")
    q25 = responses.get(25, "")
    q26 = responses.get(26, "")
    q27 = responses.get(27, "")
    q28 = responses.get(28, "")
    q29 = responses.get(29, "")
    q30 = responses.get(30, "")

    for career_name, catalog in CAREER_CATALOG.items():
        base_points = 25.0
        max_possible = 100.0
        reasons = []

        # ----------------------------------------------------
        # Category 1: Interests (Q1 - Q5) (Weight: ~25 points)
        # ----------------------------------------------------
        if q1 in catalog["target_traits"].get("q1", []):
            base_points += 6.0
            reasons.append(f"Enjoyment of '{q1.lower()}'")

        if q2 in catalog["target_traits"].get("q2", []):
            base_points += 6.0
            reasons.append(f"High interest in {q2}")

        if q3 in catalog["target_traits"].get("q3", []):
            base_points += 5.0

        if q4 in catalog["target_traits"].get("q4", []):
            base_points += 5.0
            reasons.append(f"Aptitude for solving {q4.lower()}")

        if "tech" in career_name.lower() or "software" in career_name.lower() or "data" in career_name.lower() or "ai" in career_name.lower() or "web" in career_name.lower() or "cyber" in career_name.lower():
            if q5 == "Very interested":
                base_points += 4.0
            elif q5 == "Interested":
                base_points += 2.5

        # ----------------------------------------------------
        # Category 2: Skills (Q6 - Q11) (Weight: ~20 points)
        # ----------------------------------------------------
        # Quantitative / Math
        if career_name in ["Software Developer", "Data Scientist", "AI/ML Engineer", "Financial Analyst", "Electrical Engineer", "Mechanical Engineer", "Civil Engineer"]:
            if q6 in ["Very confident", "Confident"]:
                base_points += 4.0
            if q7 in ["Excellent", "Good"]:
                base_points += 4.0
                reasons.append(f"Strong logical reasoning ({q7.lower()})")
        
        # Communication
        if career_name in ["UI/UX Designer", "Business Manager", "Entrepreneur", "Doctor/Healthcare Professional", "Teacher/Educator", "Government/Public Service Professional"]:
            if q8 in ["Excellent", "Good"]:
                base_points += 4.0
                reasons.append("Strong communication skills")

        # Computer / Tech comfort
        if career_name in ["Software Developer", "Data Scientist", "AI/ML Engineer", "Web Developer", "Cybersecurity Analyst", "UI/UX Designer"]:
            if q9 in ["Very comfortable", "Comfortable"]:
                base_points += 4.0

        # Strongest skill match
        if q10 in catalog["target_traits"].get("q10", []):
            base_points += 5.0
            reasons.append(f"Key core strength in {q10.lower()}")

        # Learning ability
        if q11 in ["Very good", "Good"]:
            base_points += 3.0

        # ----------------------------------------------------
        # Category 3: Personality (Q12 - Q17) (Weight: ~15 points)
        # ----------------------------------------------------
        if career_name in ["Business Manager", "Entrepreneur", "Civil Engineer", "Government/Public Service Professional"]:
            if q14 in ["Very comfortable", "Comfortable"]:
                base_points += 4.0
                reasons.append("Comfort in taking leadership responsibility")
        
        if career_name in ["Software Developer", "Data Scientist", "Cybersecurity Analyst", "Researcher"]:
            if q15 == "Analyze it step-by-step":
                base_points += 4.0
        elif career_name in ["UI/UX Designer", "Web Developer", "Entrepreneur"]:
            if q15 == "Try creative solutions":
                base_points += 4.0

        if q16 in catalog["target_traits"].get("q16", []):
            base_points += 4.0
            reasons.append(f"Natural {q16.lower()} disposition")

        if career_name in ["Teacher/Educator", "Business Manager", "Government/Public Service Professional", "Doctor/Healthcare Professional"]:
            if q17 in ["Very comfortable", "Comfortable"]:
                base_points += 3.0

        # ----------------------------------------------------
        # Category 4: Work Preferences (Q18 - Q21) (Weight: ~15 points)
        # ----------------------------------------------------
        if q18 in catalog["target_traits"].get("q18", []):
            base_points += 5.0
            reasons.append(f"Preference for {q18.lower()} work environment")

        if q19 in catalog["target_traits"].get("q19", []):
            base_points += 5.0
            reasons.append(f"Preference for {q19.lower()}")

        if q21 == "Yes":
            base_points += 3.0

        # ----------------------------------------------------
        # Category 5: Academic Performance (Q22 - Q25) (Weight: ~10 points)
        # ----------------------------------------------------
        if q23 in catalog["target_traits"].get("q23", []):
            base_points += 5.0
            reasons.append(f"Academic excellence in {q23}")

        # Slight penalty if their weakest subject is a critical core foundation of this career
        if career_name in ["Software Developer", "Data Scientist", "AI/ML Engineer"] and q24 == "Computer Science":
            base_points -= 4.0
        elif career_name in ["Doctor/Healthcare Professional"] and q24 == "Biology":
            base_points -= 5.0
        elif career_name in ["Financial Analyst"] and q24 == "Mathematics":
            base_points -= 4.0

        # ----------------------------------------------------
        # Category 6: Career Goals (Q26 - Q30) (Weight: ~15 points)
        # ----------------------------------------------------
        # Preferred career area exact match is a strong positive signal
        if q27 in catalog["target_traits"].get("q27", []):
            base_points += 9.0
            reasons.append(f"Direct goal alignment with {q27}")

        # Entrepreneurship interest
        if career_name in ["Entrepreneur", "Business Manager"]:
            if q28 == "Very interested":
                base_points += 7.0
                reasons.append("High ambition for entrepreneurial ventures")
            elif q28 == "Interested":
                base_points += 4.0

        # 5-10 year vision
        if q29 in catalog["target_traits"].get("q29", []):
            base_points += 6.0
            reasons.append(f"5-10 year vision as a {q29.lower()}")

        # Profile free-text keywords match
        career_keywords = catalog["title"].lower().split() + [catalog["category"].lower()]
        for kw in career_keywords:
            if len(kw) > 3:
                if kw in fav_subjects or kw in interests_text:
                    base_points += 3.0
                    break

        # Calculate final percentage (bounded between 45% and 98%)
        score_pct = int(min(98, max(42, round(base_points))))

        # Generate custom explainable sentence
        if reasons:
            # Dedup and take top 3-4 reasons
            unique_reasons = []
            for r in reasons:
                if r not in unique_reasons:
                    unique_reasons.append(r)
            top_reasons = unique_reasons[:4]
            if len(top_reasons) > 1:
                explanation = f"Your responses demonstrate {', '.join(top_reasons[:-1])} and {top_reasons[-1]}. These strengths strongly match the core competencies of {catalog['title']}."
            else:
                explanation = f"Your responses highlight {top_reasons[0]}, making {catalog['title']} a natural and compatible career pathway for your profile."
        else:
            explanation = f"Your overall assessment responses and problem-solving orientation match the requirements and work environment of {catalog['title']}."

        results.append({
            "career": catalog["title"],
            "score": score_pct,
            "explanation": explanation,
            "category": catalog["category"],
            "description": catalog["description"],
            "required_skills": catalog["required_skills"],
            "possible_roles": catalog["possible_roles"],
            "work_type": catalog["work_type"],
            "education": catalog["education"],
            "growth_outlook": catalog["growth_outlook"],
            "skill_benchmarks": catalog["skill_benchmarks"]
        })

    # Sort descending by compatibility score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def get_skill_gap_analysis(career_name, student_profile, responses):
    """
    Performs Skill Gap Analysis for the specified career:
    Compares Current Skill Level vs Required Skill Level and suggests actionable improvements.
    """
    if career_name not in CAREER_CATALOG:
        career_name = "Software Developer"

    catalog = CAREER_CATALOG[career_name]
    benchmarks = catalog["skill_benchmarks"]

    # Student skill indicators derived from responses
    q6 = responses.get(6, "Average")
    q7 = responses.get(7, "Average")
    q8 = responses.get(8, "Average")
    q9 = responses.get(9, "Average")
    q10 = responses.get(10, "")
    q11 = responses.get(11, "Average")
    q14 = responses.get(14, "Neutral")
    q17 = responses.get(17, "Average")

    skill_rows = []
    skills_to_improve = []

    level_order = {"Low": 1, "Medium": 2, "High": 3}

    for skill, req_level in benchmarks.items():
        # Heuristic to estimate current level based on skill type
        curr_level = "Medium"
        skill_lower = skill.lower()

        if any(w in skill_lower for w in ["math", "statistic", "calculus", "quantitative"]):
            if q6 == "Very confident":
                curr_level = "High"
            elif q6 in ["Confident", "Average"]:
                curr_level = "Medium"
            else:
                curr_level = "Low"

        elif any(w in skill_lower for w in ["logical", "problem solving", "analytical"]):
            if q7 == "Excellent" or q10 in ["Problem solving", "Analytical thinking"]:
                curr_level = "High"
            elif q7 == "Good":
                curr_level = "Medium"
            else:
                curr_level = "Low"

        elif any(w in skill_lower for w in ["communication", "presentation", "listening", "empathy"]):
            if q8 == "Excellent" or q10 == "Communication" or q17 == "Very comfortable":
                curr_level = "High"
            elif q8 == "Good":
                curr_level = "Medium"
            else:
                curr_level = "Low"

        elif any(w in skill_lower for w in ["program", "code", "python", "tech", "web", "circuit", "cad", "machine learning"]):
            if q9 == "Very comfortable" or q10 == "Technical skills":
                curr_level = "High"
            elif q9 == "Comfortable":
                curr_level = "Medium"
            else:
                curr_level = "Low"

        elif any(w in skill_lower for w in ["leadership", "management", "delegation", "vision"]):
            if q14 == "Very comfortable" or q10 == "Leadership":
                curr_level = "High"
            elif q14 == "Comfortable":
                curr_level = "Medium"
            else:
                curr_level = "Low"

        elif any(w in skill_lower for w in ["creative", "design", "aesthetic", "innovation"]):
            if q10 == "Creativity":
                curr_level = "High"
            else:
                curr_level = "Medium"

        # Evaluate gap
        req_val = level_order.get(req_level, 2)
        curr_val = level_order.get(curr_level, 2)

        if curr_val >= req_val:
            status = "Optimal Alignment"
            badge_class = "badge-success"
        elif curr_val == req_val - 1:
            status = "Moderate Gap"
            badge_class = "badge-warning"
            skills_to_improve.append(skill)
        else:
            status = "Needs Improvement"
            badge_class = "badge-danger"
            skills_to_improve.append(skill)

        skill_rows.append({
            "skill": skill,
            "current_level": curr_level,
            "required_level": req_level,
            "status": status,
            "badge_class": badge_class
        })

    # If no gaps found, suggest advanced mastery in the top 2 required skills
    if not skills_to_improve:
        skills_to_improve = list(benchmarks.keys())[:2]

    # Improvement recommendations
    recommendations = []
    for s in skills_to_improve:
        recommendations.append({
            "skill": s,
            "action": f"Dedicate structured practice to {s}. Take specialized courses, build targeted projects, and seek mentor feedback to elevate your proficiency."
        })

    return {
        "career": career_name,
        "rows": skill_rows,
        "recommended_skills": recommendations
    }

def get_career_roadmap(career_name):
    """Returns the 6-step personalized career roadmap for the selected career."""
    if career_name in CAREER_ROADMAPS:
        return CAREER_ROADMAPS[career_name]
    return CAREER_ROADMAPS.get("Software Developer")

def generate_ai_assistant_response(query_text, student_profile, career_results, responses):
    """
    Intelligent Rule-Based Career Assistant.
    Provides context-aware, personalized career advice utilizing the student's
    actual profile, assessment responses, and top recommended careers.
    """
    q_clean = query_text.lower().strip()

    name = student_profile.get("name", "Student")
    education = student_profile.get("education", "your current level")
    fav_sub = student_profile.get("favorite_subjects", "your favorite subject")

    top_career = career_results[0]["career"] if career_results else "Software Developer"
    top_score = career_results[0]["score"] if career_results else 88
    second_career = career_results[1]["career"] if len(career_results) > 1 else "Data Scientist"
    second_score = career_results[1]["score"] if len(career_results) > 1 else 82

    # Intent 1: "Which career is best for me?" / "best career" / "recommendation"
    if any(k in q_clean for k in ["best for me", "which career", "recommend", "suitable career", "what career should i choose"]):
        return (
            f"Hello {name}! Based on your assessment analysis, your top recommended career path is **{top_career}** with a **{top_score}% compatibility match**.\n\n"
            f"Your second highest match is **{second_career}** ({second_score}% match).\n\n"
            f"**Why {top_career} is best for you:**\n"
            f"Your responses highlighted strong performance in {fav_sub}, coupled with your problem-solving style and work preferences. "
            f"This profile demonstrates strong synergy with the practical and analytical demands of {top_career}."
        )

    # Intent 2: "What skills should I learn?" / "skills to learn" / "improve skills"
    elif any(k in q_clean for k in ["skills should i learn", "what skills", "skills to improve", "skill gap", "skills to learn"]):
        gap_data = get_skill_gap_analysis(top_career, student_profile, responses)
        skills_list = [item["skill"] for item in gap_data["recommended_skills"]]
        skills_formatted = "\n".join([f"• **{s}**: Focus on hands-on practice and targeted online courses." for s in skills_list])
        return (
            f"For your target career as a **{top_career}**, here are the critical priority skills you should learn and strengthen:\n\n"
            f"{skills_formatted}\n\n"
            f"💡 **Recommendation:** Start by strengthening one foundational skill per month using structured projects rather than passive reading."
        )

    # Intent 3: "How can I become a Data Scientist?" / specific career how-to
    elif "data scientist" in q_clean or "data science" in q_clean:
        return (
            f"To become a **Data Scientist**, follow this structured pathway:\n\n"
            f"1. **Foundations:** Master Python (or R), along with Linear Algebra, Calculus, and Statistics.\n"
            f"2. **Data Wrangling & SQL:** Learn Pandas, NumPy, and complex SQL joins for database querying.\n"
            f"3. **Machine Learning:** Study regression, classification, clustering, and Scikit-Learn.\n"
            f"4. **Visualization & Storytelling:** Build dashboards in Tableau, PowerBI, or Streamlit.\n"
            f"5. **Real-world Projects:** Complete predictive competitions on Kaggle and publish Jupyter notebooks on GitHub.\n"
            f"6. **Internships:** Apply for Junior Data Analyst or BI Intern positions to gain real industry exposure."
        )

    # Intent 4: "Software Developer" roadmap or inquiry
    elif "software developer" in q_clean or "software engineer" in q_clean or "coding" in q_clean:
        return (
            f"To excel as a **Software Developer**, here is your actionable roadmap:\n\n"
            f"1. **Core Language:** Deeply learn one core programming language (Python, Java, C++, or JavaScript).\n"
            f"2. **Data Structures & Algorithms:** Practice arrays, trees, hash maps, and sorting algorithms on platforms like LeetCode.\n"
            f"3. **Databases & Architecture:** Learn relational databases (SQL) and fundamental system architecture.\n"
            f"4. **Full-Stack Development:** Build end-to-end applications integrating frontends, APIs, and databases.\n"
            f"5. **Version Control & GitHub:** Maintain a clean commit history and collaborate with pull requests.\n"
            f"6. **Industry Internship:** Gain experience collaborating within an engineering team."
        )

    # Intent 5: "What should I study after 12th?" / Education inquiry
    elif any(k in q_clean for k in ["after 12th", "after 10th", "what to study", "degree", "college"]):
        if "12th" in education or "10th" in education or "after 12th" in q_clean:
            if top_career in ["Software Developer", "Data Scientist", "AI/ML Engineer", "Web Developer", "Cybersecurity Analyst"]:
                degree_advice = "Pursue a B.Tech / B.E. in Computer Science, Data Science, AI, or Information Technology. Alternatively, a BCA followed by MCA is an excellent pathway."
            elif top_career in ["Mechanical Engineer", "Civil Engineer", "Electrical Engineer"]:
                degree_advice = "Pursue a B.Tech / B.E. in the respective core engineering discipline from an accredited university."
            elif top_career in ["Doctor/Healthcare Professional"]:
                degree_advice = "Prepare for medical entrance exams (such as NEET/MCAT) to pursue MBBS, BDS, or specialized Allied Health Sciences (B.Sc Biotechnology/Nursing)."
            elif top_career in ["Business Manager", "Entrepreneur", "Financial Analyst"]:
                degree_advice = "Pursue a BBA, B.Com (Honours), Bachelor of Management Studies (BMS), or Economics (Hons) followed by an MBA."
            elif top_career in ["UI/UX Designer"]:
                degree_advice = "Consider a Bachelor of Design (B.Des), Human-Computer Interaction (HCI), Fine Arts (BFA), or Computer Science with design specialization."
            else:
                degree_advice = f"Pursue a relevant Bachelor's degree (BA/B.Sc/B.Com) aligned with {top_career} and build practical certifications alongside."

            return (
                f"For your current education stage ({education}) aiming towards **{top_career}**:\n\n"
                f"🎓 **Recommended Degree Choice:**\n{degree_advice}\n\n"
                f"💡 **Tip:** Alongside your formal degree, complete industry-recognized online certifications and hands-on projects to stand out to employers."
            )
        else:
            return (
                f"Since your current qualification is **{education}**, you are in an ideal position to pursue specialized certifications, postgraduate studies (like M.Tech, MS, or MBA), or direct entry-level industry roles in **{top_career}**."
            )

    # Intent 6: "Which career matches my interests?"
    elif any(k in q_clean for k in ["matches my interests", "interests match", "my interest"]):
        return (
            f"Your specified interests in **{student_profile.get('interests', 'various domains')}** and favorite subjects (**{fav_sub}**) are most compatible with:\n\n"
            f"1. **{top_career}** ({top_score}% Compatibility)\n"
            f"2. **{second_career}** ({second_score}% Compatibility)\n\n"
            f"These careers allow you to apply your natural curiosity in practical environments without feeling forced or repetitive."
        )

    # Intent 7: "Roadmap for becoming..."
    elif any(k in q_clean for k in ["roadmap", "steps to become", "path"]):
        roadmap_steps = get_career_roadmap(top_career)
        steps_text = "\n".join([f"**Step {s['step']}: {s['title']}** — {s['desc']}" for s in roadmap_steps[:4]])
        return (
            f"Here is your personalized roadmap outline for becoming a **{top_career}**:\n\n"
            f"{steps_text}\n\n"
            f"👉 Visit the **Career Roadmap** page in the top navigation to view the complete 6-step milestone breakdown, recommended tools, and certifications!"
        )

    # Fallback / General inquiry
    else:
        return (
            f"Thank you for your question, {name}!\n\n"
            f"Regarding your inquiry about *\"{query_text}\"*:\n"
            f"In the context of your top career recommendation as a **{top_career}** ({top_score}% match):\n\n"
            f"• **Focus on Fundamentals:** Ensure you build strong foundational expertise in your core subjects.\n"
            f"• **Practical Application:** Theory alone is insufficient—build tangible projects and document them.\n"
            f"• **Networking & Mentorship:** Connect with working professionals in {top_career} to gain firsthand insights.\n\n"
            f"Feel free to ask specific questions about required skills, college degrees, roadmaps, or interview preparation!"
        )
