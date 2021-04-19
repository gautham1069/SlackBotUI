from flask import Flask, request
app = Flask(__name__)
import os
import slack
# Grab client ID from your environment variables
client_id = os.environ["SLACK_CLIENT_ID"]
# Generate random string to use as state to prevent CSRF attacks
from uuid import uuid4
state = str(uuid4())
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

@app.route("/")
def index():
    return "Welcome to home page!"

# Route to kick off Oauth flow
@app.route("/begin_auth", methods=["GET"])
def pre_install():
    return f'<a href="https://slack.com/oauth/v2/authorize?scope=channels:read,groups:read,channels:manage,chat:write&client_id={ client_id }&state={ state }"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'


# Grab client Secret from your environment variables
client_secret = os.environ["SLACK_CLIENT_SECRET"]

# Route for Oauth flow to redirect to after user accepts scopes
@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    # Retrieve the auth code and state from the request params
    auth_code = request.args['code']
    received_state = request.args['state']

    # An empty string is a valid token for this request
    client = slack.WebClient()

    # verify state received in params matches state we originally sent in auth request
    if received_state == state:
        # Request the auth tokens from Slack
        response = client.oauth_v2_access(
            client_id=client_id,
            client_secret=client_secret,
            code=auth_code
        )
        print("Success")
    else:
        return "Invalid State"

    print(response)
    team = response['team']
    teamname = team['name']
    access_token = response['access_token']
    print(access_token)
    # Save the bot token to an environmental variable or to your data store
    # with open(".env", "a") as f:
    #     f.write("\n")
    #     f.write(team['name']+"="+access_token)
    #     f.write("\n")

    return "Bot is added to your workspace, please add to the channel as well. Team name: " + teamname + " and token: " + access_token

    # Don't forget to let the user know that auth has succeeded!
    # return "Auth complete!"