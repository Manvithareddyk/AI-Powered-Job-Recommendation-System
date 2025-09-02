# 🧠 AI-Powered Job Recommendation System  

An **AI-powered job recommendation engine** that uses **Natural Language Processing (NLP)** and **Machine Learning** to suggest jobs tailored to a user’s **skills, experience, and location**.  

Built using **Sentence Transformers**, **Flask**, and **scikit-learn**, this project demonstrates how intelligent job portals can go beyond keyword search to deliver **personalized, context-aware recommendations**.  

---

## 🚀 Features
- ✔️ Cleans & preprocesses job and resume data  
- ✔️ Embeds text using **BERT-based sentence transformers**  
- ✔️ Matches profiles to jobs using **cosine similarity**  
- ✔️ Calculates **skill match percentage**  
- ✔️ Applies **location-based filtering** (soft matching)  
- ✔️ Flask frontend for **interactive job search**  
- ✔️ Always returns recommendations (fallback mode if filters too strict)  

---

## 📂 Project Structure
```bash
AI-Powered-Job-Recommendation/
│── app.py                     # Flask frontend
│── recommend.py               # ML engine + recommendation logic
│── job_data_cleaned.csv       # Preprocessed job postings
│── user_profiles_cleaned.csv  # Preprocessed user profiles
│── templates/
│    └── index.html            # Frontend form + results
│── static/
│    └── style.css             # Styling for frontend
│── requirements.txt           # Project dependencies
│── README.md                  # Project documentation
