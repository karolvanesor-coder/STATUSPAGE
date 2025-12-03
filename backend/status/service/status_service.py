import json
import httpx
from datetime import datetime
from pathlib import Path

SERVICES_FILE = Path("config/storage/services.json")

# Palabras que consideramos como "servicio arriba"
UP_KEYWORDS = {"ok", "available", "up"}

async def fetch_health(url: str):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, timeout=4.0)
            data = res.json()

            # Extraemos ambos campos si existen
            status_value = (
                data.get("overall_status") or 
                data.get("status") or 
                ""  # fallback
            )

            # Normalizamos y comparamos
            status = "up" if status_value.lower() in UP_KEYWORDS else "down"

        except Exception:
            status = "down"

    return status


async def check_all_services():
    service_groups = json.loads(SERVICES_FILE.read_text())

    results = []
    up_count = 0
    total = 0

    for group in service_groups:
        group_name = group.get("group", "apis")
        services = group.get("services", [])

        for service in services:
            status = await fetch_health(service["url"])
            
            results.append({
                "component": service["name"],
                "group": group_name,
                "status": "OK" if status == "up" else "Down"
            })

            total += 1
            if status == "up":
                up_count += 1

    # Evaluamos estado general
    if up_count == total:
        overall = "Available"
    elif up_count == 0:
        overall = "Unavailable"
    else:
        overall = "Partially Available"

    return {
        "overall_status": overall,
        "checks": results,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
