from datetime import datetime
from status.interface.interface_service import StatusServiceInterface
from status.interface.interface_repository import StatusRepository
from status.interface.interface_mapper import StatusMapperInterface
from status.interface.interface_notify import NotifyInterface


class StatusServiceImpl(StatusServiceInterface):

    def __init__(self, repo: StatusRepository, mapper: StatusMapperInterface, notify: NotifyInterface):
        self.repo = repo
        self.mapper = mapper
        self.notify = notify

        # Para evitar alertas repetidas
        self.last_down_services = set()

    async def get_status(self):
        # Obtener datos
        raw = await self.repo.get_services_status()
        normalized = self.mapper.normalize(raw)

        # Agregar timestamp a la respuesta
        normalized["timestamp"] = datetime.utcnow().isoformat() + "Z"

        # --------------------------------------------------------------------
        # 1️⃣ Filtrar servicios que están CAÍDOS
        # --------------------------------------------------------------------
        down_items = [item for item in raw["checks"] if item["status"].lower() != "up"]
        down_set = {item["component"] for item in down_items}

        # Si el estado no cambió → no mandar alerta
        if down_set == self.last_down_services:
            return normalized

        # --------------------------------------------------------------------
        # 2️⃣ Agrupar los caídos por grupo
        # --------------------------------------------------------------------
        grouped = {}
        for item in down_items:
            group = item["group"].upper()
            if group not in grouped:
                grouped[group] = []
            grouped[group].append(item["component"])

        # --------------------------------------------------------------------
        # 3️⃣ Construir mensaje en Markdown
        # --------------------------------------------------------------------
        msg_lines = ["🚨 *Servicios caídos detectados*\n"]

        for group_name, items in grouped.items():
            msg_lines.append(f"*{group_name} ({len(items)})*")
            for comp in items:
                msg_lines.append(f"❌ {comp}")
            msg_lines.append("")  # salto

        msg_lines.append("⚠️ *Revisar cuanto antes.*")

        final_msg = "\n".join(msg_lines)

        # --------------------------------------------------------------------
        # 4️⃣ Enviar alerta a Telegram
        # --------------------------------------------------------------------
        await self.notify.send(final_msg)

        # Guardar el estado para evitar repetir alertas
        self.last_down_services = down_set

        return normalized
