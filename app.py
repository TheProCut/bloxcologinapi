import os
import time
import requests
from flask import Flask, redirect, request, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = "https://zer.theprocut.repl.co/callback"
DISCORD_API_URL = "https://discord.com/api"

@app.route("/")
def home():
    time.sleep(5)
    if "discord_token" in session:
        discord_user = get_discord_user()
        user_id = discord_user["id"]
        return redirect(f"https://bloxco.org/auth/auth.html?parameter={user_id}")
    else:
        return redirect(f"{DISCORD_API_URL}/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(f"{DISCORD_API_URL}/oauth2/token", data=data, headers=headers)
    token_data = response.json()
    session["discord_token"] = token_data["access_token"]
    return redirect("/")

def get_discord_user():
    headers = {
        "Authorization": f"Bearer {session['discord_token']}"
    }

    response = requests.get(f"{DISCORD_API_URL}/users/@me", headers=headers)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
