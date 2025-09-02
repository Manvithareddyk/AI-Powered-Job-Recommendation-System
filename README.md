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

## Installation & Setup
1. Clone Repository
git clone https://github.com/your-username/job-recommendation.git
cd job-recommendation

2. Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3. Install Dependencies
pip install -r requirements.txt


If you don’t have a requirements.txt, install manually:

pip install flask pandas scikit-learn sentence-transformers

4. Run Flask App
python app.py

5. Open in Browser
http://127.0.0.1:5000

## 🎯 Usage

Enter your skills (comma-separated), experience (years), and preferred location.

Click “Get Recommendations”.

The app displays Top 10 job matches with:

Job Title

Location

Similarity Score (%)

Skill Match (%)

⚠️ If no exact matches are found → you’ll see a notice and fallback recommendations.

## 📸 Demo Preview
🔹 Input Form
Skills: Python, SQL, NLP
Experience: 2
Location: Hyderabad
[ Get Recommendations ]

## 🔹 Output Table
Title	Location	Skills	Similarity	Skill Match %
Data Scientist	Hyderabad	Python, SQL	85.23%	70%
NLP Engineer	Remote	Python, NLP	81.12%	80%
📊 How It Works
flowchart TD
    A[User Input] --> B[NLP Preprocessing]
    B --> C[Sentence Transformer Embeddings]
    C --> D[Cosine Similarity + Skill Match %]
    D --> E[Ranked Job List]
    E --> F[Flask Frontend Display]

## 🌍 Real-Time Extension

Right now, the system uses static CSV datasets.
For a real-time job portal, data can come from:

Job APIs (LinkedIn, Indeed, Adzuna)

Web Scraping (BeautifulSoup, Selenium)

Company HR Databases

User data can be collected via:

Manual input (skills, experience, location)

Resume upload (PDF/DOCX) with NLP parsing

## 🔮 Future Improvements

📂 Resume Upload & Parsing

🎯 Collaborative Filtering (behavior-based recs)

📈 Skill Gap Analysis (suggesting courses)

☁️ Cloud Deployment (Render, Streamlit, AWS)
