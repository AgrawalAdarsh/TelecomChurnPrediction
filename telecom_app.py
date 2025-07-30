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
with st.form("feedback_form"):
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=18, max_value=100, value=25)
        married_display = st.selectbox("Married", ["Yes", "No"])
        dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        state = st.text_input("State", placeholder="e.g. Maharashtra")
        county = st.text_input("County", placeholder="e.g. Pune")
        area_codes = st.text_input("Area Codes", placeholder="e.g. 0731")
        roam_ic = st.number_input("Roaming Incoming", value=0.0)
        roam_og = st.number_input("Roaming Outgoing", value=0.0)
        loc_og_t2m = st.number_input("Local OG T2M", value=0.0)
        std_og_t2m = st.number_input("STD OG T2M", value=0.0)
        isd_og = st.number_input("ISD OG", value=0.0)
        total_rech_amt = st.number_input("Total Recharge Amount", value=0.0)
        total_rech_data = st.number_input("Total Recharge Data (GB)", value=0.0)
        vol_4g = st.number_input("Volume 4G (GB)", value=0.0)
        vol_5g = st.number_input("Volume 5G (GB)", value=0.0)
        arpu = st.number_input("ARPU", value=0.0)

    with col2:
        night_user = st.selectbox("Night Pack User", ["Yes", "No"])
        fb_user = st.selectbox("Facebook User", ["Yes", "No"])
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
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
        def yn(val): return 1 if val == "Yes" else 0

        # Construct DataFrame
        new_row = pd.DataFrame([{
            "Gender": gender,
            "Age": age,
            "Married": yn(married_display),
            "Number of Dependents": dependents,
            "state": state,
            "county": county,
            "area_codes": area_codes,
            "roam_ic": roam_ic,
            "roam_og": roam_og,
            "loc_og_t2m": loc_og_t2m,
            "std_og_t2m": std_og_t2m,
            "isd_og": isd_og,
            "total_rech_amt": total_rech_amt,
            "total_rech_data": total_rech_data,
            "vol_4g": vol_4g,
            "vol_5g": vol_5g,
            "arpu": arpu,
            "night_pck_user": yn(night_user),
            "fb_user": yn(fb_user),
            "Internet Service": internet_service,
            "Online Backup": yn(online_backup),
            "Device Protection Plan": yn(device_protect),
            "Premium Tech Support": yn(tech_support),
            "Streaming TV": yn(stream_tv),
            "Streaming Movies": yn(stream_movies),
            "Streaming Music": yn(stream_music),
            "Unlimited Data": yn(unlimited_data),
            "Payment Method": payment_method,
            "Satisfaction Score": satisfaction,
        }])

        # Encode categorical columns
        for col in ["Gender", "state", "county", "area_codes", "Internet Service", "Payment Method"]:
            new_row[col] = new_row[col].astype("category").cat.codes

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
