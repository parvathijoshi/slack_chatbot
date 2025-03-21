# Slackbot with OAuth and Token Management

This project demonstrates how to build a simple Slack bot using Flask and the Slack SDK that can handle OAuth authentication, store access tokens, and refresh them as needed.

## Features

- **Slack OAuth Integration**: Allows users to install the Slack app via OAuth.
- **Token Storage**: Saves access and refresh tokens securely in a JSON file.
- **Token Refresh**: Automatically refreshes tokens when they expire.
- **Slack Command Handling**: Responds to a test Slack command and sends a message to the user.

## Prerequisites

- Python 3.7 or later
- A Slack workspace where you can create and install a custom app
- A `.env` file with your Slack app credentials (Client ID, Client Secret)
- Git

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/slackbot-oauth.git
cd slackbot-oauth
```