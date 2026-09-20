import discord


def is_admin(member: discord.Member) -> bool:
    """Check whether a Discord member has Administrator permission."""
    if not member:
        return False

    return member.guild_permissions.administrator


def is_vps_owner(member: discord.Member, vps_data: dict) -> bool:
    """Check whether the member owns the VPS."""
    if not member or not vps_data:
        return False

    return str(vps_data.get("owner_id")) == str(member.id)


def can_manage_vps(member: discord.Member, vps_data: dict) -> bool:
    """Admins or the VPS owner can manage that VPS."""
    return is_admin(member) or is_vps_owner(member, vps_data)


def permission_message() -> str:
    return "❌ You don't have permission to manage this VPS."
