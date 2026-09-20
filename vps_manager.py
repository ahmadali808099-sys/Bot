import asyncio
import os
import shlex
import uuid
from datetime import datetime, timezone

from config import DEFAULT_RAM, DEFAULT_CPU, DEFAULT_DISK, OS_IMAGES
from database import add_vps, get_vps, update_vps, delete_vps


class VPSManager:
    def __init__(self):
        self.vps_processes = {}

    def generate_vps_id(self):
        return f"NC-{uuid.uuid4().hex[:8].upper()}"

    def create_record(
        self,
        owner_id,
        ram=DEFAULT_RAM,
        cpu=DEFAULT_CPU,
        disk=DEFAULT_DISK,
        os_name="ubuntu2204",
    ):
        os_name = os_name.lower()

        if os_name not in OS_IMAGES:
            raise ValueError("Unsupported operating system.")

        vps_id = self.generate_vps_id()

        return {
            "id": vps_id,
            "owner_id": str(owner_id),
            "ram": str(ram),
            "cpu": int(cpu),
            "disk": str(disk),
            "os": os_name,
            "image": OS_IMAGES[os_name],
            "status": "creating",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    async def register_vps(self, vps_data):
        await add_vps(vps_data["id"], vps_data)
        return vps_data

    async def set_status(self, vps_id, status):
        return await update_vps(vps_id, status=status)

    def get(self, vps_id):
        return get_vps(vps_id)

    async def remove(self, vps_id):
        return await delete_vps(vps_id)

    def list_user_vps(self, user_id):
        from database import get_user_vps
        return get_user_vps(user_id)

    async def run_safe_command(self, command, timeout=30):
        """
        Runs a local helper command used by the VPS backend.
        This is intentionally separate from Discord command handling.
        """
        if not command or not command.strip():
            raise ValueError("Command cannot be empty.")

        process = await asyncio.create_subprocess_exec(
            *shlex.split(command),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise TimeoutError("Command timed out.")

        return {
            "returncode": process.returncode,
            "stdout": stdout.decode(errors="replace"),
            "stderr": stderr.decode(errors="replace"),
        }


vps_manager = VPSManager()
