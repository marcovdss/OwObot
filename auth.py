import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_fflogs_token():
    url = "https://www.fflogs.com/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("FFLOGS_CLIENT_ID"),
        "client_secret": os.getenv("FFLOGS_CLIENT_SECRET")
    }
    resp = requests.post(url, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

if __name__ == "__main__":
    token = get_fflogs_token()
    print("Access token obtido:", token)
