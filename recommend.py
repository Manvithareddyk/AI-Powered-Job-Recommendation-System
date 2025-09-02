import pandas as pd
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Load datasets
# ----------------------------
jobs = pd.read_csv("job_data_cleaned.csv")
users = pd.read_csv("user_profiles_cleaned.csv")

# Define columns
job_text_col = 'Cleaned_Description'
job_title_col = 'Title'
job_id_col = 'job_id'
job_location_col = 'Location'
jobs[job_id_col] = jobs.index

user_text_col = 'Cleaned_Resume'
user_id_col = 'user_id'
user_location_col = 'Location'
user_skills_col = 'Skills'
users[user_id_col] = users.index

# ----------------------------
# Load embedding model
# ----------------------------
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# ----------------------------
# Create embeddings
# ----------------------------
print("Creating embeddings for jobs and users...")
job_embeddings = model.encode(
    jobs[job_text_col].astype(str).tolist(),
    convert_to_tensor=False
)
user_embeddings = model.encode(
    users[user_text_col].astype(str).tolist(),
    convert_to_tensor=False
)

# ----------------------------
# Similarity matrix
# ----------------------------
print("Calculating cosine similarity...")
similarity_matrix = cosine_similarity(user_embeddings, job_embeddings)

# ----------------------------
# Helper: Skill match %
# ----------------------------
def calculate_skill_match(user_skills, job_desc):
    if pd.isna(user_skills) or not user_skills:
        return 0
    user_skills_set = set([s.strip().lower() for s in user_skills.split(",")])
    job_words_set = set(re.findall(r"\w+", str(job_desc).lower()))
    match = user_skills_set.intersection(job_words_set)
    return (len(match) / len(user_skills_set)) * 100 if user_skills_set else 0

# ----------------------------
# Batch recommender (for all users in CSV)
# ----------------------------
def recommend_jobs_for_user(user_index, top_n=10, min_skill_match=30):
    sim_scores = similarity_matrix[user_index]
    user_location = users.loc[user_index, user_location_col] if user_location_col in users.columns else None
    user_skills = users.loc[user_index, user_skills_col] if user_skills_col in users.columns else None

    job_scores = []
    for job_idx, score in enumerate(sim_scores):
        job_location = jobs.loc[job_idx, job_location_col]
        job_desc = jobs.loc[job_idx, job_text_col]

        # Location filter (strict)
        if user_location and str(user_location).lower() not in str(job_location).lower():
            continue

        # Skill filter
        skill_match = calculate_skill_match(user_skills, job_desc)
        if skill_match < min_skill_match:
            continue

        job_scores.append((job_idx, score, skill_match))

    job_scores = sorted(job_scores, key=lambda x: x[1], reverse=True)[:top_n]

    return jobs.iloc[[j[0] for j in job_scores]][[job_id_col, job_title_col, job_location_col]]

# ----------------------------
# Flask-friendly recommender (for form input)
# ----------------------------
def recommend_jobs(user_profile, jobs_df=None, top_n=10, min_skill_match=10):
    """
    Recommend jobs for a single user profile dictionary.
    user_profile = {"skills": "...", "experience": "...", "location": "..."}
    """
    if jobs_df is None:
        jobs_df = jobs

    # Encode user input text
    user_text = f"{user_profile.get('skills','')} {user_profile.get('experience','')} {user_profile.get('location','')}"
    user_embedding = model.encode([user_text], convert_to_tensor=False)

    # Compute similarity with all jobs
    sim_scores = cosine_similarity(user_embedding, job_embeddings).flatten()

    job_scores = []
    for job_idx, score in enumerate(sim_scores):
        job_location = jobs.loc[job_idx, job_location_col]
        job_desc = jobs.loc[job_idx, job_text_col]

        # --------------------------
        # Location filter (soft)
        # --------------------------
        if user_profile.get("location"):
            if str(user_profile["location"]).lower() not in str(job_location).lower():
                # Reduce similarity instead of skipping
                score *= 0.8  

        # --------------------------
        # Skills filter (flexible)
        # --------------------------
        skill_match = calculate_skill_match(user_profile.get("skills",""), job_desc)
        if skill_match < min_skill_match:
            # Reduce score instead of skipping
            score *= 0.7  

        job_scores.append((job_idx, score, skill_match))

    # Sort by adjusted similarity
    job_scores = sorted(job_scores, key=lambda x: x[1], reverse=True)[:top_n]

    results = []
    for idx, sim, skill_match in job_scores:
        results.append({
            "title": jobs.loc[idx, job_title_col],
            "location": jobs.loc[idx, job_location_col],
            "skills": user_profile.get("skills", ""),
            "similarity": round(sim, 3),
            "skill_match": round(skill_match, 2)
        })

    return results

# ----------------------------
# Test run (can comment out when using Flask)
# ----------------------------
if __name__ == "__main__":
    test_user = {"skills": "python, sql", "experience": "2", "location": "Hyderabad"}
    print("\nSample Recommendations:")
    print(recommend_jobs(test_user, top_n=5))
