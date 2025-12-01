from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.services_routes import router as service_router

app = FastAPI(title="Status Page API", version="1.0.0")

# Middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas de servicios
app.include_router(service_router)

# Endpoint raíz
@app.get("/")
async def root():
    return {"status": "Backend operativo 🚀"}
