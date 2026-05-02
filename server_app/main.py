import os
import shutil
import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from shared.security_utils import CryptoManager

try:
    from server_app.ai_model import MurojaatAI
    from server_app.database import DatabaseManager
except ImportError:
    from ai_model import MurojaatAI
    from database import DatabaseManager


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "storage"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

SECRET_KEY = b"SI_O8XF6eL3_S2N9yJ4-uX0zR1vL5mN8qA2cW4bP6k8="

app = FastAPI(title="Aholi Murojaat API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DatabaseManager()
ai_engine = MurojaatAI()
crypto = CryptoManager(SECRET_KEY)


@app.get("/")
async def health_check():
    return {"status": "ok", "service": "Aholi Murojaat API"}


def safe_upload_path(filename: str) -> Path:
    safe_name = os.path.basename(filename or "")
    if not safe_name:
        raise ValueError("Uploaded file name is empty")

    extension = Path(safe_name).suffix.lower()
    if extension not in ALLOWED_UPLOAD_EXTENSIONS:
        raise ValueError("Only PDF, PNG, JPG, and JPEG files are allowed")

    unique_name = f"{uuid.uuid4().hex}{extension}"
    return UPLOAD_DIR / unique_name


@app.post("/receive_murojaat")
async def receive_data(message: str = Form(...), file: UploadFile = File(None)):
    try:
        decrypted_text = crypto.decrypt_data(message)
        category = ai_engine.predict(decrypted_text)

        file_path = None
        if file:
            upload_path = safe_upload_path(file.filename)
            with upload_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            file_path = str(upload_path)

        murojaat_id = db.add_murojaat(message, file_path)
        db.update_category(murojaat_id, category)

        return {"status": "success", "id": murojaat_id, "category": category}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
