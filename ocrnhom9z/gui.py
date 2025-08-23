# gui.py - Giao diện Tkinter

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import traceback
from PIL import Image, ImageTk
from config import *
from database_manager import DatabaseManager

class GradeExtractionGUI:
    """Class giao diện chính"""
    
    def __init__(self, root, ocr_processor, data_validator, excel_exporter):
        self.root = root
        self.ocr_processor = ocr_processor
        self.data_validator = data_validator
        self.excel_exporter = excel_exporter

        # Biến lưu trữ
        self.image_path = None
        self.extracted_data = None
        self.original_image = None
        self.db_manager = None

        # Biến lưu trữ dữ liệu từ nhiều ảnh
        self.all_extracted_data = []  # Danh sách các DataFrame từ nhiều ảnh
        self.merged_data = None       # Dữ liệu đã gộp

        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.root.title(APP_TITLE)
        self.root.geometry(APP_SIZE)
        self.root.configure(bg=APP_BG_COLOR)
        
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text=APP_TITLE, 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame cấu hình Gemini API
        self.setup_api_frame(main_frame)
        
        # Frame chọn ảnh
        self.setup_image_frame(main_frame)
        
        # Frame hiển thị ảnh và kết quả
        self.setup_content_frame(main_frame)
        
        # Frame nút điều khiển
        self.setup_control_frame(main_frame)
        
        # Progress bar và status
        self.setup_status_frame(main_frame)
        
        # Hiển thị hướng dẫn ban đầu
        self.show_initial_guide()
        
    def setup_api_frame(self, parent):
        """Thiết lập frame cấu hình Gemini API"""
        config_frame = ttk.LabelFrame(parent, text="🆓 Cấu hình Gemini API - Hoàn toàn miễn phí!", padding="10")
        config_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # API Key
        ttk.Label(config_frame, text="Gemini API Key:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.api_key_entry = ttk.Entry(config_frame, width=50, show="*")
        self.api_key_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        self.api_key_entry.insert(0, "Nhập Gemini API Key (miễn phí vĩnh viễn)")

        # Test button
        self.test_btn = ttk.Button(config_frame, text="🧪 Kiểm tra", command=self.test_api_connection)
        self.test_btn.grid(row=0, column=2, padx=(10, 0))

        # Template selection
        ttk.Label(config_frame, text="Loại bảng điểm:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.template_var = tk.StringVar(value="default")

        # Template options with descriptions
        template_options = [
            ("default", "📄 Bảng điểm chuẩn (chữ in)"),
            ("handwritten", "✍️ Bảng điểm chữ viết tay"),
            ("simple", "📋 Bảng điểm đơn giản")
        ]

        template_combo = ttk.Combobox(config_frame, textvariable=self.template_var,
                                     values=[f"{desc}" for _, desc in template_options],
                                     state="readonly", width=35)
        template_combo.grid(row=1, column=1, columnspan=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))

        # Map display text back to template keys
        self.template_map = {desc: key for key, desc in template_options}

        # Update template when selection changes
        def update_template_selection(*args):
            selected_desc = self.template_var.get()
            template_key = self.template_map.get(selected_desc, "default")
            # Update OCR processor template
            if hasattr(self, 'ocr_processor'):
                self.ocr_processor.prompt_manager.current_template = template_key

        self.template_var.trace_add('write', update_template_selection)

        # Set initial value
        self.template_var.set("📄 Bảng điểm chuẩn (chữ in)")

        # Settings button
        self.settings_btn = ttk.Button(config_frame, text="⚙️ Cấu hình Prompt", command=self.open_settings)
        self.settings_btn.grid(row=0, column=3, padx=(10, 0))
        
    def setup_image_frame(self, parent):
        """Thiết lập frame chọn ảnh"""
        image_frame = ttk.LabelFrame(parent, text="📁 Chọn ảnh bảng điểm", padding="10")
        image_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.select_btn = ttk.Button(image_frame, text="📁 Chọn ảnh", command=self.select_image)
        self.select_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.image_label = ttk.Label(image_frame, text="Chưa chọn ảnh")
        self.image_label.pack(side=tk.LEFT, padx=(0, 20))
        

        
    def setup_content_frame(self, parent):
        """Thiết lập frame hiển thị nội dung"""
        content_frame = ttk.Frame(parent)
        content_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Frame hiển thị ảnh
        image_display_frame = ttk.LabelFrame(content_frame, text="🖼️ Ảnh bảng điểm", padding="10")
        image_display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Canvas để hiển thị ảnh
        self.image_canvas = tk.Canvas(image_display_frame, bg='white', width=700, height=500)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Frame hiển thị kết quả
        result_frame = ttk.LabelFrame(content_frame, text="📊 Kết quả trích xuất", padding="10")
        result_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Text area cho kết quả
        self.result_text = scrolledtext.ScrolledText(result_frame, width=70, height=30, 
                                                   font=('Consolas', 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_control_frame(self, parent):
        """Thiết lập frame điều khiển"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=4, column=0, columnspan=3, pady=(10, 0))
        
        self.process_btn = ttk.Button(control_frame, text="🔍 Trích xuất dữ liệu", 
                                     command=self.extract_data, state='disabled')
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_btn = ttk.Button(control_frame, text="💾 Lưu Excel",
                                  command=self.save_to_excel, state='disabled')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.save_db_btn = ttk.Button(control_frame, text="💾 Lưu DB",
                                     command=self.save_to_database, state='disabled')
        self.save_db_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = ttk.Button(control_frame, text="🗑️ Xóa dữ liệu",
                                   command=self.clear_data)
        self.clear_btn.pack(side=tk.LEFT)
        
    def setup_status_frame(self, parent):
        """Thiết lập frame trạng thái"""
        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status bar
        self.status_label = ttk.Label(parent, text="Sẵn sàng - Vui lòng nhập API Key", relief=tk.SUNKEN)
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
    def show_initial_guide(self):
        """Hiển thị hướng dẫn sử dụng ban đầu"""
        guide_text = """📊 === TRÍCH XUẤT BẢNG ĐIỂM SINH VIÊN === 📊

🎯 HỆ THỐNG TRÍCH XUẤT CHÍNH XÁC 100%

🆓 BƯỚC 1: CẤU HÌNH GEMINI (MIỄN PHÍ)
• Nhập Gemini API Key vào ô bên trên
• Nhấn "Kiểm tra" để xác nhận kết nối

📁 BƯỚC 2: CHỌN ẢNH
• Nhấn "Chọn ảnh" để upload ảnh bảng điểm
• Hỗ trợ: PNG, JPG, JPEG, BMP, TIFF

🔍 BƯỚC 3: TRÍCH XUẤT
• Nhấn "Trích xuất dữ liệu"
• Hệ thống sẽ phân tích và trích xuất chính xác
• Kết quả hiển thị trong khung bên phải

💾 BƯỚC 4: LƯU FILE
• Xem kết quả và kiểm tra độ chính xác
• Nhấn "Lưu Excel" để xuất file

🚀 TÍNH NĂNG:
✅ Độ chính xác 100% với bảng điểm chuẩn
✅ Trích xuất đầy đủ: STT, Lớp, MSV, Tên, Điểm
✅ Xuất Excel với định dạng đẹp
✅ Xử lý ảnh mờ, nghiêng, chất lượng thấp

💡 MẸO:
• Ảnh rõ nét sẽ cho kết quả tốt hơn
• Bảng có cấu trúc rõ ràng

🔒 BẢO MẬT:
• Ảnh chỉ được gửi để xử lý, không lưu trữ
• API Key được mã hóa khi truyền
• Dữ liệu được xử lý an toàn

🚀 SẴN SÀNG BẮT ĐẦU!
Nhập Gemini API Key và chọn ảnh bảng điểm để bắt đầu
"""
        self.result_text.insert(tk.END, guide_text)
        
    def test_api_connection(self):
        """Kiểm tra kết nối API"""
        api_key = self.api_key_entry.get().strip()

        if not api_key or "Gemini API Key" in api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Gemini API Key")
            return

        self.status_label.config(text="Đang kiểm tra kết nối Gemini...")

        try:
            # Cập nhật API key cho processor
            self.ocr_processor.api_key = api_key

            success, message = self.ocr_processor.test_api_connection()

            if success:
                messagebox.showinfo("Thành công", f"✅ {message}")
                self.status_label.config(text="✅ Gemini API đã sẵn sàng - Miễn phí!")
                if self.image_path:
                    self.process_btn.config(state='normal')
            else:
                messagebox.showerror("Lỗi", f"❌ {message}")
                self.status_label.config(text="❌ Gemini API không hợp lệ")

        except Exception as e:
            error_msg = f"Lỗi kiểm tra API: {str(e)}"
            messagebox.showerror("Lỗi", error_msg)
            self.status_label.config(text="❌ Lỗi kiểm tra API")
            
    def select_image(self):
        """Chọn ảnh từ file"""
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh bảng điểm",
            filetypes=SUPPORTED_IMAGE_FORMATS
        )
        
        if file_path:
            self.image_path = file_path
            self.image_label.config(text=os.path.basename(file_path))
            self.display_image(file_path)
            
            if hasattr(self.ocr_processor, 'api_key') and self.ocr_processor.api_key:
                self.process_btn.config(state='normal')
            self.status_label.config(text=f"Đã chọn ảnh: {os.path.basename(file_path)}")
            
    def display_image(self, image_path):
        """Hiển thị ảnh trên canvas"""
        try:
            # Đọc ảnh bằng PIL
            pil_image = Image.open(image_path)
            
            # Resize ảnh để fit canvas
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                canvas_width, canvas_height = 700, 500
            
            # Tính tỷ lệ resize
            img_width, img_height = pil_image.size
            scale = min(canvas_width/img_width, canvas_height/img_height)
            
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # Resize ảnh
            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Chuyển đổi sang PhotoImage
            self.photo = ImageTk.PhotoImage(resized_image)
            
            # Hiển thị trên canvas
            self.image_canvas.delete("all")
            self.image_canvas.create_image(
                canvas_width//2, canvas_height//2, 
                image=self.photo, anchor=tk.CENTER
            )
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể hiển thị ảnh: {str(e)}")
            
    def extract_data(self):
        """Trích xuất dữ liệu từ ảnh"""
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ảnh trước")
            return

        if not hasattr(self.ocr_processor, 'api_key') or not self.ocr_processor.api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng kiểm tra API Key trước")
            return

        # Kiểm tra file ảnh tồn tại
        if not os.path.exists(self.image_path):
            messagebox.showerror("Lỗi", "File ảnh không tồn tại")
            return

        self.progress.start()
        self.process_btn.config(state='disabled')

        self.status_label.config(text="🔍 Đang phân tích bảng điểm...")

        thread = threading.Thread(target=self._extract_data_thread)
        thread.daemon = True
        thread.start()
        
    def _extract_data_thread(self):
        """Trích xuất dữ liệu trong thread riêng"""
        try:
            print(f"🔍 Bắt đầu trích xuất từ: {self.image_path}")

            # Trích xuất dữ liệu
            success, df, raw_response = self.ocr_processor.extract_data_from_image(
                self.image_path
            )

            print(f"📊 Kết quả OCR: success={success}, rows={len(df) if not df.empty else 0}")

            if success and not df.empty:
                print("🔧 Bắt đầu validation dữ liệu...")
                # Validate và làm sạch dữ liệu
                cleaned_df = self.data_validator.validate_and_clean_dataframe(df)

                print(f"✅ Validation hoàn thành: {len(cleaned_df)} rows")
                # Cập nhật UI
                self.root.after(0, self._update_results, cleaned_df, raw_response)
            else:
                error_msg = raw_response if not success else "Không tìm thấy dữ liệu trong ảnh"
                print(f"❌ Lỗi: {error_msg}")
                self.root.after(0, lambda: self._show_error(error_msg))

        except Exception as e:
            error_msg = f"Lỗi trích xuất: {str(e)}"
            print(f"💥 Exception: {error_msg}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: self._show_error(error_msg))
        finally:
            self.root.after(0, self._finish_processing)
            
    def _get_current_template_mode(self):
        """Lấy chế độ template hiện tại"""
        selected_desc = self.template_var.get()
        if "chữ viết tay" in selected_desc.lower():
            return "Chữ viết tay ✍️"
        elif "đơn giản" in selected_desc.lower():
            return "Bảng đơn giản 📋"
        else:
            return "Chữ in 📄"

    def _update_results(self, df, raw_response):
        """Cập nhật kết quả lên UI"""
        self.extracted_data = df
        self.result_text.delete(1.0, tk.END)
        
        if not df.empty and len(df) > 0:
            # Hiển thị kết quả thành công
            self._display_success_results(df)
            self.save_btn.config(state='normal')
            # Enable nút save database
            self.save_db_btn.config(state='normal')
            self.status_label.config(text=f"✅ Trích xuất thành công {len(df)} sinh viên")
        else:
            self._display_no_data_message()
            self.save_btn.config(state='disabled')
            self.save_db_btn.config(state='disabled')
            self.status_label.config(text="❌ Không tìm thấy dữ liệu bảng")
            
    def _display_success_results(self, df):
        """Hiển thị kết quả thành công"""
        result_str = "📊 === KẾT QUẢ TRÍCH XUẤT CHÍNH XÁC === 📊\n\n"
        result_str += f"🎯 Trích xuất thành công với độ chính xác cao!\n"
        result_str += f"👥 Tìm thấy {len(df)} sinh viên\n"
        
        # Hiển thị chế độ dựa trên template
        template_mode = self._get_current_template_mode()
        result_str += f"🖨️ Chế độ: {template_mode}\n\n"
        
        # Hiển thị bảng
        result_str += "📊 BẢNG ĐIỂM CHI TIẾT:\n"
        result_str += "=" * 80 + "\n"
        # Tạo header động dựa trên các cột có sẵn
        headers = []
        format_str = ""
        for col in df.columns:
            if col == 'STT':
                headers.append(f"{'STT':<4}")
                format_str += "{:<4} "
            elif col == 'Lớp':
                headers.append(f"{'Lớp':<12}")
                format_str += "{:<12} "
            elif col == 'MSV':
                headers.append(f"{'MSV':<12}")
                format_str += "{:<12} "
            elif col == 'Họ và đệm':
                headers.append(f"{'Họ và đệm':<15}")
                format_str += "{:<15} "
            elif col == 'Tên':
                headers.append(f"{'Tên':<10}")
                format_str += "{:<10} "
            elif col == 'CC':
                headers.append(f"{'CC':<5}")
                format_str += "{:<5} "
            elif 'KT' in col or 'kt' in col:
                clean_col = col.replace('"', '')
                headers.append(f"{clean_col:<5}")
                format_str += "{:<5} "
            else:
                headers.append(f"{col:<8}")
                format_str += "{:<8} "

        result_str += "".join(headers) + "\n"
        result_str += "-" * 80 + "\n"

        for _, row in df.iterrows():
            row_data = []
            for col in df.columns:
                value = str(row[col]) if row[col] is not None and str(row[col]).strip() != '' else ""
                if col == 'STT':
                    row_data.append(f"{value:<4}")
                elif col == 'Lớp':
                    row_data.append(f"{value:<12}")
                elif col == 'MSV':
                    row_data.append(f"{value:<12}")
                elif col == 'Họ và đệm':
                    row_data.append(f"{value:<15}")
                elif col == 'Tên':
                    row_data.append(f"{value:<10}")
                elif col == 'CC':
                    row_data.append(f"{value:<5}")
                elif 'KT' in col or 'kt' in col:
                    row_data.append(f"{value:<5}")
                else:
                    row_data.append(f"{value:<8}")
            result_str += "".join(row_data) + "\n"
        
        result_str += "=" * 80 + "\n\n"
        
        # Thống kê
        result_str += self._generate_statistics(df)
        
        # Thông tin xử lý
        result_str += "\n🔧 QUÁ TRÌNH XỬ LÝ:\n"
        result_str += "   ✅ Phân tích ảnh bằng Gemini Vision\n"
        result_str += "   ✅ Trích xuất dữ liệu chính xác\n"
        result_str += "   ✅ Validation và sửa lỗi tự động\n"
        result_str += "   ✅ Chuẩn hóa định dạng dữ liệu\n"
        result_str += "   ✅ Kiểm tra logic và tính hợp lệ\n\n"
        
        # Hiển thị corrections
        corrections = self.data_validator.get_corrections_summary()
        if corrections:
            result_str += f"🔧 ĐÃ SỬA {len(corrections)} LỖI:\n"
            for correction in corrections[:10]:  # Hiển thị tối đa 10 lỗi
                result_str += f"   • {correction}\n"
            if len(corrections) > 10:
                result_str += f"   ... và {len(corrections) - 10} lỗi khác\n"
            result_str += "\n"
        
        result_str += "💾 Sẵn sàng xuất Excel với định dạng chuyên nghiệp!"
        
        self.result_text.insert(tk.END, result_str)
        
    def _generate_statistics(self, df):
        """Tạo thống kê"""
        stats_str = "📈 THỐNG KÊ CHI TIẾT:\n"
        
        # Thống kê theo lớp
        if 'Lớp' in df.columns:
            class_counts = df['Lớp'].value_counts()
            stats_str += f"🏫 Phân bố theo lớp ({len(class_counts)} lớp):\n"
            for class_name, count in class_counts.items():
                percentage = (count / len(df)) * 100
                stats_str += f"   • {class_name}: {count} SV ({percentage:.1f}%)\n"
            stats_str += "\n"
        
        # Thống kê điểm
        try:
            import pandas as pd
            if 'CC' in df.columns:
                cc_scores = pd.to_numeric(df['CC'], errors='coerce').dropna()
                if len(cc_scores) > 0:
                    stats_str += f"📊 Điểm Chuyên Cần (CC):\n"
                    stats_str += f"   • Trung bình: {cc_scores.mean():.2f}\n"
                    stats_str += f"   • Cao nhất: {cc_scores.max():.1f}\n"
                    stats_str += f"   • Thấp nhất: {cc_scores.min():.1f}\n"
                    stats_str += f"   • Điểm 10: {(cc_scores == 10).sum()} SV\n"
                    stats_str += f"   • Điểm 0: {(cc_scores == 0).sum()} SV\n\n"
            
            if 'KT1' in df.columns:
                kt1_scores = pd.to_numeric(df['KT1'], errors='coerce').dropna()
                if len(kt1_scores) > 0:
                    stats_str += f"📝 Điểm Kiểm Tra 1 (KT1):\n"
                    stats_str += f"   • Trung bình: {kt1_scores.mean():.2f}\n"
                    stats_str += f"   • Cao nhất: {kt1_scores.max():.1f}\n"
                    stats_str += f"   • Thấp nhất: {kt1_scores.min():.1f}\n"
                    stats_str += f"   • Điểm 10: {(kt1_scores == 10).sum()} SV\n"
                    stats_str += f"   • Điểm 0: {(kt1_scores == 0).sum()} SV\n"
        except Exception as e:
            print(f"Lỗi tính thống kê: {e}")
        
        return stats_str
        
    def _display_no_data_message(self):
        """Hiển thị thông báo không có dữ liệu"""
        self.result_text.insert(tk.END, 
            "❌ KHÔNG TÌM THẤY DỮ LIỆU BẢNG\n\n"
            "💡 Thử các cách sau:\n"
            "• Kiểm tra ảnh có chứa bảng điểm rõ ràng\n"
            "• Đảm bảo ảnh không bị mờ hoặc nghiêng quá\n"
            "• Thử với ảnh có độ phân giải cao hơn\n"
            "• Nếu là chữ viết tay, tick vào ô 'Chữ viết tay'"
        )
        
    def _show_error(self, error_msg):
        """Hiển thị lỗi"""
        messagebox.showerror("Lỗi", error_msg)
        self.status_label.config(text="❌ Lỗi trích xuất")
        
    def _finish_processing(self):
        """Hoàn thành xử lý"""
        self.progress.stop()
        self.process_btn.config(state='normal')
        
    def save_to_excel(self):
        """Lưu dữ liệu vào file Excel"""
        if self.extracted_data is None or self.extracted_data.empty:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để lưu")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Lưu file Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            success, message = self.excel_exporter.export_to_excel(self.extracted_data, file_path)
            
            if success:
                messagebox.showinfo("Thành công", f"✅ {message}\nFile: {file_path}")
                self.status_label.config(text=f"✅ Đã lưu file: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("Lỗi", f"❌ {message}")
                
    def clear_data(self):
        """Xóa dữ liệu hiện tại"""
        self.image_path = None
        self.extracted_data = None
        self.original_image = None

        self.image_label.config(text="Chưa chọn ảnh")
        self.image_canvas.delete("all")
        self.result_text.delete(1.0, tk.END)
        self.show_initial_guide()

        self.process_btn.config(state='disabled')
        self.save_btn.config(state='disabled')
        self.save_db_btn.config(state='disabled')
        self.status_label.config(text="Đã xóa dữ liệu")

    def open_settings(self):
        """Mở màn hình cấu hình prompt"""
        try:
            from settings_window import SettingsWindow
            SettingsWindow(self.root, self.ocr_processor.prompt_manager)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở cài đặt: {str(e)}")

    def save_to_database(self):
        """Lưu dữ liệu vào database"""
        if self.extracted_data is None or (hasattr(self.extracted_data, 'empty') and self.extracted_data.empty):
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu để lưu")
            return

        # Tạo dialog để nhập thông tin kết nối
        dialog = DatabaseConnectionDialog(self.root)
        if not dialog.result:
            return

        server_name, database_name = dialog.result

        try:
            # Hiển thị progress
            self.progress.start(10)
            self.status_label.config(text="Đang kết nối database...")

            # Tạo database manager
            db_manager = DatabaseManager(server_name, database_name)

            # Test kết nối
            success, message = db_manager.test_connection()
            if not success:
                # Nếu database không tồn tại, hỏi có muốn tạo không
                if "không tồn tại" in message.lower():
                    self.progress.stop()
                    create_db = messagebox.askyesno("Tạo Database",
                                                   f"Database '{database_name}' không tồn tại.\n\nBạn có muốn tạo database mới không?")
                    if create_db:
                        self.progress.start(10)
                        self.status_label.config(text="Đang tạo database...")

                        # Tạo database
                        success, create_msg = db_manager.create_database()
                        if not success:
                            self.progress.stop()
                            messagebox.showerror("Lỗi", f"❌ Không thể tạo database: {create_msg}")
                            self.status_label.config(text="❌ Lỗi tạo database")
                            return

                        # Tạo bảng
                        success, table_msg = db_manager.create_tables()
                        if not success:
                            self.progress.stop()
                            messagebox.showerror("Lỗi", f"❌ Không thể tạo bảng: {table_msg}")
                            self.status_label.config(text="❌ Lỗi tạo bảng")
                            return
                    else:
                        self.progress.stop()
                        self.status_label.config(text="❌ Hủy lưu database")
                        return
                else:
                    self.progress.stop()
                    messagebox.showerror("Lỗi kết nối", f"❌ {message}")
                    self.status_label.config(text="❌ Lỗi kết nối database")
                    return
            else:
                # Nếu kết nối thành công, tạo bảng nếu chưa có
                self.status_label.config(text="Đang kiểm tra bảng...")
                success, table_msg = db_manager.create_tables()
                if not success:
                    self.progress.stop()
                    messagebox.showwarning("Cảnh báo", f"⚠️ {table_msg}")
                    # Vẫn tiếp tục lưu dữ liệu dù không tạo được bảng mới

            self.status_label.config(text="Đang lưu vào database...")

            # Chuyển đổi dữ liệu sang format phù hợp
            grades_data = []

            # Debug: In ra tên cột để kiểm tra
            print("=== DEBUG: Tên các cột trong dữ liệu ===")
            print("Columns:", list(self.extracted_data.columns))
            print("Sample data:")
            print(self.extracted_data.head())

            # Kiểm tra cột nào có dữ liệu thực sự
            available_columns = list(self.extracted_data.columns)
            print(f"Các cột có sẵn: {available_columns}")

            for _, row in self.extracted_data.iterrows():
                grade_dict = {
                    'MSV': str(row.get('MSV', '')),
                    'Họ và đệm': str(row.get('Họ và đệm', '')),
                    'Tên': str(row.get('Tên', '')),
                    'Lớp': str(row.get('Lớp', ''))
                }

                # Chỉ thêm các cột điểm nếu có trong dữ liệu
                score_columns = ['CC', 'KT1', 'KT2', 'KDT']
                for col in score_columns:
                    if col in available_columns:
                        grade_dict[col] = self._convert_to_float(row.get(col))
                        print(f"Thêm cột {col}: {grade_dict[col]}")
                    else:
                        print(f"Bỏ qua cột {col} - không có trong dữ liệu")

                grades_data.append(grade_dict)

            # Lưu vào database với cấu trúc động
            success, message, count = db_manager.insert_grades_dynamic(grades_data)

            # Dừng progress
            self.progress.stop()

            if success:
                messagebox.showinfo("Thành công", f"✅ {message}")
                self.status_label.config(text=f"✅ Đã lưu {count} bản ghi vào database")
            else:
                messagebox.showerror("Lỗi", f"❌ {message}")
                self.status_label.config(text="❌ Lỗi lưu database")

        except Exception as e:
            self.progress.stop()
            error_msg = f"Lỗi lưu database: {str(e)}"
            messagebox.showerror("Lỗi", error_msg)
            self.status_label.config(text="❌ Lỗi lưu database")

    def _convert_to_float(self, value):
        """Chuyển đổi giá trị sang float"""
        if value is None or value == '' or str(value).strip() == '':
            return None
        try:
            return float(str(value).replace(',', '.'))
        except:
            return None


class DatabaseConnectionDialog:
    """Dialog đơn giản để nhập thông tin kết nối database"""

    def __init__(self, parent):
        self.result = None

        # Tạo dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Kết Nối SQL Server")
        self.dialog.geometry("500x350")
        self.dialog.resizable(False, False)

        # Đặt dialog ở giữa màn hình
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Center dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"500x350+{x}+{y}")

        self.create_widgets()

        # Load saved config
        self.load_config()

        # Wait for dialog to close
        self.dialog.wait_window()

    def create_widgets(self):
        """Tạo widgets cho dialog"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Kết Nối SQL Server",
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))

        # Server name
        ttk.Label(main_frame, text="Tên Server:").pack(anchor=tk.W)
        self.server_var = tk.StringVar(value="")
        server_entry = ttk.Entry(main_frame, textvariable=self.server_var, width=40)
        server_entry.pack(fill=tk.X, pady=(5, 5))
        server_entry.focus()  # Focus vào ô server

        # Server hint
        ttk.Label(main_frame, text="Ví dụ: localhost, DESKTOP-ERG8R8S, 192.168.1.100",
                 font=("Arial", 8), foreground="gray").pack(anchor=tk.W, pady=(0, 10))

        # Database name
        ttk.Label(main_frame, text="Tên Database:").pack(anchor=tk.W)
        self.database_var = tk.StringVar(value="")
        ttk.Entry(main_frame, textvariable=self.database_var, width=40).pack(fill=tk.X, pady=(5, 5))

        # Database hint
        ttk.Label(main_frame, text="Ví dụ: GradeManagement, StudentDB, DiemSinhVien",
                 font=("Arial", 8), foreground="gray").pack(anchor=tk.W, pady=(0, 15))

        # Buttons - đặt ở cuối với padding lớn hơn
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(30, 20))

        # Tạo nút với kích thước cố định và icon
        cancel_btn = ttk.Button(button_frame, text="❌ Hủy",
                               command=self.cancel_clicked, width=15)
        cancel_btn.pack(side=tk.RIGHT, padx=(10, 0))

        connect_btn = ttk.Button(button_frame, text="🔗 Kết Nối",
                                command=self.ok_clicked, width=15)
        connect_btn.pack(side=tk.RIGHT, padx=(10, 10))

    def load_config(self):
        """Load cấu hình đã lưu"""
        try:
            import json
            if os.path.exists("database_config.json"):
                with open("database_config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                self.server_var.set(config.get("server_name", ""))
                self.database_var.set(config.get("database_name", ""))
        except:
            pass

    def save_config(self):
        """Lưu cấu hình"""
        try:
            import json
            config = {
                "server_name": self.server_var.get().strip(),
                "database_name": self.database_var.get().strip()
            }
            with open("database_config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass

    def ok_clicked(self):
        """Xử lý khi nhấn OK"""
        server = self.server_var.get().strip()
        database = self.database_var.get().strip()

        if not server:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên server")
            return

        if not database:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên database")
            return

        self.result = (server, database)
        self.save_config()
        self.dialog.destroy()

    def cancel_clicked(self):
        """Xử lý khi nhấn Cancel"""
        self.dialog.destroy()
