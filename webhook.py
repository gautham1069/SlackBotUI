import requests
import json
web_hook_url = 'https://hooks.slack.com/services/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'

slack_msg = {'text': 'Message from slack webhook using python.'}

requests.post(web_hook_url, data=json.dumps(slack_msg))