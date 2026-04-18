import json
from datetime import datetime

# ---------------- LOAD DATA ----------------

def load_students(file_path="students.json"):
    with open(file_path, "r") as f:
        return json.load(f)

def load_emails(file_path="emails.json"):
    with open(file_path, "r") as f:
        return json.load(f)


# ---------------- SCORING FUNCTION ----------------

def calculate_score(student, opportunity):
    score = 0
    reasons = []
    warnings = []

    # ---------- TYPE MATCH ----------
    if opportunity.get("type") in student.get("preferred_types", []):
        score += 30
        reasons.append("Matches your preferred opportunity type")

    # ---------- CGPA MATCH ----------
    min_cgpa = opportunity.get("min_cgpa")
    if min_cgpa:
        if student["cgpa"] >= min_cgpa:
            score += 20
            reasons.append(f"Your CGPA meets requirement ({min_cgpa})")
        else:
            warnings.append(f"CGPA requirement not met (Required: {min_cgpa})")
            score -= 10

    # ---------- SKILLS MATCH ----------
    required_skills = opportunity.get("skills_required", [])
    student_skills = student.get("skills", [])

    if required_skills:
        matched = set(required_skills).intersection(set(student_skills))
        if matched:
            skill_score = (len(matched) / len(required_skills)) * 20
            score += skill_score
            reasons.append(f"Matched skills: {', '.join(matched)}")

    # ---------- DEADLINE URGENCY ----------
    urgency = "unknown"
    deadline = opportunity.get("deadline")

    if deadline:
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            today = datetime.today()
            days_left = (deadline_date - today).days

            if days_left <= 3:
                score += 20
                urgency = "high"
                reasons.append("Very urgent (deadline قريب)")
            elif days_left <= 7:
                score += 15
                urgency = "medium"
            else:
                score += 5
                urgency = "low"

        except:
            urgency = "unknown"

    # ---------- LOCATION MATCH ----------
    location = opportunity.get("location", "").lower()
    pref = student.get("location_preference", "").lower()

    if location and pref:
        if pref in location or location in pref:
            score += 10
            reasons.append("Matches your preferred location")

    return {
        "score": round(score, 2),
        "reasons": reasons,
        "warnings": warnings,
        "urgency": urgency
    }


# ---------------- CHECKLIST GENERATOR ----------------

def generate_checklist(opportunity):
    checklist = []

    docs = opportunity.get("documents_required", [])
    for doc in docs:
        checklist.append(f"Prepare {doc}")

    checklist.append("Submit application")

    if opportunity.get("deadline"):
        checklist.append(f"Before deadline: {opportunity['deadline']}")

    return checklist


# ---------------- RANKING FUNCTION ----------------

def rank_opportunities(student, emails):
    results = []

    for email in emails:
        # Skip non-opportunities
        if not email.get("isOpportunity"):
            continue

        # Skip if extraction not done
        if not email.get("structured"):
            continue

        opportunity = email["structured"]

        score_data = calculate_score(student, opportunity)

        result = {
            "title": opportunity.get("title", email.get("subject")),
            "score": score_data["score"],
            "urgency": score_data["urgency"],
            "reasons": score_data["reasons"],
            "warnings": score_data["warnings"],
            "fit_percentage": f"{score_data['score']}%",
            "priority": get_priority_label(score_data["score"]),
            "checklist": generate_checklist(opportunity)
        }

        results.append(result)

    # Sort by score (highest first)
    results.sort(key=lambda x: x["score"], reverse=True)

    return results


# ---------------- PRIORITY LABEL ----------------

def get_priority_label(score):
    if score >= 80:
        return "🔥 Apply Now"
    elif score >= 50:
        return "⏳ Apply Soon"
    else:
        return "❌ Not Suitable"


# ---------------- MAIN TEST RUN ----------------

if __name__ == "__main__":
    students = load_students()
    emails = load_emails()

    # Pick first student for testing
    student = students[0]

    ranked = rank_opportunities(student, emails)

    print("\n=== TOP OPPORTUNITIES ===\n")
    for r in ranked:
        print(f"Title: {r['title']}")
        print(f"Score: {r['score']} ({r['priority']})")
        print(f"Urgency: {r['urgency']}")
        print("Reasons:", ", ".join(r["reasons"]))
        if r["warnings"]:
            print("Warnings:", ", ".join(r["warnings"]))
        print("Checklist:", r["checklist"])
        print("-" * 50)