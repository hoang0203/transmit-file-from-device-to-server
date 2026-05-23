import os
import logging
import threading
import tkinter as tk
import socket
import sys

import qrcode
import uvicorn


from tkinter import messagebox

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
    upload_dir = os.path.abspath(os.path.join(os.getcwd(), "uploads"))

    threading.Thread(target=run_fastapi_server, args=("0.0.0.0", port), daemon=True).start()

    main_frame = tk.Frame(root, bg="#e0e0e0", bd=2, relief=tk.GROOVE)
    main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
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

    # --- ĐOẠN MÃ THÊM MỚI: HIỂN THỊ ĐƯỜNG DẪN THƯ MỤC UPLOADS ---
    tk.Label(main_frame, text="Thư mục lưu file (Bôi đen để Copy):", font=("Arial", 10, "bold"), bg="#e0e0e0", fg="#333").pack(pady=(15, 5))
    
    # Dùng tk.Entry để người dùng có thể bôi đen và copy
    path_entry = tk.Entry(main_frame, font=("Arial", 10), justify="center")
    path_entry.insert(0, upload_dir)
    path_entry.config(state="readonly") # Đặt chỉ đọc để người dùng không vô tình xóa mất text
    path_entry.pack(fill=tk.X, padx=30, pady=(0, 10))

# --- MÀN HÌNH CHỌN CỔNG (BƯỚC 1) ---
def create_gui():
    root = tk.Tk()
    root.title("Transmit files - v1")
    # --- CÁCH THIẾT LẬP ICON ---
    def resource_path(relative_path):
        """ Lấy đường dẫn tuyệt đối tới tài nguyên, hoạt động cho cả khi chạy script và đã build exe """
        try:
            # PyInstaller tạo một thư mục tạm và lưu đường dẫn trong _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # Đặt icon (đảm bảo file appIcon.ico nằm cùng thư mục với main.py khi develop)
    icon_path = resource_path("appIcon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
        
    # --- ĐOẠN CODE CĂN GIỮA MÀN HÌNH ---
    window_width = 500
    window_height = 600
    
    # Lấy kích thước của màn hình máy tính
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Tính toán tọa độ x, y để đặt cửa sổ vào giữa
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    
    # Đặt kích thước và vị trí xuất hiện (format: widthxheight+x+y)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # -----------------------------------

    root.configure(bg="#e0e0e0")

    # Gán hàm on_closing vào sự kiện đóng cửa sổ
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    port_frame = tk.Frame(root, bg="#e0e0e0")
    port_frame.pack(expand=True)

    tk.Label(port_frame, text="Nhập cổng (Port) để chạy server:", font=("Arial", 12, "bold"), bg="#e0e0e0").pack(pady=10)
    port_entry = tk.Entry(port_frame, font=("Arial", 14), justify="center", width=10)
    port_entry.insert(0, "8000")
    port_entry.pack(pady=10)

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

    tk.Button(port_frame, text="Khởi động Server", font=("Arial", 11), bg="#4caf50", fg="white", command=on_start_server).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()