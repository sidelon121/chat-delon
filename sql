-- Pastikan database sudah dipilih atau buat baru
CREATE DATABASE IF NOT EXISTS chatdelon_db;
USE chatdelon_db;

-- Hapus tabel jika sudah ada (optional)
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS conversations;

-- Buat tabel conversations
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Buat tabel messages  
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT,
    role ENUM('user', 'assistant', 'system'),
    content TEXT,
    file_name VARCHAR(500),
    file_path VARCHAR(500),
    file_type VARCHAR(50),
    analysis_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- Tambahkan sample data untuk testing
INSERT INTO conversations (title) VALUES ('Obrolan Percobaan');
INSERT INTO messages (conversation_id, role, content) 
VALUES (1, 'user', 'Halo, ini pesan percobaan');
INSERT INTO messages (conversation_id, role, content) 
VALUES (1, 'assistant', 'Halo! Saya siap membantu Anda');

-- Verifikasi
SELECT * FROM conversations;
SELECT * FROM messages;