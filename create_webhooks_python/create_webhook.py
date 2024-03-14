# Import your dependencies
from nylas import Client
from dotenv import load_dotenv
import os
from nylas.models.webhooks import CreateWebhookRequest
from nylas.models.webhooks import WebhookTriggers

# Load your env variables
load_dotenv()

# Initialize Nylas client
nylas = Client(
    api_key = os.environ.get("NYLAS_API_KEY"),
    api_uri = os.environ.get("NYLAS_API_URI")
)

# Define the webhook properties
request_body = CreateWebhookRequest(trigger_types = [WebhookTriggers.MESSAGE_CREATED], 
# In the format https://YOURSERVER.COM/webhook
webhook_url = os.environ.get("WEBHOOK_URL"), 
description = "my webhook", notification_email_addresses = [os.environ.get("GRANT_ID")])

# Create the webhook
webhook, _ = nylas.webhooks.create(request_body = request_body)

# Print the newly created webhook
print(webhook)
