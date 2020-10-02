import json

import requests
import settings
import simplejson
from flask import Flask
from flask import request


def send_message(json: str) -> None:
    answer = requests.post(
        settings.DISCORD_WEBHOOK_URL,
        data=json,
        headers={"Content-Type": "application/json"},
    )


def generate_base_embed(
    avatar_url: str, username: str, color: str, title: str, url: str
):
    embed = {
        "avatar_url": avatar_url,
        "username": username,
        "embeds": [{"title": title, "url": url, "color": color, "footer": {}}],
    }
    return embed


def send_issue(avatar_url: str, username: str, title: str, url: str) -> None:
    embed = generate_base_embed(
        avatar_url, username, settings.ISSUE_MESSAGE_COLOR, title, url
    )
    embed["embeds"][0]["footer"]["text"] = "New Issue!"
    send_message(json.dumps(embed))


def send_pr(avatar_url: str, username: str, title: str, url: str) -> None:
    embed = generate_base_embed(
        avatar_url, username, settings.PR_MESSAGE_COLOR, title, url
    )
    embed["embeds"][0]["footer"]["text"] = "New Pull Request!"
    send_message(json.dumps(embed))


app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def parser():
    envelope = simplejson.loads(request.data)

    type = request.headers["X-GitHub-Event"]

    action = envelope["action"]
    if action == "opened":
        if type == "issues":
            send_issue(
                envelope["sender"]["avatar_url"],
                envelope["sender"]["login"],
                envelope["issue"]["title"],
                envelope["issue"]["url"],
            )
        elif type == "pull_request":
            send_pr(
                envelope["sender"]["avatar_url"],
                envelope["sender"]["login"],
                envelope["pull_request"]["title"],
                envelope["pull_request"]["url"],
            )

    return "OK"


app.run(host="0.0.0.0", port="5000")
