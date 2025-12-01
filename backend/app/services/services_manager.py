import json
import httpx
from datetime import datetime
from pathlib import Path

SERVICES_FILE = Path("app/data/services.json")


async def fetch_health(url: str):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, timeout=4.0)
            data = res.json()

            if "overall_status" in data:
                status = "up" if data["overall_status"].lower() in ["available", "ok"] else "down"
            elif "status" in data:
                status = "up" if data["status"].lower() in ["ok", "up"] else "down"
            else:
                status = "down"

        except Exception:
            status = "down"

    return status


async def check_all_services():
    services = json.loads(SERVICES_FILE.read_text())

    results = []
    ok_count = 0

    for service in services:
        status = await fetch_health(service["url"])
        results.append({
            "component": service["name"],
            "status": "OK" if status == "up" else "Down"
        })
        if status == "up":
            ok_count += 1

    total = len(results)

    if ok_count == total:
        overall = "Available"
    elif ok_count == 0:
        overall = "Unavailable"
    else:
        overall = "Partially Available"

    return {
        "overall_status": overall,
        "checks": results,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
