import logging
import os
import json
import uuid
import re
import sys
import unicodedata

from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)

# --- XÁC ĐỊNH BASE_DIR AN TOÀN TRƯỚC ---
if getattr(sys, 'frozen', False):
    base_dir = Path(sys._MEIPASS).resolve()
    logger.info(f"Ứng dụng chạy dưới dạng .exe, base_dir được đặt thành: {base_dir}")
else:
    base_dir = Path(__file__).resolve().parent.parent
    logger.info(f"Ứng dụng chạy dưới dạng script, base_dir được đặt thành: {base_dir}")



# --- TẠO TOKEN NGẪU NHIÊN KHI KHỞI ĐỘNG APP ---
SESSION_TOKEN = uuid.uuid4().hex
CONFIG_FILE = str(base_dir / "config.json") # Đảm bảo đường dẫn file config là tuyệt đối


def get_upload_dir():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                custom_path = config.get("upload_path")
                if custom_path:
                    path = Path(custom_path).resolve()
                    path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"Đường dẫn upload được lấy từ config: {path}")
                    return path
        except Exception as e:
            logger.error(f"Lỗi đọc file config: {e}")
    
    # Nếu không có file config hoặc lỗi, dùng mặc định
    else:
        logger.info(f"Không tìm thấy file config: {CONFIG_FILE}")
        default_dir = base_dir / "uploads"
        default_dir.mkdir(parents=True, exist_ok=True)
        return default_dir

# Khởi tạo App
app = FastAPI()

# Kiểm tra token
async def verify_token(token: str = None):
    if token != SESSION_TOKEN:
        raise HTTPException(status_code=403, detail="Token không hợp lệ hoặc đã hết hạn")
    return token

# Cấu hình templates (lưu ý đường dẫn ở đây nếu đóng gói .exe)
TEMPLATE_DIR = base_dir / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# Cấu hình phục vụ file tĩnh CSS, JS (Hỗ trợ tốt cả khi đóng gói .exe)
STATIC_DIR = base_dir / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mp4", ".pdf", ".docx", ".text", ".txt", ".mp3", ".mov"}

def sanitize_filename(name: str) -> str:
    """Loại bỏ các ký tự không hợp lệ và chuẩn hóa tên file"""
    name = unicodedata.normalize('NFC', name)
    return re.sub(r'[\\/*?:"<>|]', "", name)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request, token: str = Depends(verify_token)):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/upload")
async def upload_file(files: List[UploadFile] = File(...), token: str = Depends(verify_token)):
    upload_dir = get_upload_dir()  # Lấy đường dẫn upload mới nhất mỗi khi có request
    logger.info(f"Đường dẫn upload được lấy từ config: {upload_dir}")
    results = []
    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS: continue
        
        safe_filename = f"{os.path.splitext(sanitize_filename(file.filename))[0]}_{uuid.uuid4().hex[:6]}{file_ext}"
        file_path = upload_dir / safe_filename
        
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)
        results.append(safe_filename)
    return {"message": "Thành công", "filenames": results}

# Trong app/api.py
def get_session_token():
    return SESSION_TOKEN
