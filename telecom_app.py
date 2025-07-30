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
expected_features = model.feature_names_in_

# Streamlit page config
st.set_page_config(page_title="Telecom Feedback Collector", layout="centered")
st.markdown("# 📞 Telecom Feedback Collector")
st.markdown("### 📋 Submit Customer Feedback")
st.write("Fill out this form to record telecom customer data and predict churn.")

# Feedback form
with st.form("churn_form"):
    st.markdown("### 📝 Customer Information")

    col1, col2 = st.columns(2)

    with col1:
        month = st.selectbox("Current Month", list(range(1, 13)))
        month_join = st.selectbox("Month of Joining", list(range(1, 13)))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", 18, 100, 30)
        married = st.selectbox("Married", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        num_dependents = st.number_input("Number of Dependents", 0, 10, 0)
        state = st.text_input("State", "Maharashtra")
        county = st.text_input("County", "Pune")
        zip_code = st.text_input("Zip Code", "411001")
        area_codes = st.text_input("Area Code", "0731")
        arpu = st.number_input("ARPU", 0.0)
        arpu_4g = st.number_input("ARPU 4G", 0.0)
        arpu_5g = st.number_input("ARPU 5G", 0.0)
        fb_user = st.selectbox("Facebook User", ["Yes", "No"])
        night_user = st.selectbox("Night Pack User", ["Yes", "No"])
        latitude = st.number_input("Latitude", value=0.0)
        longitude = st.number_input("Longitude", value=0.0)

    with col2:
        total_rech_amt = st.number_input("Total Recharge Amount", value=0.0)
        total_rech_data = st.number_input("Total Recharge Data", value=0.0)
        vol_4g = st.number_input("4G Data Volume", value=0.0)
        vol_5g = st.number_input("5G Data Volume", value=0.0)
        roam_ic = st.number_input("Roaming Incoming", value=0.0)
        roam_og = st.number_input("Roaming Outgoing", value=0.0)
        loc_og_t2m = st.number_input("Local OG to Mobile", value=0.0)
        std_og_t2m = st.number_input("STD OG to Mobile", value=0.0)
        isd_og = st.number_input("ISD Outgoing", value=0.0)
        offer = st.selectbox("Is on Offer", ["Yes", "No"])
        referred = st.selectbox("Referred a Friend", ["Yes", "No"])
        num_referrals = st.number_input("Number of Referrals", 0, 20, 0)
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No"])
        internet_type = st.selectbox("Internet Type", ["Fiber optic", "DSL", "None"])
        stream_data = st.number_input("Streaming Data Consumption", value=0.0)
        internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        online_sec = st.selectbox("Online Security", ["Yes", "No"])
        online_backup = st.selectbox("Online Backup", ["Yes", "No"])
        device_protect = st.selectbox("Device Protection Plan", ["Yes", "No"])
        tech_support = st.selectbox("Premium Tech Support", ["Yes", "No"])
        stream_tv = st.selectbox("Streaming TV", ["Yes", "No"])
        stream_movies = st.selectbox("Streaming Movies", ["Yes", "No"])
        stream_music = st.selectbox("Streaming Music", ["Yes", "No"])
        unlimited_data = st.selectbox("Unlimited Data", ["Yes", "No"])
        payment_method = st.text_input("Payment Method", "Credit Card")
        satisfaction = st.slider("Satisfaction Score", 0, 10, 5)

    submitted = st.form_submit_button("Submit")

    if submitted:
        def encode_yn(val): return 1 if val == "Yes" else 0

        input_dict = {
            'Month': month,
            'Month of Joining': month_join,
            'Gender': gender,
            'Age': age,
            'Married': encode_yn(married),
            'Dependents': encode_yn(dependents),
            'Number of Dependents': num_dependents,
            'zip_code': zip_code,
            'state': state,
            'county': county,
            'area_codes': area_codes,
            'arpu': arpu,
            'arpu_4g': arpu_4g,
            'arpu_5g': arpu_5g,
            'fb_user': encode_yn(fb_user),
            'night_pck_user': encode_yn(night_user),
            'latitude': latitude,
            'longitude': longitude,
            'total_rech_amt': total_rech_amt,
            'total_rech_data': total_rech_data,
            'vol_4g': vol_4g,
            'vol_5g': vol_5g,
            'roam_ic': roam_ic,
            'roam_og': roam_og,
            'loc_og_t2m': loc_og_t2m,
            'std_og_t2m': std_og_t2m,
            'isd_og': isd_og,
            'offer': encode_yn(offer),
            'Referred a Friend': encode_yn(referred),
            'Number of Referrals': num_referrals,
            'Phone Service': encode_yn(phone_service),
            'Multiple Lines': encode_yn(multiple_lines),
            'Internet Type': internet_type,
            'Streaming Data Consumption': stream_data,
            'Internet Service': internet_service,
            'Online Security': encode_yn(online_sec),
            'Online Backup': encode_yn(online_backup),
            'Device Protection Plan': encode_yn(device_protect),
            'Premium Tech Support': encode_yn(tech_support),
            'Streaming TV': encode_yn(stream_tv),
            'Streaming Movies': encode_yn(stream_movies),
            'Streaming Music': encode_yn(stream_music),
            'Unlimited Data': encode_yn(unlimited_data),
            'Payment Method': payment_method,
            'Satisfaction Score': satisfaction
        }

        new_row = pd.DataFrame([input_dict])

        # Encode categorical columns if needed (you can customize this)
        for col in ['Gender', 'state', 'county', 'area_codes', 'Internet Type', 'Payment Method']:
            new_row[col] = new_row[col].astype("category").cat.codes

        # Add missing features with 0.0
        for feature in expected_features:
            if feature not in new_row.columns:
                new_row[feature] = 0.0

        try:
            input_for_model = new_row[expected_features]
            prediction = model.predict(input_for_model)[0]
            churn_value = int(prediction)
            new_row["Churn Value"] = churn_value

            # Save feedback
            feedback_file = "feedback_data.csv"
            if os.path.exists(feedback_file):
                new_row.to_csv(feedback_file, mode="a", header=False, index=False)
            else:
                new_row.to_csv(feedback_file, mode="w", header=True, index=False)

            st.success("✅ Submission successful!")
            st.subheader("📊 Churn Prediction")
            st.write("Predicted Churn:", "**Yes**" if churn_value == 1 else "**No**")

        except Exception as e:
            st.warning(f"⚠️ Prediction failed: {e}")

# Footer
st.markdown("---")
st.markdown("Page built by [Adarsh Agrawal](https://www.linkedin.com/in/adarsh-agrawal-3b0a76268/) 💼")
st.markdown("Data collected will be used for analysis and improving customer service.")
