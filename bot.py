import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")
PREFIX = "$"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("NetCloud VPS Manager is online.")


@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="☁️ NetCloud VPS Manager",
        description="VPS management bot",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Basic",
        value="`$ping`\n`$help`\n`$myvps`",
        inline=False
    )

    await ctx.send(embed=embed)


if not TOKEN:
    raise RuntimeError("TOKEN environment variable is missing.")

bot.run(TOKEN)
