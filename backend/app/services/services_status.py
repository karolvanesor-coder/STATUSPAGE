import httpx
from datetime import datetime

async def fetch_health(url: str):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, timeout=5.0)
            data = res.json()

            # ----- FORMATO NUEVO -----
            if "checks" in data:
                overall_status = data.get("overall_status", "").lower()
                status = "up" if overall_status in ["available", "ok"] else "down"

            # ----- FORMATO VIEJO -----
            elif "status" in data:
                status = "up" if data["status"].lower() in ["ok", "up"] else "down"

            else:
                status = "down"

        except Exception:
            status = "down"

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": status
    }
