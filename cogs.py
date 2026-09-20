import discord
from discord.ext import commands

from config import BOT_NAME
from database import get_user_vps
from vps_manager import vps_manager


class VPSCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="myvps")
    async def myvps(self, ctx):
        """Show VPS owned by the current Discord user."""
        vps_list = get_user_vps(ctx.author.id)

        if not vps_list:
            await ctx.send("📦 You don't have any VPS yet.")
            return

        embed = discord.Embed(
            title=f"☁️ {BOT_NAME}",
            description="Your VPS list",
            color=discord.Color.blue(),
        )

        for vps in vps_list:
            embed.add_field(
                name=f"🖥️ {vps.get('id', 'Unknown')}",
                value=(
                    f"Status: `{vps.get('status', 'unknown')}`\n"
                    f"RAM: `{vps.get('ram', '-')}`\n"
                    f"CPU: `{vps.get('cpu', '-')}`\n"
                    f"Disk: `{vps.get('disk', '-')}`\n"
                    f"OS: `{vps.get('os', '-')}`"
                ),
                inline=False,
            )

        await ctx.send(embed=embed)

    @commands.command(name="vpsstatus")
    async def vpsstatus(self, ctx, vps_id: str):
        """Show the current status of a VPS."""
        vps = vps_manager.get(vps_id)

        if not vps:
            await ctx.send("❌ VPS not found.")
            return

        if str(vps.get("owner_id")) != str(ctx.author.id):
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("❌ You don't have permission to view this VPS.")
                return

        embed = discord.Embed(
            title=f"🖥️ VPS Status — {vps_id}",
            color=discord.Color.green(),
        )

        embed.add_field(
            name="Status",
            value=f"`{vps.get('status', 'unknown')}`",
            inline=True,
        )

        embed.add_field(
            name="RAM",
            value=f"`{vps.get('ram', '-')}`",
            inline=True,
        )

        embed.add_field(
            name="CPU",
            value=f"`{vps.get('cpu', '-')}`",
            inline=True,
        )

        embed.add_field(
            name="Disk",
            value=f"`{vps.get('disk', '-')}`",
            inline=True,
        )

        embed.add_field(
            name="OS",
            value=f"`{vps.get('os', '-')}`",
            inline=True,
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(VPSCommands(bot))
