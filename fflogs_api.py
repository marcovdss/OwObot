import aiohttp
from config import FFLOGS_CLIENT_ID, FFLOGS_CLIENT_SECRET

fflogs_token = None

async def get_fflogs_token():
    global fflogs_token
    url = "https://www.fflogs.com/oauth/token"
    data = {"grant_type": "client_credentials"}
    auth = aiohttp.BasicAuth(FFLOGS_CLIENT_ID, FFLOGS_CLIENT_SECRET)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, auth=auth) as resp:
            if resp.status != 200:
                print(f"Erro ao obter token FF Logs: {resp.status}")
                return None
            data = await resp.json()
            fflogs_token = data.get("access_token")
            return fflogs_token

async def run_query(query, variables):
    global fflogs_token
    if fflogs_token is None:
        await get_fflogs_token()
    url = "https://www.fflogs.com/api/v2/client"
    headers = {
        "Authorization": f"Bearer {fflogs_token}",
        "Content-Type": "application/json"
    }
    json_body = {
        "query": query,
        "variables": variables
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_body, headers=headers) as resp:
            if resp.status != 200:
                print(f"Erro na requisição GraphQL: {resp.status}")
                return None
            return await resp.json()
