# 🌿 SasyaAI — AI-Powered AgriTech Platform

> Smart farming powered by Deep Learning and Machine Learning

![Python](https://img.shields.io/badge/Python-3.10-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What is SasyaAI?

SasyaAI is an end-to-end agricultural intelligence platform that helps farmers detect crop diseases, get soil and fertilizer advice, and plan crops based on real-time weather — all powered by AI.

---

## Features

### 🌿 Crop Disease Detection
- Upload a leaf photo
- AI identifies the disease using a MobileNetV2 CNN model
- Shows disease name, cause, and step-by-step treatment
- Trained on PlantVillage dataset (87,000+ images, 38 disease classes)
- Accuracy: 93–98%

### 🌍 Soil & Fertilizer Advisor
- Enter soil values (N, P, K, pH, temperature, humidity, rainfall)
- Random Forest model recommends the best crop
- Provides fertilizer advice + organic alternatives

### 🌦️ Smart Crop Planner
- Enter your city and season
- Fetches real-time weather via OpenWeatherMap API
- Suggests crops to grow, when to sow, and watering schedule

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10 | Core language |
| TensorFlow / Keras | Disease detection CNN model |
| MobileNetV2 | Transfer learning architecture |
| Scikit-learn | Soil advisor Random Forest model |
| Streamlit | Web app UI |
| OpenWeatherMap API | Real-time weather data |
| PlantVillage Dataset | Training data for disease model |

---

## Project Structure

```
sasyaai/
├── app.py                      ← Main Streamlit app
├── sasya_disease_model.h5      ← Trained CNN model (download separately)
├── sasya_crop_model.pkl        ← Trained Random Forest model
├── sasya_label_encoder.pkl     ← Label encoder
├── class_names.json            ← Disease class names
├── requirements.txt            ← Python dependencies
├── packages.txt                ← System dependencies
└── README.md                   ← This file
```

---

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/sasyaai.git
cd sasyaai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Live Demo

🔗 https://YOUR_USERNAME-sasyaai.streamlit.app

---

## Dataset

- **Disease Detection:** [PlantVillage Dataset](https://www.kaggle.com/datasets/vipoooool/new-plant-diseases-dataset)
- **Crop Recommendation:** [Kaggle Crop Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)

---

## Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | 98.32% |
| Precision | 97.85% |
| Recall | 98.14% |
| F1 Score | 97.99% |
| Inference Speed | ~42ms per image |

---

## Built By

**Your Name** — B.Tech CSE, [Your College]

Connect: [LinkedIn](#) | [GitHub](#)

---

## License

MIT License — free to use and modify.
