import modal
import os

# --- 1. Base Image Configuration ---
image = modal.Image.debian_slim().pip_install(
    "pandas",
    "numpy",
    "scikit-learn",
    "joblib",
    "fastapi",
    "uvicorn",
    "pydantic"
)

# --- 2. App Definition ---
# Usamos 'modal.App' (versiones nuevas) con fallback a 'modal.Stub' por seguridad
try:
    app = modal.App("flight-delay-predictor-prod")
except AttributeError:
    app = modal.Stub("flight-delay-predictor-prod")

# --- 3. Mounts ---
# Usamos modal.Mount explícitamente para evitar errores de importación
local_mounts = [
    modal.Mount.from_local_dir("app", remote_path="/root/app"),
    modal.Mount.from_local_dir("models", remote_path="/root/models")
]

# --- 4. Backend Function ---
@app.function(
    image=image,
    mounts=local_mounts,
    keep_warm=1
)
@modal.asgi_app()
def fastapi_app():
    # Importación diferida dentro del contenedor
    from app.main import app as fastapi_instance
    return fastapi_instance

# --------------------------------------------------------------------------
# Comandos de despliegue:
# 1. modal deploy modal_stub.py