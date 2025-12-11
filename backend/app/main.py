from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Controllers
from status.handler import status_controller

# Dependencias
from status.infra.status_repository_impl import StatusRepositoryImpl
from status.mapper.mapper_impl import StatusMapperImpl
from status.infra.telegram_notify import TelegramNotify
from status.service.service_status import StatusServiceImpl


def create_app() -> FastAPI:
    """Inicializa y configura la aplicación FastAPI."""
    app = FastAPI(
        title="Status Page API",
        version="1.0.0",
    )

    # --------------------
    # Middleware CORS
    # --------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --------------------
    # Dependencias core
    # --------------------
    repo = StatusRepositoryImpl()
    mapper = StatusMapperImpl()

    # --------------------
    # Notificaciones
    # --------------------
    telegram_notify = TelegramNotify(
        bot_token="8340353857:AAHTuZCnwl4Un6NcYE_oJB3Ia8885LwjYmg",
        chat_id="-4814683898",
    )

    # --------------------
    # Inyección de dependencias
    # --------------------
    status_controller.service = StatusServiceImpl(
        repo=repo,
        mapper=mapper,
        notify=telegram_notify,
    )

    app.include_router(status_controller.router)

    # --------------------
    # Healthcheck
    # --------------------
    @app.get("/")
    async def root():
        return {"status": "Backend operativo 🚀"}

    return app


# Instancia principal de la aplicación
app = create_app()
