from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.company.auth.otp_service import generate_otp, verify_otp
from app.company.auth.user_store import get_user_by_email
from app.company.auth.security.jwt_handler import create_jwt, decode_jwt, blacklist_token

router = APIRouter()
security = HTTPBearer()

# Step 1: Request OTP
@router.post("/request-otp")
def request_otp(email: str):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        generate_otp(email)
        return {"message": f"OTP sent to {email}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # ✅ return real error


# Step 2: Verify OTP & issue JWT
@router.post("/verify-otp")
def verify_otp_login(email: str, otp: str):
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if verify_otp(email, otp):
        token = create_jwt({"email": email, "role": user["role"]})
        return {"message": "Login successful", "token": token, "user": user}
    raise HTTPException(status_code=401, detail="Invalid OTP")

# Step 3: Logout API
@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    blacklist_token(token)
    return {"message": "Logout successful"}

# Protected Route
@router.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"message": "You are authorized", "role": payload["role"]}
