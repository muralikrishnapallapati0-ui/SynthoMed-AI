from typing import Dict, Any
import re

# ─────────────────────────────────────────────────────────────────────
# SYNTHETIC PATIENT GENERATOR (Existing Feature)
# ─────────────────────────────────────────────────────────────────────

def generate_patient_from_text(prompt: str) -> Dict[str, Any]:
    """
    Extracts structured medical data from a natural language prompt.
    """
    prompt_lower = prompt.lower()
    age = 45
    sex = "Female" if "female" in prompt_lower or "woman" in prompt_lower else "Male"
    severity = "Moderate"
    conditions = []
    symptoms = []

    words = prompt_lower.replace("-", " ").split()
    for i, word in enumerate(words):
        if word in ["year", "years", "yo"] and i > 0 and words[i-1].isdigit():
            age = int(words[i-1])
            break
        elif word == "age" and i < len(words)-1 and words[i+1].isdigit():
            age = int(words[i+1])
            break

    if any(s in prompt_lower for s in ["severe", "high", "critical", "advanced"]):
        severity = "Severe"
    elif any(s in prompt_lower for s in ["mild", "low", "early", "slight"]):
        severity = "Mild"

    if "hypertension" in prompt_lower or "blood pressure" in prompt_lower:
        conditions.append("Hypertension")
    if "diabetes" in prompt_lower:
        conditions.append("Type 2 Diabetes")
    if "cholesterol" in prompt_lower or "hyperlipidemia" in prompt_lower:
        conditions.append("Hyperlipidemia")
    if "asthma" in prompt_lower:
        conditions.append("Asthma")
    if "anxiety" in prompt_lower:
        conditions.append("Anxiety Disorder")
    if "depression" in prompt_lower:
        conditions.append("Depression")
    if "obesity" in prompt_lower or "overweight" in prompt_lower:
        conditions.append("Obesity")

    if "headache" in prompt_lower:
        symptoms.append("Headaches")
    if "fatigue" in prompt_lower or "tired" in prompt_lower:
        symptoms.append("Fatigue")
    if "dizzy" in prompt_lower or "dizziness" in prompt_lower:
        symptoms.append("Dizziness")
    if "cough" in prompt_lower:
        symptoms.append("Chronic Cough")
    if "chest pain" in prompt_lower:
        symptoms.append("Chest Pain")
    if "shortness of breath" in prompt_lower or "breathless" in prompt_lower:
        symptoms.append("Shortness of Breath")
    if "nausea" in prompt_lower:
        symptoms.append("Nausea")

    return {
        "age": age,
        "sex": sex,
        "severity": severity,
        "conditions": conditions if conditions else ["Healthy / Baseline"],
        "symptoms": symptoms if symptoms else ["None reported"]
    }


# ─────────────────────────────────────────────────────────────────────
# AI HEALTH REPORT ANALYZER (New Core Feature)
# ─────────────────────────────────────────────────────────────────────

