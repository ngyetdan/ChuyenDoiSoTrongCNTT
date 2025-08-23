# create_database.py - Tạo database và bảng cho ứng dụng

from database_manager import DatabaseManager

def create_database_and_tables():
    """Tạo database và bảng"""
    print("🗄️ === TẠO DATABASE CHO ỨNG DỤNG OCR === 🗄️\n")
    
    server_name = "DESKTOP-ERG8R8S"
    database_name = "GradeManagement"
    
    print(f"Server: {server_name}")
    print(f"Database: {database_name}")
    
    # Tạo database manager
    db_manager = DatabaseManager(server_name, database_name)
    
    print("\n1️⃣ Tạo database...")
    success, message = db_manager.create_database()
    
    if success:
        print(f"✅ {message}")
        
        print("\n2️⃣ Tạo bảng...")
        success, message = db_manager.create_tables()
        
        if success:
            print(f"✅ {message}")
            print("\n🎉 Hoàn tất! Database đã sẵn sàng sử dụng.")
        else:
            print(f"❌ {message}")
    else:
        print(f"❌ {message}")
        if "đã tồn tại" in message:
            print("\n2️⃣ Database đã có, tạo bảng...")
            success, message = db_manager.create_tables()
            if success:
                print(f"✅ {message}")
                print("\n🎉 Hoàn tất! Database đã sẵn sàng sử dụng.")
            else:
                print(f"❌ {message}")

if __name__ == "__main__":
    try:
        create_database_and_tables()
    except Exception as e:
        print(f"\n💥 Lỗi: {str(e)}")
    
    input("\nNhấn Enter để thoát...")
