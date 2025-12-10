from status.interface.interface_mapper import StatusMapperInterface


class StatusMapperImpl(StatusMapperInterface):

    def normalize(self, raw_data: dict) -> dict:
        checks = raw_data["checks"]

        up_count = sum(1 for c in checks if c["status"] == "up")
        total = len(checks)

        if up_count == total:
            overall = "Available"
        elif up_count == 0:
            overall = "Unavailable"
        else:
            overall = "Partially Available"

        # Convertimos "up/down" → "OK/Down"
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
