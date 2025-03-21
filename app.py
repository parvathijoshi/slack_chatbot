import os
import time
import json
import logging
import threading
from flask import Flask, request, redirect, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import ssl

# Load environment variables
load_dotenv()

app = Flask(__name__)

TOKEN_FILE = "slack_tokens.json"
logging.basicConfig(level=logging.INFO)

def load_tokens():
    """Load tokens from the JSON file."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    return {"teams": {}}

def save_tokens(tokens, team_id):
    """Save tokens to the JSON file."""
    all_tokens = load_tokens()
    if "teams" not in all_tokens:
        all_tokens["teams"] = {}
    all_tokens["teams"][team_id] = tokens
    with open(TOKEN_FILE, "w") as file:
        json.dump(all_tokens, file, indent=4)

def refresh_tokens(team_id):
    """Refresh Slack access token when expired."""
    tokens = load_tokens()
    team_tokens = tokens.get("teams", {}).get(team_id, {})

    refresh_token = team_tokens.get("refresh_token")
    if not refresh_token:
        logging.error(f"No refresh token found for team {team_id}!")
        return None

    try:
        # Create an SSL context that does not verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        client = WebClient(ssl=ssl_context)
        response = client.oauth_v2_access(
            client_id=os.getenv("SLACK_CLIENT_ID"),
            client_secret=os.getenv("SLACK_CLIENT_SECRET"),
            grant_type="refresh_token",
            refresh_token=refresh_token,
        )

        if response.get("ok"):
            team_tokens["access_token"] = response["access_token"]
            team_tokens["refresh_token"] = response["refresh_token"]
            team_tokens["expires_at"] = time.time() + 43200  # 12 hours
            save_tokens(team_tokens, team_id)
            logging.info(f"🔄 Token refreshed successfully for team {team_id}!")
            return team_tokens["access_token"]
        else:
            logging.error(f"Token refresh failed for team {team_id}: {response['error']}")
            return None
    except SlackApiError as e:
        logging.error(f"Slack API error during refresh for team {team_id}: {e}")
        return None

def get_valid_token(team_id):
    """Get a valid token, refreshing if expired."""
    tokens = load_tokens()
    team_tokens = tokens.get("teams", {}).get(team_id, {})

    if team_tokens.get("expires_at", 0) < time.time():
        return refresh_tokens(team_id)
    
    return team_tokens.get("access_token")

# Start token refresh loop in the background
def token_refresh_loop():
    while True:
        time.sleep(3600)  # Check every hour
        tokens = load_tokens().get("teams", {})
        for team_id in tokens.keys():
            get_valid_token(team_id)  # This will refresh if needed

threading.Thread(target=token_refresh_loop, daemon=True).start()

@app.route("/slack/install")
def install():
    """Redirect user to Slack authorization page."""
    client_id = os.getenv("SLACK_CLIENT_ID")
    return redirect(f"https://slack.com/oauth/v2/authorize?client_id={client_id}&scope=commands,chat:write")

@app.route("/slack/oauth_redirect")
def oauth_redirect():
    """Handle Slack OAuth callback."""
    code = request.args.get("code")
    if not code:
        return "Missing authorization code", 400

    try:
        # Create an SSL context that does not verify certificates
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        client = WebClient(ssl=ssl_context)
        response = client.oauth_v2_access(
            client_id=os.getenv("SLACK_CLIENT_ID"),
            client_secret=os.getenv("SLACK_CLIENT_SECRET"),
            code=code
        )

        if response.get("ok"):
            team_id = response["team"]["id"]
            save_tokens({
                "access_token": response["access_token"],
                "refresh_token": response["refresh_token"],
                "expires_at": time.time() + 43200  # 12 hours
            }, team_id)

            return "Slack app installed successfully!"
        else:
            return f"OAuth failed: {response['error']}", 400
    except SlackApiError as e:
        logging.error(f"Slack OAuth error: {e}")
        return "OAuth process failed", 500

@app.route("/slack/command", methods=["POST"])
def slack_command():
    """Handle a test Slack command."""
    team_id = request.form.get("team_id")
    user_id = request.form.get("user_id")
    
    token = get_valid_token(team_id)
    if not token:
        return jsonify({"error": "Invalid or expired token"}), 401

    client = WebClient(token=token)
    try:
        client.chat_postMessage(
            channel=user_id,
            text="Hello from your Slack bot!"
        )
        return jsonify({"response_type": "in_channel", "text": "Message sent!"})
    except SlackApiError as e:
        logging.error(f"Slack API error: {e}")
        return jsonify({"error": "Failed to send message"}), 500

if __name__ == "__main__":
    app.run(port=3000)
