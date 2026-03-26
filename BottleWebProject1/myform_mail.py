# myform_mail.py
import re

def is_valid_email(email: str) -> bool:
    """
    Проверяет, соответствует ли строка формату email.
    
    Args:
        email (str): Строка для проверки
        
    Returns:
        bool: True если email валидный, иначе False
    """
    if not email or not isinstance(email, str):
        return False
    
    # Регулярное выражение для проверки email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False
    
    # Дополнительные проверки
    local_part = email.split('@')[0]
    
    # Запрещаем точку в начале и конце локальной части
    if local_part.startswith('.') or local_part.endswith('.'):
        return False
    
    # Запрещаем две точки подряд
    if '..' in local_part:
        return False
    
    return True