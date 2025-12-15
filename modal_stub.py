from modal import App, Image, Mount, asgi_app, Secret
import os

# --- 1. Base Image Configuration ---
image = Image.debian_slim().pip_install(
    "pandas",
    "numpy",
    "scikit-learn",
    "joblib",
    "fastapi",
    "uvicorn",
    "pydantic"
)

# Definimos la App (antes Stub)
app = App("flight-delay-predictor-prod")

# --- 2. Mounts (File Transfer) ---
# Usamos la clase Mount importada directamente
local_mounts = [
    Mount.from_local_dir("app", remote_path="/root/app"),
    Mount.from_local_dir("models", remote_path="/root/models")
]

# --------------------------------------------------------------------------
# --- 3. Backend Function (FastAPI - Inference Engine) ---
# --------------------------------------------------------------------------

@app.function(
    image=image,
    mounts=local_mounts,
    # secrets=[Secret.from_name("my-api-secrets")], 
    keep_warm=1
)
@asgi_app()
def fastapi_app():
    from app.main import app as fastapi_instance
    return fastapi_instance

# --------------------------------------------------------------------------
# --- 4. Deployment Instructions ---
# --------------------------------------------------------------------------
# 1. Deploy: modal deploy modal_stub.py