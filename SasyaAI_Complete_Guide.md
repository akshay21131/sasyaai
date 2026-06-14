# SasyaAI — Complete Save, GitHub & Deployment Guide
### Everything in one place — offline, online, and presentation ready

---

## PART 1 — Save Everything from Google Colab to Your Computer

### Step 1.1 — Download your trained model files

Run this in Colab to download all files at once:

```python
from google.colab import files

# Download all model files
files.download('sasya_disease_model.h5')
files.download('sasya_crop_model.pkl')
files.download('sasya_label_encoder.pkl')
files.download('class_names.json')
```

Save all of these in one folder on your computer called `sasyaai`.

### Step 1.2 — Download app.py

Run in Colab:
```python
files.download('app.py')
```

Put this in the same `sasyaai` folder.

### Step 1.3 — Your final folder should look like this

```
sasyaai/
├── app.py
├── sasya_disease_model.h5
├── sasya_crop_model.pkl
├── sasya_label_encoder.pkl
├── class_names.json
├── requirements.txt
├── packages.txt
└── README.md
```

---

## PART 2 — Run SasyaAI Offline on Your Computer

### Step 2.1 — Install Python on your computer

1. Go to https://python.org/downloads
2. Download Python 3.10 or higher
3. During install, CHECK the box "Add Python to PATH"
4. Click Install

### Step 2.2 — Open Terminal / Command Prompt

- Windows: Press Win + R → type `cmd` → Enter
- Mac: Press Cmd + Space → type `terminal` → Enter

### Step 2.3 — Go to your project folder

```bash
cd Desktop/sasyaai
```

### Step 2.4 — Install required libraries

```bash
pip install tensorflow streamlit pillow scikit-learn requests pandas numpy
```

Wait for everything to install (takes 3–5 minutes).

### Step 2.5 — Run the app

```bash
streamlit run app.py
```

Your browser will automatically open at:
`http://localhost:8501`

SasyaAI is now running fully offline on your computer!

### Step 2.6 — Show it to anyone on the same WiFi

When Streamlit starts, it shows two URLs:
```
Local URL:   http://localhost:8501
Network URL: http://192.168.1.5:8501
```

Anyone connected to the same WiFi can open the Network URL on their phone or laptop and use SasyaAI — no internet needed!

---

## PART 3 — Upload to GitHub

### Step 3.1 — Create GitHub account

Go to https://github.com and sign up free.

### Step 3.2 — Create a new repository

1. Click the **+** icon (top right) → **New repository**
2. Repository name: `sasyaai`
3. Select: **Public**
4. Check: **Add a README file**
5. Click **Create repository**

### Step 3.3 — Install Git on your computer

Go to https://git-scm.com/downloads and install.

### Step 3.4 — Upload your files via terminal

```bash
# Go to your project folder
cd Desktop/sasyaai

# Initialize git
git init

# Add all files
git add .

# Save a checkpoint
git commit -m "Initial commit — SasyaAI v1.0"

# Connect to your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/sasyaai.git

# Upload
git push -u origin main
```

Replace YOUR_USERNAME with your actual GitHub username.

### Step 3.5 — Upload large model files using Git LFS

The .h5 model file is large (>100MB). Use Git LFS:

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.pkl"

# Add and push
git add .gitattributes
git add sasya_disease_model.h5 sasya_crop_model.pkl sasya_label_encoder.pkl
git commit -m "Add model files"
git push
```

---

## PART 4 — Deploy Online for Free (Permanent URL)

### Step 4.1 — Deploy on Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Click **New app**
4. Select repository: `sasyaai`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **Deploy!**

In 3–5 minutes your app is live at:
`https://YOUR_USERNAME-sasyaai.streamlit.app`

This link works forever and you can share it with anyone!

### Step 4.2 — Add secrets for API key (important!)

In Streamlit Cloud:
1. Go to your app → **Settings** → **Secrets**
2. Add:
```
OPENWEATHER_KEY = "your_api_key_here"
```

Then in app.py replace the API key input with:
```python
import os
api_key = os.environ.get("OPENWEATHER_KEY", "")
```

---

## PART 5 — The Landing Webpage

A beautiful webpage is included as `index.html` in this package.

To use it:
1. Open `index.html` in any browser — works offline
2. To host it online free: go to https://netlify.com → drag and drop the file
3. You get a link like `https://sasyaai.netlify.app`

---

## PART 6 — How to Present SasyaAI

### In an interview or college presentation:

**Step 1 — Open the live app** (Streamlit Cloud URL)

**Step 2 — Demo Disease Detection:**
- Have a tomato/potato leaf photo ready on your phone
- Upload it → show the disease name, confidence, treatment

**Step 3 — Demo Soil Advisor:**
- Enter sample values: N=30, P=20, K=55, Temp=25, Humidity=80, pH=6.5, Rainfall=200
- Show crop recommendation and fertilizer advice

**Step 4 — Demo Crop Planner:**
- Enter your city → show weather + crop suggestions

**Step 5 — Show GitHub repo:**
- Open your GitHub → show the code, README, model files

**What to say:**
> "SasyaAI is an end-to-end AgriTech platform I built using Python, TensorFlow, and Streamlit.
> It uses a MobileNetV2 CNN trained on 87,000+ leaf images to detect 38 crop diseases with 98% accuracy.
> The soil advisor uses a Random Forest model trained on NPK and climate data.
> The crop planner integrates real-time weather data to suggest what to grow and when.
> Everything is deployed on Streamlit Cloud and the code is open source on GitHub."

---

## PART 7 — Files Checklist

| File | What it is | Required? |
|------|-----------|-----------|
| app.py | Main app code | ✅ Yes |
| sasya_disease_model.h5 | Trained CNN | ✅ Yes |
| sasya_crop_model.pkl | Random Forest | ✅ Yes |
| sasya_label_encoder.pkl | Label encoder | ✅ Yes |
| class_names.json | Disease labels | ✅ Yes |
| requirements.txt | Library list | ✅ Yes |
| packages.txt | System libs | ✅ Yes |
| README.md | Project description | ✅ Yes |
| index.html | Landing webpage | ⭐ Recommended |

---

*Good luck presenting SasyaAI! You built something real.*
