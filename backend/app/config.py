import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
BACKEND_DIR = BASE_DIR / "backend"
STORAGE_DIR = BACKEND_DIR / "storage"
CACHE_DIR = BACKEND_DIR / "data_cache"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Database
DB_PATH = STORAGE_DIR / "contract_analyzer.db"

# CUAD File
CUAD_FILE = DATA_DIR / "CUADv1.json"

# Server configuration
HOST = "127.0.0.1"
PORT = 8000
