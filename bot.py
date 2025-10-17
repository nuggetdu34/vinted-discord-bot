import os
import discord
from discord.ext import commands
import requests

TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.command()
async def vinted(ctx, *, search):
    url = f"https://www.vinted.fr/api/v2/catalog/items?search_text={search}"
    r = requests.get(url).json()

    items = r.get("items", [])[:3]  # On prend 3 résultats

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

bot.run(TOKEN)
