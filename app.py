import json
import random
import smtplib
import os
from flask import Flask, request, jsonify, session
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS  # ✅ Import CORS

# Flask app
app = Flask(__name__)
app.secret_key = "super-secret-key"

# Enable CORS for frontend (React)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

# SMTP Config (from environment variables or hardcoded)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "rohitingleai@gmail.com"
SMTP_PASSWORD = "eddn urlf slpv xntu"

# OTP store (in-memory)
otp_store = {}

DATA_FILE = "data/auth.json"

# Load users from JSON
def load_users():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save users to JSON
def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

# Send OTP email
def send_otp_email(to_email, otp):
    try:
        msg = MIMEMultipart()
        msg["From"] = SMTP_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Your OTP for Login"

        body = f"Your One-Time Password (OTP) is: {otp}\n\nThis will expire in 5 minutes."
        msg.attach(MIMEText(body, "plain"))

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

# Step 2: Verify OTP
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

# Role-based dashboard
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

# Admin-only: Add new user
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

    # Check if email already exists
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
