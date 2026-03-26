# myform.py
from datetime import datetime
import json
import os
import re
from bottle import post, request, get
from myform_mail import is_valid_email  # Импортируем нашу функцию валидации

JSON_FILE = 'user_data.json'

def load_data():
    """Load existing data from JSON file, return empty dict if file doesn't exist"""
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_data(data):
    """Save data to JSON file with pretty formatting"""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@post('/home', method='post')
def my_form():
    mail = request.forms.get('ADRESS')
    username = request.forms.get('USERNAME')
    question = request.forms.get('QUEST')
    
    # Валидация
    if not mail or not username:
        return "Error: missing email or username"
    
    if not question:
        return "Error: missing question"
    
    # Используем функцию из myform_mail вместо прямого re.match
    if not is_valid_email(mail):
        return "Error: incorrect email format"
    
    username_pattern = r'^[A-Za-z]{4,}$'
    if not re.match(username_pattern, username):
        return "Error: username must be at least 4 characters long and contain only English letters"
    
    question_stripped = question.strip()  
    if len(question_stripped) <= 3:
        return "Error: question must be longer than 3 characters"
    if question_stripped.isdigit():
        return "Error: question cannot consist only of digits"
    
    if not question_stripped:
        return "Error: question cannot be empty or contain only spaces"
    
    user_data = load_data()
    
    if mail in user_data:
        if question_stripped not in user_data[mail]["questions"]:
            user_data[mail]["questions"].append(question_stripped)
            action = "added new question"
        else:
            action = "question already existed (duplicate skipped)"
    else:
        user_data[mail] = {
            "username": username,
            "questions": [question_stripped]
        }
        action = "created new user with first question"
    
    save_data(user_data)
    
    print(f"DEBUG - {action}: {mail} -> {username}, questions: {user_data[mail]['questions']}")
    print(f"DEBUG - Total users in database: {len(user_data)}")
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    result_message = f"Thanks, {username}! The answer '{question_stripped}' will be sent to the mail {mail}. Access Date: {current_date}"
    
    return result_message

@get('/debug')
def show_data():
    """Debug endpoint to view stored data in browser"""
    user_data = load_data()
    if not user_data:
        return "<h3>No data stored yet</h3>"
    
    result = "<h3>Stored User Data:</h3>"
    result += "<table border='1' cellpadding='5'>"
    result += "<tr><th>Email</th><th>Username</th><th>Questions</th></tr>"
    
    for email, info in user_data.items():
        questions_html = "<ul>" + "".join(f"<li>{q}</li>" for q in info["questions"]) + "</ul>"
        result += f"<tr><td>{email}</td><td>{info['username']}</td><td>{questions_html}</td></tr>"
    
    result += "</table>"
    return result

@get('/debug/json')
def show_json():
    """Debug endpoint to view raw JSON data"""
    user_data = load_data()
    return user_data