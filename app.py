from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import sqlite3
import bcrypt
import re
from recommend import recommend_jobs   # import the Flask-ready function

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure random key

# Load job dataset once
jobs_df = pd.read_csv("job_data_cleaned.csv")

# Initialize database
conn = sqlite3.connect('job_recommender.db', check_same_thread=False)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create resumes table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    skills TEXT NOT NULL,
    education TEXT,
    work_experience TEXT,
    preferred_location TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
)
''')

conn.commit()

# Hash password function using bcrypt
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

# Check password strength
def is_password_strong(password):
    # At least 8 characters, one uppercase, one lowercase, one digit, one special character
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True



@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    if request.method == "POST":
        # Get inputs from form
        skills = request.form.get("skills")
        experience = request.form.get("experience")
        location = request.form.get("location")

        # Build a user profile dict
        user_profile = {
            "skills": skills,
            "experience": experience,
            "location": location
        }

        # Call recommendation engine
        recommendations = recommend_jobs(user_profile, jobs_df, top_n=10)

    return render_template("index.html", recommendations=recommendations)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Validate inputs
        if not phone or not password or not confirm_password:
            return render_template("register.html", error="All fields are required")

        # Check phone format (simplified)
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return render_template("register.html", error="Invalid phone number format")

        # Check password strength
        if not is_password_strong(password):
            return render_template("register.html", error="Password must be at least 8 characters long, contain uppercase, lowercase, digit, and special character")

        # Check password match
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")

        # Check if phone already exists
        cursor.execute("SELECT id FROM users WHERE phone = ?", (phone,))
        if cursor.fetchone():
            return render_template("register.html", error="Phone number already registered")

        # Hash password and create user
        hashed_password = hash_password(password).decode('utf-8')
        cursor.execute("INSERT INTO users (phone, password) VALUES (?, ?)", (phone, hashed_password))
        conn.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form.get("phone")
        password = request.form.get("password")
        captcha_valid = request.form.get("captcha_valid")

        # Validate inputs
        if not phone or not password:
            return render_template("login.html", error="Phone number and password are required")

        # Check captcha validation
        if captcha_valid != "true":
            return render_template("login.html", error="Please complete the captcha first")

        # Check phone format
        if not re.match(r'^1[3-9]\d{9}$', phone):
            return render_template("login.html", error="Invalid phone number format")

        # Check user credentials
        cursor.execute("SELECT id, password FROM users WHERE phone = ?", (phone,))
        user = cursor.fetchone()
        
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user[1]):
            return render_template("login.html", error="Invalid phone or password")

        # Set session
        session["user_id"] = user[0]
        session["phone"] = phone
        return redirect(url_for("dashboard"))

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get user resume
    cursor.execute("SELECT * FROM resumes WHERE user_id = ?", (session["user_id"],))
    resume = cursor.fetchone()

    return render_template("dashboard.html", resume=resume)

@app.route("/resume", methods=["GET", "POST"])
def resume():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name")
        skills = request.form.get("skills")
        education = request.form.get("education")
        work_experience = request.form.get("work_experience")
        preferred_location = request.form.get("preferred_location")

        # Validate inputs
        if not name or not skills:
            return render_template("resume.html", error="Name and skills are required")

        # Check if resume exists
        cursor.execute("SELECT id FROM resumes WHERE user_id = ?", (session["user_id"],))
        existing_resume = cursor.fetchone()

        if existing_resume:
            # Update existing resume
            cursor.execute('''UPDATE resumes SET name = ?, skills = ?, education = ?, work_experience = ?, preferred_location = ? WHERE user_id = ?''',
                           (name, skills, education, work_experience, preferred_location, session["user_id"]))
        else:
            # Create new resume
            cursor.execute('''INSERT INTO resumes (user_id, name, skills, education, work_experience, preferred_location) VALUES (?, ?, ?, ?, ?, ?)''',
                           (session["user_id"], name, skills, education, work_experience, preferred_location))

        conn.commit()
        return redirect(url_for("dashboard"))

    # Get existing resume for editing
    cursor.execute("SELECT * FROM resumes WHERE user_id = ?", (session["user_id"],))
    resume = cursor.fetchone()

    return render_template("resume.html", resume=resume)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
