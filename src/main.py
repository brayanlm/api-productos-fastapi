from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .config.database import engine
from .apis.productos import router as productos_router

app = FastAPI(title="API de Gestión de Productos")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(productos_router)


# Endpoint de prueba
@app.get("/")
def test_db():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {"conexion": "Exitosa"}
    except Exception as e:
        return {"error": str(e)}
