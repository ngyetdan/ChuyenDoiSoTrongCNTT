# settings_window.py - Màn hình cấu hình prompt OCR

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from prompt_manager import PromptManager

class SettingsWindow:
    """Màn hình cấu hình prompt OCR"""
    
    def __init__(self, parent, prompt_manager):
        self.parent = parent
        self.prompt_manager = prompt_manager
        self.window = None
        self.current_template_name = ""
        self.columns_data = []
        
        self.create_window()
    
    def create_window(self):
        """Tạo cửa sổ setting"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚙️ Cấu hình Prompt OCR")
        self.window.geometry("1200x800")
        self.window.configure(bg="#f0f0f0")
        
        # Đặt cửa sổ ở giữa màn hình
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Frame chính
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = ttk.Label(main_frame, text="⚙️ Cấu hình Prompt OCR", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Notebook cho các tab
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab quản lý templates
        self.create_templates_tab(notebook)
        
        # Tab chỉnh sửa template
        self.create_editor_tab(notebook)
        
        # Tab preview
        self.create_preview_tab(notebook)
        
        # Frame nút điều khiển
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="💾 Lưu", 
                  command=self.save_settings).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="❌ Hủy", 
                  command=self.close_window).pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="🔄 Khôi phục mặc định", 
                  command=self.reset_to_default).pack(side=tk.LEFT)
    
    def create_templates_tab(self, notebook):
        """Tạo tab quản lý templates"""
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text="📋 Quản lý Templates")
        
        # Frame trái - danh sách templates
        left_frame = ttk.LabelFrame(tab_frame, text="📋 Danh sách Templates", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Listbox templates
        self.templates_listbox = tk.Listbox(left_frame, height=15)
        self.templates_listbox.pack(fill=tk.BOTH, expand=True)
        self.templates_listbox.bind('<<ListboxSelect>>', self.on_template_select)
        
        # Frame nút cho templates
        templates_btn_frame = ttk.Frame(left_frame)
        templates_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(templates_btn_frame, text="➕ Thêm mới", 
                  command=self.add_new_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(templates_btn_frame, text="📝 Sao chép", 
                  command=self.copy_template).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(templates_btn_frame, text="🗑️ Xóa", 
                  command=self.delete_template).pack(side=tk.LEFT)
        
        # Frame phải - thông tin template
        right_frame = ttk.LabelFrame(tab_frame, text="ℹ️ Thông tin Template", padding="10")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Tên template
        ttk.Label(right_frame, text="Tên Template:").pack(anchor=tk.W)
        self.template_name_var = tk.StringVar()
        self.template_name_entry = ttk.Entry(right_frame, textvariable=self.template_name_var, width=40)
        self.template_name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Mô tả template
        ttk.Label(right_frame, text="Mô tả:").pack(anchor=tk.W)
        self.template_desc_text = scrolledtext.ScrolledText(right_frame, height=4, width=40)
        self.template_desc_text.pack(fill=tk.X, pady=(0, 10))
        
        # Template hiện tại
        current_frame = ttk.Frame(right_frame)
        current_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(current_frame, text="Template hiện tại:").pack(side=tk.LEFT)
        self.current_template_label = ttk.Label(current_frame, text="", 
                                               font=('Arial', 10, 'bold'), 
                                               foreground="blue")
        self.current_template_label.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(current_frame, text="✅ Đặt làm mặc định", 
                  command=self.set_as_current).pack(side=tk.RIGHT)
        
        # Tải danh sách templates
        self.load_templates_list()
    
    def create_editor_tab(self, notebook):
        """Tạo tab chỉnh sửa template"""
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text="📝 Chỉnh sửa Template")
        
        # Frame trên - cấu trúc cột
        columns_frame = ttk.LabelFrame(tab_frame, text="📊 Cấu trúc cột bảng điểm", padding="10")
        columns_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Treeview cho cột
        columns_tree_frame = ttk.Frame(columns_frame)
        columns_tree_frame.pack(fill=tk.X)
        
        self.columns_tree = ttk.Treeview(columns_tree_frame, 
                                        columns=('key', 'name', 'type', 'description'), 
                                        show='headings', height=6)
        
        # Định nghĩa cột
        self.columns_tree.heading('key', text='Key')
        self.columns_tree.heading('name', text='Tên hiển thị')
        self.columns_tree.heading('type', text='Loại dữ liệu')
        self.columns_tree.heading('description', text='Mô tả')
        
        self.columns_tree.column('key', width=80)
        self.columns_tree.column('name', width=120)
        self.columns_tree.column('type', width=100)
        self.columns_tree.column('description', width=200)
        
        self.columns_tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Scrollbar cho treeview
        columns_scrollbar = ttk.Scrollbar(columns_tree_frame, orient=tk.VERTICAL, 
                                         command=self.columns_tree.yview)
        columns_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.columns_tree.configure(yscrollcommand=columns_scrollbar.set)
        
        # Nút quản lý cột
        columns_btn_frame = ttk.Frame(columns_frame)
        columns_btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(columns_btn_frame, text="➕ Thêm cột", 
                  command=self.add_column).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(columns_btn_frame, text="📝 Sửa cột", 
                  command=self.edit_column).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(columns_btn_frame, text="🗑️ Xóa cột", 
                  command=self.delete_column).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(columns_btn_frame, text="⬆️ Lên", 
                  command=self.move_column_up).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(columns_btn_frame, text="⬇️ Xuống", 
                  command=self.move_column_down).pack(side=tk.LEFT)
        
        # Frame dưới - prompt template
        prompt_frame = ttk.LabelFrame(tab_frame, text="📝 Prompt Template", padding="10")
        prompt_frame.pack(fill=tk.BOTH, expand=True)
        
        self.prompt_text = scrolledtext.ScrolledText(prompt_frame, height=15, width=80)
        self.prompt_text.pack(fill=tk.BOTH, expand=True)
    
    def create_preview_tab(self, notebook):
        """Tạo tab preview"""
        tab_frame = ttk.Frame(notebook)
        notebook.add(tab_frame, text="👁️ Preview")
        
        # Frame thông tin
        info_frame = ttk.LabelFrame(tab_frame, text="ℹ️ Thông tin Template", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.preview_info_text = scrolledtext.ScrolledText(info_frame, height=4, width=80)
        self.preview_info_text.pack(fill=tk.X)
        
        # Frame prompt preview
        preview_frame = ttk.LabelFrame(tab_frame, text="👁️ Preview Prompt", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=20, width=80, 
                                                     state=tk.DISABLED)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Nút refresh preview
        ttk.Button(tab_frame, text="🔄 Refresh Preview", 
                  command=self.refresh_preview).pack(pady=(10, 0))
    
    def load_templates_list(self):
        """Tải danh sách templates"""
        self.templates_listbox.delete(0, tk.END)
        
        template_names = self.prompt_manager.get_template_names()
        current_template = self.prompt_manager.current_template
        
        for name in template_names:
            template = self.prompt_manager.get_template(name)
            display_name = f"{template.get('name', name)}"
            if name == current_template:
                display_name += " ⭐"
            
            self.templates_listbox.insert(tk.END, display_name)
        
        # Cập nhật label template hiện tại
        current_template_info = self.prompt_manager.get_template(current_template)
        if current_template_info:
            self.current_template_label.config(text=current_template_info.get('name', current_template))
    
    def on_template_select(self, event):
        """Xử lý khi chọn template"""
        selection = self.templates_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        template_names = self.prompt_manager.get_template_names()
        
        if index < len(template_names):
            template_name = template_names[index]
            self.load_template_data(template_name)
    
    def load_template_data(self, template_name):
        """Tải dữ liệu template"""
        template = self.prompt_manager.get_template(template_name)
        if not template:
            return
        
        self.current_template_name = template_name
        
        # Cập nhật thông tin cơ bản
        self.template_name_var.set(template.get('name', ''))
        
        self.template_desc_text.delete(1.0, tk.END)
        self.template_desc_text.insert(1.0, template.get('description', ''))
        
        # Cập nhật cấu trúc cột
        self.load_columns_data(template.get('columns', []))
        
        # Cập nhật prompt
        self.prompt_text.delete(1.0, tk.END)
        self.prompt_text.insert(1.0, template.get('prompt_template', ''))
        
        # Refresh preview
        self.refresh_preview()
    
    def load_columns_data(self, columns):
        """Tải dữ liệu cột"""
        # Xóa dữ liệu cũ
        for item in self.columns_tree.get_children():
            self.columns_tree.delete(item)
        
        # Thêm dữ liệu mới
        self.columns_data = columns.copy()
        for col in columns:
            self.columns_tree.insert('', tk.END, values=(
                col.get('key', ''),
                col.get('name', ''),
                col.get('type', ''),
                col.get('description', '')
            ))
    
    def add_new_template(self):
        """Thêm template mới"""
        self.show_template_dialog()
    
    def copy_template(self):
        """Sao chép template"""
        if not self.current_template_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn template để sao chép!")
            return
        
        self.show_template_dialog(copy_from=self.current_template_name)
    
    def delete_template(self):
        """Xóa template"""
        if not self.current_template_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn template để xóa!")
            return
        
        if self.current_template_name == "default":
            messagebox.showerror("Lỗi", "Không thể xóa template mặc định!")
            return
        
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa template '{self.current_template_name}'?"):
            self.prompt_manager.delete_template(self.current_template_name)
            self.load_templates_list()
            self.current_template_name = ""
    
    def set_as_current(self):
        """Đặt template làm mặc định"""
        if not self.current_template_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn template!")
            return
        
        self.prompt_manager.set_current_template(self.current_template_name)
        self.load_templates_list()
        messagebox.showinfo("Thành công", f"Đã đặt '{self.current_template_name}' làm template mặc định!")
    
    def show_template_dialog(self, copy_from=None):
        """Hiển thị dialog tạo/sao chép template"""
        dialog = tk.Toplevel(self.window)
        dialog.title("➕ Template mới" if not copy_from else "📝 Sao chép Template")
        dialog.geometry("400x200")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Đặt dialog ở giữa
        dialog.geometry("+%d+%d" % (self.window.winfo_rootx() + 50, self.window.winfo_rooty() + 50))
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Tên template
        ttk.Label(frame, text="Tên template:").pack(anchor=tk.W)
        name_var = tk.StringVar()
        if copy_from:
            original_template = self.prompt_manager.get_template(copy_from)
            name_var.set(f"{original_template.get('name', copy_from)} - Copy")
        
        name_entry = ttk.Entry(frame, textvariable=name_var, width=40)
        name_entry.pack(fill=tk.X, pady=(0, 10))
        name_entry.focus()
        
        # Mô tả
        ttk.Label(frame, text="Mô tả:").pack(anchor=tk.W)
        desc_text = scrolledtext.ScrolledText(frame, height=4, width=40)
        desc_text.pack(fill=tk.X, pady=(0, 10))
        
        if copy_from:
            original_template = self.prompt_manager.get_template(copy_from)
            desc_text.insert(1.0, original_template.get('description', ''))
        
        # Nút
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        def create_template():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên template!")
                return
            
            # Kiểm tra tên trùng
            if name.lower() in [t.lower() for t in self.prompt_manager.get_template_names()]:
                messagebox.showerror("Lỗi", "Tên template đã tồn tại!")
                return
            
            desc = desc_text.get(1.0, tk.END).strip()
            
            if copy_from:
                # Sao chép từ template khác
                original_template = self.prompt_manager.get_template(copy_from)
                new_template = original_template.copy()
                new_template['name'] = name
                new_template['description'] = desc
            else:
                # Tạo template mới
                new_template = {
                    'name': name,
                    'description': desc,
                    'columns': [
                        {"key": "stt", "name": "STT", "type": "number", "description": "Số thứ tự"},
                        {"key": "msv", "name": "MSV", "type": "text", "description": "Mã số sinh viên"},
                        {"key": "hoten", "name": "Họ và tên", "type": "text", "description": "Họ và tên đầy đủ"}
                    ],
                    'validation_rules': {
                        "score_range": [0.0, 10.0]
                    },
                    'prompt_template': "Phân tích bảng điểm này với độ chính xác cao..."
                }
            
            # Tạo key từ tên
            template_key = name.lower().replace(' ', '_').replace('-', '_')
            
            self.prompt_manager.add_template(template_key, new_template)
            self.load_templates_list()
            
            dialog.destroy()
            messagebox.showinfo("Thành công", f"Đã tạo template '{name}'!")
        
        ttk.Button(btn_frame, text="✅ Tạo", command=create_template).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="❌ Hủy", command=dialog.destroy).pack(side=tk.RIGHT)
    
    def add_column(self):
        """Thêm cột mới"""
        self.show_column_dialog()
    
    def edit_column(self):
        """Sửa cột"""
        selection = self.columns_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột để sửa!")
            return
        
        item = selection[0]
        index = self.columns_tree.index(item)
        column_data = self.columns_data[index]
        
        self.show_column_dialog(edit_data=column_data, edit_index=index)
    
    def delete_column(self):
        """Xóa cột"""
        selection = self.columns_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột để xóa!")
            return
        
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa cột này?"):
            item = selection[0]
            index = self.columns_tree.index(item)
            
            # Xóa khỏi data và tree
            del self.columns_data[index]
            self.columns_tree.delete(item)
    
    def move_column_up(self):
        """Di chuyển cột lên"""
        selection = self.columns_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.columns_tree.index(item)
        
        if index > 0:
            # Hoán đổi trong data
            self.columns_data[index], self.columns_data[index-1] = \
                self.columns_data[index-1], self.columns_data[index]
            
            # Reload tree
            self.load_columns_data(self.columns_data)
            
            # Chọn lại item
            new_item = self.columns_tree.get_children()[index-1]
            self.columns_tree.selection_set(new_item)
    
    def move_column_down(self):
        """Di chuyển cột xuống"""
        selection = self.columns_tree.selection()
        if not selection:
            return
        
        item = selection[0]
        index = self.columns_tree.index(item)
        
        if index < len(self.columns_data) - 1:
            # Hoán đổi trong data
            self.columns_data[index], self.columns_data[index+1] = \
                self.columns_data[index+1], self.columns_data[index]
            
            # Reload tree
            self.load_columns_data(self.columns_data)
            
            # Chọn lại item
            new_item = self.columns_tree.get_children()[index+1]
            self.columns_tree.selection_set(new_item)
    
    def show_column_dialog(self, edit_data=None, edit_index=None):
        """Hiển thị dialog thêm/sửa cột"""
        dialog = tk.Toplevel(self.window)
        dialog.title("➕ Thêm cột" if not edit_data else "📝 Sửa cột")
        dialog.geometry("400x300")
        dialog.transient(self.window)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Key
        ttk.Label(frame, text="Key (định danh):").pack(anchor=tk.W)
        key_var = tk.StringVar(value=edit_data.get('key', '') if edit_data else '')
        key_entry = ttk.Entry(frame, textvariable=key_var, width=40)
        key_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Tên hiển thị
        ttk.Label(frame, text="Tên hiển thị:").pack(anchor=tk.W)
        name_var = tk.StringVar(value=edit_data.get('name', '') if edit_data else '')
        name_entry = ttk.Entry(frame, textvariable=name_var, width=40)
        name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Loại dữ liệu
        ttk.Label(frame, text="Loại dữ liệu:").pack(anchor=tk.W)
        type_var = tk.StringVar(value=edit_data.get('type', 'text') if edit_data else 'text')
        type_combo = ttk.Combobox(frame, textvariable=type_var, 
                                 values=['text', 'number', 'score'], 
                                 state='readonly', width=37)
        type_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Mô tả
        ttk.Label(frame, text="Mô tả:").pack(anchor=tk.W)
        desc_text = scrolledtext.ScrolledText(frame, height=4, width=40)
        desc_text.pack(fill=tk.X, pady=(0, 10))
        if edit_data:
            desc_text.insert(1.0, edit_data.get('description', ''))
        
        # Nút
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        def save_column():
            key = key_var.get().strip()
            name = name_var.get().strip()
            col_type = type_var.get()
            desc = desc_text.get(1.0, tk.END).strip()
            
            if not key or not name:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            column_data = {
                'key': key,
                'name': name,
                'type': col_type,
                'description': desc
            }
            
            if edit_data is not None:
                # Sửa cột
                self.columns_data[edit_index] = column_data
            else:
                # Thêm cột mới
                self.columns_data.append(column_data)
            
            # Reload tree
            self.load_columns_data(self.columns_data)
            
            dialog.destroy()
        
        ttk.Button(btn_frame, text="✅ Lưu", command=save_column).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="❌ Hủy", command=dialog.destroy).pack(side=tk.RIGHT)
        
        key_entry.focus()
    
    def refresh_preview(self):
        """Refresh preview"""
        if not self.current_template_name:
            return
        
        template = self.prompt_manager.get_template(self.current_template_name)
        if not template:
            return
        
        # Cập nhật thông tin
        info = f"Template: {template.get('name', '')}\n"
        info += f"Mô tả: {template.get('description', '')}\n"
        info += f"Số cột: {len(template.get('columns', []))}\n"
        info += f"Validation rules: {json.dumps(template.get('validation_rules', {}), ensure_ascii=False, indent=2)}"
        
        self.preview_info_text.delete(1.0, tk.END)
        self.preview_info_text.insert(1.0, info)
        
        # Cập nhật prompt preview
        prompt = template.get('prompt_template', '')
        
        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, prompt)
        self.preview_text.config(state=tk.DISABLED)
    
    def save_settings(self):
        """Lưu cài đặt"""
        if not self.current_template_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn template để lưu!")
            return
        
        try:
            # Lấy dữ liệu từ form
            template_data = {
                'name': self.template_name_var.get().strip(),
                'description': self.template_desc_text.get(1.0, tk.END).strip(),
                'columns': self.columns_data.copy(),
                'validation_rules': {},  # Có thể mở rộng sau
                'prompt_template': self.prompt_text.get(1.0, tk.END).strip()
            }
            
            # Cập nhật template
            self.prompt_manager.update_template(self.current_template_name, template_data)
            
            messagebox.showinfo("Thành công", "Đã lưu cài đặt thành công!")
            self.load_templates_list()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi lưu cài đặt: {str(e)}")
    
    def reset_to_default(self):
        """Khôi phục cài đặt mặc định"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn khôi phục tất cả về mặc định?"):
            self.prompt_manager.create_default_templates()
            self.prompt_manager.save_templates()
            self.load_templates_list()
            messagebox.showinfo("Thành công", "Đã khôi phục cài đặt mặc định!")
    
    def close_window(self):
        """Đóng cửa sổ"""
        self.window.destroy()
