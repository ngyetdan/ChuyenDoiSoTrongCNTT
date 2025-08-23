# database_config_window.py - Cửa sổ cấu hình database

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from database_manager import DatabaseManager
import json
import os

class DatabaseConfigWindow:
    """Cửa sổ cấu hình kết nối database"""
    
    def __init__(self, parent, callback=None):
        """
        Khởi tạo cửa sổ cấu hình database
        
        Args:
            parent: Cửa sổ cha
            callback: Hàm callback khi cấu hình thành công
        """
        self.parent = parent
        self.callback = callback
        self.db_manager = None
        
        # Tạo cửa sổ
        self.window = tk.Toplevel(parent)
        self.window.title("🗄️ Cấu Hình Database SQL Server")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # Đặt cửa sổ ở giữa màn hình
        self.center_window()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Load cấu hình đã lưu
        self.load_saved_config()
        
        # Focus vào cửa sổ
        self.window.transient(parent)
        self.window.grab_set()
        self.window.focus_set()
    
    def center_window(self):
        """Đặt cửa sổ ở giữa màn hình"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
    
    def create_widgets(self):
        """Tạo các widget giao diện"""
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="🗄️ Cấu Hình Database SQL Server", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame cấu hình
        config_frame = ttk.LabelFrame(main_frame, text="Thông Tin Kết Nối", padding="15")
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Server Name
        ttk.Label(config_frame, text="Tên Server:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.server_var = tk.StringVar(value="localhost")
        server_entry = ttk.Entry(config_frame, textvariable=self.server_var, width=40)
        server_entry.grid(row=0, column=1, sticky=tk.W+tk.E, padx=(10, 0), pady=5)
        
        # Database Name
        ttk.Label(config_frame, text="Tên Database:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.database_var = tk.StringVar(value="GradeManagement")
        database_entry = ttk.Entry(config_frame, textvariable=self.database_var, width=40)
        database_entry.grid(row=1, column=1, sticky=tk.W+tk.E, padx=(10, 0), pady=5)
        
        # Cấu hình grid
        config_frame.columnconfigure(1, weight=1)
        
        # Frame thông tin
        info_frame = ttk.LabelFrame(main_frame, text="Thông Tin", padding="15")
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        info_text = """
🔐 Sử dụng Windows Authentication
📝 Đảm bảo SQL Server đã bật và cho phép kết nối
🔧 Nếu database chưa tồn tại, ứng dụng sẽ tự động tạo
📊 Các bảng cần thiết sẽ được tạo tự động
        """
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
        
        # Frame nút bấm
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Nút Test Connection
        self.test_btn = ttk.Button(button_frame, text="🔍 Test Kết Nối", 
                                  command=self.test_connection)
        self.test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Nút Create Database
        self.create_db_btn = ttk.Button(button_frame, text="🗄️ Tạo Database", 
                                       command=self.create_database)
        self.create_db_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Nút Create Tables
        self.create_tables_btn = ttk.Button(button_frame, text="📋 Tạo Bảng", 
                                           command=self.create_tables)
        self.create_tables_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Text area cho log
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Tạo text widget với scrollbar
        text_frame = ttk.Frame(log_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(text_frame, height=8, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame nút cuối
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        
        # Nút Save & Close
        ttk.Button(bottom_frame, text="💾 Lưu & Đóng", 
                  command=self.save_and_close).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Nút Cancel
        ttk.Button(bottom_frame, text="❌ Hủy", 
                  command=self.window.destroy).pack(side=tk.RIGHT)
    
    def log_message(self, message: str, level: str = "INFO"):
        """Ghi log vào text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.window.update()
    
    def start_progress(self):
        """Bắt đầu progress bar"""
        self.progress.start(10)
        self.test_btn.config(state='disabled')
        self.create_db_btn.config(state='disabled')
        self.create_tables_btn.config(state='disabled')
    
    def stop_progress(self):
        """Dừng progress bar"""
        self.progress.stop()
        self.test_btn.config(state='normal')
        self.create_db_btn.config(state='normal')
        self.create_tables_btn.config(state='normal')
    
    def test_connection(self):
        """Test kết nối database trong thread riêng"""
        def test_thread():
            self.start_progress()
            self.log_message("Đang test kết nối...")
            
            try:
                server = self.server_var.get().strip()
                database = self.database_var.get().strip()
                
                if not server:
                    self.log_message("Vui lòng nhập tên server", "ERROR")
                    return
                
                if not database:
                    self.log_message("Vui lòng nhập tên database", "ERROR")
                    return
                
                # Tạo database manager
                self.db_manager = DatabaseManager(server, database)
                
                # Test kết nối
                success, message = self.db_manager.test_connection()
                
                if success:
                    self.log_message(f"✅ {message}", "SUCCESS")
                    messagebox.showinfo("Thành công", "Kết nối database thành công!")
                else:
                    self.log_message(f"❌ {message}", "ERROR")
                    
                    # Nếu database không tồn tại, hỏi có muốn tạo không
                    if "không tồn tại" in message:
                        if messagebox.askyesno("Tạo Database", 
                                             f"Database '{database}' không tồn tại.\nBạn có muốn tạo database mới không?"):
                            self.create_database()
                
            except Exception as e:
                self.log_message(f"❌ Lỗi: {str(e)}", "ERROR")
                messagebox.showerror("Lỗi", f"Lỗi test kết nối: {str(e)}")
            finally:
                self.stop_progress()
        
        # Chạy trong thread riêng để không block UI
        threading.Thread(target=test_thread, daemon=True).start()
    
    def create_database(self):
        """Tạo database mới"""
        def create_db_thread():
            self.start_progress()
            self.log_message("Đang tạo database...")
            
            try:
                server = self.server_var.get().strip()
                database = self.database_var.get().strip()
                
                if not server or not database:
                    self.log_message("Vui lòng nhập đầy đủ thông tin", "ERROR")
                    return
                
                # Tạo database manager
                if not self.db_manager:
                    self.db_manager = DatabaseManager(server, database)
                
                # Tạo database
                success, message = self.db_manager.create_database()
                
                if success:
                    self.log_message(f"✅ {message}", "SUCCESS")
                    messagebox.showinfo("Thành công", "Tạo database thành công!")
                    
                    # Tự động tạo bảng
                    self.create_tables()
                else:
                    self.log_message(f"❌ {message}", "ERROR")
                    messagebox.showerror("Lỗi", f"Lỗi tạo database: {message}")
                
            except Exception as e:
                self.log_message(f"❌ Lỗi: {str(e)}", "ERROR")
                messagebox.showerror("Lỗi", f"Lỗi tạo database: {str(e)}")
            finally:
                self.stop_progress()
        
        threading.Thread(target=create_db_thread, daemon=True).start()
    
    def create_tables(self):
        """Tạo các bảng cần thiết"""
        def create_tables_thread():
            self.start_progress()
            self.log_message("Đang tạo bảng...")
            
            try:
                server = self.server_var.get().strip()
                database = self.database_var.get().strip()
                
                if not server or not database:
                    self.log_message("Vui lòng nhập đầy đủ thông tin", "ERROR")
                    return
                
                # Tạo database manager
                if not self.db_manager:
                    self.db_manager = DatabaseManager(server, database)
                
                # Tạo bảng
                success, message = self.db_manager.create_tables()
                
                if success:
                    self.log_message(f"✅ {message}", "SUCCESS")
                    messagebox.showinfo("Thành công", "Tạo bảng thành công!")
                else:
                    self.log_message(f"❌ {message}", "ERROR")
                    messagebox.showerror("Lỗi", f"Lỗi tạo bảng: {message}")
                
            except Exception as e:
                self.log_message(f"❌ Lỗi: {str(e)}", "ERROR")
                messagebox.showerror("Lỗi", f"Lỗi tạo bảng: {str(e)}")
            finally:
                self.stop_progress()
        
        threading.Thread(target=create_tables_thread, daemon=True).start()
    
    def save_config(self):
        """Lưu cấu hình vào file"""
        config = {
            "server_name": self.server_var.get().strip(),
            "database_name": self.database_var.get().strip()
        }
        
        try:
            with open("database_config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            self.log_message("✅ Đã lưu cấu hình", "SUCCESS")
        except Exception as e:
            self.log_message(f"❌ Lỗi lưu cấu hình: {str(e)}", "ERROR")
    
    def load_saved_config(self):
        """Load cấu hình đã lưu"""
        try:
            if os.path.exists("database_config.json"):
                with open("database_config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                self.server_var.set(config.get("server_name", "localhost"))
                self.database_var.set(config.get("database_name", "GradeManagement"))
                self.log_message("✅ Đã load cấu hình đã lưu", "INFO")
        except Exception as e:
            self.log_message(f"⚠️ Không thể load cấu hình: {str(e)}", "WARNING")
    
    def save_and_close(self):
        """Lưu cấu hình và đóng cửa sổ"""
        # Lưu cấu hình
        self.save_config()
        
        # Gọi callback nếu có
        if self.callback and self.db_manager:
            self.callback(self.db_manager)
        
        # Đóng cửa sổ
        self.window.destroy()

# Import datetime cho log_message
from datetime import datetime
