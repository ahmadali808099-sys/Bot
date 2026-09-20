import asyncio
import os
import shlex


class Provisioner:
    """
    VPS provisioning backend adapter.

    The Discord bot uses this class to request VPS creation
    without putting infrastructure-specific code inside bot.py.
    """

    def __init__(self):
        self.backend_url = os.getenv("PROVISIONER_URL")

    async def create_vps(self, vps_data):
        """
        Create a VPS through the configured provisioning backend.

        The actual infrastructure backend can be connected later.
        """
        if not self.backend_url:
            raise RuntimeError(
                "PROVISIONER_URL is not configured."
            )

        # Backend integration will be connected here.
        await asyncio.sleep(0)

        return {
            "success": False,
            "message": (
                "Provisioning backend is not connected yet."
            ),
            "vps": vps_data,
        }

    async def execute_in_vps(self, vps_id, command):
        """
        Execute a command inside a VPS through the provisioning backend.
        """
        if not self.backend_url:
            raise RuntimeError(
                "PROVISIONER_URL is not configured."
            )

        if not command or not command.strip():
            raise ValueError("Command cannot be empty.")

        # Backend command execution will be connected here.
        await asyncio.sleep(0)

        return {
            "success": False,
            "message": (
                "VPS command backend is not connected yet."
            ),
            "vps_id": vps_id,
        }


provisioner = Provisioner()
