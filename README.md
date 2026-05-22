# Transmit Files - Chia sẻ file trong mạng LAN

Transmit Files là ứng dụng nhỏ gọn, cho phép bạn chia sẻ file nhanh chóng giữa máy tính và các thiết bị khác (điện thoại, máy tính bảng) cùng kết nối mạng Wi-Fi mà không cần thông qua Internet.

## Các tính năng chính
- **Không cần cài đặt:** Chạy trực tiếp file `.exe`.
- **Kết nối dễ dàng:** Quét mã QR để truy cập nhanh từ điện thoại.
- **Bảo mật:** Mỗi phiên làm việc được cấp một Token ngẫu nhiên, đảm bảo chỉ người quét QR mới có quyền truy cập.
- **Tốc độ cao:** Truyền dữ liệu trực tiếp trong mạng LAN.
- **Không quyền Admin:** Ứng dụng chạy an toàn dưới quyền người dùng thông thường.

## Định dạng file hỗ trợ
Ứng dụng cho phép tải lên các loại file sau:
- **Hình ảnh:** `.jpg`, `.jpeg`, `.png`
- **Video:** `.mp4`, `.mov`
- **Âm thanh:** `.mp3`
- **Tài liệu:** `.pdf`, `.docx`, `.txt`, `.text`

## Cách sử dụng
1. Mở ứng dụng `TransmitFiles.exe`.
2. Nhập cổng (Port) mặc định là `8000` (hoặc cổng bất kỳ đang trống).
3. Nhấn **"Khởi động Server"**.
4. Khi cửa sổ Windows Firewall hiện lên, hãy chọn **"Allow access"** để cho phép thiết bị khác kết nối.
5. Dùng điện thoại quét mã QR hiển thị trên màn hình.
6. Chọn file cần tải lên và nhấn nút Upload. File sẽ được lưu tự động vào thư mục `/uploads` trên máy tính của bạn.

## Yêu cầu hệ thống
- Hệ điều hành: Windows 10/11.
- Cùng mạng Wi-Fi giữa thiết bị gửi (điện thoại) và máy tính.

## Lưu ý cho người dùng
- **Windows Firewall:** Lần đầu tiên chạy, Windows có thể chặn kết nối. Hãy đảm bảo bạn nhấn "Allow access" cho ứng dụng.
- **Mạng:** Đảm bảo mạng Wi-Fi đang kết nối ở chế độ "Private" để thiết bị khác có thể nhìn thấy máy tính của bạn.
- **Đường dẫn:** Tất cả file bạn tải lên từ điện thoại sẽ xuất hiện trong thư mục `uploads` cùng nơi bạn đặt file `.exe`.

## Thông tin kỹ thuật
- **Backend:** FastAPI (Python)
- **Frontend:** HTML/JS, Jinja2
- **Đóng gói:** PyInstaller
- **Giao diện:** Tkinter

---
*Phát triển bởi PhanHuyHoang0203*