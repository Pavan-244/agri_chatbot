# frontend/main.py

# ✅ Fix import paths for local modules
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Streamlit config - MUST be first Streamlit command
import streamlit as st
st.set_page_config(page_title="Agri Chatbot", layout="centered")

# ✅ Imports
import tempfile
from app.chatbot import ask_chatgpt
from app.disease_model import predict_disease, load_trained_model

# ✅ Streamlit UI
st.title("🌾 AI Agri Chatbot")
st.write("Ask your farming questions or upload a leaf image for disease diagnosis.")

# 💬 Text Chat Input
user_input = st.text_input("💬 Ask something (e.g. 'Should I irrigate today?', 'What is this leaf spot?')")

if st.button("Ask"):
    if user_input:
        with st.spinner("Thinking..."):
            if "disease" in user_input.lower():
                model = load_trained_model()
                label, confidence = predict_disease(user_input, model)  # optional if used with text
                st.success(f"🌿 Disease Prediction: {label}")
                st.info(f"Confidence: {confidence*100:.2f}%")
            else:
                response = ask_chatgpt(user_input)
                st.success("🤖 " + response)

# 📷 Image Upload for Disease Diagnosis
st.markdown("---")
st.subheader("📷 Upload Crop Leaf Image")
uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Save temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file_path = temp_file.name

    # Run disease prediction
    model = load_trained_model()
    label, confidence = predict_disease(temp_file_path, model)

    st.success(f"🩺 Detected Disease: **{label}**")
    st.info(f"Confidence: {confidence*100:.2f}%")

    os.remove(temp_file_path)
