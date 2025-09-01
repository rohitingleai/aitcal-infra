import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()  # load .env file

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email(to_email: str, subject: str, body: str):
    try:
        print("📧 DEBUG: Trying to send email...")
        print("SMTP_SERVER:", SMTP_SERVER)
        print("SMTP_PORT:", SMTP_PORT)
        print("SMTP_EMAIL:", SMTP_EMAIL)
        print("SMTP_PASSWORD length:", len(SMTP_PASSWORD) if SMTP_PASSWORD else "MISSING")

        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email}")
        return True

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"❌ Email sending failed: {e}")
