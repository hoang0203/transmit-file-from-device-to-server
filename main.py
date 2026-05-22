import os
import threading
import tkinter as tk
import socket

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
    uvicorn.run(app, host=host, port=port, log_level="warning")

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
    upload_dir = os.path.join(os.getcwd(), "uploads")

    threading.Thread(target=run_fastapi_server, args=("0.0.0.0", port), daemon=True).start()

    main_frame = tk.Frame(root, bg="#e0e0e0", bd=2, relief=tk.GROOVE)
    main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    tk.Label(main_frame, text="Transmit files - v1", font=("Arial", 12, "bold"), bg="#e0e0e0", anchor="w").pack(fill=tk.X, padx=10, pady=(10, 0))
    tk.Label(main_frame, text="Quét mã QR để vào web:", font=("Arial", 14, "bold"), bg="#e0e0e0").pack(pady=(20, 10))

    try:
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(SERVER_URL)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        tk_img = ImageTk.PhotoImage(qr_img)
        qr_label = tk.Label(main_frame, image=tk_img, bg="#e0e0e0")
        qr_label.image = tk_img 
        qr_label.pack(pady=10)
    except Exception as e:
        tk.Label(main_frame, text=f"Lỗi tạo QR: {e}", fg="red").pack()

    tk.Label(main_frame, text=f"Truy cập: {SERVER_URL}", font=("Arial", 10), bg="#e0e0e0", fg="blue").pack(pady=5)
    tk.Label(main_frame, text="Lưu ý: Nếu Firewall hiện lên, hãy chọn 'Allow access'.", font=("Arial", 8, "italic"), bg="#e0e0e0", fg="red").pack(pady=5)

# --- MÀN HÌNH CHỌN CỔNG (BƯỚC 1) ---
def create_gui():
    root = tk.Tk()
    root.title("Transmit files - v1")
    root.geometry("500x550")
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