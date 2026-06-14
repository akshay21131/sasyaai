import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import pickle
import json
import requests
import pandas as pd

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
                    model, class_names = load_disease_model()
                    img_resized = img.resize((224, 224))
                    img_array = np.array(img_resized) / 255.0
                    img_array = np.expand_dims(img_array, axis=0)
                    predictions = model.predict(img_array)
                    confidence = round(float(np.max(predictions)) * 100, 2)
                    predicted_class = class_names[np.argmax(predictions)]
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
