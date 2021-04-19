import slack
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

with open(".env", "a") as f:
        f.write("username=John")
        f.write("\n")
        f.write("email=abc@gmail.com")

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
client.chat_postMessage(channel='#bug-bot', text='Hi Gautham Vootukuru')

client = slack.WebClient(token=os.environ['ANOTHER_SLACK_TOKEN'])
client.chat_postMessage(channel='#test-channel', text='Hi Gautham Vootukuru')
