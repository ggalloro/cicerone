import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# The directory containing the agent packages
AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# In-memory session storage for simplicity
SESSION_DB_URL = "sqlite:///./sessions.db"

# Create the FastAPI app using the ADK helper
app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    session_service_uri=SESSION_DB_URL,
    web=False
)

# Mount the static directory to serve HTML, CSS, JS
app.mount("/static", StaticFiles(directory="cicerone-single/static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('cicerone-single/static/index.html')

if __name__ == "__main__":
    # Use the PORT environment variable if available (for cloud deployments)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
