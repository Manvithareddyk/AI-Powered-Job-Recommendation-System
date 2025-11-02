from flask import Flask, render_template, request
import pandas as pd
from recommend import recommend_jobs   # import the Flask-ready function
import PyPDF2
from docx import Document
import re

app = Flask(__name__)

# Load job dataset once
jobs_df = pd.read_csv("job_data_cleaned.csv")

# Function to read PDF file
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to read Word file
def read_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to parse resume text and extract skills, experience, and location
def parse_resume(text):
    # Define patterns for extracting information
    skills_pattern = r'(?i)skills|technical skills|proficient in|expertise|competencies'
    experience_pattern = r'(?i)experience|work experience|years of experience|total experience'
    location_pattern = r'(?i)location|preferred location|current location|based in'
    
    # Extract skills
    skills_match = re.search(skills_pattern, text)
    skills = ""
    if skills_match:
        # Get text after skills heading
        skills_section = text[skills_match.end():]
        # Find the next heading to stop
        next_heading = re.search(r'\n\s*[A-Z][a-zA-Z\s]+:', skills_section)
        if next_heading:
            skills_section = skills_section[:next_heading.start()]
        # Extract skills (assuming they are comma-separated or on new lines)
        skills = re.sub(r'[^a-zA-Z0-9,\s]', '', skills_section).strip()
        # Replace newlines with commas
        skills = skills.replace('\n', ', ')
    
    # Extract experience
    experience_match = re.search(experience_pattern, text)
    experience = ""
    if experience_match:
        # Get text after experience heading
        experience_section = text[experience_match.end():]
        # Find the next heading to stop
        next_heading = re.search(r'\n\s*[A-Z][a-zA-Z\s]+:', experience_section)
        if next_heading:
            experience_section = experience_section[:next_heading.start()]
        # Extract years of experience
        years_match = re.search(r'(\d+)\s*years?', experience_section)
        if years_match:
            experience = years_match.group(1)
    
    # Extract location
    location_match = re.search(location_pattern, text)
    location = ""
    if location_match:
        # Get text after location heading
        location_section = text[location_match.end():]
        # Find the next heading to stop
        next_heading = re.search(r'\n\s*[A-Z][a-zA-Z\s]+:', location_section)
        if next_heading:
            location_section = location_section[:next_heading.start()]
        # Extract location (assuming it's a city name)
        location = re.sub(r'[^a-zA-Z\s]', '', location_section).strip()
    
    return skills, experience, location

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    skills = ""
    experience = ""
    location = ""
    
    if request.method == "POST":
        # Get inputs from form
        skills = request.form.get("skills")
        experience = request.form.get("experience")
        location = request.form.get("location")
        
        # Check if resume file is uploaded
        if "resume" in request.files and request.files["resume"].filename != "":
            resume_file = request.files["resume"]
            
            # Read file content based on file type
            if resume_file.filename.endswith('.pdf'):
                text = read_pdf(resume_file)
            elif resume_file.filename.endswith('.docx') or resume_file.filename.endswith('.doc'):
                text = read_docx(resume_file)
            else:
                text = ""
            
            # Parse resume if text is extracted
            if text:
                parsed_skills, parsed_experience, parsed_location = parse_resume(text)
                
                # Use parsed values if user didn't provide manual inputs
                if not skills:
                    skills = parsed_skills
                if not experience:
                    experience = parsed_experience
                if not location:
                    location = parsed_location
        
        # Validate inputs
        if not skills:
            skills = ""
        if not experience:
            experience = ""
        if not location:
            location = ""

        # Build a user profile dict
        user_profile = {
            "skills": skills,
            "experience": experience,
            "location": location
        }

        # Call recommendation engine
        recommendations = recommend_jobs(user_profile, jobs_df, top_n=10)

    return render_template("index.html", recommendations=recommendations, skills=skills, experience=experience, location=location)

if __name__ == "__main__":
    app.run(debug=True)
