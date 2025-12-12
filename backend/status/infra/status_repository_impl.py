import json
from pathlib import Path
from typing import Any, Dict, List

import httpx

from status.interface.interface_repository import StatusRepository

SERVICES_FILE = Path("config/storage/services.json")
UP_KEYWORDS = {"ok", "available", "up"}


class StatusRepositoryImpl(StatusRepository):
    """Repositorio para obtener el estado de los servicios definidos en un JSON."""

    async def get_services_status(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Obtiene el estado de todos los servicios agrupados.

        Devuelve:
            Dict con la clave 'checks' que contiene una lista de servicios y su estado.
        """
        groups = json.loads(SERVICES_FILE.read_text(encoding="utf-8"))
        results: List[Dict[str, str]] = []

        async with httpx.AsyncClient() as client:
            for group in groups:
                group_name = group.get("group", "apis")

                for service in group.get("services", []):
                    status = "down"
                    try:
                        response = await client.get(
                            service["url"],
                            timeout=4,
                            follow_redirects=True
                        )

                        # 1️⃣ Si responde 200 → está UP (aunque no tenga JSON)
                        if response.status_code == 200:
                            status = "up"

                        # 2️⃣ Si tiene JSON válido con claves conocidas → mejor aún
                        try:
                            body = response.json()
                            value = str(body.get("overall_status") or body.get("status") or "").lower()
                            if value in UP_KEYWORDS:
                                status = "up"
                        except Exception:
                            # Si no es JSON válido, no pasa nada
                            pass

                    except httpx.RequestError:
                        # Mantener 'down' si ocurre un error de conexión
                        pass

                    results.append({
                        "component": service.get("name", "unknown"),
                        "group": group_name,
                        "status": status
                    })

        return {"checks": results}
