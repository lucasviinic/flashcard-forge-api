import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from models.user_model import Users


email_pass = os.getenv('EMAIL_PASS')

def send_feedback_email(user_info: Users, feedback_content: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('EMAIL_SENDER')
    sender_password = email_pass
    recipient_email = os.getenv('EMAIL_RECIPIENT')

    message = MIMEMultipart()
    message["From"] = "Flashly Feedbacks"
    message["To"] = recipient_email
    message["Subject"] = f"Feedback de {user_info.name} (ID: {user_info.id})"

    default_picture = "https://i.pinimg.com/236x/a8/da/22/a8da222be70a71e7858bf752065d5cc3.jpg"
    profile_picture = getattr(user_info, 'picture', default_picture)

    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                padding: 0;
                box-sizing: border-box;
            }}
            .feedback {{
                display: flex;
                align-items: center;
                margin-bottom: 20px;
            }}
            .feedback img {{
                width: 100px;
                height: 100px;
                border-radius: 50%;
                object-fit: cover;
                margin-right: 15px;
            }}
            .comment {{
                font-style: italic;
                color: #555;
            }}
            .details {{
                margin-top: 10px;
                font-size: 0.8em;
            }}
            .details p {{
                margin: 5px 0;
            }}
        </style>
    </head>
    <body>

        <div class="feedback">
            <img src={profile_picture} alt="User Image">
            <p class="comment">"{feedback_content}" - <strong>{user_info.name}</strong></p>
        </div>
    </body>
    </html>
    """
    message.attach(MIMEText(email_body, "html"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        print("E-mail enviado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False
