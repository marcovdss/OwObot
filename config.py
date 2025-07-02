import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
FFLOGS_CLIENT_ID = os.getenv("FFLOGS_CLIENT_ID")
FFLOGS_CLIENT_SECRET = os.getenv("FFLOGS_CLIENT_SECRET")
USER_DATA_FILE = "user_characters.json"
