import React, { useState } from "react";
import emailsData from "../../botbrains/emails.json";
import profilesData from "../../botbrains/profile.json";

// ---------- CLASSIFIER ----------
const opportunityKeywords = [
  "internship",
  "scholarship",
  "apply",
  "deadline",
  "program",
  "fellowship",
  "contest",
  "funding",
  "volunteer",
  "research",
  "exchange",
  "competition",
  "seed funding"
];

const isOpportunity = (email) => {
  const text = (email.subject + " " + email.body).toLowerCase();
  return opportunityKeywords.some((w) => text.includes(w));
};

const Emails = () => {
  const [step, setStep] = useState(1); // 1 = profile, 2 = inbox
  const [selectedProfile, setSelectedProfile] = useState(null);

  const [selectedEmail, setSelectedEmail] = useState(null);
  const [selectedForAction, setSelectedForAction] = useState([]);

  const emails = emailsData.map((email) => ({
    ...email,
    isOpportunity: isOpportunity(email),
  }));

  const toggleSelect = (id) => {
    if (selectedForAction.includes(id)) {
      setSelectedForAction(selectedForAction.filter((i) => i !== id));
    } else {
      if (selectedForAction.length < 15) {
        setSelectedForAction([...selectedForAction, id]);
      } else {
        alert("Max 15 emails allowed");
      }
    }
  };

  // ---------------- STEP 1: PROFILE SELECTION ----------------
  if (step === 1) {
  return (
    <div style={{ padding: 20 }}>
      <h1>👨‍🎓 Select Student Profile</h1>

      <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
        {profilesData.map((p) => (
          <div
            key={p.id}
            onClick={() => {
              setSelectedProfile(p);
              setStep(2);
            }}
            style={{
              border: "1px solid #ddd",
              borderRadius: 12,
              padding: 15,
              width: 300,
              cursor: "pointer",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
              backgroundColor: "#fff"
            }}
          >
            <h3>{p.name}</h3>

            <p><b>Degree:</b> {p.degree}</p>
            <p><b>Semester:</b> {p.semester}</p>
            <p><b>CGPA:</b> {p.cgpa}</p>

            <hr />

            <p><b>Skills:</b> {p.skills.join(", ")}</p>
            <p><b>Interests:</b> {p.interests.join(", ")}</p>

            <p><b>Preferred Types:</b> {p.preferred_types.join(", ")}</p>

            <p><b>Location Preference:</b> {p.location_preference}</p>

            <p>
              <b>Financial Need:</b>{" "}
              {p.financial_need ? "Yes" : "No"}
            </p>

            <p><b>Experience:</b> {p.experience_level}</p>

            {p.past_experience && (
              <p>
                <b>Past Experience:</b> {p.past_experience.join(", ")}
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
  // ---------------- STEP 2: EMAIL INBOX ----------------
  return (
    <div style={{ display: "flex", height: "100vh" }}>

      {/* LEFT PANEL */}
      <div style={{ width: "40%", borderRight: "1px solid #ddd", padding: 10 }}>

        <button
          onClick={() => setStep(1)}
          style={{ marginBottom: 10 }}
        >
          ⬅ Change Profile
        </button>

        <h3>👨‍🎓 {selectedProfile?.name}</h3>

        <hr />

        <h2>📧 Inbox</h2>

        {emails.map((email) => (
          <div
            key={email.id}
            style={{
              padding: "10px",
              marginBottom: "8px",
              borderRadius: "8px",
              backgroundColor: email.isOpportunity ? "#e6fff0" : "#f5f5f5",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              cursor: "pointer"
            }}
          >
            <span onClick={() => setSelectedEmail(email)}>
              {email.subject}
            </span>

            {email.isOpportunity && (
              <input
                type="checkbox"
                checked={selectedForAction.includes(email.id)}
                onChange={() => toggleSelect(email.id)}
              />
            )}
          </div>
        ))}

        <p>Selected: {selectedForAction.length} / 15</p>
      </div>

      {/* RIGHT PANEL */}
      <div style={{ width: "60%", padding: 20 }}>
        {selectedEmail ? (
          <>
            <h2>{selectedEmail.subject}</h2>

            <p style={{ whiteSpace: "pre-line" }}>
              {selectedEmail.body}
            </p>

            <hr />

            <strong>
              {selectedEmail.isOpportunity
                ? "🎯 Opportunity Email"
                : "📩 Normal Email"}
            </strong>
          </>
        ) : (
          <h3>Select an email</h3>
        )}
      </div>
    </div>
  );
};

export default Emails;