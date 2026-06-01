<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Gemini_Vision_API-4285F4?style=for-the-badge&logo=google&logoColor=white"/>
<img src="https://img.shields.io/badge/SQL_Server-CC2927?style=for-the-badge&logo=microsoftsqlserver&logoColor=white"/>
<img src="https://img.shields.io/badge/Excel_Export-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white"/>

# 📊 OCR Grade Table Extractor

**Tự động trích xuất bảng điểm sinh viên từ ảnh — hỗ trợ cả chữ in lẫn chữ viết tay.**

Ứng dụng sử dụng **Google Gemini Vision API** để nhận diện và chuyển đổi dữ liệu thành file Excel hoặc lưu thẳng vào SQL Server, với độ chính xác lên đến **93–97%**.

[🎥 Xem Demo](https://drive.google.com/file/d/1ScCwLsb9wyB02us2pqNhJPm1CS9ZbEjE/view?usp=sharing) · [🐛 Báo lỗi](https://github.com/Yennguyen124/Tu-dong-nhap-bang-diem-sinh-vien-qua-hinh-anh-su-dung-OCR/issues) · [⭐ Star dự án](https://github.com/Yennguyen124/Tu-dong-nhap-bang-diem-sinh-vien-qua-hinh-anh-su-dung-OCR)

</div>

---

## ✨ Tính năng

| Nhóm | Chi tiết |
|------|----------|
| 🔍 Trích xuất | Nhận diện chữ in + chữ viết tay, hỗ trợ ảnh mờ/nghiêng/chất lượng thấp |
| 🛠 Xử lý dữ liệu | Tự động sửa lỗi OCR, chuẩn hóa tên tiếng Việt, loại bỏ trùng lặp theo MSV |
| 💾 Xuất dữ liệu | Xuất Excel (.xlsx) định dạng chuẩn hoặc lưu vào SQL Server |
| ⚙️ Cấu hình | 4 template có sẵn + hỗ trợ tạo template tùy chỉnh |

**Định dạng ảnh hỗ trợ:** PNG · JPG · JPEG · BMP · TIFF

---

## 🖼 Giao diện

<img width="1876" alt="Màn hình chính" src="https://github.com/user-attachments/assets/8eb181e1-dbda-4cc0-8758-e6bc31d57b8d"/>
<img width="1505" alt="Kết quả trích xuất" src="https://github.com/user-attachments/assets/63862d88-8ee3-4bb0-ab0a-ac1ebff6893f"/>
<img width="1505" alt="Xuất Excel" src="https://github.com/user-attachments/assets/308ed8c5-ea4b-41d5-b1b2-572cc1e9442c"/>
<img width="1843" alt="Lưu SQL Server" src="https://github.com/user-attachments/assets/9a69ccd7-bba9-4e3e-8e2c-9d1b6c7b1cb9"/>

---

## ⚡ Cài đặt

### Yêu cầu
- Python **3.8+**
- Windows (khuyến nghị)
- SQL Server *(tùy chọn)*

### Các bước

**1. Clone repo**
```bash
git clone https://github.com/Yennguyen124/Tu-dong-nhap-bang-diem-sinh-vien-qua-hinh-anh-su-dung-OCR.git
cd Tu-dong-nhap-bang-diem-sinh-vien-qua-hinh-anh-su-dung-OCR
```

**2. Cài dependencies**
```bash
pip install -r requirements.txt
```

**3. Lấy API Key miễn phí**

Truy cập [Google AI Studio](https://ai.google.dev/) → tạo API Key → nhập vào ứng dụng khi được yêu cầu.

**4. Chạy ứng dụng**
```bash
python main.py
```

---

## 📖 Hướng dẫn sử dụng

```
1. Nhập Gemini API Key  →  nhấn "Kiểm tra hệ thống"
2. Nhấn "Chọn ảnh"      →  upload bảng điểm cần xử lý
3. Nhấn "Trích xuất"    →  hệ thống tự động nhận diện & gộp kết quả
4. Lưu kết quả          →  xuất Excel hoặc lưu vào SQL Server
```

> Hệ thống tự động thử nhiều template, gộp kết quả và loại bỏ dữ liệu trùng lặp theo MSV.

---

## 📦 Thư viện sử dụng

| Thư viện | Phiên bản | Mục đích |
|----------|-----------|----------|
| `google-generativeai` | 0.3.2 | Tích hợp Gemini Vision API |
| `pandas` | 2.0.3 | Xử lý dữ liệu bảng |
| `openpyxl` | 3.1.2 | Xuất file Excel |
| `Pillow` | 10.0.1 | Xử lý ảnh |
| `pyodbc` | 4.0.39 | Kết nối SQL Server |
| `requests` | 2.31.0 | HTTP requests |

---

## 🗂 Cấu trúc dự án

```
📁 project/
├── main.py                  # Điểm khởi chạy
├── gui.py                   # Giao diện Tkinter
├── ocr_processor.py         # Xử lý OCR & Gemini API
├── data_validator.py        # Validation & sửa lỗi dữ liệu
├── excel_exporter.py        # Xuất file Excel
├── database_manager.py      # Kết nối & thao tác SQL Server
├── database_config_window.py# Cấu hình kết nối DB
├── grade_table_app.py       # Logic ứng dụng chính
├── prompt_manager.py        # Quản lý prompt AI
├── settings_window.py       # Cửa sổ cài đặt
├── config.py                # Cấu hình hệ thống
├── prompt_templates.json    # Template prompt có sẵn
├── database_config.json     # Cấu hình database
└── requirements.txt         # Dependencies
```

---

<div align="center">

Nếu thấy project hữu ích, hãy để lại một ⭐ để ủng hộ nhóm nhé!

Được phát triển bởi **Nhóm 9** — Ngành Hệ Thống Thông Tin, Đại học Đại Nam

</div>
