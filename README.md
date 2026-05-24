# 🚀 Transmit Files

**Transmit Files** là ứng dụng chia sẻ file tốc độ cao trong mạng nội bộ (LAN), cho phép bạn truyền tải dữ liệu giữa máy tính và các thiết bị di động (điện thoại, máy tính bảng) thông qua kết nối Wi-Fi một cách nhanh chóng mà không cần Internet hay dây cáp kết nối.

---

## ✨ Các tính năng chính

* **Không cần cài đặt phức tạp:** Chạy trực tiếp file `.exe` tiện lợi hoặc khởi chạy nhanh chóng từ mã nguồn Python.
* **Kết nối thông minh:** Hỗ trợ quét mã QR để truy cập nhanh giao diện tải file từ điện thoại/máy tính bảng.
* **Bảo mật phiên làm việc:** Mỗi phiên khởi động được cấp một mật mã (Token) ngẫu nhiên, đảm bảo chỉ thiết bị quét mã QR đúng mới có quyền truy cập và truyền file.
* **Tốc độ tối đa:** Truyền dữ liệu trực tiếp qua mạng băng thông nội bộ, không bị bóp băng thông bởi Internet.
* **Thân thiện & Tối giản:** Giao diện trực quan, không yêu cầu quyền Quản trị viên (Admin) phức tạp để vận hành thông thường.

---

## 📂 Định dạng file hỗ trợ

Ứng dụng tối ưu hóa và hỗ trợ tải lên đa dạng các loại định dạng file:

| Loại dữ liệu | Định dạng hỗ trợ |
| :--- | :--- |
| **🖼️ Hình ảnh** | `.jpg`, `.jpeg`, `.png` |
| **🎥 Video** | `.mp4`, `.mov` |
| **🎵 Âm thanh** | `.mp3` |
| **📄 Tài liệu** | `.pdf`, `.docx`, `.txt`, `.text` |

---

## 🛠️ Hướng dẫn cài đặt và chạy từ mã nguồn (Cách 1)

Nếu bạn muốn phát triển hoặc chạy ứng dụng trực tiếp bằng mã nguồn Python, hãy thực hiện theo các bước dưới đây:

### 1. Yêu cầu tiên quyết
* Đã cài đặt **[Python](https://www.python.org/downloads/)** (phiên bản 3.9 trở lên).
* Đã tích hợp công cụ quản lý thư viện `pip`.

### 2. Thiết lập môi trường
Mở Terminal (hoặc PowerShell / Command Prompt) tại thư mục gốc của dự án và chạy các lệnh sau:

* **Tạo môi trường ảo (Virtual Environment):**
    ```bash
    python -m venv venv
    ```

* **Kích hoạt môi trường ảo:**
    * *Trên Windows (PowerShell):*
        ```powershell
        .\venv\Scripts\activate
        ```
    * *Trên Windows (CMD):*
        ```cmd
        .\venv\Scripts\Activate.bat
        ```
    * *Trên macOS/Linux:*
        ```bash
        source venv/bin/activate
        ```

* **Cài đặt các thư viện phụ thuộc:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Hướng dẫn sử dụng chi tiết
1.  Khởi động giao diện chính của ứng dụng bằng lệnh:
    ```bash
    python main.py
    ```
2.  Nhập cổng (**Port**) kết nối mong muốn (Mặc định là `8000` hoặc nhập một cổng bất kỳ đang trống).
3.  Nhấn nút **"Khởi động Server"**.
4.  **Lưu ý quan trọng:** Khi hộp thoại *Windows Defender Firewall* hiển thị lần đầu, hãy tích chọn và nhấn **"Allow access"** để cho phép các thiết bị khác trong mạng kết nối tới máy tính của bạn.
5.  Dùng điện thoại hoặc máy tính bảng quét mã QR hiển thị trên màn hình máy tính để truy cập trang tải file.
6.  Chọn file cần truyền từ thiết bị di động và nhấn **Upload**. File tải lên sẽ tự động lưu vào thư mục máy tính của bạn.

---

## 📦 Phiên bản đóng gói & Tùy chỉnh nâng cao (Cách 2)

Nếu bạn muốn sở hữu phiên bản đóng gói sẵn cài đặt như các ứng dụng Windows thông thường, cấu hình chạy ẩn, hoặc có nhu cầu hiệu chỉnh tính năng riêng theo yêu cầu, vui lòng liên hệ:
* 📩 **Email:** [phanhuyhoang0203@gmail.com](mailto:phanhuyhoang0203@gmail.com)

---

## 💻 Yêu cầu hệ thống

* **Hệ điều hành:** Windows 10 / Windows 11.
* **Kết nối mạng:** Máy tính và thiết bị di động (điện thoại/máy tính bảng) bắt buộc phải kết nối chung một mạng Wi-Fi/LAN.

---

## ⚠️ Lưu ý quan trọng cho người dùng

* **Windows Firewall:** Trong lần đầu tiên khởi chạy, nếu hệ thống không thể kết nối, hãy kiểm tra tường lửa Windows và đảm bảo đã cấp quyền truy cập công khai/nội bộ cho ứng dụng.
* **Chế độ mạng Wi-Fi:** Hãy đảm bảo cấu hình mạng Wi-Fi trên Windows của bạn đang ở chế độ **"Private"** (Riêng tư) để các thiết bị khác trong mạng LAN có thể tìm thấy và kết nối được với máy tính.
* **Thư mục lưu trữ:** Tất cả các file được tải lên thành công từ điện thoại sẽ xuất hiện tại thư mục `uploads` nằm ngay cùng cấp vị trí với file chạy ứng dụng của bạn.

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

* **Backend:** FastAPI (Python)
* **Frontend:** HTML5 / JavaScript, Jinja2 template engine
* **Giao diện Desktop:** Tkinter (Python)

---
*Phát triển và bảo trì bởi **PhanHuyHoang0203***
