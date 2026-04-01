from pathlib import Path

APP_TITLE = "Steg"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "Steg web application"
DEFAULT_ARCHITECTURE = "dense"
MAX_IMAGE_DIMENSION = 2048
OUTPUT_RETENTION_SECONDS = 3600

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
RUNTIME_DIR = BASE_DIR / "runtime"
UPLOAD_DIR = RUNTIME_DIR / "uploads"
OUTPUT_DIR = RUNTIME_DIR / "outputs"
