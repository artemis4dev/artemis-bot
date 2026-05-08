import requests

TOKEN = "SEU_TOKEN"

url = f"https://api.telegram.org/bot{8645674167:AAH9NCm_MHzHhSYSzivgSgmnXcU8vEYNGVU}/getUpdates"

r = requests.get(url)

print(r.json())