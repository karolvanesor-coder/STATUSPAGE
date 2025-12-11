from typing import Dict, Any
from status.interface.interface_mapper import StatusMapperInterface


class StatusMapperImpl(StatusMapperInterface):
    """Implementación de StatusMapperInterface que normaliza datos crudos de servicios."""

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convierte los datos crudos de servicios en una estructura lista para el dominio.

        Args:
            raw_data (Dict[str, Any]): Datos de servicios crudos, típicamente desde el repositorio.

        Returns:
            Dict[str, Any]: Diccionario con estado general y lista de componentes normalizados.
        """
        checks = raw_data.get("checks", [])

        up_count = sum(1 for c in checks if c["status"] == "up")
        total = len(checks)

        if up_count == total:
            overall = "Available"
        elif up_count == 0:
            overall = "Unavailable"
        else:
            overall = "Partially Available"

        # Mapear "up/down" → "OK/Down"
        output_checks = [
            {
                "component": c["component"],
                "group": c["group"],
                "status": "OK" if c["status"] == "up" else "Down"
            }
            for c in checks
        ]

        return {
            "overall_status": overall,
            "checks": output_checks
        }
