import os
import json
import discord
from discord.ext import commands
from data_manager import load_user_data, save_user_data
from fflogs_api import run_query

from utils import format_duration, clean_character_name

intents = discord.Intents.default()
intents.message_content = True  # importante para ler comandos com texto

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.command()
async def vincular(ctx, *, args: str):
    parts = args.split()
    if len(parts) < 2:
        await ctx.send("Use: !vincular <servidor> [região] <Nome_Sobrenome>")
        return
    
    server = parts[0]
    region = "NA"  # padrão
    if len(parts) >= 3:
        if parts[1].upper() in ("NA", "EU", "JP", "OC", "KR"):
            region = parts[1].upper()
            character_name = " ".join(parts[2:])
        else:
            character_name = " ".join(parts[1:])
    else:
        character_name = " ".join(parts[1:])

    # Caminho do arquivo
    file_path = "user_characters.json"

    # Lê os dados atuais (ou cria um novo dicionário)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            user_data = json.load(f)
    else:
        user_data = {}

    # Atualiza os dados do usuário
    user_data[str(ctx.author.id)] = {
        "server": server,
        "region": region,
        "name": character_name
    }

    # Salva no arquivo
    with open(file_path, "w") as f:
        json.dump(user_data, f, indent=2)

    await ctx.send(f"✅ Personagem vinculado: {character_name} ({server}, {region})")

@bot.command()
async def perfil(ctx, member: discord.Member = None, server: str = None, region: str = "NA", *, name: str = None):
    user_id = str(member.id) if member else str(ctx.author.id)
    
    if not server or not name:
        user_data = load_user_data()
        if user_id not in user_data:
            await ctx.send(f"{member.mention if member else 'Você'} ainda não vinculou um personagem. Use `!vincular servidor região Nome_Do_Personagem`.")
            return
        saved_data = user_data[user_id]
        server = server or saved_data["server"]
        region = region or saved_data["region"]
        name = name or saved_data["name"]
        name = clean_character_name(name)
    
    query = """
    query($name: String!, $server: String!, $region: String!) {
      characterData {
        character(name: $name, serverSlug: $server, serverRegion: $region) {
          id
          name
          server { name }
          zoneRankings
        }
      }
    }
    """
    variables = {
        "name": name,
        "server": server.lower(),
        "region": region.upper()
    }

    try:
        result = await run_query(query, variables)
        if not result or "data" not in result or not result["data"]:
            await ctx.send(f"Resposta inválida da API FF Logs: {result}")
            return

        char = result["data"]["characterData"]["character"]
        if char:
            char_id = char.get("id")
            name = char["name"]
            server_name = char["server"]["name"]
            zone_rankings = char["zoneRankings"]
            if isinstance(zone_rankings, str):
                import json
                zone_rankings = json.loads(zone_rankings)

            best_avg = zone_rankings.get("bestPerformanceAverage", None)
            median_avg = zone_rankings.get("medianPerformanceAverage", None)
            all_stars = zone_rankings.get("allStars", [])
            all_star_rank = all_stars[0]["rank"] if all_stars else "N/A"

            best_avg_str = f"{best_avg:.2f}" if isinstance(best_avg, (int, float)) else "N/A"
            median_avg_str = f"{median_avg:.2f}" if isinstance(median_avg, (int, float)) else "N/A"

            profile_url = f"https://www.fflogs.com/character/id/{char_id}" if char_id else "N/A"

            await ctx.send(
                f"**{name}** ({server_name})\n"
                f"🔸 Best Avg: {best_avg_str}\n"
                f"🔸 Median Avg: {median_avg_str}\n"
                f"🌟 All-Star Rank: {all_star_rank}\n"
                f"🔗 [Perfil FFLogs]({profile_url})"
            )
        else:
            await ctx.send("Personagem não encontrado.")
    except Exception as e:
        await ctx.send(f"Erro ao buscar dados: {e}")

# O comando recente pode seguir padrão parecido, com load_user_data, clean_character_name e chamada run_query

@bot.command()
async def recente(ctx, server: str = None, region: str = "NA", *, character_name: str = None):
    user_id = str(ctx.author.id)
    if not server or not character_name:
        user_data = load_user_data()
        if user_id not in user_data:
            await ctx.send("Você ainda não vinculou um personagem. Use `!vincular servidor região Nome_Do_Personagem`.")
            return
        saved_data = user_data[user_id]
        server = server or saved_data.get("server")
        region = region or saved_data.get("region")
        character_name = character_name or saved_data.get("name")  # <-- ajustar para "name"

    character_name = clean_character_name(character_name)

    # resto do código...


    query = """
    query($name: String!, $server: String!, $region: String!) {
      characterData {
        character(name: $name, serverSlug: $server, serverRegion: $region) {
          name
          recentReports(limit: 1) {
            data {
              code
              title
              startTime
              endTime
              fights(killType: All) {
                id
                encounterID
                name
                startTime
                endTime
                kill
                difficulty
              }
            }
          }
        }
      }
    }
    """
    variables = {
        "name": character_name,
        "server": server.lower(),
        "region": region.upper()
    }

    try:
        result = await run_query(query, variables)
        character = result["data"]["characterData"]["character"]
        if not character:
            await ctx.send("Personagem não encontrado.")
            return

        char_name = character["name"]
        reports = character["recentReports"]["data"]
        if not reports:
            await ctx.send("Nenhuma luta recente encontrada.")
            return

        report = reports[0]
        fights = report["fights"]
        if not fights:
            await ctx.send("Nenhuma luta encontrada no relatório mais recente.")
            return

        last_fights = sorted(fights, key=lambda x: x["startTime"], reverse=True)[:3]

        lines = [f"**📝 Últimas 3 lutas de {char_name}:**"]
        for fight in last_fights:
            duration_str = format_duration(fight["endTime"] - fight["startTime"])
            boss_name = fight["name"]
            kill = "✅ Vitória" if fight["kill"] else "❌ Wipe"
            difficulty = {1: "Normal", 101: "Savage", 4: "Ultimate"}.get(fight["difficulty"], "Desconhecida")
            log_link = f"https://www.fflogs.com/reports/{report['code']}#fight={fight['id']}"

            lines.append(
                f"\n🔹 **{boss_name}** ({difficulty})\n"
                f"{kill} – ⏱️ {duration_str}\n"
                f"🔗 [Ver log]({log_link})"
            )

        await ctx.send("\n".join(lines))
    except Exception as e:
        await ctx.send(f"Erro ao buscar lutas: {e}")

@bot.command(name="help")
async def custom_help(ctx):
    help_text = (
        "**📘 Comandos disponíveis:**\n\n"
        "🔹 `!vincular <servidor> [região] <Nome_Sobrenome>`\n"
        "Vincula um personagem à sua conta para consultas futuras.\n"
        "_Exemplo:_ `!vincular lamia NA Jiro Strahelnder`\n\n"

        "🔹 `!perfil [@membro] [servidor] [região] <Nome_Sobrenome>`\n"
        "Busca os dados de FFLogs de um personagem.\n"
        "_Exemplos:_\n"
        "• `!perfil lamia NA Jiro Strahelnder`\n"
        "• `!perfil @membro`\n\n"

        "🔹 `!recente <servidor> [região] <Nome_Sobrennder>`\n"
        "Mostra as últimas 3 lutas recentes de um personagem.\n"
        "_Exemplo:_ `!recente lamia NA Jiro Strahelnder`\n"
    )
    await ctx.send(help_text)

