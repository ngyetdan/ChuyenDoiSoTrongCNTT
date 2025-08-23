# prompt_manager.py - Quản lý các prompt templates cho OCR

import json
import os
from typing import Dict, List, Optional

class PromptManager:
    """Class quản lý các prompt templates cho OCR"""
    
    def __init__(self, config_file="prompt_templates.json"):
        self.config_file = config_file
        self.templates = {}
        self.current_template = "default"
        self.load_templates()
    
    def load_templates(self):
        """Tải các template từ file config"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.templates = data.get('templates', {})
                    self.current_template = data.get('current_template', 'default')
            else:
                # Tạo template mặc định
                self.create_default_templates()
                self.save_templates()
        except Exception as e:
            print(f"Lỗi tải templates: {e}")
            self.create_default_templates()
    
    def save_templates(self):
        """Lưu templates vào file"""
        try:
            data = {
                'templates': self.templates,
                'current_template': self.current_template
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Lỗi lưu templates: {e}")
    
    def create_default_templates(self):
        """Tạo các template mặc định"""
        self.templates = {
            "default": {
                "name": "Bảng điểm chuẩn CNTT",
                "description": "Template cho bảng điểm sinh viên CNTT với cấu trúc chuẩn",
                "columns": [
                    {"key": "stt", "name": "STT", "type": "number", "description": "Số thứ tự"},
                    {"key": "lop", "name": "Lớp", "type": "text", "description": "Mã lớp (CNTT XX-XX)"},
                    {"key": "msv", "name": "MSV", "type": "text", "description": "Mã số sinh viên 10 số"},
                    {"key": "ho", "name": "Họ và đệm", "type": "text", "description": "Họ và tên đệm"},
                    {"key": "ten", "name": "Tên", "type": "text", "description": "Tên riêng"},
                    {"key": "cc", "name": "CC", "type": "score", "description": "Điểm chuyên cần"},
                ],
                "validation_rules": {
                    "msv_pattern": "^(15|17|18|19|20|21|22|23|24)\\d{8}$",
                    "class_pattern": "^CNTT \\d{2}-\\d{2}$",
                    "score_range": [0.0, 10.0]
                },
                "prompt_template": """🤖 Bạn là chuyên gia OCR Gemini với độ chính xác cao. Phân tích bảng điểm sinh viên này CHÍNH XÁC 100%.
✍️ HỖ TRỢ CẢ CHỮ IN VÀ CHỮ VIẾT TAY!

🎯 CẤU TRÚC BẢNG ĐIỂM LINH HOẠT - NHẬN DIỆN TỰ ĐỘNG:
Bảng có thể có các cột sau (không nhất thiết đầy đủ):
- STT: Số thứ tự (1, 2, 3...)
- Lớp: Mã lớp (CNTT 15-01, CNTT 17-02, KTPM 18-01, ATTT 19-02...)
- MSV: Mã số sinh viên 8-10 số (1571020050, 1771020073, 20210001...)
- Họ và đệm: Họ + tên đệm (Nguyễn Văn, Trần Thị, Lê Minh...)
- Tên: Tên riêng (Anh, Bình, Cường, Hoa...)
- CC/Chuyên cần: Điểm chuyên cần (0.0 - 10.0)
- KT1/Kiểm tra: Điểm kiểm tra (0.0 - 10.0)
- Điểm khác: TX1, TX2, GK, CK, TB, Tổng kết... (0.0 - 10.0)

🔍 QUY TẮC NHẬN DIỆN THÔNG MINH:
1. ĐỌC TỪNG KÝ TỰ - KHÔNG ĐOÁN MẠO - NHÌN KỸ TỪNG CHỮ
2. PHÂN BIỆT: số 0 ≠ chữ O, số 1 ≠ chữ I/l, số 5 ≠ chữ S, số 6 ≠ chữ G
3. Tên Việt: BẮT BUỘC có dấu (ă, â, ê, ô, ơ, ư, đ, á, à, ả, ã, ạ...)
4. MSV: 8-10 số, có thể bắt đầu 15/17/18/19/20/21/22/23/24
5. Lớp: Format XX XX-XX hoặc XXXX XX-XX (CNTT, KTPM, ATTT...)
6. Điểm: Số thập phân 0.0-10.0
7. NHẬN DIỆN CỘT TỰ ĐỘNG: Dựa vào header để xác định loại cột
8. ⚠️ QUAN TRỌNG: NẾU KHÔNG ĐỌC ĐƯỢC TÊN - HÃY NHÌN KỸ LẠI - ĐỪNG ĐỂ TRỐNG!

