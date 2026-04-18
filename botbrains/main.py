from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from scoring_engine import rank_opportunities

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD FILES ----------------

def load_students():
    with open("students.json", "r") as f:
        return json.load(f)

def load_emails():
    with open("parsed_emails.json", "r") as f:
        return json.load(f)


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "Opportunity Inbox Copilot API 🚀"
    }


# ---------------- GET ALL STUDENTS ----------------

@app.get("/students")
def get_students():
    return load_students()


# ---------------- RANK OPPORTUNITIES ----------------

@app.get("/rank/{student_id}")
def rank(student_id: str):

    students = load_students()
    emails = load_emails()

    # ---------- find student ----------
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        return {"error": "Student not found"}

    # ---------- run ranking ----------
    ranked = rank_opportunities(student, emails)

    return {
        "student": student,
        "total_opportunities": len(ranked),
        "top_3": ranked[:3],
        "buckets": {
            "apply_now": [r for r in ranked if r["priority"] == "🔥 Apply Now"],
            "apply_soon": [r for r in ranked if r["priority"] == "⏳ Apply Soon"],
            "not_suitable": [r for r in ranked if r["priority"] == "❌ Not Suitable"]
        },
        "all_ranked": ranked
    }