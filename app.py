import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pickle
import json
import requests
import pandas as pd
<<<<<<< HEAD
from datetime import datetime
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SasyaAI — Smart Farming",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Farmer-first, earthy, warm
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Lora:wght@400;600&display=swap');

/* ── ROOT TOKENS ── */
:root {
    --soil:    #3d2b1f;
    --leaf:    #2d6a4f;
    --sprout:  #52b788;
    --sky:     #90e0ef;
    --straw:   #f4e285;
    --cream:   #fdfaf4;
    --muted:   #6b7c6a;
    --danger:  #c0392b;
    --warning: #e67e22;
}

html, body, [data-testid="stApp"] {
    background-color: var(--cream) !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1b4332 0%, #2d6a4f 60%, #40916c 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #d8f3dc !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMarkdown p { color: #b7e4c7 !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: white !important;
    border-radius: 10px !important;
}

/* ── HEADER HERO BANNER ── */
.hero-banner {
    background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
    border-radius: 20px;
    padding: 40px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '🌾';
    position: absolute;
    right: 40px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 80px;
    opacity: 0.25;
}
.hero-banner h1 {
    font-family: 'Lora', serif;
    font-size: 2.2rem;
    font-weight: 600;
    color: white;
    margin: 0 0 8px 0;
    line-height: 1.3;
}
.hero-banner p {
    color: #b7e4c7;
    font-size: 1rem;
    margin: 0;
    max-width: 560px;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    color: #d8f3dc;
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 14px;
}

