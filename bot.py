import discord
from config import DISCORD_TOKEN
from fflogs_api import get_fflogs_token
from commands import bot  # Importa o bot com os comandos prontos

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    token = await get_fflogs_token()
    if token:
        print("Token FF Logs obtido com sucesso!")
    else:
        print("Erro ao obter token FF Logs.")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
