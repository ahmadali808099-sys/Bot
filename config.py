import os

# Discord
TOKEN = os.getenv("TOKEN")
PREFIX = "$"

# Bot settings
BOT_NAME = "NetCloud VPS Manager"

# Default VPS resources
DEFAULT_RAM = "4G"
DEFAULT_CPU = 4
DEFAULT_DISK = "50G"

# Supported operating systems
OS_IMAGES = {
    "ubuntu2204": "ubuntu:22.04",
    "ubuntu2004": "ubuntu:20.04",
    "debian10": "debian:10",
    "debian11": "debian:11",
    "debian12": "debian:12",
    "debian13": "debian:13",
}

# SSHX temporary web terminal command
SSHX_COMMAND = "curl -sSf https://sshx.io/get | sh -s run"
