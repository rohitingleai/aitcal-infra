import json
import random
import smtplib
from flask import Flask, request, jsonify, session
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "super-secret-key"

CORS(app, resources={r"/*": {"origins": "http://localhost:5176"}}, supports_credentials=True)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "rohitingleai@gmail.com"
SMTP_PASSWORD = "eddn urlf slpv xntu"
otp_store = {}
DATA_FILE = "data/auth.json"

def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)import json
import random
import smtplib
from flask import Flask, request, jsonify, session
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "super-secret-key"

CORS(app, resources={r"/*": {"origins": "http://localhost:5176"}}, supports_credentials=True)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "rohitingleai@gmail.com"
SMTP_PASSWORD = "eddn urlf slpv xntu"
otp_store = {}
DATA_FILE = "data/auth.json"

def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def send_otp_email(to_email, otp):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Your OTP for AITCAL Login"
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OTP Verification</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f1419; color: #ffffff;">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #0f1419;">
                <tr>
                    <td align="center" style="padding: 40px 20px;">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #1a2332; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">

                            <!-- Header with Logo -->
                            <tr>
                                <td align="center" style="padding: 40px 40px 20px 40px; background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%); border-radius: 12px 12px 0 0;">
                                    <img src="https://aitcal.com/assets/aitcallogo-DbITu7l4.png" alt="AITCAL Logo" style="max-width: 180px; height: auto; margin-bottom: 20px;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; text-align: center;">Security Verification</h1>
                                </td>
                            </tr>

                            <!-- Main Content -->
                            <tr>
                                <td style="padding: 40px;">
                                    <div style="text-align: center; margin-bottom: 30px;">
                                        <h2 style="margin: 0 0 20px 0; color: #ffffff; font-size: 24px; font-weight: 500;">Your One-Time Password</h2>
                                        <p style="margin: 0 0 30px 0; color: #cbd5e1; font-size: 16px; line-height: 1.6;">
                                            We've generated a secure OTP for your AITCAL account login. Please use the code below to complete your authentication.
                                        </p>
                                    </div>

                                    <!-- OTP Display -->
                                    <div style="background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%); border-radius: 8px; padding: 30px; margin: 30px 0; text-align: center; border: 2px solid #3b82f6;">
                                        <div style="font-size: 36px; font-weight: 700; color: #ffffff; letter-spacing: 8px; margin-bottom: 10px; font-family: 'Courier New', monospace;">
                                            {otp}
                                        </div>
                                        <p style="margin: 0; color: #e2e8f0; font-size: 14px; font-weight: 500;">
                                            One-Time Password
                                        </p>
                                    </div>

                                    <!-- Important Information -->
                                    <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin: 30px 0; border-left: 4px solid #ef4444;">
                                        <h3 style="margin: 0 0 15px 0; color: #ef4444; font-size: 18px; font-weight: 600;">⚠️ Important Security Information</h3>
                                        <ul style="margin: 0; padding-left: 20px; color: #cbd5e1; line-height: 1.6;">
                                            <li style="margin-bottom: 8px;">This OTP will expire in <strong style="color: #ffffff;">5 minutes</strong></li>
                                            <li style="margin-bottom: 8px;">Never share this code with anyone</li>
                                            <li style="margin-bottom: 8px;">AITCAL staff will never ask for your OTP</li>
                                            <li>If you didn't request this, please contact our security team immediately</li>
                                        </ul>
                                    </div>

                                    <!-- Call to Action -->
                                    <div style="text-align: center; margin: 30px 0;">
                                        <p style="margin: 0 0 20px 0; color: #cbd5e1; font-size: 16px;">
                                            Return to your login page and enter the code above to continue.
                                        </p>
                                        <a href="#" style="display: inline-block; background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%); color: #ffffff; text-decoration: none; padding: 12px 30px; border-radius: 6px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);">
                                            Continue to Login
                                        </a>
                                    </div>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="padding: 30px 40px; background-color: #0f172a; border-radius: 0 0 12px 12px; text-align: center;">
                                    <div style="border-top: 1px solid #334155; padding-top: 20px;">
                                        <p style="margin: 0 0 15px 0; color: #64748b; font-size: 14px;">
                                            This email was sent by <strong style="color: #3b82f6;">AITCAL</strong> Security System
                                        </p>
                                        <p style="margin: 0; color: #475569; font-size: 12px; line-height: 1.5;">
                                            If you have any questions or concerns about your account security,<br>
                                            please contact our support team at <a href="mailto:security@aitcal.com" style="color: #3b82f6; text-decoration: none;">security@aitcal.com</a>
                                        </p>
                                    </div>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        text_content = f"""
        AITCAL - Security Verification

        Your One-Time Password (OTP) is: {otp}

        IMPORTANT SECURITY INFORMATION:
        • This OTP will expire in 5 minutes
        • Never share this code with anyone
        • AITCAL staff will never ask for your OTP
        • If you didn't request this, please contact our security team immediately

        Return to your login page and enter the code above to continue.

        This email was sent by AITCAL Security System.
        For support, contact: security@aitcal.com
        """
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

