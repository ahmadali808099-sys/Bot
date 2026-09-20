import json
import os
import asyncio

DATABASE_FILE = "vps_db.json"

_lock = asyncio.Lock()


def _ensure_database():
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w", encoding="utf-8") as file:
            json.dump({"vps": {}}, file, indent=4)


def load_database():
    _ensure_database()

    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return {"vps": {}}

        if "vps" not in data or not isinstance(data["vps"], dict):
            data["vps"] = {}

        return data

    except (json.JSONDecodeError, OSError):
        return {"vps": {}}


async def save_database(data):
    async with _lock:
        with open(DATABASE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


def get_vps(vps_id):
    database = load_database()
    return database["vps"].get(str(vps_id))


def get_user_vps(user_id):
    database = load_database()
    user_id = str(user_id)

    return [
        vps
        for vps in database["vps"].values()
        if str(vps.get("owner_id")) == user_id
    ]


async def add_vps(vps_id, vps_data):
    database = load_database()
    database["vps"][str(vps_id)] = vps_data
    await save_database(database)


async def update_vps(vps_id, **updates):
    database = load_database()
    vps_id = str(vps_id)

    if vps_id not in database["vps"]:
        return False

    database["vps"][vps_id].update(updates)
    await save_database(database)

    return True


async def delete_vps(vps_id):
    database = load_database()
    vps_id = str(vps_id)

    if vps_id not in database["vps"]:
        return False

    del database["vps"][vps_id]
    await save_database(database)

    return True
