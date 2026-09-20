import discord

from invite_system import (
    get_all_plans,
    get_user_invites,
    can_claim_plan,
    claim_plan
)

from channel_manager import channel_manager
from vps_manager import vps_manager


class PlanSelect(discord.ui.Select):

    def __init__(self):
        plans = get_all_plans()
        options = []

        for plan in plans[:25]:
            options.append(
                discord.SelectOption(
                    label=plan["name"][:100],
                    description=(
                        f'{plan["required_invites"]} invites • '
                        f'{plan["ram"]} RAM • '
                        f'{plan["disk"]} Disk'
                    )[:100],
                    value=str(plan["id"])
                )
            )

        if not options:
            options.append(
                discord.SelectOption(
                    label="No plans available",
                    value="none"
                )
            )

        super().__init__(
            placeholder="📨 Select an Invite Plan",
            options=options
        )

    async def callback(self, interaction):
        plan_id = self.values[0]

        if plan_id == "none":
            await interaction.response.send_message(
                "❌ No invite plans are available.",
                ephemeral=True
            )
            return

        plan = next(
            (
                p for p in get_all_plans()
                if str(p["id"]) == str(plan_id)
            ),
            None
        )

        if not plan:
            await interaction.response.send_message(
                "❌ Plan not found.",
                ephemeral=True
            )
            return

        invites = get_user_invites(
            interaction.user.id
        )

        required = int(
            plan["required_invites"]
        )

        remaining = max(
            0,
            required - invites
        )

        embed = discord.Embed(
            title=f"📨 {plan['name']}",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📨 Your Invites",
            value=f"`{invites}`",
            inline=True
        )

        embed.add_field(
            name="🎯 Required",
            value=f"`{required}`",
            inline=True
        )

        embed.add_field(
            name="⏳ Remaining",
            value=f"`{remaining}`",
            inline=True
        )

        embed.add_field(
            name="🖥️ VPS",
            value=(
                f"RAM: `{plan['ram']}`\n"
                f"CPU: `{plan['cpu']}`\n"
                f"Disk: `{plan['disk']}`\n"
                f"OS: `{plan['os']}`"
            ),
            inline=False
        )

        if can_claim_plan(
            interaction.user.id,
            plan_id
        ):
            embed.description = (
                "✅ You have enough valid invites.\n"
                "Click **Claim VPS** below."
            )

            view = ClaimView(
                plan_id,
                interaction.user.id
            )
        else:
            embed.description = (
                f"❌ You need **{remaining}** more "
                "valid invites to claim this plan."
            )

            view = None

        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True
        )


class PlanView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(PlanSelect())


class ClaimView(discord.ui.View):

    def __init__(self, plan_id, user_id):
        super().__init__(timeout=120)

        self.plan_id = str(plan_id)
        self.user_id = str(user_id)

    @discord.ui.button(
        label="Claim VPS",
        style=discord.ButtonStyle.green,
        emoji="🖥️"
    )
    async def claim(
        self,
        interaction,
        button
    ):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message(
                "❌ This button is not for you.",
                ephemeral=True
            )
            return

        plan = await claim_plan(
            interaction.user.id,
            self.plan_id
        )

        if not plan:
            await interaction.response.send_message(
                "❌ You cannot claim this plan.",
                ephemeral=True
            )
            return

        vps = vps_manager.create_record(
            owner_id=interaction.user.id,
            ram=plan["ram"],
            cpu=plan["cpu"],
            disk=plan["disk"],
            os_name=plan["os"]
        )

        await vps_manager.register_vps(vps)

        channel = await channel_manager.create_private_vps_channel(
            interaction.guild,
            interaction.user,
            vps["id"]
        )

        await interaction.response.send_message(
            "✅ VPS claimed successfully!\n"
            f"🔐 Private channel created: {channel.mention}",
            ephemeral=True
      )
