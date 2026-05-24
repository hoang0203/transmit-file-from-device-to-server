import os
import logging
import json
import threading
import tkinter as tk
import socket
import sys

import qrcode
import uvicorn

# Thêm filedialog vào phần import
from tkinter import messagebox, filedialog 

from PIL import Image, ImageTk

from app.api import app, get_session_token

# --- HÀM LẤY IP LOCAL ---
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# --- HÀM KIỂM TRA CỔNG TRỐNG ---
def is_port_free(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) != 0
    except:
        return False

# --- HÀM CHẠY SERVER BACKEND ---
def run_fastapi_server(host, port):
    # Tắt hoàn toàn log của uvicorn để không gây xung đột với GUI
    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.error").handlers = []
    
    # Ép luồng xuất dữ liệu về null nếu chạy dưới dạng .exe
    if getattr(sys, 'frozen', False):
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        
    uvicorn.run(app, host=host, port=port, log_level="critical")

# --- HÀM XỬ LÝ KHI ĐÓNG CỬA SỔ ---
def on_closing(root):
    if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn đóng ứng dụng chia sẻ file?"):
        root.destroy()
        os._exit(0)  # Ngắt toàn bộ tiến trình

# --- MÀN HÌNH QR (BƯỚC 2) ---
def show_qr_interface(root, port):
    LOCAL_IP = get_local_ip()
    TOKEN = get_session_token() # Lấy token từ api.py
    SERVER_URL = f"http://{LOCAL_IP}:{port}/?token={TOKEN}"
    
    # Tạo biến lưu đường dẫn tuyệt đối đến thư mục uploads
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                custom_path = config.get("upload_path")
                if custom_path:
                    upload_dir = os.path.abspath(custom_path)
                else:
                    upload_dir = os.path.abspath(os.path.join(os.getcwd(), "uploads"))
        except Exception as e:
            print(f"Lỗi đọc file config, sử dụng mặc định: {e}")
            upload_dir = os.path.abspath(os.path.join(os.getcwd(), "uploads"))
    else:
        upload_dir = os.path.abspath(os.path.join(os.getcwd(), "uploads"))

    threading.Thread(target=run_fastapi_server, args=("0.0.0.0", port), daemon=True).start()

    main_frame = tk.Frame(root, bg="#e0e0e0", bd=2, relief=tk.GROOVE)
    main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    # ================= ĐOẠN CODE THÊM MỚI (NÚT CÀI ĐẶT) =================
    def on_restart():
        if messagebox.askyesno("Khởi động lại", "Bạn có muốn quay lại màn hình chọn cổng?\n(Việc này sẽ khởi động lại ứng dụng và ngắt kết nối hiện tại)"):
            root.destroy()
            try:
                # Lệnh này sẽ khởi động lại chính file .py hoặc .exe đang chạy
                os.execl(sys.executable, sys.executable, *sys.argv)
            except Exception as e:
                # Backup trong trường hợp execl gặp sự cố (hiếm khi xảy ra)
                import subprocess
                subprocess.Popen([sys.executable] + sys.argv)
                os._exit(0)

    # Đặt nút ở góc trên bên trái bằng place()
    btn_settings = tk.Button(main_frame, text="Cài đặt", font=("Arial", 10), bg="#8fa6d4", fg="white", cursor="hand2", command=on_restart)
    btn_settings.place(x=10, y=10) 
    # ====================================================================

    tk.Label(main_frame, text="Quét mã QR để vào web:", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(pady=(20, 10))

    try:
        qr = qrcode.QRCode(version=1, box_size=6, border=2)
        qr.add_data(SERVER_URL)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        tk_img = ImageTk.PhotoImage(qr_img)
        qr_label = tk.Label(main_frame, image=tk_img, bg="#e0e0e0")
        qr_label.image = tk_img 
        qr_label.pack(pady=10)
    except Exception as e:
        tk.Label(main_frame, text=f"Lỗi tạo QR: {e}", fg="red").pack()

    tk.Label(main_frame, text=f"""Truy cập:"""
             , font=("Arial", 10), bg="#e0e0e0", fg="blue").pack(pady=5)
    tk.Label(main_frame, text=f"""{SERVER_URL}"""
             , font=("Arial", 10), bg="#e0e0e0", fg="blue").pack(pady=5)
    tk.Label(main_frame, text="Lưu ý: Nếu Firewall hiện lên, hãy chọn 'Allow access'.", font=("Arial", 8, "italic"), bg="#e0e0e0", fg="red").pack(pady=5)

    tk.Label(main_frame, text="Thư mục lưu file (Bôi đen để Copy):", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333").pack(pady=(15, 5))
    
    path_entry = tk.Entry(main_frame, font=("Arial", 10), justify="center")
    path_entry.insert(0, upload_dir)
    path_entry.config(state="readonly") 
    path_entry.pack(fill=tk.X, padx=30, pady=(0, 10))


# --- MÀN HÌNH CHỌN CỔNG & THƯ MỤC LƯU (BƯỚC 1) ---
def create_gui():
    root = tk.Tk()
    root.title("Transmit files - v1")
    
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    icon_path = resource_path("appIcon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
        
    window_width = 500
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    root.configure(bg="#e0e0e0")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    port_frame = tk.Frame(root, bg="#e0e0e0")
    port_frame.pack(expand=True)

    # 1. KHU VỰC NHẬP PORT
    tk.Label(port_frame, text="Nhập cổng (Port) để chạy server:", font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=(0, 10))
    port_entry = tk.Entry(port_frame, font=("Arial", 14), justify="center", width=10)
    port_entry.insert(0, "8000")
    port_entry.pack(pady=5)

    def on_start_server():
        port_str = port_entry.get().strip()
        try:
            port = int(port_str)
            if not is_port_free(port):
                messagebox.showerror("Lỗi", f"Cổng {port} đang bận, hãy thử cổng khác!")
                return
            
            port_frame.destroy()
            show_qr_interface(root, port)
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")

    tk.Button(port_frame, text="Khởi động Server", font=("Arial", 11), bg="#4caf50", fg="white", cursor="hand2", command=on_start_server).pack(pady=(15, 40))

    # 2. KHU VỰC CHỌN THƯ MỤC
    # Đọc config.json nếu có
    initial_path = ""
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                initial_path = config.get("upload_path", "")
        except Exception:
            pass
    else:
        initial_path = os.path.abspath(os.path.join(os.getcwd(), "uploads"))

    # Frame chứa Label và Nút Folder Icon
    folder_label_frame = tk.Frame(port_frame, bg="#e0e0e0")
    folder_label_frame.pack(pady=(0, 5))

    tk.Label(folder_label_frame, text="Chọn đường dẫn lưu file:", font=("Arial", 12), bg="#e0e0e0").pack(side=tk.LEFT)

    # Hàm xử lý khi bấm nút chọn folder
    def choose_folder():
        selected_dir = filedialog.askdirectory(title="Chọn thư mục lưu file")
        if selected_dir: # Nếu người dùng không nhấn Cancel
            # Chuyển đổi định dạng đường dẫn cho chuẩn Windows/Linux
            selected_dir = os.path.normpath(selected_dir)
            
            # Cập nhật hiển thị trên UI
            path_entry_step1.config(state="normal")
            path_entry_step1.delete(0, tk.END)
            path_entry_step1.insert(0, selected_dir)
            path_entry_step1.config(state="readonly")
            
            # Lưu vào config.json
            try:
                with open("config.json", "w", encoding="utf-8") as f:
                    # ensure_ascii=False để không bị lỗi font nếu đường dẫn có tiếng Việt
                    json.dump({"upload_path": selected_dir}, f, indent=4, ensure_ascii=False)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file config: {e}")

    # Nút icon folder
    btn_folder = tk.Button(folder_label_frame, text="(chọn thư mục*)", font=("Arial", 10), bg="#4caf50", fg="white", cursor="hand2", command=choose_folder)
    btn_folder.pack(side=tk.LEFT, padx=(5, 0))

    # Ô hiển thị đường dẫn đã chọn (Readonly)
    path_entry_step1 = tk.Entry(port_frame, font=("Arial", 12), justify="center", width=35)
    path_entry_step1.insert(0, initial_path)
    path_entry_step1.config(state="readonly")
    path_entry_step1.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()