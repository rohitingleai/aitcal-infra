import random, time, json
from pathlib import Path
from app.company.auth.email_service import send_email

OTP_FILE = Path("data/otps.json")

def generate_otp(email: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_data = {"email": email, "otp": otp, "timestamp": time.time()}

    if OTP_FILE.exists():
        with open(OTP_FILE, "r") as f:
            otps = json.load(f)
    else:
        otps = []

    otps = [o for o in otps if o["email"] != email]  # remove old OTP
    otps.append(otp_data)

    with open(OTP_FILE, "w") as f:
        json.dump(otps, f, indent=2)

    subject = "Your Login OTP - AITCAL Infra"
    body = f"Hello,\n\nYour OTP is: {otp}\nIt will expire in 5 minutes.\n\n- AITCAL Infra Team"
    send_email(email, subject, body)

    return otp

def verify_otp(email: str, otp: str) -> bool:
    if not OTP_FILE.exists():
        return False

    with open(OTP_FILE, "r") as f:
        otps = json.load(f)

    for o in otps:
        if o["email"] == email and o["otp"] == otp:
            if time.time() - o["timestamp"] <= 300:  # 5 min expiry
                return True
    return False
