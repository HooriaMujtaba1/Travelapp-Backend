from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    user = reset_password_token.user
    uid = user.id
    token = reset_password_token.key

    # ✅ Direct link to API endpoint
    reset_link = f"http://127.0.0.1:8000/api/password_reset/confirm/?user_id={uid}&token={token}"

    email_message = f"""
    You requested a password reset.

    Click the link below to open the API endpoint in your browser.

    Reset Link:
    {reset_link}

    """

    send_mail(
        subject="Password Reset Request",
        message=email_message,
        from_email="hooriamughal275@gmail.com",
        recipient_list=[user.email],
        fail_silently=False,
    )


