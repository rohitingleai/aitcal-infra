# otp_login.py
import os
import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

# --------------------
# STEP 1: Load env vars
# --------------------
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# --------------------
# STEP 2: FastAPI App
# --------------------
app = FastAPI(title="OTP Login System")

# Store OTPs temporarily (in-memory)
otp_storage = {}  # {email: {"otp": "123456", "expiry": datetime}}

# --------------------
# STEP 3: Helper to send OTP
# --------------------
def send_otp_email(receiver_email: str, otp: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = "Your OTP Code - Secure Login"

        body = f"Hello,\n\nYour OTP code is: {otp}\n\nIt will expire in 2 minutes."
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.sendmail(SMTP_EMAIL, receiver_email, msg.as_string())

        print(f"✅ OTP sent to {receiver_email}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")

# --------------------
# STEP 4: API Models
# --------------------
class RequestOTP(BaseModel):
    email: str

class VerifyOTP(BaseModel):
    email: str
    otp: str

# --------------------
# STEP 5: Request OTP API
# --------------------
@app.post("/auth/request-otp")
def request_otp(data: RequestOTP):
    otp = "".join(random.choices(string.digits, k=6))
    expiry = datetime.utcnow() + timedelta(minutes=2)

    otp_storage[data.email] = {"otp": otp, "expiry": expiry}
    send_otp_email(data.email, otp)

    return {"message": "OTP sent successfully. Please check your email."}

# --------------------
# STEP 6: Verify OTP API
# --------------------
@app.post("/auth/verify-otp")
def verify_otp(data: VerifyOTP):
    if data.email not in otp_storage:
        raise HTTPException(status_code=400, detail="No OTP requested for this email")

    stored_otp = otp_storage[data.email]["otp"]
    expiry = otp_storage[data.email]["expiry"]

    if datetime.utcnow() > expiry:
        raise HTTPException(status_code=400, detail="OTP expired")

    if data.otp != stored_otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # ✅ OTP success → you can create session/JWT here
    del otp_storage[data.email]  # remove used OTP
    return {"message": "Login successful ✅"}


