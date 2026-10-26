import streamlit as st
import csv
import io
from database import get_db, Project, SyntheticPatient, HealthSummaryReport
from ai_service import generate_patient_from_text, analyze_health_data

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SynthoMed AI — Healthcare Intelligence Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Premium CSS ──────────────────────────────────────────────────────────────
st.markdown("""

<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  .main {
    background-color: #f0f4f8;
  }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
  }

  section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
  }

  section[data-testid="stSidebar"] h1 {
    color: #38bdf8 !important;
  }

  section[data-testid="stSidebar"] .stSelectbox label,
  section[data-testid="stSidebar"] .stTextInput label {
    color: #94a3b8 !important;
    font-size: 12px;
  }

  /* Cards */
  .card {
    background: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid #e2e8f0;
    margin-bottom: 1.25rem;
  }

  .card-title {
    font-size: 1rem;
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* Hero Banner */
  .hero-banner {
    background: linear-gradient(135deg, #0369a1 0%, #0284c7 50%, #0ea5e9 100%);
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 1.5rem;
    color: white;
    box-shadow: 0 8px 24px rgba(3,105,161,0.25);
  }

  .hero-banner h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    color: white;
  }

  .hero-banner p {
    font-size: 1rem;
    opacity: 0.9;
    margin: 0.5rem 0 0 0;
    color: white;
  }

  /* Warning Banner */
  .warn-banner {
    background: #fffbeb;
    border: 1px solid #fbbf24;
    border-left: 4px solid #f59e0b;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
  }

  .warn-banner strong {
    color: #92400e;
    display: block;
    margin-bottom: 0.25rem;
  }

  .warn-banner span {
    color: #78350f;
    font-size: 0.875rem;
  }

  /* Urgent Banner */
  .urgent-banner {
    background: #fef2f2;
    border: 1px solid #fca5a5;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
  }

  /* Result Sections */
  .result-section {
    background: #f8fafc;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .result-section h4 {
    margin: 0 0 0.5rem 0;
    color: #1e40af;
    font-size: 0.9rem;
    font-weight: 600;
  }

  .result-section ul {
    margin: 0;
    padding-left: 1.25rem;
  }

  .result-section ul li {
    font-size: 0.875rem;
    color: #374151;
    margin-bottom: 0.25rem;
  }

  /* Pill badges */
  .badge-red {
    background: #fee2e2;
    color: #991b1b;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
  }

  .badge-amber {
    background: #fef3c7;
    color: #92400e;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
  }

  .badge-blue {
    background: #dbeafe;
    color: #1e40af;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
  }

  .badge-green {
    background: #dcfce7;
    color: #166534;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
    margin: 2px;
  }

  /* Divider */
  .divider {
    border-top: 1px solid #e2e8f0;
    margin: 1.25rem 0;
  }

  /* Metric overrides */
  [data-testid="metric-container"] {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    border: 1px solid #e2e8f0;
  }

  /* Buttons */
  .stButton > button {
    border-radius: 8px;
    font-weight: 600;
    border: none;
    transition: all 0.2s ease;
  }

  .stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }

  /* FIXED INPUT FIELDS: readable text and white backgrounds */
  .stTextInput input,
  .stTextArea textarea,
  .stNumberInput input,
  .stSelectbox input,
  [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
    caret-color: #111827 !important;
    opacity: 1 !important;
  }

  /* Ensure typed text remains visible */
  .stTextInput input,
  .stTextArea textarea,
  .stNumberInput input,
  [data-baseweb="input"] input,
  [data-baseweb="textarea"] textarea {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
  }

  /* Placeholder text */
  .stTextInput input::placeholder,
  .stTextArea textarea::placeholder,
  input::placeholder,
  textarea::placeholder {
    color: #6b7280 !important;
    -webkit-text-fill-color: #6b7280 !important;
    opacity: 1 !important;
    font-weight: 400 !important;
  }

  /* Input focus state */
  .stTextInput input:focus,
  .stTextArea textarea:focus,
  .stNumberInput input:focus,
  [data-baseweb="input"] input:focus,
  [data-baseweb="textarea"] textarea:focus {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    border-color: #0284c7 !important;
    box-shadow: 0 0 0 2px rgba(2,132,199,0.2) !important;
  }

  /* Disabled fields and file previews */
  .stTextArea textarea:disabled,
  input:disabled {
    background-color: #f3f4f6 !important;
    color: #374151 !important;
    -webkit-text-fill-color: #374151 !important;
    opacity: 1 !important;
  }

  /* Dropdown text */
  [data-baseweb="select"] input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
  }

  [data-baseweb="popover"] *,
  [data-baseweb="menu"] * {
    color: #111827;
  }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9;
    border-radius: 10px;
    padding: 4px;
  }

  .stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
  }

  .stTabs [aria-selected="true"] {
    background: white;
    color: #0369a1;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }

  /* Fix label colors in main content */
  .main .stTextInput label,
  .main .stTextArea label,
  .main .stSelectbox label,
  .main .stNumberInput label,
  .main .stRadio label,
  .main .stCheckbox label,
  .main .stMultiSelect label,
  [data-testid="stForm"] label,
  div[class*="stTextInput"] label,
  div[class*="stTextArea"] label,
  div[class*="stNumberInput"] label,
  div[class*="stSelectbox"] label {
    color: #111827 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
  }

  /* Radio labels */
  .main .stRadio > div > label {
    color: #1f2937 !important;
  }

  /* Preserve the original Streamlit text colors */
  .main p,
  .main li,
  .main span,
  .main div {
    color: inherit;
  }

  /* History table */
  .history-table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  }

  .history-table th {
    background: #1e40af;
    color: white;
    padding: 10px 14px;
    font-size: 0.8rem;
    font-weight: 600;
    text-align: left;
  }

  .history-table td {
    padding: 9px 14px;
    font-size: 0.82rem;
    color: #1f2937;
    border-bottom: 1px solid #f1f5f9;
  }

  .history-table tr:hover td {
    background: #eff6ff;
  }

  footer {
    visibility: hidden;
  }
</style>

""", unsafe_allow_html=True)


