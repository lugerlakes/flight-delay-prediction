# modal_stub.py — Deploy FastAPI via Modal v1.x
import os
import modal
import uvicorn
import shlex
import subprocess
from pathlib import Path

api_script = Path(__file__).parent / "app" / "main.py"
api_remote = "/root/flight-delay-prediction/app/main.py"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("fastapi", "uvicorn", "joblib", "pandas", "numpy", "python-dotenv")
    .add_local_file(str(api_script), api_remote)
)

app = modal.App(name="flight-delay-api", image=image)

@app.function()
@modal.web_server(port=int(os.getenv("FASTAPI_PORT", "8000")))
def run_api():
    cmd = f"uvicorn app.main:app --host 0.0.0.0 --port {os.getenv('FASTAPI_PORT', 8000)}"
    subprocess.Popen(cmd, shell=True)
