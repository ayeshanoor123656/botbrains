from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from scoring_engine import rank_opportunities

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD DATA ----------------

def load_students():
    with open("students.json") as f:
        return json.load(f)

def load_emails():
    with open("emails.json") as f:
        return json.load(f)


# ---------------- MOCK EXTRACTION (TEMP) ----------------
# ⚠️ Replace this with your friend's function later

def mock_extract(email):
    body = email["body"].lower()

    return {
        "title": email["subject"],
        "type": "internship" if "internship" in body else
                "scholarship" if "scholarship" in body else
                "competition" if "competition" in body else
                "fellowship" if "fellowship" in body else "other",

        "deadline": "2026-04-20",  # temporary (replace later)
        "min_cgpa": 3.0,
        "skills_required": ["python"],
        "location": "remote",
        "documents_required": ["cv"]
    }


# ---------------- MAIN API ----------------

@app.get("/")
def home():
    return {"message": "Opportunity Ranking API Running 🚀"}


@app.get("/rank/{student_id}")
def rank(student_id: str):
    students = load_students()
    emails = load_emails()

    # ---------- Find student ----------
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        return {"error": "Student not found"}

    # ---------- Run extraction ----------
    for email in emails:
        if email["isOpportunity"]:
            # Replace this with real extraction later
            email["structured"] = mock_extract(email)

    # ---------- Run ranking ----------
    ranked = rank_opportunities(student, emails)

    return {
        "student": student["name"],
        "results": ranked
    }