# ─── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🧬 SynthoMed AI")
    st.markdown("#### Healthcare Intelligence Platform")
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["🏥 AI Health Analyzer", "🧬 Synthetic Data Generator", "📊 Report History"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("**About**")
    st.caption("SynthoMed AI uses rule-based clinical extraction and structured AI analysis to help users understand their health data. All outputs are informational only.")
    st.divider()
    st.caption("v2.0 · For Education & Research")


# ╔══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — AI HEALTH ANALYZER
# ╔══════════════════════════════════════════════════════════════════════════════
if page == "🏥 AI Health Analyzer":

    # Hero
    st.markdown("""
    <div class="hero-banner">
        <h1>🏥 AI Health Report Analyzer</h1>
        <p>Provide your medical data, symptoms, and health history. Our AI engine will analyze the information and generate a structured, personalized health summary.</p>
    </div>
    """, unsafe_allow_html=True)

    # Safety Warning
    st.markdown("""
    <div class="warn-banner">
        <strong>⚠️ IMPORTANT DISCLAIMER</strong>
        <span>This AI provides an <strong>informational summary based only on the data you provide</strong>. It is NOT a medical diagnosis and cannot replace a qualified healthcare professional. Always consult your doctor for medical advice.</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Input Form ────────────────────────────────────────────────────
    st.markdown("### 📋 Step 1 — Enter Your Health Information")
    
    with st.container():
        col_a, col_b, col_c = st.columns(3)
        age_val = col_a.number_input("Age (years)", min_value=1, max_value=120, value=35)
        sex_val = col_b.selectbox("Biological Sex", ["Male", "Female", "Other / Prefer not to say"])
        demo_val = col_c.text_input("Ethnicity / Region (optional)", placeholder="e.g. South Asian")

    st.markdown("### 📄 Step 2 — Add Your Medical Report / Test Results")
    st.caption("Choose how you want to provide your report — upload a file OR paste the text manually (or both).")

    upload_tab, paste_tab = st.tabs(["📁 Upload Report File", "✍️ Paste / Type Text"])

    uploaded_file_text = ""
    with upload_tab:
        uploaded_file = st.file_uploader(
            "Upload your medical report file",
            type=["txt", "pdf"],
            help="Supported formats: .txt and .pdf"
        )
        if uploaded_file is not None:
            file_type = uploaded_file.name.split(".")[-1].lower()
            if file_type == "txt":
                uploaded_file_text = uploaded_file.read().decode("utf-8", errors="ignore")
                st.success(f"✅ File '{uploaded_file.name}' loaded successfully ({len(uploaded_file_text)} characters).")
                st.text_area("File Content Preview", value=uploaded_file_text[:800] + ("..." if len(uploaded_file_text) > 800 else ""), height=150, disabled=True)
            elif file_type == "pdf":
                try:
                    import io as _io
                    pdf_bytes = uploaded_file.read()
                    # Try to extract text from PDF using basic byte parsing
                    # We decode printable text from the PDF binary
                    raw = pdf_bytes.decode("latin-1", errors="ignore")
                    import re as _re
                    # Extract readable strings (sequences of printable chars)
                    strings = _re.findall(r'[\x20-\x7e]{4,}', raw)
                    uploaded_file_text = " ".join(strings)
                    st.success(f"✅ PDF '{uploaded_file.name}' processed ({len(uploaded_file_text)} characters extracted).")
                    st.text_area("Extracted Text Preview", value=uploaded_file_text[:800] + ("..." if len(uploaded_file_text) > 800 else ""), height=150, disabled=True)
                    if len(uploaded_file_text) < 50:
                        st.warning("⚠️ Very little text could be extracted from this PDF. It may be a scanned image. Please use the 'Paste Text' tab to manually enter the report values.")
                except Exception as e:
                    st.error(f"Could not read the PDF file: {e}. Please use the Paste tab instead.")

    pasted_text = ""
    with paste_tab:
        pasted_text = st.text_area(
            "Paste any medical report, lab results, or doctor notes here",
            height=180,
            placeholder="e.g.\nHemoglobin: 10.2 g/dL\nHbA1c: 8.1%\nBlood Pressure: 148/92 mmHg\nFasting Glucose: 185 mg/dL\nDoctor Note: Patient has been on Metformin 500mg for 3 years..."
        )

    # Merge both sources
    report_text = (uploaded_file_text + "\n" + pasted_text).strip()

    col1, col2 = st.columns(2)
    symptoms_text = col1.text_area(
        "💬 Step 3 — Current Symptoms (comma-separated)",
        height=120,
        placeholder="e.g. persistent headache, fatigue, dizziness, frequent urination, blurred vision"
    )
    history_text = col2.text_area(
        "📂 Medical History & Known Conditions",
        height=120,
        placeholder="e.g. Diagnosed with Type 2 Diabetes in 2019. Family history of hypertension. Underwent appendectomy in 2015."
    )
    
    medications_text = st.text_input(
        "💊 Current Medications (optional, voluntarily provided)",
        placeholder="e.g. Metformin 500mg twice daily, Amlodipine 5mg once daily"
    )

    st.divider()

    generate_btn = st.button(
        "🔍 Generate My AI Health Summary",
        width="stretch",
        type="primary"
    )

    if generate_btn:
        has_input = any([report_text.strip(), symptoms_text.strip(), history_text.strip()])
        if not has_input:
            st.warning("Please provide at least one piece of health information (report, symptoms, or medical history).")
        else:
            with st.spinner("Analyzing your health data..."):
                result = analyze_health_data(
                    age=age_val,
                    sex=sex_val,
                    symptoms=symptoms_text,
                    medical_history=history_text,
                    report_text=report_text,
                    medications=medications_text
                )
                
                # Save to database
                db = get_db()
                report_record = HealthSummaryReport(
                    age=age_val,
                    demographics=f"{sex_val}, {demo_val}",
                    medical_history=history_text,
                    current_symptoms=symptoms_text,
                    uploaded_reports_text=report_text
                )
                report_record.report_data = result
                db.add(report_record)
                db.commit()
                report_id = report_record.id
                db.close()

            # ── RESULTS DISPLAY ────────────────────────────────────────
            st.markdown("---")
            
            # Urgent banner if needed
            if result["is_urgent"]:
                st.markdown("""
                <div class="urgent-banner">
                    <strong>🚨 URGENT ATTENTION REQUIRED</strong><br>
                    <span>Your reported symptoms may indicate a serious medical condition. Please seek emergency medical care or call emergency services immediately. Do not rely solely on this summary.</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"### 📊 Health Summary Report · `{report_id}`")
            st.caption(f"Patient Profile: {age_val} years old · {sex_val}")

            # Action Level
            if result["action_color"] == "red":
                st.error(result["action_level"])
            elif result["action_color"] == "orange":
                st.warning(result["action_level"])
            else:
                st.success(result["action_level"])

            # ── Section Grid ───────────────────────────────────────────
            col_l, col_r = st.columns(2)

            with col_l:
                # Detected Conditions
                st.markdown('<div class="card"><div class="card-title">🩺 Detected Conditions & Risk Indicators</div>', unsafe_allow_html=True)
                for c in result["detected_conditions"]:
                    st.markdown(f'<span class="badge-red">{c}</span>', unsafe_allow_html=True)
                if result["risk_indicators"]:
                    st.markdown("<br>**Risk Indicators:**", unsafe_allow_html=True)
                    for r in result["risk_indicators"]:
                        st.markdown(f"- {r}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Abnormal Values
                if result["abnormal_values"]:
                    st.markdown('<div class="card"><div class="card-title">⚠️ Flagged Abnormal Lab Values</div>', unsafe_allow_html=True)
                    for v in result["abnormal_values"]:
                        st.markdown(v)
                    st.markdown('</div>', unsafe_allow_html=True)

                # Symptoms
                st.markdown('<div class="card"><div class="card-title">💬 Reported Symptoms</div>', unsafe_allow_html=True)
                for s in result["symptoms_list"]:
                    st.markdown(f'<span class="badge-amber">{s}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_r:
                # Precautions
                st.markdown('<div class="card"><div class="card-title">🛡️ Precautions & Lifestyle Recommendations</div>', unsafe_allow_html=True)
                for i, p in enumerate(result["precautions"]):
                    st.markdown(f"{i+1}. {p}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Doctor Questions
                st.markdown('<div class="card"><div class="card-title">💡 Questions to Discuss with Your Doctor</div>', unsafe_allow_html=True)
                for q in result["doctor_questions"]:
                    st.markdown(f"- {q}")
                st.markdown('</div>', unsafe_allow_html=True)

            # Final Disclaimer
            st.divider()
            st.markdown("""
            <div class="warn-banner">
                <strong>📋 SYNTHETIC AI SUMMARY — NOT A DIAGNOSIS</strong>
                <span>This report was generated by an AI system based solely on the data you provided. It contains <strong>no access to your actual medical records</strong> and may not reflect your true health status. Always consult a licensed healthcare professional before making any health decisions.</span>
            </div>
            """, unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SYNTHETIC DATA GENERATOR
# ╔══════════════════════════════════════════════════════════════════════════════
elif page == "🧬 Synthetic Data Generator":

    st.markdown("""
    <div class="hero-banner">
        <h1>🧬 Synthetic Patient Data Generator</h1>
        <p>Generate realistic, completely artificial patient profiles for research, education, and software testing — without using real patient data.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-banner">
        <strong>⚠️ SYNTHETIC DATA WARNING</strong>
        <span>All generated patients are artificial. This data does NOT represent real individuals and must not be used for clinical, legal, or insurance purposes.</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Project Management ─────────────────────────────────────────────
    db = get_db()

    with st.sidebar:
        st.divider()
        st.markdown("**📂 Project Management**")
        with st.expander("➕ New Project"):
            new_name = st.text_input("Project Name", key="np_name")
            new_purpose = st.selectbox("Purpose", ["Research", "Education", "Software Testing"], key="np_purpose")
            if st.button("Create", key="np_btn", width="stretch"):
                if new_name:
                    proj = Project(name=new_name, purpose=new_purpose)
                    db.add(proj); db.commit()
                    st.success("Created!"); st.rerun()

        projects = db.query(Project).all()
        if projects:
            proj_map = {p.name: p for p in projects}
            sel = st.selectbox("Active Project", list(proj_map.keys()), key="sel_proj")
            active_project = proj_map[sel]
        else:
            st.info("Create a project first.")
            db.close()
            st.stop()

    st.header(f"📁 {active_project.name}")
    st.caption(f"Purpose: {active_project.purpose} · ID: {active_project.id}")

    tab1, tab2 = st.tabs(["✨ Generate Patient", "📋 Dataset Viewer"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Natural Language Generator**")
        st.caption("Describe the synthetic patient you want to generate in plain English.")
        prompt = st.text_area(
            "Patient Description",
            placeholder="e.g. Generate a 62-year old male with severe asthma and high blood pressure experiencing dizziness.",
            height=100,
            label_visibility="collapsed"
        )
        if st.button("✨ Generate Synthetic Patient", type="primary", width="stretch"):
            if prompt:
                with st.spinner("Generating synthetic patient..."):
                    extracted = generate_patient_from_text(prompt)
                    patient = SyntheticPatient(
                        project_id=active_project.id,
                        age=extracted["age"],
                        sex=extracted["sex"],
                        severity=extracted["severity"],
                        conditions=extracted["conditions"],
                        symptoms=extracted["symptoms"]
                    )
                    db.add(patient); db.commit()
                
                st.success(f"Patient `{patient.id}` generated!")
                c1, c2, c3 = st.columns(3)
                c1.metric("Age", patient.age)
                c2.metric("Sex", patient.sex)
                c3.metric("Severity", patient.severity)
                badges_c = " ".join([f'<span class="badge-red">{c}</span>' for c in patient.conditions])
                badges_s = " ".join([f'<span class="badge-amber">{s}</span>' for s in patient.symptoms])
                st.markdown(f"**Conditions:** {badges_c}", unsafe_allow_html=True)
                st.markdown(f"**Symptoms:** {badges_s}", unsafe_allow_html=True)
            else:
                st.warning("Please enter a description.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        patients = db.query(SyntheticPatient).filter(SyntheticPatient.project_id == active_project.id).all()
        if not patients:
            st.info("No patients generated for this project yet. Use the generator above.")
        else:
            data = [{
                "Synthetic ID": p.id, "Age": p.age, "Sex": p.sex,
                "Severity": p.severity,
                "Conditions": ", ".join(p.conditions),
                "Symptoms": ", ".join(p.symptoms)
            } for p in patients]
            st.dataframe(data, width="stretch")
            
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=data[0].keys())
            writer.writeheader(); writer.writerows(data)
            st.download_button(
                "⬇️ Download as CSV",
                data=output.getvalue().encode("utf-8"),
                file_name=f"{active_project.name.replace(' ','_')}_synthetic_dataset.csv",
                mime="text/csv"
            )

    db.close()


# ╔══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — REPORT HISTORY
# ╔══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Report History":

    st.markdown("""
    <div class="hero-banner">
        <h1>📊 Report History</h1>
        <p>Review all submitted health data and generated AI analysis reports stored in your local database.</p>
    </div>
    """, unsafe_allow_html=True)

    db = get_db()

    tab_h1, tab_h2 = st.tabs(["🏥 Health Analysis Reports", "🧬 Synthetic Patient Records"])

    # ── Tab 1: Health Analysis Reports ──────────────────────────────────────────
    with tab_h1:
        reports = db.query(HealthSummaryReport).all()
        if not reports:
            st.info("No health analysis reports found. Go to the AI Health Analyzer to generate one.")
        else:
            st.markdown(f"**{len(reports)} report(s) found**")
            st.divider()

            for r in reports:
                rd = r.report_data
                with st.expander(f"📋 Report `{r.id}` — Age {r.age} · {r.demographics}", expanded=False):
                    col_i, col_o = st.columns(2)

                    with col_i:
                        st.markdown("#### 📥 User Input Data")
                        st.markdown(f"**Age:** {r.age}")
                        st.markdown(f"**Demographics:** {r.demographics}")
                        if r.current_symptoms:
                            st.markdown(f"**Reported Symptoms:**")
                            st.info(r.current_symptoms)
                        if r.medical_history:
                            st.markdown(f"**Medical History:**")
                            st.info(r.medical_history)
                        if r.uploaded_reports_text:
                            st.markdown(f"**Pasted Report / Lab Results:**")
                            st.code(r.uploaded_reports_text[:600] + ("..." if len(r.uploaded_reports_text) > 600 else ""))

                    with col_o:
                        st.markdown("#### 📤 AI Generated Report")
                        if rd:
                            if rd.get("is_urgent"):
                                st.error(rd.get("action_level", ""))
                            elif rd.get("action_color") == "orange":
                                st.warning(rd.get("action_level", ""))
                            else:
                                st.success(rd.get("action_level", ""))

                            st.markdown("**Detected Conditions:**")
                            for c in rd.get("detected_conditions", []):
                                st.markdown(f'<span class="badge-red">{c}</span>', unsafe_allow_html=True)
                            
                            if rd.get("abnormal_values"):
                                st.markdown("**⚠️ Abnormal Values:**")
                                for v in rd.get("abnormal_values", []):
                                    st.markdown(v)

                            st.markdown("**Precautions:**")
                            for p_item in rd.get("precautions", [])[:4]:
                                st.markdown(f"- {p_item}")

            # Summary table
            st.divider()
            st.markdown("### Summary Table")
            table_rows = ""
            for r in reports:
                rd = r.report_data
                action = rd.get("action_level", "N/A") if rd else "N/A"
                conds = ", ".join(rd.get("detected_conditions", [])[:2]) if rd else "N/A"
                table_rows += f"""
                <tr>
                    <td>{r.id}</td>
                    <td>{r.age}</td>
                    <td>{r.demographics}</td>
                    <td>{r.current_symptoms[:60] + '...' if r.current_symptoms and len(r.current_symptoms) > 60 else (r.current_symptoms or 'N/A')}</td>
                    <td>{conds}</td>
                    <td>{action}</td>
                </tr>"""

            st.markdown(f"""
            <table class="history-table">
                <thead>
                    <tr>
                        <th>Report ID</th><th>Age</th><th>Demographics</th>
                        <th>Symptoms (preview)</th><th>Conditions Found</th><th>Action Level</th>
                    </tr>
                </thead>
                <tbody>{table_rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

    # ── Tab 2: Synthetic Patient Records ────────────────────────────────────────
    with tab_h2:
        all_projects = db.query(Project).all()
        if not all_projects:
            st.info("No projects found. Go to the Synthetic Data Generator to create patients.")
        else:
            all_patients = db.query(SyntheticPatient).all()
            if not all_patients:
                st.info("No synthetic patients found yet.")
            else:
                st.markdown(f"**{len(all_patients)} synthetic patient record(s) across {len(all_projects)} project(s)**")

                # Full table
                proj_map_all = {p.id: p.name for p in all_projects}
                table_rows2 = ""
                for pat in all_patients:
                    proj_name = proj_map_all.get(pat.project_id, "Unknown")
                    conds = ", ".join(pat.conditions)
                    syms = ", ".join(pat.symptoms)
                    table_rows2 += f"""
                    <tr>
                        <td>{pat.id}</td>
                        <td>{proj_name}</td>
                        <td>{pat.age}</td>
                        <td>{pat.sex}</td>
                        <td>{pat.severity}</td>
                        <td>{conds}</td>
                        <td>{syms}</td>
                    </tr>"""

                st.markdown(f"""
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Synthetic ID</th><th>Project</th><th>Age</th>
                            <th>Sex</th><th>Severity</th><th>Conditions</th><th>Symptoms</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows2}</tbody>
                </table>
                """, unsafe_allow_html=True)

                # CSV Download
                st.divider()
                csv_data = [{"Synthetic ID": p.id, "Project": proj_map_all.get(p.project_id, "?"),
                              "Age": p.age, "Sex": p.sex, "Severity": p.severity,
                              "Conditions": ", ".join(p.conditions), "Symptoms": ", ".join(p.symptoms)}
                             for p in all_patients]
                out = io.StringIO()
                writer = csv.DictWriter(out, fieldnames=csv_data[0].keys())
                writer.writeheader(); writer.writerows(csv_data)
                st.download_button("⬇️ Download All Synthetic Records as CSV",
                                   data=out.getvalue().encode("utf-8"),
                                   file_name="all_synthetic_patients.csv", mime="text/csv")

    db.close()
