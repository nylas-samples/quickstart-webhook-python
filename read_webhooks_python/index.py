# Import packages
from flask import Flask, request, render_template
import hmac
import hashlib
import os
from dataclasses import dataclass
import pendulum

# Array to hold webhook dataclass
webhooks = []

# Webhook dataclass
@dataclass
class Webhook:
    _id: str
    date: str
    subject: str
    from_email: str
    from_name: str

# Get today’s date
today = pendulum.now()

# Create the Flask app and load the configuration
app = Flask(__name__)

# To read and insert webhook data
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # We are connected to Nylas, let’s give back the challenge
    if request.method == "GET" and "challenge" in request.args:
        print(" * Nylas connected to the webhook!")
        return request.args["challenge"]

    if request.method == "POST":
        is_genuine = verify_signature(
            message=request.data,
            key=os.environ["CLIENT_SECRET"].encode("utf8"),
            signature=request.headers.get("X-Nylas-Signature"),
        )

        if not is_genuine:
            return "Signature verification failed!", 401
        data = request.get_json()

        hook = Webhook(
            data["data"]["object"]["id"],
            pendulum.from_timestamp(
            data["data"]["object"]["date"], today.timezone.name
            ).strftime("%d/%m/%Y %H:%M:%S"),
            data["data"]["object"]["subject"],
            data["data"]["object"]["from"][0]["email"],
            data["data"]["object"]["from"][0]["name"],
        )
        webhooks.append(hook)
        return "Webhook received", 200

# Main page
@app.route("/")
def index():
    return render_template("main.html", webhooks=webhooks)

# Signature verification
def verify_signature(message, key, signature):
    digest = hmac.new(key, msg=message, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)

# Run our application
if __name__ == "__main__":
    app.run()
