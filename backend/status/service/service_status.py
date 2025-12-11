from datetime import datetime
from typing import Dict, Any, Set

from status.interface.interface_service import StatusServiceInterface
from status.interface.interface_repository import StatusRepository
from status.interface.interface_mapper import StatusMapperInterface
from status.interface.interface_notify import NotifyInterface


class StatusServiceImpl(StatusServiceInterface):
    """Implementación de StatusServiceInterface con alertas a Telegram y normalización de datos."""

    def __init__(self, repo: StatusRepository, mapper: StatusMapperInterface, notify: NotifyInterface):
        self.repo = repo
        self.mapper = mapper
        self.notify = notify
        self.last_down_services: Set[str] = set()  # Para evitar alertas repetidas

    async def get_status(self) -> Dict[str, Any]:
        # 1️⃣ Obtener datos y normalizarlos
        raw = await self.repo.get_services_status()
        normalized = self.mapper.normalize(raw)
        normalized["timestamp"] = datetime.utcnow().isoformat() + "Z"

        # 2️⃣ Filtrar servicios caídos
        down_items = [item for item in raw.get("checks", []) if item["status"].lower() != "up"]
        down_set = {item["component"] for item in down_items}

        # No enviar alerta si el estado no cambió
        if down_set == self.last_down_services:
            return normalized

        # 3️⃣ Agrupar servicios caídos por grupo
        grouped = {}
        for item in down_items:
            group = item["group"].upper()
            grouped.setdefault(group, []).append(item["component"])

        # 4️⃣ Construir mensaje en Markdown
        msg_lines = ["🚨 *Servicios caídos detectados*\n"]
        for group_name, components in grouped.items():
            msg_lines.append(f"*{group_name} ({len(components)})*")
            for comp in components:
                msg_lines.append(f"❌ {comp}")
            msg_lines.append("")  # salto de línea

        msg_lines.append("⚠️ *Revisar cuanto antes.*")
        final_msg = "\n".join(msg_lines)

        # 5️⃣ Enviar alerta a Telegram
        await self.notify.send(final_msg)

        # 6️⃣ Guardar estado actual de servicios caídos
        self.last_down_services = down_set

        return normalized
