from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)
DATA_FILE = 'user_data.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next_question', methods=['POST'])
def next_question():
    current_answers = request.json
    next_q = get_next_question(current_answers)
    return jsonify(next_q)

def get_next_question(answers):
    if not answers:
        return {"question": "What is your name?", "options": [], "key": "name"}
    if "name" in answers and "age" not in answers:
        return {"question": "What is your age?", "options": [], "key": "age"}
    if "age" in answers and "medical_history" not in answers:
        return {"question": "Do you have any relevant medical history?", "options": ["Yes", "No"], "key": "medical_history"}
    if "medical_history" in answers and answers["medical_history"] == "Yes" and "medical_details" not in answers:
        return {"question": "Please describe your medical history.", "options": [], "key": "medical_details"}
    if "medical_history" in answers and "diagnosed" not in answers:
        return {"question": "Have you been diagnosed with breast cancer?", "options": ["Yes", "No"], "key": "diagnosed"}
    if answers.get("diagnosed") == "Yes":
        if "diagnosed_stage" not in answers:
            return {"question": "What is the diagnosed stage?", "options": [], "key": "diagnosed_stage"}
        if "diagnosed_stage" in answers and "diagnosed_report" not in answers:
            return {"question": "Please upload your diagnosed report.", "options": [], "key": "diagnosed_report"}
        if "diagnosed_report" in answers and "cbc_report" not in answers:
            return {"question": "Please provide the Complete Blood Count (CBC) report.", "options": [], "key": "cbc_report"}
        if "cbc_report" in answers and "mammogram" not in answers:
            return {"question": "Please provide the Mammogram report.", "options": [], "key": "mammogram"}
        if "mammogram" in answers and "ultrasound" not in answers:
            return {"question": "Please provide the Breast Ultrasound report.", "options": [], "key": "ultrasound"}
        if "ultrasound" in answers and "mri" not in answers:
            return {"question": "Please provide the Breast MRI report.", "options": [], "key": "mri"}
        if "mri" in answers and "biopsy" not in answers:
            return {"question": "Please provide the Core Needle Biopsy report.", "options": [], "key": "biopsy"}
        if "biopsy" in answers and "genetic_testing" not in answers:
            return {"question": "Please provide the Genetic Testing report.", "options": [], "key": "genetic_testing"}
    if answers.get("diagnosed") == "No":
        if "last_screening" not in answers:
            return {"question": "When was your last screening?", "options": [], "key": "last_screening"}
        if "last_screening" in answers and "screening_frequency" not in answers:
            return {"question": "How frequently do you get screened?", "options": ["Annually", "Every 2 years", "Every 5 years", "Never"], "key": "screening_frequency"}

    save_to_csv(answers)
    return {"question": "Thank you for completing the survey!", "options": [], "key": None}

def save_to_csv(data):
    new_data = pd.DataFrame([data])
    if not os.path.isfile(DATA_FILE):
        new_data.to_csv(DATA_FILE, index=False)
    else:
        existing_data = pd.read_csv(DATA_FILE)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        updated_data.to_csv(DATA_FILE, index=False)

if __name__ == '__main__':
    app.run(debug=True)
