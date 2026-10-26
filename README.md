# SynthoMed AI
## AI-Powered Healthcare Data Platform
### Complete Project Documentation

> 🌐 **Live Application:**  [https://synthomed-ai-5xfkcdkdd7l5tdp4cytsss.streamlit.app/](https://synthomed-ai-5xfkcdkdd7l5tdp4cytsss.streamlit.app/)

---


## Table of Contents
1. [What is SynthoMed AI?](#1-what-is-synthomed-ai)
2. [Problem It Solves](#2-problem-it-solves)
3. [Key Features](#3-key-features)
4. [How it Works](#4-how-it-works)
5. [Technology Used](#5-technology-used)
6. [Project File Structure](#6-project-file-structure)
7. [How to Run (Local)](#7-how-to-run-local)
8. [How to Deploy Online (Free)](#8-how-to-deploy-online-free)
9. [User Guide](#9-user-guide)
10. [Safety & Disclaimer](#10-safety--disclaimer)

---

## 1. What is SynthoMed AI?

**SynthoMed AI** is an AI-assisted healthcare data platform with two powerful tools built into one application:

| Tool | What it does |
|------|-------------|
| 🏥 **AI Health Analyzer** | You enter your medical information, symptoms, and lab results. The AI reads the data and gives you a structured health summary with precautions and suggested next steps. |
| 🧬 **Synthetic Data Generator** | Researchers and students can generate realistic *fake* patient profiles for testing, learning, and software development — without using any real patient data. |

> ⚠️ **SynthoMed AI is NOT a doctor.** It is an educational and research tool. Always consult a licensed healthcare professional for medical decisions.

---

## 2. Problem It Solves

**Problem 1 — Analyzing Your Own Reports:**
When you get a blood test or medical report, the numbers can be confusing. Doctors are often too busy to explain everything in detail. SynthoMed AI lets you paste your report and get a plain-English summary of what the values mean, what might need attention, and what questions to ask your doctor.

**Problem 2 — Lack of Safe Medical Training Data:**
Healthcare developers, researchers, and students need realistic patient data to build software and run experiments. But real patient data is private and protected by law. SynthoMed AI generates completely artificial (synthetic) patient records that look real but contain no actual personal information.

---

## 3. Key Features

### 🏥 AI Health Analyzer
- ✅ Paste any lab report, blood test results, or doctor notes
- ✅ Enter your symptoms in plain English
- ✅ Add your medical history and current medications
- ✅ Get a structured AI-generated health summary including:
  - Detected health concerns
  - Flagged abnormal lab values (with reference ranges)
  - Personalized precautions and lifestyle tips
  - Questions to ask your doctor
  - Urgency level (Routine → Important → Urgent)
- ✅ Every report is saved with a unique Report ID
- ✅ Emergency alert for potentially serious symptoms

### 🧬 Synthetic Data Generator
- ✅ Create research projects to organize your data
- ✅ Type a natural language description like *"Generate a 55-year-old with diabetes and fatigue"*
- ✅ The AI extracts structured medical data automatically
- ✅ Each generated patient gets a unique Synthetic ID (e.g., `SYN-A3F2B1C9`)
- ✅ View all generated patients in a clean data table
- ✅ Download the entire dataset as a CSV file

### 📊 Report History
- ✅ View all previously submitted health analyses
- ✅ Review original input data side-by-side with the AI-generated report
- ✅ Summary table of all reports at a glance
- ✅ Download all synthetic patient records as CSV

---

## 4. How it Works

### AI Health Analyzer Flow
```
User enters data (symptoms, reports, history)
            ↓
ai_service.py extracts key medical information
using pattern matching and clinical keyword detection
            ↓
Conditions, abnormal values, and risk factors are identified
            ↓
Personalized precautions and doctor questions are generated
            ↓
Report is saved to SQLite database (synthomed.db)
            ↓
Structured health summary is displayed to user
```

### Synthetic Data Generator Flow
```
User types natural language description of a patient
            ↓
ai_service.py parses the text to extract:
  - Age, Sex, Severity
  - Medical Conditions
  - Symptoms
            ↓
SyntheticPatient record saved to database
with unique SYN-XXXXXXXX identifier
            ↓
Patient appears in project's dataset table
            ↓
CSV export available for download
```

---

## 5. Technology Used

| Technology | Role | Why it was chosen |
|---|---|---|
| **Python** | Core programming language | Simple, powerful, great for data |
| **Streamlit** | User Interface + Application server | Builds web UIs in pure Python — no HTML/CSS needed |
| **SQLAlchemy** | Database ORM | Easy database operations in Python |
| **SQLite** | Database | Zero-installation, file-based database — perfect for local development |
| **Regex (re)** | Lab value extraction | Reliably extracts numeric values from free-text reports |

---

## 6. Project File Structure

```
synthomed-ai/
│
├── app.py              ← Main application (all UI and page logic)
├── ai_service.py       ← AI brain (health analysis + patient extraction)
├── database.py         ← Database models (Project, Patient, Report tables)
├── requirements.txt    ← Python packages to install
├── run.bat             ← One-click Windows launcher script
├── README.md           ← This documentation file
└── synthomed.db        ← Auto-created SQLite database (appears after first run)
```

**What each file does:**
- `app.py` — This is the main file. It contains the entire user interface (UI), the page navigation (sidebar), and connects the AI service to the database.
- `ai_service.py` — This is the "brain" of the application. It contains two functions: one that analyzes real health data from the user, and one that generates synthetic patient profiles from text descriptions.
- `database.py` — Defines the structure of the database: what tables exist, what columns they have, and how data is stored and retrieved.
- `requirements.txt` — A list of Python packages that need to be installed for the application to run.
- `run.bat` — A Windows batch script that automatically sets up the Python environment, installs all dependencies, and launches the application.

---

## 7. How to Run (Local)

### Prerequisites
- Windows 10 or 11
- Python 3.10 or newer ([Download from python.org](https://www.python.org/downloads/))
  - ⚠️ During Python installation, check **"Add python.exe to PATH"**

### Step 1 — Navigate to the project folder
Open PowerShell or Command Prompt and type:
```powershell
cd "c:\Users\murali krishna\OneDrive\Desktop\langchain\healthcare\synthomed-ai"
```

### Step 2 — Install dependencies and launch
```powershell``
py -m pip install streamlit sqlalchemy
streamlit run app.py
```

The application will automatically open at **http://localhost:8501** in your default browser.

### Alternative: Double-click Launcher
Double-click the `run.bat` file in your File Explorer. It will install all requirements and open the app automatically.

---

## 8. How to Deploy Online (Free)

You can publish SynthoMed AI online for free using **Streamlit Community Cloud**. This gives you a permanent public URL that anyone can visit.

### Step 1 — Create a GitHub Account
Go to [github.com](https://github.com) and create a free account if you don't have one.

### Step 2 — Create a New GitHub Repository
1. Click the **+** button on GitHub → **New repository**
2. Name it `synthomed-ai`
3. Make it **Public**
4. Click **Create repository**

### Step 3 — Upload Your Files to GitHub
In your project folder, open PowerShell and run:
```powershell
git init
git add .
git commit -m "Initial SynthoMed AI deployment"
git remote add origin https://github.com/YOUR_USERNAME/synthomed-ai.git
git push -u origin main
```
*(Replace `YOUR_USERNAME` with your GitHub username)*

### Step 4 — Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **New App**
4. Select your `synthomed-ai` repository
5. Set the main file path to `app.py`
6. Click **Deploy**

Application public URL like:
```
https://synthomed-ai-5xfkcdkdd7l5tdp4cytsss.streamlit.app/
```

Anyone with that link can use the application from their browser!

> **Note:** The free Streamlit Cloud tier uses an ephemeral (temporary) database. This means the SQLite data resets when the app goes to sleep. For a permanent database, you would need to configure a cloud database like Supabase or PlanetScale.

---

## 9. User Guide

### Using the AI Health Analyzer

1. Click **🏥 AI Health Analyzer** in the left sidebar.
2. Enter your **age** and **sex** in Step 1.
3. In Step 2, paste any lab report text. Example:
   ```
   Hemoglobin: 10.2 g/dL
   HbA1c: 8.1%
   Blood Pressure: 148/92 mmHg
   ```
4. In Step 3, type your symptoms separated by commas. Example:
   ```
   persistent headache, fatigue, blurred vision
   ```
5. Fill in your medical history (e.g., "Diagnosed with diabetes in 2019") and any medications.
6. Click **Generate My AI Health Summary**.
7. Review the structured report including conditions, precautions, and doctor questions.

### Using the Synthetic Data Generator

1. Click **🧬 Synthetic Data Generator** in the sidebar.
2. In the sidebar, create a new project (e.g., "Diabetes Research Study").
3. Select your active project.
4. Type a patient description in the text box. Example:
   ```
   Generate a 62-year old male with severe asthma and high cholesterol.
   ```
5. Click **Generate Synthetic Patient**.
6. Go to **Dataset Viewer** tab to see all generated patients.
7. Click **Download as CSV** to export the data.

---

## 10. Safety & Disclaimer

> ### ⚠️ IMPORTANT NOTICE
>
> **SynthoMed AI is strictly an educational, research, and informational tool.**
>
> - The AI Health Analyzer output is a **general informational summary only**, based solely on the data the user provides.
> - It is **NOT a medical diagnosis** and **cannot replace a qualified healthcare professional**.
> - The Synthetic Data Generator produces **completely artificial data** that does not represent any real person.
> - **Never use the output of this platform for clinical decision-making, insurance purposes, legal documentation, or any real medical treatment.**
> - If you believe you are experiencing a medical emergency, please contact your local emergency services immediately.

---

*SynthoMed AI · Built for educational and research purposes · Not for clinical use*
