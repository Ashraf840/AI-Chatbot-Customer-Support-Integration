from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect


class EmailService:
    def __init__(self, from_email, to_email):
        self.from_email = from_email
        self.to_email = to_email
    
    def send_mail_cso(self, username=None, password=None):
        login_page_url = "http://127.0.0.1:8080/auth/cso-auth/login/"
        context = {
            "username": username,
            "email": self.to_email,
            "password": password,
            'login_page_url': login_page_url,
        }
        text_content = render_to_string(
            'email_templates/authenticationApp/cso_auth/account_creation_info.txt', 
            context
        )
        html_content = render_to_string(
            'email_templates/authenticationApp/cso_auth/account_creation_info.html', 
            context
        )
        send_mail(
            subject='New Account for CSO - DRMC',
            message= text_content,
            from_email=f'{self.from_email}',
            recipient_list=[self.to_email],
            html_message=html_content,
            fail_silently=False
        )
