import json
import httpx
from pathlib import Path
from typing import Dict, Any

from status.interface.interface_repository import StatusRepository

SERVICES_FILE = Path("config/storage/services.json")
UP_KEYWORDS = {"ok", "available", "up"}


class StatusRepositoryImpl(StatusRepository):

    async def get_services_status(self) -> Dict[str, Any]:

        groups = json.loads(SERVICES_FILE.read_text())
        results = []

        async with httpx.AsyncClient() as client:
            for group in groups:
                group_name = group.get("group", "apis")

                for service in group["services"]:
                    try:
                        res = await client.get(service["url"], timeout=4)
                        body = res.json()

                        value = (
                            body.get("overall_status")
                            or body.get("status")
                            or ""
                        )

                        status = "up" if value.lower() in UP_KEYWORDS else "down"

                    except:
                        status = "down"

                    results.append({
                        "component": service["name"],
                        "group": group_name,
                        "status": status
                    })

        return {"checks": results}
