import json
import os
import asyncio
from datetime import datetime, timezone

INVITE_FILE = "invite_plans.json"

_lock = asyncio.Lock()


def default_data():
    return {
        "plans": {},
        "users": {}
    }


def load_data():
    if not os.path.exists(INVITE_FILE):
        return default_data()

    try:
        with open(INVITE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return default_data()

        data.setdefault("plans", {})
        data.setdefault("users", {})

        return data

    except (json.JSONDecodeError, OSError):
        return default_data()


async def save_data(data):
    async with _lock:
        with open(INVITE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)


def get_user_data(user_id):
    data = load_data()

    return data["users"].setdefault(
        str(user_id),
        {
            "valid_invites": 0,
            "claimed_plans": []
        }
    )


def get_user_invites(user_id):
    user = get_user_data(user_id)
    return int(user.get("valid_invites", 0))


async def set_user_invites(user_id, amount):
    data = load_data()

    user = data["users"].setdefault(
        str(user_id),
        {
            "valid_invites": 0,
            "claimed_plans": []
        }
    )

    user["valid_invites"] = max(0, int(amount))

    await save_data(data)


async def add_user_invites(user_id, amount):
    current = get_user_invites(user_id)

    await set_user_invites(
        user_id,
        current + int(amount)
    )


def create_plan(
    plan_id,
    name,
    required_invites,
    ram,
    cpu,
    disk,
    os_name
):
    data = load_data()

    data["plans"][str(plan_id)] = {
        "id": str(plan_id),
        "name": str(name),
        "required_invites": int(required_invites),
        "ram": str(ram),
        "cpu": int(cpu),
        "disk": str(disk),
        "os": str(os_name),
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    return data


async def save_plan(
    plan_id,
    name,
    required_invites,
    ram,
    cpu,
    disk,
    os_name
):
    data = create_plan(
        plan_id,
        name,
        required_invites,
        ram,
        cpu,
        disk,
        os_name
    )

    await save_data(data)


def get_plan(plan_id):
    data = load_data()
    return data["plans"].get(str(plan_id))


def get_all_plans():
    data = load_data()
    return list(data["plans"].values())


def has_claimed_plan(user_id, plan_id):
    user = get_user_data(user_id)

    for claim in user.get("claimed_plans", []):
        if str(claim.get("plan_id")) == str(plan_id):
            return True

    return False


def can_claim_plan(user_id, plan_id):
    plan = get_plan(plan_id)

    if not plan:
        return False

    if has_claimed_plan(user_id, plan_id):
        return False

    return (
        get_user_invites(user_id)
        >= int(plan["required_invites"])
    )


async def claim_plan(user_id, plan_id):
    data = load_data()

    plan = data["plans"].get(str(plan_id))

    if not plan:
        return None

    user = data["users"].setdefault(
        str(user_id),
        {
            "valid_invites": 0,
            "claimed_plans": []
        }
    )

    if any(
        str(claim.get("plan_id")) == str(plan_id)
        for claim in user.get("claimed_plans", [])
    ):
        return None

    current_invites = int(
        user.get("valid_invites", 0)
    )

    required = int(
        plan["required_invites"]
    )

    if current_invites < required:
        return None

    user["valid_invites"] = (
        current_invites - required
    )

    user.setdefault("claimed_plans", [])

    user["claimed_plans"].append({
        "plan_id": str(plan_id),
        "claimed_at": datetime.now(
            timezone.utc
        ).isoformat()
    })

    await save_data(data)

    return plan


def invite_note(user_id, plan_id):
    plan = get_plan(plan_id)

    if not plan:
        return "❌ Invite plan not found."

    current = get_user_invites(user_id)
    required = int(plan["required_invites"])

    remaining = max(
        0,
        required - current
    )

    if has_claimed_plan(user_id, plan_id):
        return "✅ You have already claimed this plan."

    if remaining == 0:
        return (
            f"📨 Your invites: **{current}**\n"
            f"🎯 Required invites: **{required}**\n\n"
            "✅ You can claim this VPS plan."
        )

    return (
        f"📨 Your invites: **{current}**\n"
        f"🎯 Required invites: **{required}**\n"
        f"⏳ Remaining invites: **{remaining}**"
                    )