/* ── STAT CARDS ── */
.stat-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
.stat-card {
    background: white;
    border-radius: 14px;
    padding: 20px 24px;
    flex: 1;
    min-width: 140px;
    border: 1.5px solid #e8f5e9;
    box-shadow: 0 2px 12px rgba(45,106,79,0.06);
}
.stat-card .num {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--leaf);
    line-height: 1;
    margin-bottom: 4px;
}
.stat-card .lbl {
    font-size: 0.78rem;
    color: var(--muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ── FEATURE CARDS ── */
.feature-card {
    background: white;
    border-radius: 16px;
    padding: 28px;
    border: 1.5px solid #e8f5e9;
    box-shadow: 0 2px 16px rgba(45,106,79,0.07);
    height: 100%;
    transition: box-shadow 0.2s;
}
.feature-card:hover { box-shadow: 0 6px 28px rgba(45,106,79,0.14); }
.feature-icon { font-size: 2.2rem; margin-bottom: 12px; }
.feature-card h3 {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--soil);
    margin-bottom: 6px;
}
.feature-card p { color: var(--muted); font-size: 0.88rem; line-height: 1.6; margin: 0; }
.ftag {
    display: inline-block;
    background: #d8f3dc;
    color: var(--leaf);
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-top: 12px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

/* ── RESULT CARDS ── */
.result-box {
    background: white;
    border-radius: 16px;
    padding: 28px 32px;
    border: 2px solid #52b788;
    box-shadow: 0 4px 24px rgba(82,183,136,0.15);
    margin-top: 20px;
}
.disease-name {
    font-family: 'Lora', serif;
    font-size: 1.7rem;
    font-weight: 600;
    color: var(--soil);
    margin-bottom: 4px;
}
.confidence-pill {
    display: inline-block;
    background: #d8f3dc;
    color: var(--leaf);
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 20px;
}
.info-row { margin-bottom: 16px; }
.info-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
}
.info-value {
    font-size: 0.95rem;
    color: var(--soil);
    line-height: 1.6;
}
.healthy-box {
    background: #d8f3dc;
    border: 2px solid #52b788;
    border-radius: 16px;
    padding: 24px 28px;
    text-align: center;
    margin-top: 20px;
}
.healthy-box .big { font-size: 3rem; margin-bottom: 8px; }
.healthy-box h3 { color: var(--leaf); font-size: 1.3rem; font-weight: 700; }
.healthy-box p { color: #2d6a4f; font-size: 0.9rem; margin-top: 4px; }

/* ── HISTORY TABLE ── */
.history-card {
    background: white;
    border-radius: 14px;
    padding: 20px 24px;
    border: 1.5px solid #e8f5e9;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 8px rgba(0,0,0,0.04);
}
.history-disease { font-weight: 700; color: var(--soil); font-size: 0.95rem; }
.history-meta { color: var(--muted); font-size: 0.8rem; margin-top: 2px; }
.history-conf {
    background: #d8f3dc;
    color: var(--leaf);
    border-radius: 10px;
    padding: 4px 12px;
    font-size: 0.82rem;
    font-weight: 700;
}

/* ── CROP PLAN CARDS ── */
.crop-plan-card {
    background: white;
    border-radius: 14px;
    padding: 20px 24px;
    border-left: 4px solid var(--sprout);
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 12px;
}
.crop-plan-card h4 { color: var(--soil); font-weight: 700; margin-bottom: 8px; font-size: 1rem; }
.crop-detail { display: flex; gap: 24px; }
.crop-detail-item { font-size: 0.85rem; color: var(--muted); }
.crop-detail-item span { color: var(--soil); font-weight: 600; display: block; margin-top: 2px; }

/* ── SOIL RESULT ── */
.soil-result {
    background: linear-gradient(135deg, #1b4332, #2d6a4f);
    border-radius: 16px;
    padding: 32px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.soil-result .crop-rec { font-family: 'Lora', serif; font-size: 2rem; font-weight: 600; margin-bottom: 6px; }
.soil-result .sub { color: #b7e4c7; font-size: 0.9rem; }

/* ── AUTH FORM ── */
.auth-wrapper {
    max-width: 440px;
    margin: 20px auto;
    background: white;
    border-radius: 20px;
    padding: 40px;
    border: 1.5px solid #e8f5e9;
    box-shadow: 0 4px 30px rgba(45,106,79,0.1);
}
.auth-wrapper h2 {
    font-family: 'Lora', serif;
    color: var(--soil);
    font-size: 1.6rem;
    margin-bottom: 6px;
    text-align: center;
}
.auth-wrapper .sub { color: var(--muted); font-size: 0.88rem; text-align: center; margin-bottom: 28px; }

/* ── SIDEBAR LOGO ── */
.sidebar-logo {
    padding: 24px 20px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 8px;
}
.sidebar-logo h2 { font-size: 1.5rem; font-weight: 800; color: white !important; margin: 0; }
.sidebar-logo p { color: #b7e4c7 !important; font-size: 0.78rem; margin: 4px 0 0; }

/* ── USER CHIP ── */
.user-chip {
    background: rgba(255,255,255,0.12);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 0 0 16px;
    font-size: 0.82rem;
    color: #d8f3dc !important;
    border: 1px solid rgba(255,255,255,0.15);
}

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: var(--leaf) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 10px 20px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #40916c !important; }
[data-testid="stFileUploader"] {
    background: white !important;
    border: 2px dashed #52b788 !important;
    border-radius: 14px !important;
    padding: 20px !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    border-radius: 10px !important;
    border-color: #c8e6c9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stAlert { border-radius: 12px !important; }
h1,h2,h3 { font-family: 'Plus Jakarta Sans', sans-serif; }
.stMetric { background: white; border-radius: 12px; padding: 16px; border: 1.5px solid #e8f5e9; }
div[data-testid="metric-container"] { background: white; border-radius: 12px; padding: 16px; border: 1.5px solid #e8f5e9; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SUPABASE CONFIG — users paste their own keys
# ─────────────────────────────────────────────
SUPABASE_URL = st.secrets.get("SUPABASE_URL", "")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "")

def supabase_request(method, path, data=None, token=None):
    """Generic Supabase REST call."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None, "Supabase not configured"
    url = f"{SUPABASE_URL}/rest/v1{path}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        if method == "GET":
            r = requests.get(url, headers=headers, timeout=8)
        elif method == "POST":
            r = requests.post(url, headers=headers, json=data, timeout=8)
        elif method == "PATCH":
            r = requests.patch(url, headers=headers, json=data, timeout=8)
        if r.status_code in (200, 201):
            return r.json(), None
        return None, r.json().get("message", "Request failed")
    except Exception as e:
        return None, str(e)

def auth_request(path, data):
    """Supabase Auth REST call."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None, "Supabase not configured"
    url = f"{SUPABASE_URL}/auth/v1{path}"
    headers = {"apikey": SUPABASE_KEY, "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=data, timeout=8)
        body = r.json()
        if r.status_code in (200, 201) and "access_token" in body:
            return body, None
        return None, body.get("error_description") or body.get("msg") or "Auth failed"
    except Exception as e:
        return None, str(e)

def save_prediction(user_id, token, disease, confidence, crop_type="Unknown"):
    """Save a prediction to Supabase predictions table."""
    data = {
        "user_id": user_id,
        "disease": disease,
        "confidence": float(confidence),
        "crop_type": crop_type,
        "created_at": datetime.utcnow().isoformat()
    }
    supabase_request("POST", "/predictions", data=data, token=token)

def get_predictions(user_id, token):
    """Fetch prediction history for a user."""
    result, _ = supabase_request(
        "GET",
        f"/predictions?user_id=eq.{user_id}&order=created_at.desc&limit=20",
        token=token
    )
    return result or []


# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
for key, default in [
    ("logged_in", False), ("user_email", ""), ("user_id", ""),
    ("access_token", ""), ("auth_mode", "login"),
    ("local_history", [])
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────
# ALL 38 DISEASE INFO
# ─────────────────────────────────────────────
DISEASE_INFO = {
    # TOMATO (10 classes)
    "Tomato___Bacterial_spot": {
        "crop": "Tomato", "cause": "Bacteria: Xanthomonas campestris pv. vesicatoria",
        "severity": "Moderate",
        "treatment": "Apply copper-based bactericide every 7–10 days. Use certified disease-free seeds. Avoid working with wet plants. Remove and destroy infected debris."
    },
    "Tomato___Early_blight": {
        "crop": "Tomato", "cause": "Fungus: Alternaria solani — warm, humid conditions",
        "severity": "Moderate",
        "treatment": "Apply Mancozeb or Chlorothalonil fungicide. Remove infected lower leaves. Avoid overhead watering. Mulch the soil base. Rotate crops next season."
    },
    "Tomato___Late_blight": {
        "crop": "Tomato", "cause": "Oomycete: Phytophthora infestans — cool wet weather",
        "severity": "High",
        "treatment": "Apply copper-based fungicide immediately. Remove and destroy all infected plants — do not compost. Improve air circulation. Avoid wetting leaves."
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato", "cause": "Fungus: Passalora fulva — high humidity environments",
        "severity": "Moderate",
        "treatment": "Improve greenhouse ventilation. Reduce humidity below 85%. Apply Mancozeb or Chlorothalonil. Remove affected leaves immediately."
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato", "cause": "Fungus: Septoria lycopersici",
        "severity": "Moderate",
        "treatment": "Remove lower infected leaves. Apply copper fungicide. Mulch around base. Avoid overhead irrigation. Rotate crops annually."
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato", "cause": "Pest: Tetranychus urticae — hot dry conditions",
        "severity": "Moderate",
        "treatment": "Spray neem oil or insecticidal soap every 3 days. Increase humidity around plant. Introduce predatory mites (Phytoseiulus persimilis). Avoid water stress."
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato", "cause": "Fungus: Corynespora cassiicola",
        "severity": "Moderate",
        "treatment": "Apply Azoxystrobin or Difenoconazole fungicide. Remove infected leaves. Avoid overhead irrigation. Ensure good canopy airflow."
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato", "cause": "Begomovirus spread by silverleaf whitefly",
        "severity": "High",
        "treatment": "Remove and destroy infected plants immediately. Control whitefly population with yellow sticky traps and imidacloprid. Use TYLCV-resistant tomato varieties. Install insect nets."
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato", "cause": "Tobacco Mosaic Virus (TMV) — spreads by contact",
        "severity": "High",
        "treatment": "Remove and destroy infected plants. Disinfect all tools with 10% bleach solution. Wash hands thoroughly before handling plants. Use TMV-resistant varieties."
    },
    "Tomato___healthy": {
        "crop": "Tomato", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Plant is healthy! Continue regular monitoring, balanced fertilization, and proper watering."
    },
    # POTATO (3 classes)
    "Potato___Early_blight": {
        "crop": "Potato", "cause": "Fungus: Alternaria solani",
        "severity": "Moderate",
        "treatment": "Apply Mancozeb fungicide at first sign. Remove infected leaves. Avoid overhead watering. Hill soil around plants to prevent tuber infection."
    },
    "Potato___Late_blight": {
        "crop": "Potato", "cause": "Oomycete: Phytophthora infestans — same pathogen as Great Famine",
        "severity": "High",
        "treatment": "Apply copper fungicide immediately. Destroy ALL infected plants and tubers — do not compost. Harvest tubers quickly if outbreak is severe. Use resistant varieties next season."
    },
    "Potato___healthy": {
        "crop": "Potato", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Plant is healthy! Continue hilling, adequate watering, and scout regularly for early signs."
    },
    # CORN / MAIZE (4 classes)
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Maize", "cause": "Fungus: Cercospora zeae-maydis — warm humid nights",
        "severity": "High",
        "treatment": "Apply Strobilurin or Triazole fungicide. Plant resistant hybrids. Improve field drainage. Crop rotation with non-host crops for 2 years."
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Maize", "cause": "Fungus: Puccinia sorghi",
        "severity": "Moderate",
        "treatment": "Apply fungicide (Mancozeb or Propiconazole) at early infection. Plant resistant hybrids. Scouting weekly during silking stage."
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Maize", "cause": "Fungus: Exserohilum turcicum",
        "severity": "High",
        "treatment": "Apply Propiconazole or Azoxystrobin fungicide. Use resistant varieties. Crop rotation. Destroy infected crop debris after harvest."
    },
    "Corn_(maize)___healthy": {
        "crop": "Maize", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Plant is healthy! Scout weekly, ensure proper spacing for airflow, and maintain balanced nutrients."
    },
    # GRAPE (4 classes)
    "Grape___Black_rot": {
        "crop": "Grape", "cause": "Fungus: Guignardia bidwellii",
        "severity": "High",
        "treatment": "Apply Mancozeb or Myclobutanil before bloom and after. Remove all mummified fruit from vine and ground. Prune for better air circulation. Spray every 7–10 days during wet weather."
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape", "cause": "Complex of wood-rotting fungi (Phaeomoniella, Phaeoacremonium)",
        "severity": "High",
        "treatment": "No complete cure. Remove and destroy infected wood. Avoid large pruning wounds. Seal wounds with fungicidal paste. Remove severely affected vines."
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape", "cause": "Fungus: Isariopsis clavispora",
        "severity": "Moderate",
        "treatment": "Apply copper fungicide. Remove and destroy infected leaves. Improve vineyard air circulation through canopy management."
    },
    "Grape___healthy": {
        "crop": "Grape", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Vine is healthy! Maintain pruning schedule, check for pests, and test soil annually."
    },
    # APPLE (4 classes)
    "Apple___Apple_scab": {
        "crop": "Apple", "cause": "Fungus: Venturia inaequalis — cool, wet spring weather",
        "severity": "Moderate",
        "treatment": "Apply Captan or Myclobutanil at bud break and after every rain. Rake and destroy all fallen leaves in autumn. Prune for better airflow. Use scab-resistant varieties."
    },
    "Apple___Black_rot": {
        "crop": "Apple", "cause": "Fungus: Botryosphaeria obtusa",
        "severity": "Moderate",
        "treatment": "Prune and destroy infected branches 8–10 inches below visible symptoms. Apply fungicide (Captan). Remove all mummified fruit. Avoid injuring bark."
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple", "cause": "Fungus: Gymnosporangium juniperi-virginianae — alternates between juniper and apple",
        "severity": "Moderate",
        "treatment": "Remove nearby juniper/cedar trees if possible. Apply Myclobutanil fungicide at pink bud stage. Use rust-resistant apple varieties."
    },
    "Apple___healthy": {
        "crop": "Apple", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Tree is healthy! Continue annual pruning, balanced fertilization, and pest monitoring."
    },
    # ORANGE (1 class)
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange/Citrus", "cause": "Bacteria: Candidatus Liberibacter — spread by Asian citrus psyllid",
        "severity": "Critical",
        "treatment": "No cure exists. Remove and destroy infected trees immediately to prevent spread. Control psyllid vector with imidacloprid. Plant certified disease-free nursery stock only. Report to local agriculture authority."
    },
    # PEACH (2 classes)
    "Peach___Bacterial_spot": {
        "crop": "Peach", "cause": "Bacteria: Xanthomonas campestris pv. pruni",
        "severity": "Moderate",
        "treatment": "Apply copper bactericide in spring before bloom. Use resistant varieties. Avoid overhead irrigation. Remove infected twigs during dormant pruning."
    },
    "Peach___healthy": {
        "crop": "Peach", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Tree is healthy! Thin fruit early, maintain good drainage, and monitor for brown rot near harvest."
    },
    # PEPPER (2 classes)
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Bell Pepper", "cause": "Bacteria: Xanthomonas euvesicatoria",
        "severity": "Moderate",
        "treatment": "Apply copper bactericide. Use certified disease-free seeds and transplants. Avoid overhead irrigation. Rotate crops for 2–3 years."
    },
    "Pepper,_bell___healthy": {
        "crop": "Bell Pepper", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Plant is healthy! Ensure consistent moisture, stake plants for support, and fertilize with balanced NPK."
    },
    # CHERRY (2 classes)
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry", "cause": "Fungus: Podosphaera clandestina",
        "severity": "Moderate",
        "treatment": "Apply sulfur or potassium bicarbonate fungicide. Remove infected shoots. Ensure good canopy airflow. Avoid excess nitrogen fertilizer."
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Tree is healthy! Prune annually for shape and airflow, and net against birds near harvest."
    },
    # STRAWBERRY (2 classes)
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry", "cause": "Fungus: Diplocarpon earlianum",
        "severity": "Moderate",
        "treatment": "Remove and destroy infected leaves. Apply Captan or Myclobutanil fungicide. Improve air circulation between rows. Avoid overhead irrigation."
    },
    "Strawberry___healthy": {
        "crop": "Strawberry", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Plants are healthy! Renovate bed after harvest, remove runners, and apply balanced fertilizer."
    },
    # SQUASH (1 class)
    "Squash___Powdery_mildew": {
        "crop": "Squash", "cause": "Fungus: Podosphaera xanthii — dry conditions, moderate temperatures",
        "severity": "Moderate",
        "treatment": "Apply neem oil, potassium bicarbonate, or sulfur fungicide. Remove severely infected leaves. Improve plant spacing for airflow. Use resistant varieties."
    },
    # SOYBEAN (1 class)
    "Soybean___healthy": {
        "crop": "Soybean", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Plants are healthy! Ensure good nodulation for nitrogen fixation and scout for soybean aphids."
    },
    # RASPBERRY (1 class)
    "Raspberry___healthy": {
        "crop": "Raspberry", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Canes are healthy! Prune old canes after fruiting, support with trellises, and check for spotted wing drosophila."
    },
    # BLUEBERRY (1 class)
    "Blueberry___healthy": {
        "crop": "Blueberry", "cause": "No disease detected",
        "severity": "None",
        "treatment": "Bushes are healthy! Maintain acidic soil pH (4.5–5.5), mulch heavily, and net against birds."
    },
}

SEVERITY_COLOR = {
    "None": "#52b788",
    "Moderate": "#e67e22",
    "High": "#c0392b",
    "Critical": "#6c0c0c"
}


# ─────────────────────────────────────────────
# MODEL LOADERS
# ─────────────────────────────────────────────
@st.cache_resource
def load_disease_model():
    model = tf.keras.models.load_model("sasya_disease_model.h5")
    with open("class_names.json") as f:
        class_names = json.load(f)
    return model, class_names

@st.cache_resource
def load_crop_model():
    with open("sasya_crop_model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("sasya_label_encoder.pkl", "rb") as f:
        le = pickle.load(f)
    return model, le


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h2>🌾 SasyaAI</h2>
        <p>Smart farming, powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown(f"""
        <div class="user-chip">
            👤 &nbsp;<strong>{st.session_state.user_email}</strong>
        </div>
        """, unsafe_allow_html=True)

    page = st.selectbox(
        "Navigate",
        ["🏠 Home", "🌿 Disease Detection", "🌍 Soil Advisor",
         "🌦️ Crop Planner", "📊 My History", "🔐 Account"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("""
    <div style='color:#b7e4c7;font-size:0.78rem;padding:0 4px'>
    <strong style='color:#d8f3dc'>📚 About</strong><br><br>
    SasyaAI uses Deep Learning and ML to help farmers detect diseases, plan crops, and improve yield.<br><br>
    <strong style='color:#d8f3dc'>🤖 Models</strong><br>
    MobileNetV2 CNN · Random Forest<br><br>
    <strong style='color:#d8f3dc'>📦 Dataset</strong><br>
    PlantVillage · 87,000+ images · 38 classes
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🌱 AI-Powered AgriTech Platform</div>
        <h1>Smarter farming starts<br>with knowing your crop</h1>
        <p>Detect diseases from a leaf photo, get fertilizer advice from your soil values, and plan the right crops for your season — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-row">
        <div class="stat-card"><div class="num">38</div><div class="lbl">Disease Classes</div></div>
        <div class="stat-card"><div class="num">98.3%</div><div class="lbl">Model Accuracy</div></div>
        <div class="stat-card"><div class="num">87K+</div><div class="lbl">Training Images</div></div>
        <div class="stat-card"><div class="num">3</div><div class="lbl">AI Features</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌿</div>
            <h3>Crop Disease Detection</h3>
            <p>Photo of a leaf → instant disease diagnosis with cause and treatment steps. Covers tomato, potato, maize, grapes, apple, and more.</p>
            <span class="ftag">CNN · MobileNetV2</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌍</div>
            <h3>Soil & Fertilizer Advisor</h3>
            <p>Enter NPK, pH and rainfall values. The model identifies the ideal crop for your soil and tells you exactly what fertilizer to apply.</p>
            <span class="ftag">Random Forest · ML</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🌦️</div>
            <h3>Smart Crop Planner</h3>
            <p>Live weather for your city, matched to your season — gives you which crops to sow, when to sow them, and watering schedules.</p>
            <span class="ftag">Weather API · Logic</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Use the sidebar to navigate between features. Sign in to save your prediction history.")


# ─────────────────────────────────────────────
# PAGE: DISEASE DETECTION
# ─────────────────────────────────────────────
elif page == "🌿 Disease Detection":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">Computer Vision · CNN</div>
        <h1>Crop Disease Detection</h1>
        <p>Upload a clear, close-up photo of a single leaf. SasyaAI will identify the disease, its cause, severity, and treatment steps.</p>
    </div>
    """, unsafe_allow_html=True)

    col_up, col_tip = st.columns([3, 2])

    with col_tip:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📸</div>
            <h3>For best results</h3>
            <p>
            ✅ Close-up of a single leaf<br>
            ✅ Good natural lighting<br>
            ✅ Plain background (ground/soil)<br>
            ✅ In focus, not blurry<br><br>
            ❌ Avoid shadows on the leaf<br>
            ❌ Avoid multiple overlapping leaves
            </p>
            <span class="ftag">38 disease classes supported</span>
        </div>
        """, unsafe_allow_html=True)

    with col_up:
        uploaded_file = st.file_uploader(
            "Upload a leaf image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Supported: JPG, PNG, WEBP"
        )

        if uploaded_file:
            img = Image.open(uploaded_file).convert("RGB")
            col_img, col_btn = st.columns([1, 1])
            with col_img:
                st.image(img, caption="Your uploaded leaf", use_container_width=True)
            with col_btn:
                st.markdown("<br>", unsafe_allow_html=True)
                analyze = st.button("🔬 Analyze Disease", use_container_width=True)

            if analyze:
                with st.spinner("Analyzing leaf with MobileNetV2 CNN..."):
=======

st.set_page_config(page_title="SasyaAI", page_icon="🌿", layout="wide")

st.title("🌿 SasyaAI")
st.caption("AI-powered farming assistant — disease detection, soil advice, and crop planning")
st.divider()

page = st.sidebar.selectbox(
    "Choose a feature",
    ["🌿 Crop Disease Detection", "🌍 Soil & Fertilizer Advisor", "🌦️ Smart Crop Planner"]
)

if page == "🌿 Crop Disease Detection":
    st.header("🌿 Crop Disease Detection")
    st.write("Upload a clear close-up photo of a leaf — SasyaAI will identify the disease.")

    @st.cache_resource
    def load_disease_model():
        model = tf.keras.models.load_model("sasya_disease_model.h5")
        with open("class_names.json") as f:
            class_names = json.load(f)
        return model, class_names

    disease_info = {
        "Tomato___Early_blight":   {"cause": "Fungus: Alternaria solani", "treatment": "Apply Mancozeb fungicide. Remove infected leaves. Avoid overhead watering."},
        "Tomato___Late_blight":    {"cause": "Phytophthora infestans", "treatment": "Apply copper fungicide. Remove infected plants. Improve air circulation."},
        "Tomato___Leaf_Mold":      {"cause": "Fungus: Passalora fulva", "treatment": "Improve ventilation. Apply Mancozeb. Remove affected leaves."},
        "Tomato___Septoria_leaf_spot": {"cause": "Fungus: Septoria lycopersici", "treatment": "Remove lower leaves. Apply copper fungicide. Mulch around base."},
        "Tomato___Spider_mites Two-spotted_spider_mite": {"cause": "Pest: Spider mites", "treatment": "Spray neem oil. Increase humidity. Introduce predatory mites."},
        "Tomato___Target_Spot":    {"cause": "Fungus: Corynespora cassiicola", "treatment": "Apply Azoxystrobin fungicide. Remove infected leaves."},
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {"cause": "Virus spread by whiteflies", "treatment": "Remove infected plants. Use yellow sticky traps. Use resistant varieties."},
        "Tomato___Tomato_mosaic_virus": {"cause": "Tobacco Mosaic Virus", "treatment": "Remove infected plants. Disinfect tools. Wash hands before handling."},
        "Tomato___Bacterial_spot": {"cause": "Bacteria: Xanthomonas campestris", "treatment": "Apply copper bactericide. Use disease-free seeds."},
        "Tomato___healthy":        {"cause": "No disease!", "treatment": "Plant is healthy. Keep monitoring regularly."},
        "Potato___Early_blight":   {"cause": "Fungus: Alternaria solani", "treatment": "Apply Mancozeb. Remove infected leaves. Avoid overhead watering."},
        "Potato___Late_blight":    {"cause": "Phytophthora infestans", "treatment": "Apply copper fungicide. Destroy infected plants immediately."},
        "Potato___healthy":        {"cause": "No disease!", "treatment": "Plant is healthy."},
        "Corn_(maize)___Common_rust_": {"cause": "Fungus: Puccinia sorghi", "treatment": "Apply fungicide early. Plant resistant hybrids. Rotate crops."},
        "Corn_(maize)___Northern_Leaf_Blight": {"cause": "Fungus: Exserohilum turcicum", "treatment": "Apply Propiconazole. Use resistant varieties. Crop rotation."},
        "Corn_(maize)___healthy":  {"cause": "No disease!", "treatment": "Plant is healthy."},
        "Grape___Black_rot":       {"cause": "Fungus: Guignardia bidwellii", "treatment": "Apply Mancozeb before bloom. Remove mummified fruit."},
        "Grape___healthy":         {"cause": "No disease!", "treatment": "Plant is healthy."},
        "Apple___Apple_scab":      {"cause": "Fungus: Venturia inaequalis", "treatment": "Apply fungicide at bud break. Rake fallen leaves."},
        "Apple___healthy":         {"cause": "No disease!", "treatment": "Plant is healthy."},
        "Pepper,_bell___Bacterial_spot": {"cause": "Bacteria: Xanthomonas campestris", "treatment": "Apply copper bactericide. Use disease-free seeds."},
        "Pepper,_bell___healthy":  {"cause": "No disease!", "treatment": "Plant is healthy."},
    }

    uploaded_file = st.file_uploader("Upload a leaf image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(img, caption="Uploaded leaf", width=250)
        with col2:
            if st.button("🔍 Analyze Disease", use_container_width=True):
                with st.spinner("Analyzing your leaf..."):
>>>>>>> d8ae5e8ac119587ccd7e12d824b078666187df8e
                    model, class_names = load_disease_model()
                    img_resized = img.resize((224, 224))
                    img_array = np.array(img_resized) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)
                    predictions = model.predict(img_array)
                    confidence = round(float(np.max(predictions)) * 100, 2)
                    predicted_class = class_names[np.argmax(predictions)]
<<<<<<< HEAD

                if confidence < 65:
                    st.warning(f"⚠️ Low confidence ({confidence}%) — the model isn't sure. Please retake the photo in better lighting with the leaf filling most of the frame.")
                else:
                    info = DISEASE_INFO.get(predicted_class, {
                        "crop": "Unknown",
                        "cause": "Could not determine cause",
                        "severity": "Unknown",
                        "treatment": "Please consult a local agronomist for advice."
                    })
                    disease_only = predicted_class.split("___")[-1].replace("_", " ").strip()
                    severity_col = SEVERITY_COLOR.get(info["severity"], "#666")

                    if info["severity"] == "None":
                        st.markdown(f"""
                        <div class="healthy-box">
                            <div class="big">✅</div>
                            <h3>Plant looks healthy!</h3>
                            <p>{info['treatment']}</p>
                            <p style='margin-top:10px;color:#2d6a4f;font-weight:600'>Confidence: {confidence}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="result-box">
                            <div class="disease-name">{disease_only}</div>
                            <div class="confidence-pill">🎯 {confidence}% confidence</div>
                            &nbsp;&nbsp;
                            <span style='background:{severity_col};color:white;border-radius:20px;padding:4px 14px;font-size:0.82rem;font-weight:700'>
                                ⚠️ {info["severity"]} severity
                            </span>
                            <br><br>
                            <div class="info-row">
                                <div class="info-label">🌾 Crop</div>
                                <div class="info-value">{info["crop"]}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">🔬 Cause</div>
                                <div class="info-value">{info["cause"]}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">💊 Treatment</div>
                                <div class="info-value">{info["treatment"]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # Save to local history always
                    entry = {
                        "disease": disease_only,
                        "crop": info.get("crop", "Unknown"),
                        "confidence": confidence,
                        "severity": info.get("severity", "Unknown"),
                        "time": datetime.now().strftime("%d %b %Y, %H:%M")
                    }
                    st.session_state.local_history.insert(0, entry)

                    # Save to Supabase if logged in
                    if st.session_state.logged_in:
                        save_prediction(
                            st.session_state.user_id,
                            st.session_state.access_token,
                            disease_only, confidence, info.get("crop", "Unknown")
                        )
                        st.caption("✅ Saved to your history")


# ─────────────────────────────────────────────
# PAGE: SOIL ADVISOR
# ─────────────────────────────────────────────
elif page == "🌍 Soil Advisor":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">Machine Learning · Random Forest</div>
        <h1>Soil & Fertilizer Advisor</h1>
        <p>Enter your soil test values and environmental conditions. SasyaAI will recommend the best crop and the exact fertilizers needed.</p>
    </div>
    """, unsafe_allow_html=True)

    col_form, col_guide = st.columns([3, 2])

    with col_guide:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧪</div>
            <h3>How to get your soil values</h3>
            <p>
            <strong>Option 1 — Soil testing kit</strong><br>
            Available at any agri-supply store. Test NPK and pH at home.<br><br>
            <strong>Option 2 — Krishi Vigyan Kendra (KVK)</strong><br>
            Government soil testing labs across India. Free or low cost.<br><br>
            <strong>Option 3 — Estimate by crop history</strong><br>
            Use typical values for your region as a starting point.
            </p>
            <span class="ftag">22 crops supported</span>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        with st.form("soil_form"):
            st.subheader("Soil Nutrient Values")
            c1, c2, c3 = st.columns(3)
            with c1:
                N = st.number_input("Nitrogen (N) kg/ha", 0, 200, 90)
            with c2:
                P = st.number_input("Phosphorus (P) kg/ha", 0, 200, 42)
            with c3:
                K = st.number_input("Potassium (K) kg/ha", 0, 200, 43)

            st.subheader("Environmental Conditions")
            c4, c5 = st.columns(2)
            with c4:
                temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
                humidity    = st.number_input("Humidity (%)", 0.0, 100.0, 80.0)
            with c5:
                ph       = st.number_input("Soil pH", 0.0, 14.0, 6.5)
                rainfall = st.number_input("Annual Rainfall (mm)", 0.0, 500.0, 200.0)

            submitted = st.form_submit_button("🌱 Get Recommendation", use_container_width=True)

        if submitted:
            model, le = load_crop_model()
            input_data = pd.DataFrame(
                [[N, P, K, temperature, humidity, ph, rainfall]],
                columns=["N","P","K","temperature","humidity","ph","rainfall"]
            )
            prediction = model.predict(input_data)
            crop = le.inverse_transform(prediction)[0]

            st.markdown(f"""
            <div class="soil-result">
                <div class="sub">Best crop for your soil</div>
                <div class="crop-rec">🌾 {crop.title()}</div>
                <div class="sub">Based on your NPK, pH, temperature, humidity and rainfall values</div>
            </div>
            """, unsafe_allow_html=True)

            ferts = []
            if N < 50:
                ferts.append(("🌿 Nitrogen is low", "Apply Urea (46-0-0) at 50–100 kg/ha", "Organic: compost, green manure, or farmyard manure"))
            elif N > 120:
                ferts.append(("⚠️ Nitrogen is high", "Reduce N application for this crop", "Risk of leaf burn and groundwater contamination"))
            if P < 30:
                ferts.append(("🌿 Phosphorus is low", "Apply DAP (18-46-0) or SSP at 25–50 kg/ha", "Organic: bone meal or rock phosphate"))
            if K < 40:
                ferts.append(("🌿 Potassium is low", "Apply MOP (0-0-60) at 30–60 kg/ha", "Organic: wood ash or banana peels"))
            if ph < 5.5:
                ferts.append(("⚠️ Soil is too acidic", "Apply agricultural lime at 1–2 tonnes/ha", "Re-test pH after 2 months"))
            elif ph > 8.0:
                ferts.append(("⚠️ Soil is too alkaline", "Apply elemental sulfur at 100–200 kg/ha", "Organic: add compost to lower pH gradually"))

            if not ferts:
                st.success("✅ Your soil nutrients and pH are well-balanced for this crop. No corrective fertilizer needed — maintain with regular organic matter additions.")
            else:
                st.subheader("Fertilizer Recommendations")
                for issue, chemical, organic in ferts:
                    with st.expander(issue):
                        c_a, c_b = st.columns(2)
                        with c_a:
                            st.markdown(f"**Chemical option:**\n\n{chemical}")
                        with c_b:
                            st.markdown(f"**Organic option:**\n\n{organic}")


# ─────────────────────────────────────────────
# PAGE: CROP PLANNER
# ─────────────────────────────────────────────
elif page == "🌦️ Crop Planner":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">Weather API · Season Logic</div>
        <h1>Smart Crop Planner</h1>
        <p>Live weather for your location, matched to the current season — tells you the best crops to grow, when to sow, and how often to water.</p>
    </div>
    """, unsafe_allow_html=True)

    CROP_CALENDAR = {
        "summer": [
            {"crop": "Tomato",     "emoji": "🍅", "sow": "March – April",    "harvest": "June – July",    "water": "Every 2 days",  "tip": "Mulch to retain moisture in heat."},
            {"crop": "Okra",       "emoji": "🫛", "sow": "February – March", "harvest": "May – June",     "water": "Every 3 days",  "tip": "Soak seeds overnight before sowing."},
            {"crop": "Watermelon", "emoji": "🍉", "sow": "March",            "harvest": "June",           "water": "Every 4 days",  "tip": "Needs sandy soil and full sun."},
            {"crop": "Cucumber",   "emoji": "🥒", "sow": "Feb – March",      "harvest": "April – May",    "water": "Every 2 days",  "tip": "Train on trellis for better fruit."},
            {"crop": "Groundnut",  "emoji": "🥜", "sow": "March – April",    "harvest": "June – July",    "water": "Every 5 days",  "tip": "Requires well-drained sandy loam."},
        ],
        "winter": [
            {"crop": "Wheat",    "emoji": "🌾", "sow": "October – November", "harvest": "March – April", "water": "Every 7 days",  "tip": "Requires cool temperatures below 25°C."},
            {"crop": "Mustard",  "emoji": "🌼", "sow": "October",            "harvest": "February",      "water": "Every 10 days", "tip": "Frost-tolerant, good for North India."},
            {"crop": "Peas",     "emoji": "🫛", "sow": "Oct – November",     "harvest": "Jan – Feb",     "water": "Every 5 days",  "tip": "Fix nitrogen — ideal before wheat."},
            {"crop": "Onion",    "emoji": "🧅", "sow": "October – Nov",      "harvest": "March",         "water": "Every 4 days",  "tip": "Stop watering 2 weeks before harvest."},
            {"crop": "Carrot",   "emoji": "🥕", "sow": "August – October",   "harvest": "Nov – January", "water": "Every 4 days",  "tip": "Loose, deep sandy soil for straight roots."},
        ],
        "monsoon": [
            {"crop": "Rice",     "emoji": "🌾", "sow": "June – July",   "harvest": "Oct – Nov",    "water": "Keep field flooded", "tip": "Transplant seedlings after 25–30 days in nursery."},
            {"crop": "Maize",    "emoji": "🌽", "sow": "June",          "harvest": "September",    "water": "Every 5 days",       "tip": "Plant on ridges to avoid waterlogging."},
            {"crop": "Soybean",  "emoji": "🫘", "sow": "June – July",   "harvest": "Sept – Oct",   "water": "Every 6 days",       "tip": "Inoculate seeds with Rhizobium bacteria."},
            {"crop": "Cotton",   "emoji": "🌿", "sow": "May – June",    "harvest": "Oct – Dec",    "water": "Every 7 days",       "tip": "Requires deep black soil (Vertisol)."},
            {"crop": "Turmeric", "emoji": "🟡", "sow": "May – June",    "harvest": "Dec – Jan",    "water": "Every 4 days",       "tip": "Needs 80% shade in early growth stage."},
        ],
    }

    col_input, col_weather = st.columns([2, 3])

    with col_input:
        st.subheader("Your Location")
        api_key = st.text_input("OpenWeatherMap API Key", type="password",
                                help="Free at openweathermap.org — takes 15 mins to activate after signup")
        city   = st.text_input("City name", "Delhi")
        season = st.selectbox("Current season", ["summer", "winter", "monsoon"])
        get_plan = st.button("🌾 Get My Crop Plan", use_container_width=True)

    with col_weather:
        if get_plan:
            if not api_key:
                st.error("Please enter your OpenWeatherMap API key.")
            else:
                with st.spinner(f"Fetching live weather for {city}..."):
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    resp = requests.get(url, timeout=8).json()

                if resp.get("cod") != 200:
                    st.error("❌ City not found or API key inactive. Wait 15 minutes after creating a new key.")
                else:
                    temp = resp["main"]["temp"]
                    hum  = resp["main"]["humidity"]
                    desc = resp["weather"][0]["description"].title()
                    feels = resp["main"]["feels_like"]

                    c1, c2, c3 = st.columns(3)
                    c1.metric("🌡️ Temperature", f"{temp}°C", f"Feels {feels}°C")
                    c2.metric("💧 Humidity", f"{hum}%")
                    c3.metric("☁️ Conditions", desc)

                    st.markdown(f"<br>", unsafe_allow_html=True)
                    st.subheader(f"Best crops for {city} this {season}")

                    crops = CROP_CALENDAR.get(season, [])
                    for c in crops:
                        st.markdown(f"""
                        <div class="crop-plan-card">
                            <h4>{c['emoji']} {c['crop']}</h4>
                            <div class="crop-detail">
                                <div class="crop-detail-item">Sow in<span>{c['sow']}</span></div>
                                <div class="crop-detail-item">Harvest<span>{c['harvest']}</span></div>
                                <div class="crop-detail-item">Watering<span>{c['water']}</span></div>
                            </div>
                            <p style='margin-top:10px;font-size:0.82rem;color:#6b7c6a'>💡 {c['tip']}</p>
                        </div>
                        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: PREDICTION HISTORY
# ─────────────────────────────────────────────
elif page == "📊 My History":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">Prediction History</div>
        <h1>My Scan History</h1>
        <p>All your disease detection scans, saved for reference. Sign in to sync history across devices.</p>
    </div>
    """, unsafe_allow_html=True)

    # Try Supabase first, fall back to local
    remote_history = []
    if st.session_state.logged_in:
        remote_history = get_predictions(st.session_state.user_id, st.session_state.access_token)

    local_history = st.session_state.local_history

    if not remote_history and not local_history:
        st.info("📭 No scans yet. Go to **Disease Detection** and analyze a leaf to see your history here.")
    else:
        if remote_history:
            st.subheader(f"☁️ Cloud history ({len(remote_history)} scans)")
            for item in remote_history:
                sev = ""
                dt = item.get("created_at", "")[:16].replace("T", " at ")
                conf = item.get("confidence", 0)
                st.markdown(f"""
                <div class="history-card">
                    <div>
                        <div class="history-disease">{item.get('disease','Unknown')}</div>
                        <div class="history-meta">🌾 {item.get('crop_type','Unknown')} &nbsp;·&nbsp; 🕐 {dt}</div>
                    </div>
                    <div class="history-conf">{conf:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)

        if local_history:
            st.subheader(f"💾 Session history ({len(local_history)} scans)")
            for item in local_history:
                sv_col = SEVERITY_COLOR.get(item.get("severity", ""), "#666")
                st.markdown(f"""
                <div class="history-card">
                    <div>
                        <div class="history-disease">{item['disease']}</div>
                        <div class="history-meta">🌾 {item['crop']} &nbsp;·&nbsp; 🕐 {item['time']}</div>
                    </div>
                    <div style="display:flex;gap:8px;align-items:center">
                        <span style="background:{sv_col};color:white;border-radius:10px;padding:3px 10px;font-size:0.78rem;font-weight:700">{item['severity']}</span>
                        <div class="history-conf">{item['confidence']}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: ACCOUNT (Auth)
# ─────────────────────────────────────────────
elif page == "🔐 Account":
    if st.session_state.logged_in:
        st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-badge">Signed In</div>
            <h1>Welcome back! 👋</h1>
            <p>{st.session_state.user_email}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        local_count = len(st.session_state.local_history)
        col1.metric("Session Scans", local_count)
        col2.metric("Account", "Active")
        col3.metric("Plan", "Free")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Sign Out", use_container_width=False):
            for k in ["logged_in", "user_email", "user_id", "access_token"]:
                st.session_state[k] = "" if k != "logged_in" else False
            st.session_state.logged_in = False
            st.rerun()

    else:
        # Check if Supabase is configured
        supabase_configured = bool(SUPABASE_URL and SUPABASE_KEY)

        if not supabase_configured:
            st.markdown("""
            <div class="hero-banner">
                <div class="hero-badge">Setup Required</div>
                <h1>Set up login</h1>
                <p>Add your Supabase credentials to enable user accounts and sync prediction history across devices.</p>
            </div>
            """, unsafe_allow_html=True)

            st.info("""
            **To enable login, follow these steps:**

            **1.** Go to [supabase.com](https://supabase.com) → Create a free account → New project

            **2.** Go to **Settings → API** → Copy your **Project URL** and **anon/public key**

            **3.** In your project, go to **SQL Editor** and run this to create the predictions table:
            ```sql
            create table predictions (
                id uuid default gen_random_uuid() primary key,
                user_id uuid references auth.users,
                disease text,
                confidence float,
                crop_type text,
                created_at timestamptz default now()
            );
            alter table predictions enable row level security;
            create policy "Users see own predictions" on predictions
                for all using (auth.uid() = user_id);
            ```

            **4.** Add to your Streamlit secrets (`.streamlit/secrets.toml` locally, or Streamlit Cloud secrets):
            ```toml
            SUPABASE_URL = "https://your-project.supabase.co"
            SUPABASE_KEY = "your-anon-key-here"
            ```

            **5.** Restart the app — login will appear here automatically.
            """)

        else:
            tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

            with tab_login:
                st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
                st.markdown('<h2>Welcome back</h2><p class="sub">Sign in to your SasyaAI account</p>', unsafe_allow_html=True)
                email_l = st.text_input("Email", key="login_email", placeholder="farmer@example.com")
                pass_l  = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
                if st.button("Sign In →", use_container_width=True, key="login_btn"):
                    if email_l and pass_l:
                        with st.spinner("Signing in..."):
                            result, err = auth_request("/token?grant_type=password",
                                                       {"email": email_l, "password": pass_l})
                        if result:
                            st.session_state.logged_in    = True
                            st.session_state.user_email   = email_l
                            st.session_state.user_id      = result["user"]["id"]
                            st.session_state.access_token = result["access_token"]
                            st.success("✅ Signed in!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {err}")
                    else:
                        st.warning("Please enter email and password.")
                st.markdown('</div>', unsafe_allow_html=True)

            with tab_signup:
                st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
                st.markdown('<h2>Create account</h2><p class="sub">Free forever. No credit card needed.</p>', unsafe_allow_html=True)
                email_s = st.text_input("Email", key="signup_email", placeholder="farmer@example.com")
                pass_s  = st.text_input("Password (min 6 chars)", type="password", key="signup_pass", placeholder="••••••••")
                pass_c  = st.text_input("Confirm password", type="password", key="signup_conf", placeholder="••••••••")
                if st.button("Create Account →", use_container_width=True, key="signup_btn"):
                    if not email_s or not pass_s:
                        st.warning("Please fill in all fields.")
                    elif pass_s != pass_c:
                        st.error("❌ Passwords don't match.")
                    elif len(pass_s) < 6:
                        st.error("❌ Password must be at least 6 characters.")
                    else:
                        with st.spinner("Creating account..."):
                            result, err = auth_request("/signup", {"email": email_s, "password": pass_s})
                        if result:
                            st.success("✅ Account created! Check your email to confirm, then sign in.")
                        else:
                            st.error(f"❌ {err}")
                st.markdown('</div>', unsafe_allow_html=True)
=======
                    disease_only = predicted_class.split("___")[-1].replace("_", " ").strip()
                    info = disease_info.get(predicted_class, {"cause": "Unknown", "treatment": "Consult an agronomist"})

                if confidence < 70:
                    st.warning(f"Low confidence ({confidence}%) — please use a clearer close-up photo.")
                else:
                    st.success("Analysis complete!")
                    st.metric("Disease Detected", disease_only)
                    st.metric("Confidence", f"{confidence}%")
                    st.info(f"**Cause:** {info['cause']}")
                    st.success(f"**Treatment:** {info['treatment']}")

elif page == "🌍 Soil & Fertilizer Advisor":
    st.header("🌍 Soil & Fertilizer Advisor")
    st.write("Enter your soil values to get crop and fertilizer recommendations.")

    @st.cache_resource
    def load_crop_model():
        with open("sasya_crop_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open("sasya_label_encoder.pkl", "rb") as f:
            le = pickle.load(f)
        return model, le

    col1, col2, col3 = st.columns(3)
    with col1:
        N = st.number_input("Nitrogen (N)", 0, 200, 90)
        P = st.number_input("Phosphorus (P)", 0, 200, 42)
        K = st.number_input("Potassium (K)", 0, 200, 43)
    with col2:
        temperature = st.number_input("Temperature (°C)", 0.0, 50.0, 25.0)
        humidity    = st.number_input("Humidity (%)", 0.0, 100.0, 80.0)
    with col3:
        ph       = st.number_input("Soil pH", 0.0, 14.0, 6.5)
        rainfall = st.number_input("Rainfall (mm)", 0.0, 500.0, 200.0)

    if st.button("🌱 Get Recommendation", use_container_width=True):
        model, le = load_crop_model()
        input_data = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                      columns=["N","P","K","temperature","humidity","ph","rainfall"])
        prediction = model.predict(input_data)
        crop = le.inverse_transform(prediction)[0]
        ferts = []
        if N < 50:  ferts.append("✅ Apply Urea for Nitrogen. Organic: Add compost.")
        if P < 30:  ferts.append("✅ Apply DAP for Phosphorus. Organic: Add bone meal.")
        if K < 40:  ferts.append("✅ Apply MOP for Potassium. Organic: Add wood ash.")
        if not ferts: ferts = ["✅ Soil nutrients are balanced — no fertilizer needed!"]
        st.success("Recommendation ready!")
        st.metric("Best Crop for Your Soil", crop.title())
        st.divider()
        st.subheader("Fertilizer Advice")
        for f in ferts:
            st.write(f)

elif page == "🌦️ Smart Crop Planner":
    st.header("🌦️ Smart Crop Planner")
    st.write("Get weather-based crop suggestions and watering schedules.")
    api_key = st.text_input("OpenWeatherMap API Key", type="password")
    city    = st.text_input("Your city", "Mumbai")
    season  = st.selectbox("Current season", ["summer", "winter", "monsoon"])

    if st.button("🌾 Get Crop Plan", use_container_width=True):
        if not api_key:
            st.error("Please enter your API key.")
        else:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            resp = requests.get(url).json()
            if resp.get("cod") != 200:
                st.error("City not found or API key not active yet.")
            else:
                temp = resp["main"]["temp"]
                hum  = resp["main"]["humidity"]
                desc = resp["weather"][0]["description"]
                st.info(f"📍 {city}: {temp}°C | {hum}% humidity | {desc}")
                crop_map = {
                    "summer":  [("Tomato","March–April","Every 2 days"),("Okra","Feb–March","Every 3 days"),("Watermelon","March","Every 4 days")],
                    "winter":  [("Wheat","Oct–Nov","Every 7 days"),("Mustard","October","Every 10 days"),("Peas","Oct–Nov","Every 5 days")],
                    "monsoon": [("Rice","June–July","Keep flooded"),("Maize","June","Every 5 days"),("Soybean","June–July","Every 6 days")],
                }
                st.subheader("Recommended crops:")
                for crop, sow, water in crop_map.get(season, []):
                    with st.expander(f"🌱 {crop}"):
                        st.write(f"**Sow in:** {sow}")
                        st.write(f"**Watering:** {water}")
>>>>>>> d8ae5e8ac119587ccd7e12d824b078666187df8e
