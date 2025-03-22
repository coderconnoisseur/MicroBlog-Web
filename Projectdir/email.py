from flask_mail import Message
from flask import render_template
from Projectdir import app
from Projectdir import mail

def send_email(subject,sender,recipients,text_body,html_body):
    msg=Message(subject=subject,sender=sender,recipients=recipients)
    msg.body=text_body
    msg.html=html_body
    mail.send(msg)
    # Debugging: Print email content before sending
    print("\n--- Debugging Email Content ---")
    print(f"Subject: {msg.subject}")
    print(f"From: {msg.sender}")
    print(f"To: {msg.recipients}")
    print(f"Body:\n{msg.body}")
    print("\n--- End of Email ---\n")

def send_password_reset_email(user):
    token=user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/reset_password.txt',user=user,token=token),
            html_body=render_template('email/reset_password.html',user=user,token=token))