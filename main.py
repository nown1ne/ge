from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from supabase import create_client, Client

SUPABASE_URL = 'https://zqxdgopzsaoyhctnghaa.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxeGRnb3B6c2FveWhjdG5naGFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY1NjkzNDEsImV4cCI6MjAzMjE0NTM0MX0.2kOPWjNeeEQQyXzfC_ORHOV1UZMoNXJg5pYOPoKlUgM'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

    save_to_supabase(answers)
    return {"question": "Thank you for completing the survey!", "options": [], "key": None}

def save_to_supabase(data):
    data = {
        "user_id": "32223c22-956c-446f-84db-6895775ae1fa",
        "name": data.get("name"),
        "age": data.get("age"),
        "medical_history": data.get("medical_details", ""),
        "diagnosed": data.get("diagnosed"),
        "diagnosed_stage": data.get("diagnosed_stage"),
        "diagnosed_report": data.get("diagnosed_report"),
        "cbc_report": data.get("cbc_report"),
        "mammogram": data.get("mammogram"),
        "ultrasound": data.get("ultrasound"),
        "mri": data.get("mri"),
        "biopsy": data.get("biopsy"),
        "genetic_testing": data.get("genetic_testing"),
        "last_screening": data.get("last_screening"),
        "screening_frequency": data.get("screening_frequency"),
    }

    supabase.table("survey_responses").insert(data).execute()

if __name__ == '__main__':
    app.run(debug=True)