✍️ QUY TẮC ĐẶC BIỆT CHO CHỮ VIẾT TAY:
9. CHỮ VIẾT TAY: Phân tích cẩn thận từng nét chữ, đường cong
10. CHỮ HOA VIẾT TAY: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
11. CHỮ THƯỜNG VIẾT TAY: a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z
12. SỐ VIẾT TAY: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 - chú ý nét viết đặc trưng
13. DẤU TIẾNG VIỆT VIẾT TAY: á, à, ả, ã, ạ, ă, ắ, ằ, ẳ, ẵ, ặ, â, ấ, ầ, ẩ, ẫ, ậ...
14. TÊN VIỆT VIẾT TAY THÔNG DỤNG: Anh, Bình, Cường, Dũng, Giang, Hòa, Kiên, Linh, Minh, Nam, Phong, Quang, Sơn, Thành, Văn, Xuân...

📋 TEMPLATE JSON CHUẨN - CHỈ CÁC CỘT CÓ TRONG BẢNG:
{
  "students": [
    {
      "stt": "1",
      "lop": "CNTT 17-02",
      "msv": "1771020073",
      "ho": "Nguyễn Văn",
      "ten": "Anh",
      "cc": "8.5",
      "kt1": "7.0"
    }
  ]
}

🎯 QUY TẮC PHÂN CHIA TÊN CHÍNH XÁC:
- "ho": Họ + tên đệm (VD: "Bùi Tiến", "Nguyễn Văn", "Trần Thị")
- "ten": CHỈ tên cuối cùng (VD: "Đạt", "Anh", "Bình")

📝 VÍ DỤ PHÂN CHIA ĐÚNG:
- "Bùi Tiến Đạt" → ho="Bùi Tiến", ten="Đạt" ✅
- "Nguyễn Văn Anh" → ho="Nguyễn Văn", ten="Anh" ✅
- "Trần Bình" → ho="Trần", ten="Bình" ✅
- "Lê Minh Quốc" → ho="Lê Minh", ten="Quốc" ✅

🔄 NHẬN DIỆN BẢNG ĐIỂM ĐA DẠNG:
- Bảng CNTT: STT, Lớp, MSV, Họ đệm, Tên, CC, KT1
- Bảng đơn giản: STT, MSV, Họ tên, Điểm
- Bảng chi tiết: STT, Lớp, MSV, Họ tên, TX1, TX2, GK, CK, TB
- Bảng đại học: STT, MSV, Họ tên, Môn học, Tín chỉ, Điểm
- CHỈ XUẤT CÁC CỘT CÓ TRONG BẢNG - KHÔNG TẠO CỘT KHÔNG TỒN TẠI

⚠️ LỖI GEMINI THƯỜNG GẶP - TRÁNH:
- "Nguyen" → "Nguyễn" (thiếu dấu tiếng Việt)
- "CNIT/CNT" → "CNTT" (sai ký tự)
- "I77I020073" → "1771020073" (nhầm I và 1)
- "O.O/0.O" → "0.0" (nhầm O và 0)
- "S.5" → "5.5" (nhầm S và 5)
- Tạo cột không có trong bảng
- CẮT NGẮN TÊN: "Nguyễn Vũ Yến Nhi" → "Nguyễn Vũ Yến" (BỎ SÓT "Nhi")

🔥 PHÂN CHIA TÊN CHÍNH XÁC - QUAN TRỌNG:
- ĐỌC HẾT tất cả từ trong tên, KHÔNG BỎ SÓT
- "Nguyễn Vũ Yến Nhi" → ho="Nguyễn Vũ Yến", ten="Nhi"
- "Trần Thị Hương Giang" → ho="Trần Thị Hương", ten="Giang"
- "Lê Minh Tuấn" → ho="Lê Minh", ten="Tuấn"
- "Võ An" → ho="Võ", ten="An"

