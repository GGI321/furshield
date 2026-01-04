from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_welcome_email(user):
    subject = "Welcome to FurShield 🐾"
    html_content = render_to_string(
        'emails/welcome.html',
        {'user': user}
    )

    email = EmailMultiAlternatives(
        subject,
        '',
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
