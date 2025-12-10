import requests
import json

TELEGRAM_TOKEN = "8119131809:AAHBSSxxQ3ldLzow6afTv1SLneSKfdmeaNY"

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
response = requests.get(url)

print("=" * 60)
print("TELEGRAM WEBHOOK INFO")
print("=" * 60)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