🎯 OUTPUT YÊU CẦU:
- CHỈ trả về JSON thuần, KHÔNG giải thích
- CHỈ XUẤT CÁC CỘT THỰC SỰ CÓ TRONG BẢNG
- ⚠️ TUYỆT ĐỐI KHÔNG ĐỂ TRỐNG "ho" và "ten" - HÃY ĐỌC KỸ LẠI!
- ⚠️ TUYỆT ĐỐI KHÔNG CẮT NGẮN TÊN - ĐỌC HẾT TẤT CẢ TỪ!
- Nếu thực sự không đọc được: ghi tên gần đúng nhất có thể
- Kiểm tra logic: STT tăng dần, MSV hợp lệ
- Đảm bảo tên có đủ dấu tiếng Việt

🔥 LỆNH ĐẶC BIỆT CHO GEMINI:
- ZOOM VÀO TỪNG DÒNG - ĐỌC TỪNG CHỮ CÁI
- KHÔNG BAO GIỜ ĐỂ TRỐNG TÊN SINH VIÊN
- NẾU MỜ: HÃY ĐOÁN DỰA TRÊN NGỮ CẢNH VÀ TÊN VIỆT THÔNG DỤNG
- VÍ DỤ: Nếu thấy "Ng...n V.n" → có thể là "Nguyễn Văn"

✍️ HƯỚNG DẪN CHỮ VIẾT TAY:
- PHÂN TÍCH NÉT VIẾT: Đường thẳng, đường cong, góc cạnh
- CHỮ LIỀN: Tách từng ký tự riêng biệt
- CHỮ NGHIÊNG: Điều chỉnh góc nhìn để đọc đúng
- NÉT MỜ: Dựa vào ngữ cảnh và tên Việt thông dụng
- VÍ DỤ CHỬ VIẾT TAY: "Nguyễn" có thể viết liền, "Văn" có nét đặc trưng

🎯 BẢNG ĐIỂM HỖN HỢP (IN + VIẾT TAY):
- Header thường là CHỮ IN
- Tên sinh viên có thể là CHỮ VIẾT TAY
- Điểm số có thể là CHỮ VIẾT TAY
- MSV thường là CHỮ IN hoặc CHỮ SỐ VIẾT TAY

GEMINI - NHẬN DIỆN THÔNG MINH CẢ CHỮ IN VÀ CHỮ VIẾT TAY!"""
            },

            "handwritten": {
                "name": "Bảng điểm chữ viết tay",
                "description": "Template chuyên biệt cho bảng điểm có chữ viết tay",
                "columns": [
                    {"key": "stt", "name": "STT", "type": "number", "description": "Số thứ tự"},
                    {"key": "lop", "name": "Lớp", "type": "text", "description": "Mã lớp"},
                    {"key": "msv", "name": "MSV", "type": "text", "description": "Mã số sinh viên"},
                    {"key": "ho", "name": "Họ và đệm", "type": "text", "description": "Họ và tên đệm viết tay"},
                    {"key": "ten", "name": "Tên", "type": "text", "description": "Tên riêng viết tay"},
                    {"key": "cc", "name": "CC", "type": "score", "description": "Điểm chuyên cần"},
                    {"key": "kt1", "name": "KT1", "type": "score", "description": "Điểm kiểm tra"}
                ],
                "validation_rules": {
                    "msv_pattern": "^(15|17|18|19|20|21|22|23|24)\\d{8}$",
                    "class_pattern": "^[A-Z]{2,4} \\d{2}-\\d{2}$",
                    "score_range": [0.0, 10.0]
                },
                "prompt_template": """🤖✍️ Chuyên gia OCR Gemini - CHUYÊN BIỆT CHỮ VIẾT TAY!

🎯 BẢNG ĐIỂM CHỮ VIẾT TAY - PHÂN TÍCH SIÊU CHÍNH XÁC:
Bảng này có thể chứa:
- Header: CHỮ IN (STT, Lớp, MSV, Họ và đệm, Tên, CC, KT1...)
- Tên sinh viên: CHỮ VIẾT TAY (Nguyễn Văn Anh, Trần Thị Bình...)
- Điểm số: CHỮ VIẾT TAY (7.5, 8.0, 9.5...)
- MSV: CHỮ SỐ (1771020073, 1851020045...)

✍️ CHUYÊN GIA NHẬN DIỆN CHỮ VIẾT TAY:
1. 🔍 PHÂN TÍCH NÉT VIẾT:
   - Đường thẳng: I, l, 1, T, L, F, E
   - Đường cong: O, o, 0, C, c, S, s, G, g
   - Góc cạnh: A, V, W, M, N, K, k
   - Vòng tròn: O, o, 0, a, e, d, p, q, b

2. 📝 CHỮ VIỆT VIẾT TAY THÔNG DỤNG:
   - Họ: Nguyễn, Trần, Lê, Phạm, Hoàng, Huỳnh, Phan, Vũ, Võ, Đặng, Bùi, Đỗ, Hồ, Ngô, Dương, Lý
   - Tên đệm: Văn, Thị, Minh, Hữu, Đức, Quang, Thanh, Hồng, Kim, Xuân
   - Tên: Anh, Bình, Cường, Dũng, Giang, Hòa, Kiên, Linh, Minh, Nam, Phong, Quang, Sơn, Thành, Tùng, Việt

3. 🔢 SỐ VIẾT TAY ĐẶC TRƯNG:
   - 0: Hình oval, có thể nghiêng
   - 1: Đường thẳng, có thể có chân
   - 2: Đường cong trên, đường thẳng dưới
   - 3: Hai đường cong
   - 4: Hai đường thẳng giao nhau
   - 5: Đường thẳng trên, đường cong dưới
   - 6: Đường cong lớn
   - 7: Đường thẳng nghiêng
   - 8: Hai vòng tròn
   - 9: Vòng tròn trên, đường thẳng dưới

4. 🎯 ĐIỂM SỐ VIẾT TAY:
   - 0.0, 1.0, 2.0... 10.0
   - 7.5, 8.5, 9.5 (phổ biến)
   - Chú ý dấu thập phân "."

JSON OUTPUT - CHỈ CÁC CỘT CÓ TRONG BẢNG:
{
  "students": [
    {
      "stt": "1",
      "lop": "CNTT 17-02",
      "msv": "1771020073",
      "ho": "Nguyễn Văn",
      "ten": "Anh",
      "cc": "8.5",
      "kt1": "7.0"
    }
  ]
}

⚠️ LỆNH TUYỆT ĐỐI:
- KHÔNG BAO GIỜ ĐỂ TRỐNG TÊN SINH VIÊN
- NẾU VIẾT TAY MỜ: ĐOÁN DỰA TRÊN TÊN VIỆT THÔNG DỤNG
- PHÂN TÍCH TỪNG NÉT VIẾT MỘT CÁCH CẨN THẬN
- ƯU TIÊN TÊN CÓ DẤU TIẾNG VIỆT

GEMINI - CHUYÊN GIA CHỮ VIẾT TAY VIỆT NAM!"""
            },

            "simple": {
                "name": "Bảng điểm đơn giản",
                "description": "Template đơn giản cho bảng điểm cơ bản",
                "columns": [
                    {"key": "stt", "name": "STT", "type": "number", "description": "Số thứ tự"},
                    {"key": "msv", "name": "MSV", "type": "text", "description": "Mã số sinh viên"},
                    {"key": "hoten", "name": "Họ và tên", "type": "text", "description": "Họ và tên đầy đủ"},
                    {"key": "diem", "name": "Điểm", "type": "score", "description": "Điểm số"}
                ],
                "validation_rules": {
                    "msv_pattern": "^\\d{8,10}$",
                    "score_range": [0.0, 10.0]
                },
                "prompt_template": """🤖 Phân tích bảng điểm đơn giản này với độ chính xác cao.

🎯 CẤU TRÚC BẢNG:
- STT: Số thứ tự
- MSV: Mã số sinh viên (8-10 số)
- Họ và tên: Tên đầy đủ có dấu tiếng Việt
- Điểm: Điểm số (0.0-10.0)

📋 TEMPLATE JSON:
{
  "students": [
    {
      "stt": "1",
      "msv": "1771020073",
      "hoten": "Nguyễn Văn Anh",
      "diem": "8.5"
    }
  ]
}

