from fastapi import FastAPI
from pydantic import BaseModel
import os

from discord_webhook import DiscordWebhook, DiscordEmbed

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
app = FastAPI()

class Alert(BaseModel):
    annotations: dict
    labels: dict

class Alerts(BaseModel):
    alerts: list[Alert]

def get_embed_playload(severity: str, alertname: str, description: str) -> DiscordEmbed:
    return DiscordEmbed(
        title=f'[{severity.upper()}] - {alertname}',
        description=description,
        color='ff0000'
    )

def send_discord_webhook(severity: str, alertname: str, description: str) -> None:
    embed = get_embed_playload(severity, alertname, description)
    webhook.add_embed(embed)
    response = webhook.execute()
    return response

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.post('/alerts')
def send_discord_webhook_post(alerts: Alerts):
    for alert in alerts.alerts:
        severity = alert.labels['severity']
        alertname = alert.labels['alertname']
        description = alert.annotations['description']
        send_discord_webhook(severity, alertname, description)
    return alerts