def analyze_health_data(
    age: int,
    sex: str,
    symptoms: str,
    medical_history: str,
    report_text: str,
    medications: str
) -> Dict[str, Any]:
    """
    Analyzes user-provided health information and generates a structured
    AI-assisted health summary report.

    This uses rule-based extraction + structured output for the MVP.
    If an OpenAI / LangChain key is added later, plug it in here.
    """

    text_blob = f"{symptoms} {medical_history} {report_text} {medications}".lower()

    # ── 1. Detected Conditions & Concerns ──────────────────────────────
    detected_conditions = []
    abnormal_values = []
    risk_indicators = []

    # Cardio
    if any(k in text_blob for k in ["hypertension", "high blood pressure", "hbp"]):
        detected_conditions.append("Hypertension (High Blood Pressure)")
        risk_indicators.append("Cardiovascular risk elevated — monitor BP regularly")
    if any(k in text_blob for k in ["chest pain", "chest tightness", "angina"]):
        detected_conditions.append("Possible cardiac-related chest symptoms")
        risk_indicators.append("⚠️ Chest pain may require urgent evaluation")
    if any(k in text_blob for k in ["palpitation", "irregular heartbeat", "arrhythmia"]):
        detected_conditions.append("Possible cardiac arrhythmia")
        risk_indicators.append("Irregular heartbeat — consult cardiologist")

    # Metabolic
    if any(k in text_blob for k in ["diabetes", "high sugar", "blood glucose", "hba1c"]):
        detected_conditions.append("Diabetes Mellitus (Type 2 likely)")
        risk_indicators.append("Blood glucose management critical for long-term organ health")
    if any(k in text_blob for k in ["cholesterol", "ldl", "hdl", "triglyceride"]):
        detected_conditions.append("Dyslipidemia (Abnormal Cholesterol)")
        risk_indicators.append("Elevated cholesterol is a modifiable cardiovascular risk factor")

    # Respiratory
    if any(k in text_blob for k in ["asthma", "breathless", "shortness of breath", "wheez"]):
        detected_conditions.append("Respiratory Issue (Possible Asthma / COPD)")
        risk_indicators.append("Monitor oxygen levels; avoid known triggers")
    if any(k in text_blob for k in ["cough", "phlegm", "sputum"]):
        detected_conditions.append("Respiratory Symptoms Noted")

    # Mental health
    if any(k in text_blob for k in ["anxiety", "stress", "panic"]):
        detected_conditions.append("Anxiety / Stress-Related Symptoms")
        risk_indicators.append("Psychological well-being is critical for overall health")
    if any(k in text_blob for k in ["depression", "sad", "hopeless"]):
        detected_conditions.append("Possible Mood Disorder Symptoms")
        risk_indicators.append("⚠️ Persistent low mood should be evaluated by a professional")

    # Lab abnormal values
    lab_patterns = {
        "hemoglobin": (r"hemoglobin[:\s]+(\d+\.?\d*)", 12.0, 17.5, "g/dL"),
        "glucose": (r"glucose[:\s]+(\d+\.?\d*)", 70, 100, "mg/dL"),
        "creatinine": (r"creatinine[:\s]+(\d+\.?\d*)", 0.6, 1.2, "mg/dL"),
        "hba1c": (r"hba1c[:\s]+(\d+\.?\d*)", 4.0, 5.7, "%"),
        "wbc": (r"wbc[:\s]+(\d+\.?\d*)", 4.5, 11.0, "x10³/µL"),
    }
    for label, (pattern, low, high, unit) in lab_patterns.items():
        match = re.search(pattern, text_blob)
        if match:
            val = float(match.group(1))
            if val < low:
                abnormal_values.append(f"**{label.upper()}:** {val} {unit} — *Below normal range ({low}–{high} {unit})*")
            elif val > high:
                abnormal_values.append(f"**{label.upper()}:** {val} {unit} — *Above normal range ({low}–{high} {unit})*")

    # ── 2. Symptoms Analysis ────────────────────────────────────────────
    symptoms_list = [s.strip().capitalize() for s in symptoms.split(',') if s.strip()] if symptoms else []
    urgent_symptoms = ["chest pain", "severe breathlessness", "unconscious", "stroke", "paralysis", "seizure", "vomiting blood"]
    is_urgent = any(us in text_blob for us in urgent_symptoms)

    # ── 3. General Precautions ─────────────────────────────────────────
    precautions = [
        "Stay well-hydrated (8–10 glasses of water per day)",
        "Maintain a balanced diet rich in vegetables, whole grains, and lean proteins",
        "Aim for at least 30 minutes of moderate physical activity most days of the week",
        "Ensure 7–8 hours of quality sleep per night",
        "Avoid smoking and limit alcohol consumption",
        "Monitor blood pressure and blood sugar regularly if previously diagnosed",
        "Practice stress management techniques such as deep breathing or meditation",
    ]
    if "hypertension" in text_blob or "blood pressure" in text_blob:
        precautions.insert(0, "Reduce sodium (salt) intake to under 2,300 mg per day")
    if "diabetes" in text_blob or "glucose" in text_blob:
        precautions.insert(0, "Monitor blood glucose levels regularly as per your doctor's advice")
        precautions.insert(1, "Avoid sugary beverages, refined carbs, and processed foods")

    # ── 4. Doctor Questions ────────────────────────────────────────────
    doctor_questions = [
        "Based on my test results, do my levels require medication or lifestyle changes?",
        "Are my current medications still appropriate for my condition?",
        "What specific diet plan would you recommend given my reported conditions?",
        "Do I need any follow-up tests or specialist referrals?",
        "What warning symptoms should prompt me to seek emergency care immediately?",
        "How frequently should I schedule routine monitoring for my current health status?",
    ]
    if is_urgent:
        doctor_questions.insert(0, "My symptoms include urgent indicators — should I go to emergency care now?")

    # ── 5. Recommended Action Level ───────────────────────────────────
    if is_urgent:
        action_level = "🚨 URGENT — Seek immediate medical attention"
        action_color = "red"
    elif risk_indicators:
        action_level = "⚠️ IMPORTANT — Schedule a consultation with your doctor soon"
        action_color = "orange"
    else:
        action_level = "✅ ROUTINE — Maintain lifestyle habits and attend regular check-ups"
        action_color = "green"

    return {
        "detected_conditions": detected_conditions if detected_conditions else ["No specific conditions identified from provided data"],
        "symptoms_list": symptoms_list if symptoms_list else ["No specific symptoms provided"],
        "abnormal_values": abnormal_values,
        "risk_indicators": risk_indicators,
        "precautions": precautions,
        "doctor_questions": doctor_questions,
        "action_level": action_level,
        "action_color": action_color,
        "is_urgent": is_urgent
    }