🎯 YÊU CẦU:
- Đọc chính xác từng ký tự
- Tên phải có dấu tiếng Việt
- CHỈ trả về JSON, không giải thích"""
            },

            "detailed": {
                "name": "Bảng điểm chi tiết",
                "description": "Template chi tiết với nhiều loại điểm và thông tin sinh viên",
                "columns": [
                    {"key": "stt", "name": "STT", "type": "number", "description": "Số thứ tự"},
                    {"key": "lop", "name": "Lớp", "type": "text", "description": "Mã lớp"},
                    {"key": "msv", "name": "MSV", "type": "text", "description": "Mã số sinh viên"},
                    {"key": "hoten", "name": "Họ và tên", "type": "text", "description": "Họ và tên đầy đủ"},
                    {"key": "gioitinh", "name": "Giới tính", "type": "text", "description": "Nam/Nữ"},
                    {"key": "diemtx1", "name": "TX1", "type": "score", "description": "Điểm thường xuyên 1"},
                    {"key": "diemtx2", "name": "TX2", "type": "score", "description": "Điểm thường xuyên 2"},
                    {"key": "diemgk", "name": "GK", "type": "score", "description": "Điểm giữa kỳ"},
                    {"key": "diemck", "name": "CK", "type": "score", "description": "Điểm cuối kỳ"},
                    {"key": "diemtb", "name": "TB", "type": "score", "description": "Điểm trung bình"},
                    {"key": "xeploai", "name": "Xếp loại", "type": "text", "description": "Xếp loại học tập"}
                ],
                "validation_rules": {
                    "msv_pattern": "^(15|17|18|19|20|21|22|23|24)\\d{8}$",
                    "class_pattern": "^[A-Z]{2,4} \\d{2}-\\d{2}$",
                    "score_range": [0.0, 10.0],
                    "gender_values": ["Nam", "Nữ"],
                    "grade_values": ["Xuất sắc", "Giỏi", "Khá", "Trung bình", "Yếu", "Kém"]
                },
                "prompt_template": """🤖 Bạn là chuyên gia OCR Gemini với độ chính xác cao. Phân tích bảng điểm chi tiết này CHÍNH XÁC 100%.

🎯 CẤU TRÚC BẢNG ĐIỂM CHI TIẾT:
- STT: Số thứ tự (1, 2, 3...)
- Lớp: Mã lớp (CNTT 17-02, KTPM 18-01...)
- MSV: Mã số sinh viên 10 số (1771020073...)
- Họ và tên: Tên đầy đủ có dấu tiếng Việt
- Giới tính: Nam hoặc Nữ
- TX1: Điểm thường xuyên 1 (0.0-10.0)
- TX2: Điểm thường xuyên 2 (0.0-10.0)
- GK: Điểm giữa kỳ (0.0-10.0)
- CK: Điểm cuối kỳ (0.0-10.0)
- TB: Điểm trung bình (0.0-10.0)
- Xếp loại: Xuất sắc/Giỏi/Khá/Trung bình/Yếu/Kém

🔍 QUY TẮC CHẶT CHẼ:
1. ĐỌC TỪNG KÝ TỰ - KHÔNG ĐOÁN MẠO
2. Tên Việt: BẮT BUỘC có dấu
3. MSV: ĐÚNG 10 số
4. Điểm: Số thập phân 0.0-10.0
5. Giới tính: CHỈ "Nam" hoặc "Nữ"

📋 TEMPLATE JSON:
{
  "students": [
    {
      "stt": "1",
      "lop": "CNTT 17-02",
      "msv": "1771020073",
      "hoten": "Nguyễn Văn Anh",
      "gioitinh": "Nam",
      "diemtx1": "8.0",
      "diemtx2": "7.5",
      "diemgk": "8.5",
      "diemck": "9.0",
      "diemtb": "8.3",
      "xeploai": "Giỏi"
    }
  ]
}

🎯 OUTPUT YÊU CẦU:
- CHỈ trả về JSON thuần, KHÔNG giải thích
- Nếu không đọc được: ghi "unclear"
- Đảm bảo tên có đủ dấu tiếng Việt

