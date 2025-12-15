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

# --- CORRECCIÓN AQUÍ: Usamos 'App' en lugar de 'Stub' ---
app = modal.App("flight-delay-predictor-prod")

# --- 2. Mounts (File Transfer) ---
local_mounts = [
    modal.Mount.from_local_dir("app", remote_path="/root/app"),
    modal.Mount.from_local_dir("models", remote_path="/root/models")
]

# --------------------------------------------------------------------------
# --- 3. Backend Function (FastAPI - Inference Engine) ---
# --------------------------------------------------------------------------

# --- CORRECCIÓN AQUÍ: Usamos @app.function en lugar de @stub.function ---
@app.function(
    image=image,
    mounts=local_mounts,
    # secrets=[modal.Secret.from_name("my-api-secrets")], 
    keep_warm=1
)
@modal.asgi_app()
def fastapi_app():
    from app.main import app as fastapi_instance
    return fastapi_instance

# --------------------------------------------------------------------------
# --- 4. Deployment Instructions ---
# --------------------------------------------------------------------------
#
# 1. Deploy the Backend:
#    $ modal deploy modal_stub.py