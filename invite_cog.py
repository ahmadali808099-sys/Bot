import discord
from discord.ext import commands

from invite_system import (
    save_plan,
    get_all_plans
)

from invite_ui import PlanView


class InvitePlanModal(
    discord.ui.Modal,
    title="Create Invite Plan"
):

    plan_name = discord.ui.TextInput(
        label="Plan Name",
        placeholder="Example: Starter VPS",
        max_length=50
    )

    required_invites = discord.ui.TextInput(
        label="Required Invites",
        placeholder="Example: 5"
    )

    ram = discord.ui.TextInput(
        label="RAM",
        placeholder="Example: 4G"
    )

    cpu = discord.ui.TextInput(
        label="CPU",
        placeholder="Example: 2"
    )

    disk = discord.ui.TextInput(
        label="Disk",
        placeholder="Example: 30G"
    )

    async def on_submit(self, interaction):
        try:
            required = int(
                self.required_invites.value
            )

            cpu = int(
                self.cpu.value
            )

            if required < 1 or cpu < 1:
                raise ValueError

        except ValueError:
            await interaction.response.send_message(
                "❌ Required Invites and CPU must be valid numbers.",
                ephemeral=True
            )
            return

        plan_id = (
            f"PLAN-{len(get_all_plans()) + 1:04d}"
        )

        await save_plan(
            plan_id=plan_id,
            name=self.plan_name.value,
            required_invites=required,
            ram=self.ram.value,
            cpu=cpu,
            disk=self.disk.value,
            os_name="ubuntu2204"
        )

        await interaction.response.send_message(
            "✅ Invite Plan created!\n\n"
            f"📦 Name: `{self.plan_name.value}`\n"
            f"🆔 ID: `{plan_id}`\n"
            f"📨 Required Invites: `{required}`\n"
            f"🧠 RAM: `{self.ram.value}`\n"
            f"⚙️ CPU: `{cpu}`\n"
            f"💾 Disk: `{self.disk.value}`\n"
            "🐧 Default OS: `Ubuntu 22.04`",
            ephemeral=True
        )


class InviteAdminView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(
        label="Create Invite Plan",
        style=discord.ButtonStyle.green,
        emoji="📨"
    )
    async def create_plan(
        self,
        interaction,
        button
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ Admins only.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(
            InvitePlanModal()
        )

    @discord.ui.button(
        label="Invite Plans",
        style=discord.ButtonStyle.blurple,
        emoji="📋"
    )
    async def plans(
        self,
        interaction,
        button
    ):
        plans = get_all_plans()

        if not plans:
            await interaction.response.send_message(
                "❌ No invite plans have been created yet.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📨 NetCloud Invite Plans",
            color=discord.Color.blue()
        )

        for plan in plans[:25]:
            embed.add_field(
                name=(
                    f"{plan['name']} • "
                    f"`{plan['id']}`"
                ),
                value=(
                    f"📨 Invites: `{plan['required_invites']}`\n"
                    f"🧠 RAM: `{plan['ram']}`\n"
                    f"⚙️ CPU: `{plan['cpu']}`\n"
                    f"💾 Disk: `{plan['disk']}`\n"
                    f"🐧 OS: `{plan['os']}`"
                ),
                inline=False
            )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


class InviteCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="inviteplans"
    )
    async def inviteplans(self, ctx):
        plans = get_all_plans()

        if not plans:
            await ctx.send(
                "📨 No Invite Plans are available."
            )
            return

        embed = discord.Embed(
            title="📨 Invite VPS Plans",
            description=(
                "Select a plan below.\n"
                "Your valid invites will be checked "
                "before claiming."
            ),
            color=discord.Color.blue()
        )

        await ctx.send(
            embed=embed,
            view=PlanView()
        )

    @commands.command(
        name="createinviteplan"
    )
    @commands.has_permissions(
        administrator=True
    )
    async def createinviteplan(self, ctx):
        embed = discord.Embed(
            title="📨 Invite Plan Manager",
            description=(
                "Click **Create Invite Plan** "
                "to create a new VPS invite plan."
            ),
            color=discord.Color.blue()
        )

        await ctx.send(
            embed=embed,
            view=InviteAdminView()
        )


async def setup(bot):
    await bot.add_cog(
        InviteCommands(bot)
      )
