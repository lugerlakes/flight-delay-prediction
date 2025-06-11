# modal_streamlit_stub.py — Deploy Streamlit via Modal v1.x
import os
import modal
import shlex
import subprocess
from pathlib import Path

# Locate your Streamlit entrypoint in the project (inside 'app' folder)
streamlit_script_local = Path(__file__).parent / "app" / "streamlit_app.py"
streamlit_script_remote = "/root/flight-delay-prediction/app/streamlit_app.py"

# Build an image with required dependencies and include the script
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("streamlit==1.33.0", "requests", "python-dotenv")
    .add_local_file(str(streamlit_script_local), streamlit_script_remote)
)

# Define the Modal app
app = modal.App(name="flight-delay-streamlit", image=image)

@app.function()
@modal.concurrent(max_inputs=10)
@modal.web_server(port=int(os.getenv("STREAMLIT_PORT", "8501")))
def run_streamlit():
    cmd = f"streamlit run {shlex.quote(streamlit_script_remote)} " \
          f"--server.port {os.getenv('STREAMLIT_PORT', 8501)} " \
          "--server.address=0.0.0.0 --server.enableCORS=false " \
          "--server.enableXsrfProtection=false"
    subprocess.Popen(cmd, shell=True)
