# test_email_validator.py
import unittest
from myform_mail import is_valid_email

class TestEmailValidator(unittest.TestCase):
    """Unit-тесты для проверки валидации email"""
    
    def test_valid_emails(self):
        """Тест с assertTrue для корректных email адресов"""
        list_mail_cor = [
            "simple@example.com",
            "very.common@example.com",
            "user+mailbox@example.com",
            "user.name@example.co.uk",
            "test@gmail.com",
            "m.m@mail.ru",
            "user@subdomain.example.com",
            "12345@example.com"
        ]
        
        for email in list_mail_cor:
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email), 
                              f"Email должен быть валидным: {email}")
    
    def test_invalid_emails(self):
        """Тест с assertFalse для некорректных email адресов"""
        list_mail_uncor = [
            "",                          # Пустая строка
            "1",                         # Нет @
            "m1@",                       # Нет домена
            "@mail.ru",                  # Нет локальной части
            "user@.com",                 # Точка после @
            "user@domain..com",          # Две точки
            "user@domain.",              # Точка в конце
            "user name@domain.com",      # Пробел
            "user@domain.c",             # Короткий домен
            ".user@domain.com",          # Точка в начале
            "user.@domain.com",          # Точка в конце
            "user@domain#example.com"    # Недопустимый символ
        ]
        
        for email in list_mail_uncor:
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email),
                               f"Email не должен быть валидным: {email}")

if __name__ == '__main__':
    unittest.main()