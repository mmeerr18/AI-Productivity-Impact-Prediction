import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="AI Productivity Prediction", page_icon="🤖", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e1e2f, #2b5876, #4e4376);
}
.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    color: white;
}
.sub-text {
    text-align: center;
    font-size: 17px;
    color: #eeeeee;
    margin-bottom: 25px;
}
.card {
    background: rgba(255,255,255,0.12);
    padding: 20px;
    border-radius: 18px;
    margin-bottom: 20px;
}
.stButton>button {
    background-color: #ff7b54;
    color: white;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #ff5722;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Productivity Impact Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">An interactive system to predict the impact of AI on productivity.</div>', unsafe_allow_html=True)

with open("model.pkl", "rb") as file:
    data = pickle.load(file)

model = data["model"]
features = data["features"]

user_input = {}

# Maps
age_map = {
    "Under 18": 1,
    "18–25": 2,
    "26–35": 3,
    "Over 35": 4
}

status_map = {
    "Student": 1,
    "Employee": 2,
    "Student and employed": 3,
    "None of the above": 4
}

field_map = {
    "Technology / IT": 1,
    "Healthcare": 2,
    "Business / Administration": 3,
    "Other": 4
}

hours_map = {
    "Less than 1 hour": 1,
    "1–3 hours": 2,
    "4–6 hours": 3,
    "More than 6 hours": 4
}

yes_no_map = {
    "Yes": 1,
    "No": 2,
    "Maybe / Sometimes": 3
}

scale_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

purpose_map = {
    "Studying / Learning": 1,
    "Work tasks": 2,
    "Research": 3,
    "Writing / Editing": 4,
    "Other": 5
}

task_map = {
    "Writing": 1,
    "Solving problems": 2,
    "Research": 3,
    "Summarizing": 4,
    "Other": 5
}

tools_map = {
    "ChatGPT": 1,
    "Google Gemini": 2,
    "Microsoft Copilot": 3,
    "Other AI tools": 4
}

frequency_map = {
    "Rarely": 1,
    "1–2 times per week": 2,
    "3–5 times per week": 3,
    "Daily": 4
}

st.markdown("""
<div class="card">
<h3 style="color:white;">👤 Basic Information</h3>
</div>
""", unsafe_allow_html=True)
st.caption("Hover over the (?) icon to understand each option")
# Important: these names must match model features
for feature in features:

    if feature.startswith("1-"):
        answer = st.radio("1. What is your age group?", list(age_map.keys()))
        user_input[feature] = age_map[answer]

    elif feature.startswith("2-"):
        answer = st.radio("2. What is your current status?", list(status_map.keys()))
        user_input[feature] = status_map[answer]

    elif feature.startswith("3-"):
        answer = st.radio("3. What field do you study or work in?", list(field_map.keys()))
        user_input[feature] = field_map[answer]

    elif feature.startswith("4-"):
        user_input[feature] = st.slider(
            "4. How many hours do you spend using the internet per day?",
             1, 4, 1,
            help="1 = Less than 1 hour | 2 = 1–3 hours | 3 = 4–6 hours | 4 = More than 6 hours"
       )

    elif feature.startswith("5-"):
        user_input[feature] = st.slider(
            "5. What is your level of knowledge about Artificial Intelligence?",
            1, 5, 3,
            help="1 = Very Low | 5 = Very High"
        )

    elif feature.startswith("6-"):
       user_input[feature] = st.slider(
          "6. Do you use Artificial Intelligence tools in your study or work?",
           1, 3, 1,
           help="1 = Yes | 2 = No | 3 = Maybe / Sometimes"
       )
    elif feature.startswith("7-"):
       user_input[feature] = st.slider(
          "7. How often do you use AI tools per week?",
           1, 4, 1,
           help="1 = Rarely | 2 = 1–2 times/week | 3 = 3–5 times/week | 4 = Daily"
       )

    elif feature.startswith("8-"):
        answer = st.radio(
            "8. What is your main purpose for using AI tools?",
            list(purpose_map.keys())
        )
        user_input[feature] = purpose_map[answer]

    elif feature.startswith("9-"):
        answer = st.radio(
            "9. For which type of tasks do you usually use AI tools?",
            list(task_map.keys())
        )
        user_input[feature] = task_map[answer]

    elif feature.startswith("10-"):
        answer = st.radio(
            "10. Which AI tools do you use most often?",
            list(tools_map.keys())
        )
        user_input[feature] = tools_map[answer]

    else:
        if "AI Impact Questions" not in st.session_state:
            st.session_state["AI Impact Questions"] = True
            st.markdown("""
            <div class="card">
            <h3 style="color:white;">📊 AI Impact Questions</h3>
            <p style="color:white; font-size:16px;">
            Please rate each statement from <b>1 to 5</b><br>
            1 = Strongly Disagree | 2 = Disagree | 3 = Neutral | 4 = Agree | 5 = Strongly Agree
            </p>
            </div>
            """, unsafe_allow_html=True)

        user_input[feature] = st.slider(
            feature,
            1, 5, 3
        )

input_data = pd.DataFrame([user_input], columns=features)

st.write("")

if st.button("Predict 🚀"):
    prediction = model.predict(input_data)[0]

    st.success(f"Prediction Result: {prediction}")

    if prediction == 1:
        st.info("The predicted impact of AI on productivity is low.")
    elif prediction == 2:
        st.info("The predicted impact of AI on productivity is moderate.")
    elif prediction == 3:
        st.info("The predicted impact of AI on productivity is high.")
    else:
        st.info("Prediction completed successfully.")