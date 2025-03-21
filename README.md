Slackbot with OAuth and Token Management
This project demonstrates how to build a simple Slack bot using Flask and the Slack SDK that can handle OAuth authentication, store access tokens, and refresh them as needed.

Features
Slack OAuth Integration: Allows users to install the Slack app via OAuth.
Token Storage: Saves access and refresh tokens securely in a JSON file.
Token Refresh: Automatically refreshes tokens when they expire.
Slack Command Handling: Responds to a test Slack command and sends a message to the user.
Prerequisites
Python 3.7 or later
A Slack workspace where you can create and install a custom app
A .env file with your Slack app credentials (Client ID, Client Secret)
Git
Setup and Installation
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/slackbot-oauth.git
cd slackbot-oauth
2. Set Up a Virtual Environment
For the best environment isolation, it's recommended to use a virtual environment.

bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Install Dependencies
Use pip to install the required Python packages.

bash
Copy
Edit
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root of your project and add the following variables with your own Slack app credentials:

ini
Copy
Edit
SLACK_CLIENT_ID=your-client-id
SLACK_CLIENT_SECRET=your-client-secret
5. Run the App
Once the dependencies are installed and the environment variables are set, you can run the Flask app:

bash
Copy
Edit
python app.py
The app will run on http://localhost:3000.

Visit http://localhost:3000/slack/install to start the Slack OAuth authorization process.
After authorization, the app will store the OAuth tokens in a slack_tokens.json file.
The bot will automatically refresh tokens if they expire.
6. Deploy the App (Optional)
To deploy the app to a cloud service like Heroku, AWS, or any other platform, follow the deployment guide for that platform and push your project.

File Structure
bash
Copy
Edit
.
├── app.py                # Main application file
├── slack_tokens.json      # File where OAuth tokens are saved
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (Slack credentials)
└── README.md              # This file
How the App Works
Install Slack App: The /slack/install route redirects users to Slack's OAuth page.
OAuth Callback: After the user authorizes the app, Slack will redirect back to the /slack/oauth_redirect route where the OAuth tokens are exchanged and stored.
Token Refresh: Tokens are checked for expiration and refreshed automatically in the background.
Send Slack Command: The /slack/command route is available to trigger a message from the bot to a user.
Development
If you're developing and need to make changes to the bot:

Modify the app.py file with new routes or logic.
Update the .env file if you change your Slack credentials.
Push changes to your Git repository using:
bash
Copy
Edit
git add .
git commit -m "Updated functionality"
git push origin main
Troubleshooting
SSL Certificate Errors: If you're running the app locally and encountering SSL verification errors, ensure you have the correct certificates installed on your system. Alternatively, you can temporarily bypass SSL verification (not recommended for production) by modifying the WebClient initialization to disable SSL verification.
