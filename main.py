import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


AGENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    # Use the PORT environment variable if available (for cloud deployments)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
