import streamlit as st
import pandas as pd
import os
import gdown
import joblib

# Download model and dataset if not already present
if not os.path.exists("churn_model.pkl"):
    gdown.download(id="1tny8CuUQi8dIMXfLG4-f83Q4-FOu8Yid", output="churn_model.pkl", quiet=False)

if not os.path.exists("final_telco.csv"):
    gdown.download(id="1YqVkzauyfM7SVcU7cRgLbVWkVeloJTl2", output="final_telco.csv", quiet=False)

# Load model and data
model = joblib.load("churn_model.pkl")
df = pd.read_csv("final_telco.csv")

# Streamlit page config
st.set_page_config(page_title="Telecom Feedback Collector", layout="centered")
st.markdown("# 📞 Telecom Feedback Collector")
st.markdown("### 📋 Submit Customer Feedback")
st.write("Fill out this form to record telecom customer data.")

# Feedback form
with st.form("feedback_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        married_display = st.selectbox("Married", ["Yes", "No"])
        dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        state = st.text_input("State", placeholder="e.g. Madhya Pradesh")
        county = st.text_input("County", placeholder="e.g. India")
        area_codes = st.text_input("Area Codes", placeholder="e.g. 0731")
        roam_ic = st.text_input("Roaming Incoming", placeholder="e.g. 20.5")
        roam_og = st.text_input("Roaming Outgoing", placeholder="e.g. 15.0")
        loc_og_t2m = st.text_input("Local OG T2M", placeholder="e.g. 50.2")

    with col2:
        online_backup = st.selectbox("Online Backup", ["Yes", "No"])
        device_protect = st.selectbox("Device Protection Plan", ["Yes", "No"])
        tech_support = st.selectbox("Premium Tech Support", ["Yes", "No"])
        stream_tv = st.selectbox("Streaming TV", ["Yes", "No"])
        stream_movies = st.selectbox("Streaming Movies", ["Yes", "No"])
        stream_music = st.selectbox("Streaming Music", ["Yes", "No"])
        unlimited_data = st.selectbox("Unlimited Data", ["Yes", "No"])
        payment_method = st.text_input("Payment Method", placeholder="e.g. Credit Card")
        satisfaction = st.slider("Satisfaction Score", min_value=0, max_value=10, value=5)

    submitted = st.form_submit_button("Submit")

    if submitted:
        # Convert Yes/No to 1/0
        married = 1 if married_display == "Yes" else 0
        online_backup_val = 1 if online_backup == "Yes" else 0
        device_protect_val = 1 if device_protect == "Yes" else 0
        tech_support_val = 1 if tech_support == "Yes" else 0
        stream_tv_val = 1 if stream_tv == "Yes" else 0
        stream_movies_val = 1 if stream_movies == "Yes" else 0
        stream_music_val = 1 if stream_music == "Yes" else 0
        unlimited_data_val = 1 if unlimited_data == "Yes" else 0

        # Form initial row (without churn)
        new_row = pd.DataFrame([{
            "Gender": gender,
            "Age": age,
            "Married": married,
            "Number of Dependents": dependents,
            "state": state,
            "county": county,
            "area_codes": area_codes,
            "roam_ic": roam_ic,
            "roam_og": roam_og,
            "loc_og_t2m": loc_og_t2m,
            "Online Backup": online_backup_val,
            "Device Protection Plan": device_protect_val,
            "Premium Tech Support": tech_support_val,
            "Streaming TV": stream_tv_val,
            "Streaming Movies": stream_movies_val,
            "Streaming Music": stream_music_val,
            "Unlimited Data": unlimited_data_val,
            "Payment Method": payment_method,
            "Satisfaction Score": satisfaction,
        }])

        # Prepare input for model prediction
        input_for_model = new_row.copy()
        categorical_cols = ["Gender", "state", "county", "area_codes", "Payment Method"]
        for col in categorical_cols:
            input_for_model[col] = input_for_model[col].astype("category").cat.codes

        try:
            prediction = model.predict(input_for_model)[0]
            churn_value = int(prediction)

            # Add predicted churn to the row
            new_row["Churn Value"] = churn_value

            # Save to feedback CSV
            feedback_file = "feedback_data.csv"
            if os.path.exists(feedback_file):
                new_row.to_csv(feedback_file, mode='a', index=False, header=False)
            else:
                new_row.to_csv(feedback_file, mode='w', index=False, header=True)

            st.success("✅ Submission successful!")
            st.subheader("📊 Churn Prediction")
            st.write("Predicted Churn:", "**Yes**" if churn_value == 1 else "**No**")

        except Exception as e:
            st.warning(f"⚠️ Prediction failed: {e}")

# Footer
st.markdown("---")
st.markdown("Page built by [Adarsh Agrawal](https://www.linkedin.com/in/adarsh-agrawal-3b0a76268/) 💼")
st.markdown("Data collected will be used for analysis and improving customer service.")
st.markdown("Feel free to reach out for any queries or suggestions!")
