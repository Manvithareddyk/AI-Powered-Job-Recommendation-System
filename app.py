from flask import Flask, render_template, request
import pandas as pd
from recommend import recommend_jobs   # import the Flask-ready function

app = Flask(__name__)

# Load job dataset once
jobs_df = pd.read_csv("job_data_cleaned.csv")

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

if __name__ == "__main__":
    app.run(debug=True)
