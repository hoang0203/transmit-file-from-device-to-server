import os
import uuid
import re
import sys


from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, Request, HTTPException, Depends
from fastapi.security import APIKeyQuery
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# --- TẠO TOKEN NGẪU NHIÊN KHI KHỞI ĐỘNG APP ---
SESSION_TOKEN = uuid.uuid4().hex
print(f"[*] Đường dẫn truy cập: http://<IP>:PORT/?token={SESSION_TOKEN}")

# Thêm đoạn code này để xác định đúng đường dẫn thực tế
if getattr(sys, 'frozen', False):
    # Đang chạy dưới dạng file .exe
    base_dir = Path(sys._MEIPASS)
else:
    # Đang chạy file script Python bình thường
    base_dir = Path(os.getcwd())
    
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
STATIC_DIR = base_dir / "static"            # <-- THÊM DÒNG NÀY
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static") # <-- THÊM DÒNG NÀY
UPLOAD_DIR = Path(os.getcwd()) / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mp4", ".pdf", ".docx", ".text", ".txt", ".mp3", ".mov"}

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)

@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request, token: str = Depends(verify_token)):
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/upload")
async def upload_file(files: List[UploadFile] = File(...), token: str = Depends(verify_token)):
    results = []
    for file in files:
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS: continue
        
        safe_filename = f"{os.path.splitext(sanitize_filename(file.filename))[0]}_{uuid.uuid4().hex[:6]}{file_ext}"
        file_path = UPLOAD_DIR / safe_filename
        
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)
        results.append(safe_filename)
    return {"message": "Thành công", "filenames": results}

# Trong app/api.py
def get_session_token():
    return SESSION_TOKEN