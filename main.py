from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key
# Supabase configuration
SUPABASE_URL = 'https://zqxdgopzsaoyhctnghaa.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxeGRnb3B6c2FveWhjdG5naGFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY1NjkzNDEsImV4cCI6MjAzMjE0NTM0MX0.2kOPWjNeeEQQyXzfC_ORHOV1UZMoNXJg5pYOPoKlUgM'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('questionnaire'))
    return render_template('index.html')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    response = supabase.auth.sign_up({'email': email, 'password': password})
    if 'error' in response:
        return jsonify({"error": response['error']['message']}), 400
    if 'data' in response and 'user' in response['data']:
        session['user'] = response['data']['user']
        return redirect(url_for('questionnaire'))
    else:
        return jsonify({"error": "Invalid response from Supabase"}), 400

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    response = supabase.auth.sign_in_with_password({'email': email, 'password': password})
    if 'error' in response:
        return jsonify({"error": response['error']['message']}), 400
    if 'data' in response and 'user' in response['data']:
        session['user'] = response['data']['user']
        return redirect(url_for('questionnaire'))
    else:
        return jsonify({"error": "Invalid response from Supabase"}), 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/questionnaire')
def questionnaire():
    # if 'user' not in session:
    #     return redirect(url_for('index'))
    return render_template('survey.html')

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
            return {"question": "Please describe your diagnosed report.", "options": [], "key": "diagnosed_report"}
        if "diagnosed_report" in answers and "cbc_report" not in answers:
            return {"question": "Please describe the Complete Blood Count (CBC) report.", "options": [], "key": "cbc_report"}
        if "cbc_report" in answers and "mammogram" not in answers:
            return {"question": "Please describe the Mammogram report.", "options": [], "key": "mammogram"}
        if "mammogram" in answers and "ultrasound" not in answers:
            return {"question": "Please describe the Breast Ultrasound report.", "options": [], "key": "ultrasound"}
        if "ultrasound" in answers and "mri" not in answers:
            return {"question": "Please describe the Breast MRI report.", "options": [], "key": "mri"}
        if "mri" in answers and "biopsy" not in answers:
            return {"question": "Please describe the Core Needle Biopsy report.", "options": [], "key": "biopsy"}
        if "biopsy" in answers and "genetic_testing" not in answers:
            return {"question": "Please describe the Genetic Testing report.", "options": [], "key": "genetic_testing"}
    if answers.get("diagnosed") == "No":
        if "last_screening" not in answers:
            return {"question": "When was your last screening?", "options": [], "key": "last_screening"}
        if "last_screening" in answers and "screening_frequency" not in answers:
            return {"question": "How frequently do you get screened?", "options": ["Annually", "Every 2 years", "Every 5 years", "Never"], "key": "screening_frequency"}

    save_to_supabase(answers)
    return {"question": "Thank you for completing the survey!", "options": [], "key": None}

def save_to_supabase(data):
    supabase.table('survey_responses').insert(data).execute()

if __name__ == '__main__':
    app.run(debug=True)
