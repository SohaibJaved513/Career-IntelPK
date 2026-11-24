from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = "careerintelpk-development-key"
    UPLOAD_FOLDER = ROOT_DIR / "uploads"
    DATA_PATH = ROOT_DIR / "data" / "processed" / "clean_jobs.csv"
    SKILL_PATH = ROOT_DIR / "data" / "processed" / "skill_counts.csv"
    ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
