from typing import Any, Dict

from status.interface.interface_mapper import StatusMapperInterface


class StatusMapperImpl(StatusMapperInterface):
    """Normaliza el estado de los servicios y calcula el estado general."""

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        checks = raw_data.get("checks", [])

        up_count = sum(1 for c in checks if c["status"] == "up")
        total = len(checks)

        if up_count == total:
            overall = "Available"
        elif up_count == 0:
            overall = "Unavailable"
        else:
            overall = "Partially Available"

        # Normalización de estados para el frontend
        output_checks = [
            {
                "component": c["component"],
                "group": c["group"],
                "status": "OK" if c["status"] == "up" else "Down",
            }
            for c in checks
        ]

        return {
            "overall_status": overall,
            "checks": output_checks,
        }
