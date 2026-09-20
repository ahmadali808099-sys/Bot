import asyncio
import discord
from discord.ext import commands

from config import TOKEN, PREFIX, BOT_NAME
from cogs import VPSCommands


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class NetCloudBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        await self.add_cog(VPSCommands(self))

    async def on_ready(self):
        print("=" * 40)
        print(f"{BOT_NAME} is online")
        print(f"Logged in as: {self.user}")
        print("=" * 40)


bot = NetCloudBot()


@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="☁️ NetCloud VPS Manager",
        description="VPS management commands",
        color=discord.Color.blue(),
    )

    embed.add_field(
        name="📦 VPS",
        value=(
            f"`{PREFIX}myvps`\n"
            f"`{PREFIX}vpsstatus <VPS_ID>`"
        ),
        inline=False,
    )

    embed.add_field(
        name="🔧 Basic",
        value=f"`{PREFIX}ping`",
        inline=False,
    )

    await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! `{latency}ms`")


async def main():
    if not TOKEN:
        raise RuntimeError(
            "TOKEN environment variable is missing."
        )

    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
