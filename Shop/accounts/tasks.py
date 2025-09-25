from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_password_reset_email_task(subject, message, from_email, recipient_list, html_message=None):
    """Simple task to send email asynchronously"""
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )