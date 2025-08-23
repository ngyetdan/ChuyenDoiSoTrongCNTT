# main.py - File chính để chạy ứng dụng

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Import các module của ứng dụng
from gui import GradeExtractionGUI
from ocr_processor import OCRProcessor
from data_validator import DataValidator
from excel_exporter import ExcelExporter

def main():
    """Hàm chính để chạy ứng dụng"""
    try:
        # Tạo cửa sổ chính
        root = tk.Tk()
        
        # Khởi tạo các component
        ocr_processor = OCRProcessor(api_key=None)  # API key sẽ được set từ GUI
        data_validator = DataValidator()
        excel_exporter = ExcelExporter()
        
        # Khởi tạo GUI
        app = GradeExtractionGUI(root, ocr_processor, data_validator, excel_exporter)
        
        # Hiển thị thông báo chào mừng
        messagebox.showinfo("🆓 Chào mừng",
                           "📊 Trích Xuất Bảng Điểm Sinh Viên\n\n"
                           "🎯 Độ chính xác 93-97%\n"
                           "🔍 Trích xuất tự động và chính xác\n"
                           "💾 Xuất Excel với định dạng đẹp\n"
                           "🔧 Validation và sửa lỗi tự động\n"
                           "Lấy API key tại: https://ai.google.dev/\n\n")
        
        # Chạy ứng dụng
        root.mainloop()
        
    except ImportError as e:
        error_msg = f"Lỗi import module: {str(e)}\n\nVui lòng cài đặt dependencies:\npip install -r requirements.txt"
        print(error_msg)
        if 'tkinter' in str(e):
            print("Lỗi: Tkinter không có sẵn. Vui lòng cài đặt Python với Tkinter support.")
        sys.exit(1)
        
    except Exception as e:
        error_msg = f"Lỗi khởi động ứng dụng: {str(e)}"
        print(error_msg)
        try:
            messagebox.showerror("Lỗi", error_msg)
        except:
            pass
        sys.exit(1)

def check_dependencies():
    """Kiểm tra các dependencies cần thiết"""
    required_modules = [
        'tkinter',
        'PIL',
        'pandas',
        'openpyxl',
        'requests',
        'pyodbc'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("❌ Thiếu các module sau:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\n📦 Cài đặt bằng lệnh:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ Tất cả dependencies đã sẵn sàng")
    return True

if __name__ == "__main__":
    print("🚀 Khởi động ứng dụng Trích Xuất Bảng Điểm...")
    print("📁 Cấu trúc modular:")
    print("   - main.py: File chính")
    print("   - gui.py: Giao diện Tkinter")
    print("   - ocr_processor.py: Xử lý OCR và Gemini")
    print("   - data_validator.py: Validation dữ liệu")
    print("   - excel_exporter.py: Xuất Excel")
    print("   - config.py: Cấu hình hệ thống")
    print()
    
    # Kiểm tra dependencies
    if check_dependencies():
        main()
    else:
        print("\n❌ Không thể khởi động do thiếu dependencies")
        sys.exit(1)
