from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from smartkdb import SmartKDB

app = FastAPI(title="SmartKDB Control Center")

# Initialize DB
db_path = os.getenv("SMARTKDB_PATH", "mydb.kdb")
db = SmartKDB(db_path)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "frontend")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
    return "<h1>SmartKDB Dashboard</h1><p>Frontend not found.</p>"

@app.get("/api/tables")
def get_tables():
    return list(db.tables.keys())

@app.get("/api/stats")
def get_stats():
    return db.brain.stats

@app.post("/api/query")
def run_query(table: str, query: dict):
    # Stub for query execution via API
    return {"status": "not_implemented_in_gui_yet"}

def start_server(host="0.0.0.0", port=8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)
