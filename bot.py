import os
import discord
from discord.ext import commands
import requests

# Récupération du token depuis les variables d'environnement
TOKEN = os.getenv("DISCORD_TOKEN")

# Activer les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True  # indispensable pour lire les messages

# Créer le bot avec le préfixe "!"
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def vinted(ctx, *, search):
    url = f"https://www.vinted.fr/api/v2/catalog/items?search_text={search}"
    r = requests.get(url).json()

    # On prend les 3 premiers résultats
    items = r.get("items", [])[:3]

    if not items:
        await ctx.send("❌ Aucun résultat trouvé.")
        return

    for item in items:
        embed = discord.Embed(
            title=item["title"],
            url=f"https://www.vinted.fr{item['url']}",
            description=f"💶 {item['price']} € | 👕 Taille: {item['size_title']} | 🏷️ {item['brand_title']}"
        )
        embed.set_image(url=item["photo"]["url"])
        await ctx.send(embed=embed)

# Lancer le bot
bot.run(TOKEN)
