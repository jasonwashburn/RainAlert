import requests
from twilio.rest import Client
import os

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
OWM_API_KEY = os.environ.get("OWM_API_KEY")
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_KEY = os.getenv("TWILIO_KEY")
FROM_NUMBER = os.getenv("FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

account_sid = TWILIO_SID
auth_token = TWILIO_KEY

parameters = {"lat": 42.563179,
              "lon": -114.460281,
              "appid": OWM_API_KEY,
              "exclude": 'minutely,daily,currently'}

response = requests.get(OWM_ENDPOINT, params=parameters)

response.raise_for_status()

hourly_data = response.json()['hourly']

rain_hours = [{hour['dt']: hour['weather'][0]['id']} for hour in hourly_data[:12] if hour['weather'][0]['id'] < 700]
if rain_hours:
    print("Bring an Umbrella")
    account_sid = TWILIO_SID
    auth_token = TWILIO_KEY
    client = Client(account_sid, auth_token)
    message = client.messages.create(body="🌧 Bring an Umbrella️ 🌧", from_=FROM_NUMBER, to=TO_NUMBER)

    print(message.status)
