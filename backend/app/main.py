import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import router as employee_router
from app.web.routes import router as web_router
from app.db.connection import get_conn
from loguru import logger

app = FastAPI(title="Employee Management API", version="1.0.0")

def init_database():
    """Initialize the database schema on startup."""
    conn = None
    cursor = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        
        schema_file = Path(__file__).resolve().parent / "db" / "migrations" / "schema.sql"
        with open(schema_file, 'r') as f:
            schema = f.read()
        
        # Execute schema (may contain multiple statements)
        for statement in schema.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        
        conn.commit()
        logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.on_event("startup")
def startup_event():
    init_database()

# CORS (handy if you call these APIs from a separate frontend or Postman)
origins = os.getenv("CORS_ORIGINS", "http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

# All CRUD routes are under /api
app.include_router(employee_router, prefix="/api")

# Serve frontend static files and templates
root = Path(__file__).resolve().parents[1].parent  # backend/..
frontend_static = os.path.join(root, "frontend", "static")
if os.path.isdir(frontend_static):
    app.mount("/static", StaticFiles(directory=frontend_static), name="static")

# mount simple web routes (renders templates)
app.include_router(web_router)