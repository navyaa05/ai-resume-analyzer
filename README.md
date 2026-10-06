# AI Resume Analyzer 

A simple web application that checks how well a resume matches a job description.

The user uploads their resume, pastes a job description, and the application analyzes both to give a match score, identify skills, find missing skills, and provide suggestions.

## Features

- Upload a resume as PDF or DOCX
- Extract text from the resume
- Compare the resume with a job description
- Calculate a job match score
- Calculate a skill match score
- Find skills mentioned in the resume
- Find skills required by the job
- Identify missing skills
- Give recommendations for improving the resume

## How it works

1. Upload your resume.
2. Paste the job description.
3. Click "Analyze Resume".
4. The application extracts the resume text.
5. It checks the skills mentioned in both the resume and job description.
6. It uses TF-IDF and cosine similarity to calculate the overall match.
7. It shows the results and missing skills.

## Technologies Used

- Python
- Flask
- HTML
- CSS
- Scikit-learn
- PyMuPDF
- python-docx
- Git
- GitHub

## Project Structure

```text
ai-resume-analyzer/
│
├── templates/
│   ├── index.html
│   └── results.html
│
├── static/
├── uploads/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Run the Project
1. Clone the repository
git clone https://github.com/navyaa05/ai-resume-analyzer.git

2. Open the project
cd ai-resume-analyzer

3. Create a virtual environment
py -m venv venv

4. Activate the virtual environment
For PowerShell:
.\venv\Scripts\Activate.ps1

5. Install the required packages
pip install -r requirements.txt

6. Start the application
py app.py

Then open:
http://127.0.0.1:5000

Example
The application can compare a resume with a job description and show results such as:
Job Match Score: 65.42%

Skill Match: 75%

Skills Found:
Python
Java
Git
SQL

Missing Skills:
AWS
Docker
Kubernetes

## Future Improvements
Some things I would like to add in the future:
- Better AI-based resume analysis
- More advanced skill extraction
- Job recommendations
- Resume improvement suggestions
- Database for storing previous analyses
- User accounts
- Cloud deployment
- Docker
- GitHub Actions and CI/CD
- Automated testing

## Author
Navyashree Kodanda
MSc Advanced Computer Science
University of Hertfordshire

