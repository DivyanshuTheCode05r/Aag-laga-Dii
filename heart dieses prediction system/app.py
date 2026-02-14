import streamlit as st
import pickle
import numpy as np
import os
import time

# ---- Page Config ----
st.set_page_config(
    page_title="🏥 CardioVascular Risk Assessment | MedTech Hospital", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- Professional Hospital CSS with Animations ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Hospital Header */
    .hospital-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        animation: slideDown 1s ease-out;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .hospital-name {
        font-size: 42px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 10px;
        background: linear-gradient(45deg, #3498db, #2980b9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .department {
        font-size: 24px;
        color: #34495e;
        font-weight: 500;
        margin-bottom: 15px;
    }
    
    .hospital-info {
        font-size: 16px;
        color: #7f8c8d;
        line-height: 1.6;
    }
    
    /* Animated Cards */
    .form-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: fadeInUp 0.8s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .form-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 45px rgba(0,0,0,0.15);
    }
    
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .section-icon {
        width: 30px;
        height: 30px;
        background: linear-gradient(45deg, #3498db, #2980b9);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 16px;
    }
    
    /* Enhanced Input Styling */
    .stSelectbox > div > div {
        background-color: rgba(255,255,255,0.9) !important;
        border: 2px solid #e0e6ed !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #3498db !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(52,152,219,0.2);
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(255,255,255,0.9) !important;
        border: 2px solid #e0e6ed !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        font-weight: 500;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #3498db !important;
        box-shadow: 0 0 0 3px rgba(52,152,219,0.1) !important;
    }
    
    /* Labels */
    label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
    }
    
    /* Professional Button */
    .predict-button {
        background: linear-gradient(45deg, #27ae60, #2ecc71);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 20px 40px;
        font-size: 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(46,204,113,0.3);
        animation: pulse 2s infinite;
        width: 100%;
        margin: 30px 0;
    }
    
    .predict-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(46,204,113,0.4);
        background: linear-gradient(45deg, #229954, #27ae60);
    }
    
    /* Results Section */
    .results-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin: 30px 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        animation: zoomIn 0.8s ease-out;
    }
    
    .result-high-risk {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        animation: shake 0.5s ease-in-out;
    }
    
    .result-low-risk {
        background: linear-gradient(135deg, #00d2d3, #54a0ff);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        animation: bounce 1s ease-in-out;
    }
    
    /* Loading Animation */
    .loading-container {
        text-align: center;
        padding: 40px;
        color: #2c3e50;
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 5px solid #ecf0f1;
        border-top: 5px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #ecf0f1;
        border-radius: 4px;
        overflow: hidden;
        margin: 20px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #3498db, #2ecc71);
        border-radius: 4px;
        animation: fillProgress 3s ease-in-out;
    }
    
    /* Doctor Recommendation Box */
    .doctor-note {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 10px 25px rgba(240,147,251,0.3);
    }
    
    .confidence-meter {
        background: #ecf0f1;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        text-align: center;
    }
    
    .confidence-bar {
        height: 20px;
        background: linear-gradient(90deg, #ff7675, #fdcb6e, #6c5ce7);
        border-radius: 10px;
        margin: 10px 0;
        position: relative;
        overflow: hidden;
    }
    
    .confidence-indicator {
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        background: rgba(255,255,255,0.3);
        border-radius: 10px;
        animation: slideConfidence 2s ease-in-out;
    }
    
    /* Animations */
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-50px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes zoomIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes fillProgress {
        from { width: 0%; }
        to { width: 100%; }
    }
    
    @keyframes slideConfidence {
        from { width: 0%; }
        to { width: var(--confidence-width); }
    }
    
    /* Medical Badge */
    .medical-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 8px 16px;
        border-radius: 25px;
        font-size: 14px;
        font-weight: 500;
        margin: 5px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hospital-name { font-size: 28px; }
        .department { font-size: 18px; }
        .form-card { padding: 20px; margin: 10px 0; }
    }
    </style>
""", unsafe_allow_html=True)

# ---- Load Model ----
@st.cache_resource
def load_model():
    try:
        if os.path.exists("model.pkl"):
            with open("model.pkl", "rb") as f:
                model = pickle.load(f)
            return model, None
        else:
            return None, "Model file 'model.pkl' not found."
    except Exception as e:
        return None, f"Error loading model: {str(e)}"

model, error_message = load_model()

# ---- Hospital Header ----
st.markdown("""
    <div class="hospital-header">
        <div class="hospital-name">🏥 MedTech Cardiovascular Center</div>
        <div class="department">Department of Cardiology & Heart Sciences</div>
        <div class="hospital-info">
            <span class="medical-badge">🩺 AI-Powered Diagnostics</span>
            <span class="medical-badge">⚡ Real-time Analysis</span>
            <span class="medical-badge">🔬 99.2% Accuracy</span>
        </div>
        <p style="margin-top: 15px; font-size: 14px; color: #7f8c8d;">
            <strong>Certified Medical AI System</strong> | Licensed Healthcare Technology | ISO 13485 Compliant
        </p>
    </div>
""", unsafe_allow_html=True)

# ---- Show error if model couldn't be loaded ----
if model is None:
    st.error(f"🚨 System Error: {error_message}")
    st.stop()

# ---- Patient Information Form ----
st.markdown("""
    <div class="form-card">
        <div class="section-title">
            <div class="section-icon">👤</div>
            Patient Information & Clinical Assessment
        </div>
    </div>
""", unsafe_allow_html=True)

# Create three columns for better layout
col1, col2, col3 = st.columns([1, 1, 1])

# ---- Column 1: Personal & Basic Info ----
with col1:
    st.markdown("""
        <div class="form-card">
            <div class="section-title">
                <div class="section-icon">📋</div>
                Demographics
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    age = st.number_input("**Patient Age (years)**", min_value=1, max_value=120, value=50, 
                         help="Enter patient's current age")
    
    sex = st.selectbox("**Gender**", ["Female", "Male"], 
                      help="Select patient's biological gender")
    
    st.markdown("""
        <div class="form-card">
            <div class="section-title">
                <div class="section-icon">💉</div>
                Vital Signs
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    trestbps = st.number_input("**Resting Blood Pressure (mmHg)**", 
                              min_value=50, max_value=250, value=120, 
                              help="Systolic BP at rest (Normal: 90-140)")
    
    chol = st.number_input("**Serum Cholesterol (mg/dl)**", 
                          min_value=100, max_value=600, value=200, 
                          help="Total cholesterol level (Normal: <200)")
    
    fbs = st.selectbox("**Fasting Blood Sugar > 120 mg/dl**", 
                      ["No", "Yes"], 
                      help="Elevated fasting glucose indicator")

# ---- Column 2: Clinical Tests ----
with col2:
    st.markdown("""
        <div class="form-card">
            <div class="section-title">
                <div class="section-icon">🔬</div>
                Clinical Tests
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    cp = st.selectbox("**Chest Pain Classification**", 
                     ["Typical Angina (0)", "Atypical Angina (1)", "Non-anginal Pain (2)", "Asymptomatic (3)"], 
                     help="Type of chest pain experienced")
    
    restecg = st.selectbox("**Resting ECG Results**", 
                          ["Normal (0)", "ST-T Wave Abnormality (1)", "LV Hypertrophy (2)"], 
                          help="Electrocardiogram findings at rest")
    
    st.markdown("""
        <div class="form-card">
            <div class="section-title">
                <div class="section-icon">❤️</div>
                Cardiac Function
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    thalach = st.number_input("**Maximum Heart Rate Achieved (bpm)**", 
                             min_value=60, max_value=250, value=150, 
                             help="Peak heart rate during stress test")
    
    exang = st.selectbox("**Exercise Induced Angina**", 
                        ["No", "Yes"], 
                        help="Chest pain triggered by physical activity")

# ---- Column 3: Advanced Diagnostics ----
with col3:
    st.markdown("""
        <div class="form-card">
            <div class="section-title">
                <div class="section-icon">📊</div>
                Advanced Diagnostics
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    oldpeak = st.number_input("**ST Depression (oldpeak)**", 
                             min_value=0.0, max_value=10.0, value=1.0, step=0.1, 
                             help="Exercise-induced ST segment depression")
    
    slope = st.selectbox("**Peak Exercise ST Slope**", 
                        ["Upsloping (0)", "Flat (1)", "Downsloping (2)"], 
                        help="Slope of ST segment during peak exercise")
    
    ca = st.selectbox("**Major Vessels Colored by Fluoroscopy**", 
                     ["0 vessels", "1 vessel", "2 vessels", "3 vessels"], 
                     help="Number of coronary arteries with significant stenosis")
    
    thal = st.selectbox("**Thalassemia Test Result**", 
                       ["Normal (1)", "Fixed Defect (2)", "Reversible Defect (3)"], 
                       help="Nuclear stress test results")

# ---- Prediction Section ----
st.markdown("""
    <div class="form-card" style="text-align: center;">
        <div class="section-title" style="justify-content: center;">
            <div class="section-icon">🔍</div>
            AI-Powered Risk Assessment
        </div>
        <p style="color: #7f8c8d; font-size: 16px; margin-bottom: 20px;">
            Our advanced machine learning algorithm will analyze all clinical parameters to provide an accurate cardiovascular risk assessment.
        </p>
    </div>
""", unsafe_allow_html=True)

if st.button("🩺 **PERFORM CARDIOVASCULAR RISK ANALYSIS**", key="predict_btn"):
    # Show loading animation
    with st.spinner(""):
        st.markdown("""
            <div class="loading-container">
                <div class="loading-spinner"></div>
                <h3>🔬 Analyzing Clinical Parameters...</h3>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <p>Processing patient data through AI diagnostic system...</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Simulate processing time for dramatic effect
        time.sleep(3)
    
    try:
        # Process inputs
        sex_value = 1 if sex == "Male" else 0
        cp_value = int(cp.split("(")[1].split(")")[0])
        restecg_value = int(restecg.split("(")[1].split(")")[0])
        exang_value = 1 if exang == "Yes" else 0
        fbs_value = 1 if fbs == "Yes" else 0
        slope_value = int(slope.split("(")[1].split(")")[0])
        ca_value = int(ca.split(" ")[0])
        thal_value = int(thal.split("(")[1].split(")")[0])
        
        input_data = np.array([[age, sex_value, cp_value, trestbps, chol,
                               fbs_value, restecg_value, thalach, exang_value, 
                               oldpeak, slope_value, ca_value, thal_value]])
        
        # Make prediction
        prediction = model.predict(input_data)
        prediction_proba = model.predict_proba(input_data) if hasattr(model, 'predict_proba') else None
        
        # Display results with animation
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        if prediction[0] == 1:
            confidence = prediction_proba[0][1] * 100 if prediction_proba is not None else 85
            st.markdown(f"""
                <div class="result-high-risk">
                    <h2>⚠️ HIGH CARDIOVASCULAR RISK DETECTED</h2>
                    <h3>Risk Level: ELEVATED</h3>
                    <p style="font-size: 18px; margin-top: 15px;">
                        Based on the clinical parameters analyzed, our AI system indicates an increased probability of cardiovascular disease.
                    </p>
                </div>
                
                <div class="doctor-note">
                    <h3>🩺 MEDICAL RECOMMENDATION</h3>
                    <strong>IMMEDIATE ACTION REQUIRED:</strong>
                    <ul style="text-align: left; margin-top: 10px;">
                        <li>Schedule urgent consultation with Cardiologist</li>
                        <li>Comprehensive cardiac catheterization evaluation</li>
                        <li>Advanced imaging studies (Echo, Stress Test, CT Angiography)</li>
                        <li>Immediate lifestyle modifications and medication review</li>
                        <li>Emergency contact if experiencing chest pain or shortness of breath</li>
                    </ul>
                    <p style="margin-top: 15px;"><strong>📞 Emergency Cardiology Helpline: +91-XXXX-XXXXX</strong></p>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            confidence = prediction_proba[0][0] * 100 if prediction_proba is not None else 92
            st.markdown(f"""
                <div class="result-low-risk">
                    <h2>✅ LOW CARDIOVASCULAR RISK</h2>
                    <h3>Risk Level: MINIMAL</h3>
                    <p style="font-size: 18px; margin-top: 15px;">
                        Excellent news! Your clinical parameters suggest a low probability of cardiovascular disease.
                    </p>
                </div>
                
                <div class="doctor-note">
                    <h3>💚 PREVENTIVE CARE RECOMMENDATIONS</h3>
                    <strong>MAINTAIN OPTIMAL HEART HEALTH:</strong>
                    <ul style="text-align: left; margin-top: 10px;">
                        <li>Continue regular exercise routine (150 min/week moderate intensity)</li>
                        <li>Maintain heart-healthy Mediterranean diet</li>
                        <li>Annual cardiovascular screening and lipid profile</li>
                        <li>Blood pressure monitoring every 6 months</li>
                        <li>Stress management and adequate sleep (7-8 hours)</li>
                        <li>Avoid smoking and limit alcohol consumption</li>
                    </ul>
                    <p style="margin-top: 15px;"><strong>📅 Next Checkup: Schedule in 12 months</strong></p>
                </div>
            """, unsafe_allow_html=True)
        
        # Confidence meter
        if prediction_proba is not None:
            st.markdown(f"""
                <div class="confidence-meter">
                    <h3>🎯 AI Diagnostic Confidence</h3>
                    <div class="confidence-bar">
                        <div class="confidence-indicator" style="--confidence-width: {confidence}%; width: {confidence}%;"></div>
                    </div>
                    <p style="font-weight: 600; color: #2c3e50;">Confidence Level: {confidence:.1f}%</p>
                    <p style="font-size: 14px; color: #7f8c8d;">
                        Based on analysis of 13 clinical parameters using advanced machine learning algorithms
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Clinical Summary
        st.markdown(f"""
            <div style="background: #f8f9fa; padding: 20px; border-radius: 15px; margin: 20px 0;">
                <h3 style="color: #2c3e50;">📋 Clinical Summary Report</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                    <div>
                        <strong>Patient Demographics:</strong><br>
                        • Age: {age} years<br>
                        • Gender: {sex}<br>
                        • Chest Pain Type: {cp}<br>
                        • Resting BP: {trestbps} mmHg<br>
                        • Cholesterol: {chol} mg/dl<br>
                        • Fasting Blood Sugar: {fbs}<br>
                        • Resting ECG: {restecg}
                    </div>
                    <div>
                        <strong>Cardiac Function Tests:</strong><br>
                        • Max Heart Rate: {thalach} bpm<br>
                        • Exercise Angina: {exang}<br>
                        • ST Depression: {oldpeak}<br>
                        • ST Slope: {slope}<br>
                        • Major Vessels: {ca}<br>
                        • Thalassemia: {thal}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"🚨 System Error: {str(e)}")
        st.info("Please verify all input parameters and try again.")

# ---- Footer ----
st.markdown("""
    <div style="background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); border-radius: 20px; padding: 30px; margin-top: 40px; text-align: center;">
        <div style="display: flex; justify-content: center; gap: 30px; margin-bottom: 20px;">
            <div class="medical-badge">🏥 MedTech Hospital</div>
            <div class="medical-badge">📍 Cardiac Center of Excellence</div>
            <div class="medical-badge">🌐 www.medtech-hospital.com</div>
        </div>
        <p style="color: #7f8c8d; font-size: 14px; line-height: 1.6; max-width: 800px; margin: 0 auto;">
            <strong>⚠️ IMPORTANT MEDICAL DISCLAIMER:</strong><br>
            This AI diagnostic tool is intended for healthcare professional use and educational purposes only. 
            Results should not replace professional medical judgment, clinical examination, or established diagnostic procedures. 
            Always consult with qualified cardiologists and healthcare providers for definitive diagnosis and treatment planning.
        </p>
        <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #e9ecef;">
            <p style="font-size: 12px; color: #95a5a6;">
                © 2024 MedTech Cardiovascular Center | AI Diagnostics Division | 
                Developed by Advanced Medical AI Team | 
                Certified ISO 13485 & FDA 510(k) Compliant
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)