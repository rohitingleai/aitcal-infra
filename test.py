import httpx

url = "http://127.0.0.1:8000/auth/request-otp"
params = {"email": "rohitingle34@gmail.com"}

resp = httpx.post(url, params=params)

print("Status code:", resp.status_code)
print("Headers:", resp.headers)
print("Raw text:", resp.text)
