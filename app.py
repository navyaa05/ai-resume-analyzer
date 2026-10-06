from flask import Flask, render_template, request
import fitz
import os
import re
from docx import Document

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)

# ==========================================
# CONFIGURATION
# ==========================================

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


# ==========================================
# SKILLS DATABASE
# ==========================================

SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "TypeScript",
    "HTML",
    "CSS",
    "SQL",
    "NoSQL",
    "AWS",
    "Azure",
    "Google Cloud",
    "GCP",
    "Docker",
    "Kubernetes",
    "Git",
    "GitHub",
    "GitLab",
    "Jenkins",
    "CI/CD",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "AI",
    "Natural Language Processing",
    "NLP",
    "Data Science",
    "Data Structures",
    "Algorithms",
    "Flask",
    "Django",
    "FastAPI",
    "React",
    "Node.js",
    "Spring",
    "REST API",
    "REST",
    "PostgreSQL",
    "MongoDB",
    "MySQL",
    "Linux",
    "Terraform",
    "Ansible",
    "PyTorch",
    "TensorFlow",
    "Scikit-learn"
]


# ==========================================
# SKILL EXTRACTION
# ==========================================

def extract_skills(text):

    found_skills = []

    for skill in SKILLS:

        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text,
            re.IGNORECASE
        ):
            found_skills.append(skill)

    return found_skills


# ==========================================
# RECOMMENDATIONS
# ==========================================

def generate_recommendations(missing_skills):

    recommendations = []

    for skill in missing_skills:

        recommendations.append(
            f"Add a project or practical experience demonstrating {skill}."
        )

    if not recommendations:

        recommendations.append(
            "Your resume covers the main skills identified in the job description."
        )

    return recommendations


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")


# ==========================================
# ANALYZE RESUME
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files.get("resume")

    job_description = request.form.get(
        "job",
        ""
    )

    resume_text = ""


    # ======================================
    # CHECK RESUME
    # ======================================

    if not resume or not resume.filename:

        return render_template(
            "results.html",
            resume_name="No resume uploaded",
            match_score=0,
            skill_match_score=0,
            resume_skills=[],
            job_skills=[],
            missing_skills=[],
            recommendations=[
                "Please upload a PDF or DOCX resume."
            ],
            message="Resume upload required."
        )


    # ======================================
    # PDF
    # ======================================

    if resume.filename.lower().endswith(".pdf"):

        resume_data = resume.read()

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume.filename
        )

        with open(file_path, "wb") as file:

            file.write(resume_data)

        pdf = fitz.open(
            stream=resume_data,
            filetype="pdf"
        )

        for page in pdf:

            resume_text += page.get_text()

        pdf.close()


    # ======================================
    # DOCX
    # ======================================

    elif resume.filename.lower().endswith(".docx"):

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume.filename
        )

        resume.save(file_path)

        document = Document(file_path)

        for paragraph in document.paragraphs:

            resume_text += paragraph.text + "\n"


    # ======================================
    # INVALID FILE
    # ======================================

    else:

        return render_template(
            "results.html",
            resume_name=resume.filename,
            match_score=0,
            skill_match_score=0,
            resume_skills=[],
            job_skills=[],
            missing_skills=[],
            recommendations=[
                "Please upload a PDF or DOCX file."
            ],
            message="Unsupported file type."
        )


    # ======================================
    # EXTRACT SKILLS
    # ======================================

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )


    # ======================================
    # FIND MISSING SKILLS
    # ======================================

    resume_skill_names = [
        skill.lower()
        for skill in resume_skills
    ]

    missing_skills = [

        skill

        for skill in job_skills

        if skill.lower()
        not in resume_skill_names

    ]


    # ======================================
    # RECOMMENDATIONS
    # ======================================

    recommendations = generate_recommendations(
        missing_skills
    )


    # ======================================
    # OVERALL MATCH SCORE
    # ======================================

    match_score = 0

    if (
        resume_text.strip()
        and job_description.strip()
    ):

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            [
                resume_text,
                job_description
            ]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        match_score = round(
            similarity * 100,
            2
        )


    # ======================================
    # SKILL MATCH SCORE
    # ======================================

    skill_match_score = 0

    if job_skills:

        matched_skills = [

            skill

            for skill in job_skills

            if skill.lower()
            in resume_skill_names

        ]

        skill_match_score = round(
            (
                len(matched_skills)
                / len(job_skills)
            ) * 100,
            2
        )


    # ======================================
    # RESULTS
    # ======================================

    return render_template(
        "results.html",

        resume_name=resume.filename,

        match_score=match_score,

        skill_match_score=skill_match_score,

        resume_skills=resume_skills,

        job_skills=job_skills,

        missing_skills=missing_skills,

        recommendations=recommendations,

        message="Resume analyzed successfully!"
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )