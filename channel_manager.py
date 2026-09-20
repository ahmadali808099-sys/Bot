import discord


CATEGORY_NAME = "NETCLOUD VPS"


class ChannelManager:

    async def get_or_create_category(
        self,
        guild: discord.Guild
    ):
        category = discord.utils.get(
            guild.categories,
            name=CATEGORY_NAME
        )

        if category:
            return category

        return await guild.create_category(
            CATEGORY_NAME,
            reason="NetCloud VPS category"
        )

    async def create_private_vps_channel(
        self,
        guild: discord.Guild,
        member: discord.Member,
        vps_id: str
    ):
        category = await self.get_or_create_category(
            guild
        )

        overwrites = {
            guild.default_role:
                discord.PermissionOverwrite(
                    view_channel=False
                ),

            member:
                discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    attach_files=True,
                    embed_links=True
                )
        }

        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = (
                    discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True,
                        read_message_history=True,
                        manage_channels=True
                    )
                )

        channel_name = f"vps-{str(vps_id).lower()}"

        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            reason="Private VPS channel"
        )

        embed = discord.Embed(
            title="☁️ NetCloud VPS",
            description=(
                f"Welcome {member.mention}!\n\n"
                f"🖥️ VPS ID: `{vps_id}`\n"
                "🔐 This channel is private.\n\n"
                "Only you and administrators can see this channel."
            ),
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📦 VPS Setup",
            value=(
                "Your VPS setup will appear here "
                "once provisioning starts."
            ),
            inline=False
        )

        await channel.send(
            content=member.mention,
            embed=embed
        )

        return channel


channel_manager = ChannelManager()
