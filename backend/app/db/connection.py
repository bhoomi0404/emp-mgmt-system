import os
from dotenv import load_dotenv
from mysql.connector.pooling import MySQLConnectionPool
from loguru import logger

# Load .env in local dev (in containers/VM, env vars come from runtime)
load_dotenv(override=False)

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "emp_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "emp_pass")
DB_NAME = os.getenv("DB_NAME", "employee_db")
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))

config = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "charset": "utf8mb4",
    "autocommit": False,
}

logger.info(f"MySQL pool -> {DB_HOST}:{DB_PORT}/{DB_NAME}, size={POOL_SIZE}")
pool = MySQLConnectionPool(pool_name="emp_pool", pool_size=POOL_SIZE, **config)

def get_conn():
    """Return a connection from the pool. Caller must close()."""
    return pool.get_connection()