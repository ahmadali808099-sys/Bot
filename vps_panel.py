import discord

from database import get_vps, update_vps
from permissions import can_manage_vps
from sshx_manager import sshx_manager
from vps_manager import vps_manager


class VPSControlPanel(discord.ui.View):

    def __init__(self, vps_id: str):
        super().__init__(timeout=None)
        self.vps_id = str(vps_id)

    async def get_vps_and_check(
        self,
        interaction: discord.Interaction
    ):
        vps = get_vps(self.vps_id)

        if not vps:
            await interaction.response.send_message(
                "❌ VPS not found.",
                ephemeral=True
            )
            return None

        if not can_manage_vps(
            interaction.user,
            vps
        ):
            await interaction.response.send_message(
                "❌ You don't have permission to manage this VPS.",
                ephemeral=True
            )
            return None

        return vps

    @discord.ui.button(
        label="Start",
        emoji="🟢",
        style=discord.ButtonStyle.success,
        custom_id="vps_panel_start"
    )
    async def start(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        vps = await self.get_vps_and_check(interaction)

        if not vps:
            return

        await interaction.response.defer(
            ephemeral=True
        )

        # Backend connection will perform the
        # real VPS start operation.
        await update_vps(
            self.vps_id,
            status="starting"
        )

        await interaction.followup.send(
            f"🟢 VPS `{self.vps_id}` start requested.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Stop",
        emoji="🔴",
        style=discord.ButtonStyle.danger,
        custom_id="vps_panel_stop"
    )
    async def stop(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        vps = await self.get_vps_and_check(interaction)

        if not vps:
            return

        await interaction.response.defer(
            ephemeral=True
        )

        await update_vps(
            self.vps_id,
            status="stopping"
        )

        await interaction.followup.send(
            f"🔴 VPS `{self.vps_id}` stop requested.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Restart",
        emoji="🔄",
        style=discord.ButtonStyle.primary,
        custom_id="vps_panel_restart"
    )
    async def restart(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        vps = await self.get_vps_and_check(interaction)

        if not vps:
            return

        await interaction.response.defer(
            ephemeral=True
        )

        await update_vps(
            self.vps_id,
            status="restarting"
        )

        await interaction.followup.send(
            f"🔄 VPS `{self.vps_id}` restart requested.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Status",
        emoji="📊",
        style=discord.ButtonStyle.secondary,
        custom_id="vps_panel_status"
    )
    async def status(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        vps = await self.get_vps_and_check(interaction)

        if not vps:
            return

        embed = discord.Embed(
            title=f"📊 VPS Status — {self.vps_id}",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Status",
            value=f"`{vps.get('status', 'unknown')}`",
            inline=True
        )

        embed.add_field(
            name="RAM",
            value=f"`{vps.get('ram', '-')}`",
            inline=True
        )

        embed.add_field(
            name="CPU",
            value=f"`{vps.get('cpu', '-')}`",
            inline=True
        )

        embed.add_field(
            name="Disk",
            value=f"`{vps.get('disk', '-')}`",
            inline=True
        )

        embed.add_field(
            name="OS",
            value=f"`{vps.get('os', '-')}`",
            inline=True
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    @discord.ui.button(
        label="Console",
        emoji="🖥️",
        style=discord.ButtonStyle.secondary,
        custom_id="vps_panel_console"
    )
    async def console(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        vps = await self.get_vps_and_check(interaction)

        if not vps:
            return

        await interaction.response.send_message(
            "🖥️ Console backend is ready to be connected.\n"
            "The actual command execution backend "
            "will be connected next.",
            ephemeral=True
        )

    @discord.ui.button(
        label="SSHX",
        emoji="🌐",
        style=discord.ButtonStyle.primary,
        custom_id="vps_panel_sshx"
    )
    async def sshx(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        vps = await self.get_vps_and_check(interaction)

        if not vps:
            return

        await interaction.response.send_message(
            "🌐 Creating temporary SSHX terminal...\n"
            "The VPS execution backend must be connected "
            "before a real SSHX URL can be generated.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Delete",
        emoji="🗑️",
        style=discord.ButtonStyle.danger,
        custom_id="vps_panel_delete"
    )
    async def delete(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        vps = await self.get_vps_and_check(interaction)

        if not vps:
            return

        # Delete confirmation is handled before
        # removing the VPS record.
        await interaction.response.send_message(
            "⚠️ VPS deletion requires confirmation.\n"
            f"VPS: `{self.vps_id}`\n\n"
            "Use the admin/user delete command to "
            "confirm permanent deletion.",
            ephemeral=True
        )


def create_vps_panel(vps_id: str):
    return VPSControlPanel(vps_id)
