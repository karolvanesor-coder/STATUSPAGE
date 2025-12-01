import json
import os

def load_services():
    config_path = os.path.join(os.path.dirname(__file__), "services.json")

    try:
        with open(config_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Si no existe el archivo, devolvemos un servicio Dropi por defecto
        return [
            {
                "name": "Dropi",
                "type": "dropi",
                "country": "Colombia",
                "url": "https://api-v2.dropi.co/system/configuration/health"
            }
        ]