# Step 1: Request OTP
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    users = load_users()
    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp

    if send_otp_email(email, otp):
        return jsonify({"message": "OTP sent to your email"}), 200
    else:
        return jsonify({"error": "Failed to send OTP"}), 500

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    if otp_store.get(email) == otp:
        users = load_users()
        user = next((u for u in users if u["email"] == email), None)
        if user:
            session["user"] = user  # store session
            otp_store.pop(email, None)  # remove OTP
            return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"error": "Invalid OTP"}), 400

@app.route("/dashboard", methods=["GET"])
def dashboard():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    role = user["role"]
    if role == "admin":
        return jsonify({"message": f"Welcome Admin {user['name']}", "data": "All system data"})
    elif role == "employee":
        return jsonify({"message": f"Welcome Employee {user['name']}", "data": "Employee dashboard"})
    elif role == "client":
        return jsonify({"message": f"Welcome Client {user['name']}", "data": "Client portal"})
    elif role == "vendor":
        return jsonify({"message": f"Welcome Vendor {user['name']}", "data": "Vendor resources"})
    else:
        return jsonify({"error": "Unknown role"}), 403

@app.route("/admin/add-user", methods=["POST"])
def add_user():
    user = session.get("user")
    if not user or user["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    role = data.get("role")
    if not all([name, email, role]):
        return jsonify({"error": "Missing fields"}), 400
    users = load_users()
    if any(u["email"] == email for u in users):
        return jsonify({"error": "User with this email already exists"}), 409
    new_id = max(u["id"] for u in users) + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": name,
        "email": email,
        "role": role
    }
    users.append(new_user
    save_users(users)
    return jsonify({"message": "User added successfully", "user": new_user}), 201

if __name__ == "__main__":
    app.run(debug=True)


def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def send_otp_email(to_email, otp):
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Your OTP for AITCAL Login"
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OTP Verification</title>
        </head>
        <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f1419; color: #ffffff;">
            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #0f1419;">
                <tr>
                    <td align="center" style="padding: 40px 20px;">
                        <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #1a2332; border-radius: 12px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);">

                            <!-- Header with Logo -->
                            <tr>
                                <td align="center" style="padding: 40px 40px 20px 40px; background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #2563eb 100%); border-radius: 12px 12px 0 0;">
                                    <img src="https://aitcal.com/assets/aitcallogo-DbITu7l4.png" alt="AITCAL Logo" style="max-width: 180px; height: auto; margin-bottom: 20px;">
                                    <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; text-align: center;">Security Verification</h1>
                                </td>
                            </tr>

                            <!-- Main Content -->
                            <tr>
                                <td style="padding: 40px;">
                                    <div style="text-align: center; margin-bottom: 30px;">
                                        <h2 style="margin: 0 0 20px 0; color: #ffffff; font-size: 24px; font-weight: 500;">Your One-Time Password</h2>
                                        <p style="margin: 0 0 30px 0; color: #cbd5e1; font-size: 16px; line-height: 1.6;">
                                            We've generated a secure OTP for your AITCAL account login. Please use the code below to complete your authentication.
                                        </p>
                                    </div>

                                    <!-- OTP Display -->
                                    <div style="background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%); border-radius: 8px; padding: 30px; margin: 30px 0; text-align: center; border: 2px solid #3b82f6;">
                                        <div style="font-size: 36px; font-weight: 700; color: #ffffff; letter-spacing: 8px; margin-bottom: 10px; font-family: 'Courier New', monospace;">
                                            {otp}
                                        </div>
                                        <p style="margin: 0; color: #e2e8f0; font-size: 14px; font-weight: 500;">
                                            One-Time Password
                                        </p>
                                    </div>

                                    <!-- Important Information -->
                                    <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin: 30px 0; border-left: 4px solid #ef4444;">
                                        <h3 style="margin: 0 0 15px 0; color: #ef4444; font-size: 18px; font-weight: 600;">⚠️ Important Security Information</h3>
                                        <ul style="margin: 0; padding-left: 20px; color: #cbd5e1; line-height: 1.6;">
                                            <li style="margin-bottom: 8px;">This OTP will expire in <strong style="color: #ffffff;">5 minutes</strong></li>
                                            <li style="margin-bottom: 8px;">Never share this code with anyone</li>
                                            <li style="margin-bottom: 8px;">AITCAL staff will never ask for your OTP</li>
                                            <li>If you didn't request this, please contact our security team immediately</li>
                                        </ul>
                                    </div>

                                    <!-- Call to Action -->
                                    <div style="text-align: center; margin: 30px 0;">
                                        <p style="margin: 0 0 20px 0; color: #cbd5e1; font-size: 16px;">
                                            Return to your login page and enter the code above to continue.
                                        </p>
                                        <a href="#" style="display: inline-block; background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%); color: #ffffff; text-decoration: none; padding: 12px 30px; border-radius: 6px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);">
                                            Continue to Login
                                        </a>
                                    </div>
                                </td>
                            </tr>

                            <!-- Footer -->
                            <tr>
                                <td style="padding: 30px 40px; background-color: #0f172a; border-radius: 0 0 12px 12px; text-align: center;">
                                    <div style="border-top: 1px solid #334155; padding-top: 20px;">
                                        <p style="margin: 0 0 15px 0; color: #64748b; font-size: 14px;">
                                            This email was sent by <strong style="color: #3b82f6;">AITCAL</strong> Security System
                                        </p>
                                        <p style="margin: 0; color: #475569; font-size: 12px; line-height: 1.5;">
                                            If you have any questions or concerns about your account security,<br>
                                            please contact our support team at <a href="mailto:security@aitcal.com" style="color: #3b82f6; text-decoration: none;">security@aitcal.com</a>
                                        </p>
                                    </div>
                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        text_content = f"""
        AITCAL - Security Verification

        Your One-Time Password (OTP) is: {otp}

        IMPORTANT SECURITY INFORMATION:
        • This OTP will expire in 5 minutes
        • Never share this code with anyone
        • AITCAL staff will never ask for your OTP
        • If you didn't request this, please contact our security team immediately

        Return to your login page and enter the code above to continue.

        This email was sent by AITCAL Security System.
        For support, contact: security@aitcal.com
        """
        part1 = MIMEText(text_content, "plain")
        part2 = MIMEText(html_content, "html")
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

# Step 1: Request OTP
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    users = load_users()
    user = next((u for u in users if u["email"] == email), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp

    if send_otp_email(email, otp):
        return jsonify({"message": "OTP sent to your email"}), 200
    else:
        return jsonify({"error": "Failed to send OTP"}), 500

@app.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    if otp_store.get(email) == otp:
        users = load_users()
        user = next((u for u in users if u["email"] == email), None)
        if user:
            session["user"] = user  # store session
            otp_store.pop(email, None)  # remove OTP
            return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"error": "Invalid OTP"}), 400

@app.route("/dashboard", methods=["GET"])
def dashboard():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    role = user["role"]
    if role == "admin":
        return jsonify({"message": f"Welcome Admin {user['name']}", "data": "All system data"})
    elif role == "employee":
        return jsonify({"message": f"Welcome Employee {user['name']}", "data": "Employee dashboard"})
    elif role == "client":
        return jsonify({"message": f"Welcome Client {user['name']}", "data": "Client portal"})
    elif role == "vendor":
        return jsonify({"message": f"Welcome Vendor {user['name']}", "data": "Vendor resources"})
    else:
        return jsonify({"error": "Unknown role"}), 403

@app.route("/admin/add-user", methods=["POST"])
def add_user():
    user = session.get("user")
    if not user or user["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    role = data.get("role")
    if not all([name, email, role]):
        return jsonify({"error": "Missing fields"}), 400
    users = load_users()
    if any(u["email"] == email for u in users):
        return jsonify({"error": "User with this email already exists"}), 409
    new_id = max(u["id"] for u in users) + 1 if users else 1
    new_user = {
        "id": new_id,
        "name": name,
        "email": email,
        "role": role
    }
    users.append(new_user)
    save_users(users)
    return jsonify({"message": "User added successfully", "user": new_user}), 201

if __name__ == "__main__":
    app.run(debug=True)
