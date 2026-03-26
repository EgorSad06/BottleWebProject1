from bottle import post, request, re
from datetime import datetime

@post('/home', method='post')
def my_form():

    mail = request.forms.get('ADRESS')
    username = request.forms.get('USERNAME')
    Question = request.forms.get('QUEST')
    
    if not mail or not username:
        return "Error: incorrect form"

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, mail):
        return "Error: incorrect mail"
    

    username_pattern = r'^[A-Za-z]{4,}$'
    if not re.match(username_pattern, username):
        return "Error: username must be at least 4 characters long and contain only English letters"
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    result_message = f"Thanks, {username}! The answer'{Question}' will be sent to the mail {mail}. Access Date: {current_date}"
    
    return result_message