GEMINI - HÃY ĐỌC CHÍNH XÁC!"""
            },

            "university": {
                "name": "Bảng điểm đại học",
                "description": "Template cho bảng điểm đại học với tín chỉ và GPA",
                "columns": [
                    {"key": "stt", "name": "STT", "type": "number", "description": "Số thứ tự"},
                    {"key": "msv", "name": "MSV", "type": "text", "description": "Mã số sinh viên"},
                    {"key": "hoten", "name": "Họ và tên", "type": "text", "description": "Họ và tên đầy đủ"},
                    {"key": "mamh", "name": "Mã MH", "type": "text", "description": "Mã môn học"},
                    {"key": "tenmh", "name": "Tên môn học", "type": "text", "description": "Tên môn học"},
                    {"key": "tinchi", "name": "Tín chỉ", "type": "number", "description": "Số tín chỉ"},
                    {"key": "diemso", "name": "Điểm số", "type": "score", "description": "Điểm số (0-10)"},
                    {"key": "diemchu", "name": "Điểm chữ", "type": "text", "description": "Điểm chữ (A, B, C, D, F)"},
                    {"key": "diemhe4", "name": "Điểm hệ 4", "type": "score", "description": "Điểm hệ 4 (0-4)"}
                ],
                "validation_rules": {
                    "msv_pattern": "^\\d{8,10}$",
                    "score_range": [0.0, 10.0],
                    "gpa_range": [0.0, 4.0],
                    "letter_grades": ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]
                },
                "prompt_template": """🤖 Phân tích bảng điểm đại học này với độ chính xác cao.

🎯 CẤU TRÚC BẢNG ĐIỂM ĐẠI HỌC:
- STT: Số thứ tự
- MSV: Mã số sinh viên
- Họ và tên: Tên đầy đủ có dấu tiếng Việt
- Mã MH: Mã môn học
- Tên môn học: Tên đầy đủ môn học
- Tín chỉ: Số tín chỉ (1-6)
- Điểm số: Điểm số (0.0-10.0)
- Điểm chữ: A+, A, B+, B, C+, C, D+, D, F
- Điểm hệ 4: Điểm GPA (0.0-4.0)

📋 TEMPLATE JSON:
{
  "students": [
    {
      "stt": "1",
      "msv": "1771020073",
      "hoten": "Nguyễn Văn Anh",
      "mamh": "IT101",
      "tenmh": "Nhập môn Công nghệ thông tin",
      "tinchi": "3",
      "diemso": "8.5",
      "diemchu": "B+",
      "diemhe4": "3.5"
    }
  ]
}

🎯 YÊU CẦU:
- Đọc chính xác từng ký tự
- Tên phải có dấu tiếng Việt
- CHỈ trả về JSON, không giải thích"""
            }
        }
    
    def get_template_names(self) -> List[str]:
        """Lấy danh sách tên các template"""
        return list(self.templates.keys())
    
    def get_template(self, name: str) -> Optional[Dict]:
        """Lấy template theo tên"""
        return self.templates.get(name)
    
    def get_current_template(self) -> Dict:
        """Lấy template hiện tại"""
        return self.templates.get(self.current_template, self.templates.get("default", {}))
    
    def set_current_template(self, name: str):
        """Đặt template hiện tại"""
        if name in self.templates:
            self.current_template = name
            self.save_templates()
    
    def add_template(self, name: str, template: Dict):
        """Thêm template mới"""
        self.templates[name] = template
        self.save_templates()
    
    def update_template(self, name: str, template: Dict):
        """Cập nhật template"""
        if name in self.templates:
            self.templates[name] = template
            self.save_templates()
    
    def delete_template(self, name: str):
        """Xóa template"""
        if name in self.templates and name != "default":
            del self.templates[name]
            if self.current_template == name:
                self.current_template = "default"
            self.save_templates()
    
    def get_current_prompt(self) -> str:
        """Lấy prompt của template hiện tại"""
        template = self.get_current_template()
        return template.get("prompt_template", "")
    
    def get_current_columns(self) -> List[Dict]:
        """Lấy cấu trúc cột của template hiện tại"""
        template = self.get_current_template()
        return template.get("columns", [])
    
    def get_current_validation_rules(self) -> Dict:
        """Lấy quy tắc validation của template hiện tại"""
        template = self.get_current_template()
        return template.get("validation_rules", {})
