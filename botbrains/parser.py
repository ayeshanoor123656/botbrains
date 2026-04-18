import json
import re


# -----------------------------------
# Extract URL
# -----------------------------------
def extract_url(text):
    match = re.search(r'https?://\S+', text)
    if match:
        return match.group()
    return ""


# -----------------------------------
# Extract Email Contact
# -----------------------------------
def extract_email(text):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if match:
        return match.group()
    return ""


# -----------------------------------
# Extract Deadline
# -----------------------------------
def extract_deadline(text):
    match = re.search(r'Deadline[:\-]?\s*(.*?)(\.|$)', text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""


# -----------------------------------
# Extract Opportunity Type
# -----------------------------------
def extract_type(subject, body):
    text = (subject + " " + body).lower()

    if "internship" in text:
        return "Internship"
    elif "scholarship" in text:
        return "Scholarship"
    elif "competition" in text or "contest" in text:
        return "Competition"
    elif "fellowship" in text:
        return "Fellowship"
    elif "exchange" in text:
        return "Exchange Program"
    elif "research assistant" in text:
        return "Research Opportunity"
    elif "volunteer" in text:
        return "Volunteer Program"
    elif "admission" in text or "masters" in text:
        return "Admission"
    else:
        return "Other"


# -----------------------------------
# Detect Opportunity
# -----------------------------------
def detect_opportunity(subject, body):
    text = (subject + " " + body).lower()

    keywords = [
        "applications open",
        "scholarship",
        "internship",
        "competition",
        "contest",
        "fellowship",
        "exchange",
        "opportunity",
        "research assistant",
        "volunteer",
        "admission"
    ]

    for word in keywords:
        if word in text:
            return True

    return False


# -----------------------------------
# Extract Required Documents
# -----------------------------------
def extract_required_documents(text):
    docs = []

    possible_docs = [
        "CV",
        "Transcript",
        "Cover Letter",
        "Passport",
        "Recommendation Letter",
        "Recommendation Letters",
        "Personal Statement",
        "Income Certificate",
        "Application form",
        "Registration form",
        "Pitch deck",
        "GitHub Profile",
        "LinkedIn Profile",
        "SOP",
        "Student ID cards"
    ]

    for doc in possible_docs:
        if doc.lower() in text.lower():
            docs.append(doc)

    return docs


# -----------------------------------
# Extract Benefits
# -----------------------------------
def extract_benefits(text):
    benefits = []

    possible_benefits = [
        "stipend",
        "cash prize",
        "certificates",
        "networking",
        "mentorship",
        "tuition fee coverage",
        "tuition covered",
        "travel support",
        "leadership training",
        "free certifications",
        "seed funding",
        "health insurance",
        "internship opportunities"
    ]

    for item in possible_benefits:
        if item.lower() in text.lower():
            benefits.append(item)

    return benefits


# -----------------------------------
# Manual Email Parsing
# -----------------------------------
def parse_email(email):
    subject = email["subject"]
    body = email["body"]

    parsed = {
        "title": subject,
        "type": extract_type(subject, body),
        "organization": "",
        "deadline": extract_deadline(body),
        "eligibility": [],
        "required_documents": extract_required_documents(body),
        "location": "",
        "benefits": extract_benefits(body),
        "application_link": extract_url(body),
        "contact_info": extract_email(body),
        "urgency_level": "",
        "isOpportunity": detect_opportunity(subject, body)
    }

    return parsed


# -----------------------------------
# Load email.json
# -----------------------------------
with open("email.json", "r", encoding="utf-8") as file:
    emails = json.load(file)


# -----------------------------------
# Parse All Emails
# -----------------------------------
for email in emails:
    print(f"Parsing Email ID: {email['id']}")

    email["structured"] = parse_email(email)


# -----------------------------------
# Save Output File
# -----------------------------------
with open("parsed_emails.json", "w", encoding="utf-8") as file:
    json.dump(emails, file, indent=4, ensure_ascii=False)


print("Parsing completed successfully!")
print("Saved to parsed_emails.json")