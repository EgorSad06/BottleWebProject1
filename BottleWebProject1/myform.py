from bottle import post, request, re, get
from datetime import datetime
import pdb

user_data = {}

@post('/home', method='post')
def my_form():
    mail = request.forms.get('ADRESS')
    username = request.forms.get('USERNAME')
    question = request.forms.get('QUEST')
    
    pdb.set_trace()
    
    if not mail or not username:
        return "Error: incorrect form"

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, mail):
        return "Error: incorrect mail"
    
    username_pattern = r'^[A-Za-z]{4,}$'
    if not re.match(username_pattern, username):
        return "Error: username must be at least 4 characters long and contain only English letters"
    
    user_data[mail] = [username, question]
    
    print(f"DEBUG - Added entry: {mail} -> [{username}, {question}]")
    print(f"DEBUG - Total entries: {len(user_data)}")
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    result_message = f"Thanks, {username}! The answer '{question}' will be sent to the mail {mail}. Access Date: {current_date}"
    
    return result_message

@get('/debug')
def show_data():
    """Debug endpoint to view stored data"""
    if not user_data:
        return "<h3>No data stored yet</h3>"
    
    result = "<h3>Stored User Data:</h3>"
    result += "<table border='1' cellpadding='5'>"
    result += "<tr><th>Email</th><th>Username</th><th>Question</th></tr>"
    
    for email, data in user_data.items():
        result += f"<tr><td>{email}</td><td>{data[0]}</td><td>{data[1]}</td></tr>"
    
    result += "</table>"
    return result

@get('/debug/console')
def console_debug():
    """Debug endpoint that triggers console debugging"""
    import sys
    pdb.set_trace()
    return "Check console for debugger"