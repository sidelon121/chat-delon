from database import ChatDatabase

db = ChatDatabase()
# Test connection
conn = db.get_connection()  # ✅ PERBAIKI: get_connection() BUKAN sc.connection()
if conn.is_connected():
    print("✅ Database connected successfully!")
    
    # Test if tables exist
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("📊 Tables found:", tables)
    
    conn.close()
else:
    print("❌ Database connection failed!")