# OCR Grade Table Extractor

OCR Grade Table Extractor là công cụ giúp tự động **trích xuất dữ liệu từ bảng điểm sinh viên** trong ảnh và chuyển đổi thành **Excel** hoặc lưu trực tiếp vào **SQL Server**.  
Ứng dụng sử dụng **Google Gemini Vision API** để nhận diện chính xác cả **chữ in và chữ viết tay**.

---


## ✨ Tính năng

### 1. Trích xuất thông minh
- Nhận diện **chữ in + chữ viết tay** trong cùng một ảnh  
- Tự động phát hiện **cấu trúc bảng điểm**  
- Hỗ trợ ảnh mờ, nghiêng, chất lượng thấp  
- Hỗ trợ nhiều định dạng: PNG, JPG, JPEG, BMP, TIFF  

### 2. Xử lý dữ liệu
- Kiểm tra & **sửa lỗi tự động** (MSV, tên, điểm số)  
- Chuẩn hóa tên tiếng Việt có dấu  
- Loại bỏ sinh viên trùng lặp theo MSV  
- Gộp dữ liệu từ nhiều template khác nhau  

### 3. Xuất dữ liệu
- Xuất **Excel (.xlsx)** với định dạng chuyên nghiệp  
- Lưu vào **SQL Server** (xử lý trùng lặp tự động)  
- Thống kê chi tiết: điểm trung bình, phân bố lớp  

### 4. Cấu hình linh hoạt
- 4 template có sẵn: CNTT chuẩn, Đơn giản, Chi tiết, Đại học  
- Cho phép tạo **template tùy chỉnh**  
- Cấu hình prompt AI dễ dàng  

---

## ⚡ Cài đặt

### Yêu cầu hệ thống
- Python **3.8+**  
- Windows (khuyến nghị)  
- SQL Server (tùy chọn, cho tính năng lưu DB)  

### Thư viện chính
- **tkinter** – Giao diện người dùng  
- **pandas** – Xử lý dữ liệu  
- **openpyxl** – Xuất file Excel  
- **Pillow** – Xử lý ảnh  
- **google-generativeai** – Tích hợp Gemini API  
- **pyodbc** – Kết nối SQL Server
  
### 🛠 Các bước cài đặt

1. **Clone repository**
   ```bash
   git clone https://github.com/Yennguyen124/Tu-dong-nhap-bang-diem-sinh-vien-qua-hinh-anh-su-dung-OCR.git
2. **Cài đặt dependencies**
   ```bash
   pip install -r requirements.txt

### 3  .Lấy API Key miễn phí
- Truy cập Google AI Studio
- Tạo API Key cho Gemini
- Nhập API Key vào ứng dụng khi được yêu cầu
4. **Chạy chương trình**
   ```bash
   python main.py
   


##  Hướng dẫn sử dụng

1. **Cấu hình API**  
   - Nhập **Gemini API Key** (miễn phí).  
   - Nhấn **"Kiểm tra hệ thống"** để xác nhận.  

2. **Chọn ảnh**  
   - Nhấn **"Chọn ảnh"** để upload bảng điểm.  
   - Hỗ trợ các định dạng: PNG, JPG, JPEG, BMP, TIFF.  

3. **Trích xuất dữ liệu**  
   - Nhấn **"Trích xuất dữ liệu"**.  
   - Hệ thống sẽ tự động:  
     - Thử template hiện tại.  
     - Thử template chữ viết tay nếu cần.  
     - Gộp kết quả từ nhiều template.  
     - Loại bỏ dữ liệu trùng lặp.  

4. **Lưu kết quả**  
   - Xuất file Excel (.xlsx) với định dạng chuẩn.  
   - Hoặc lưu trực tiếp vào SQL Server (tự động xử lý trùng lặp).  

---

## ✨ Tính năng nổi bật

### 🤖 AI thông minh  
- Sử dụng **Google Gemini Vision** – AI tiên tiến.  
- Tự động nhận diện cấu trúc bảng điểm.  
- Hỗ trợ cả chữ in và chữ viết tay trong cùng một ảnh.  

### 🎯 Độ chính xác cao  
- Validation thông minh với database tên tiếng Việt.  
- Tự động sửa lỗi OCR.  
- Loại bỏ dữ liệu trùng lặp theo **Mã Sinh Viên (MSV)**.  

### 💡 Hoàn toàn miễn phí  
- Sử dụng **Gemini API miễn phí**.  
- Không giới hạn số lượng ảnh xử lý.  
- **Mã nguồn mở**, dễ dàng tùy chỉnh và phát triển.

## Hình ảnh demo


<img width="1876" height="1025" alt="image" src="https://github.com/user-attachments/assets/8eb181e1-dbda-4cc0-8758-e6bc31d57b8d" />
<img width="1505" height="1031" alt="image" src="https://github.com/user-attachments/assets/63862d88-8ee3-4bb0-ab0a-ac1ebff6893f" />
<img width="1505" height="1031" alt="image" src="https://github.com/user-attachments/assets/308ed8c5-ea4b-41d5-b1b2-572cc1e9442c" />
<img width="1843" height="1023" alt="image" src="https://github.com/user-attachments/assets/9a69ccd7-bba9-4e3e-8e2c-9d1b6c7b1cb9" />




