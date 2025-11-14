import os
<<<<<<< HEAD
from flask import Flask, render_template, request, send_from_directory, jsonify, send_file
from datetime import datetime
from dotenv import load_dotenv
from ai_provider import get_ai_provider
from database import ChatDatabase
from file_processor import FileProcessor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
=======
from flask import Flask, render_template, request, send_from_directory, jsonify
from datetime import datetime
from dotenv import load_dotenv
from ai_providers import get_ai_provider

app = Flask(__name__)
>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe

# Load environment variables
load_dotenv()

<<<<<<< HEAD
# Inisialisasi AI provider, database, file processor
=======
# Inisialisasi AI provider
>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
try:
    ai_provider = get_ai_provider()
    print(f"✅ AI Provider berhasil dimuat: {os.getenv('AI_PROVIDER', 'groq')}")
except Exception as e:
    print(f"⚠️  Warning: {str(e)}")
    ai_provider = None

<<<<<<< HEAD
db = ChatDatabase()
file_processor = FileProcessor()
=======
>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe

# ===== ROUTES =====

@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
=======

>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
@app.route('/chat')
def chat():
    return render_template('chat.html')

<<<<<<< HEAD
=======

>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
@app.route('/chat', methods=['POST'])
def chat_api():
    """
    API endpoint untuk chat dengan AI
<<<<<<< HEAD
=======
    Menerima JSON dengan format: {"message": "user message"}
>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
    """
    if not ai_provider:
        return jsonify({
            "success": False,
<<<<<<< HEAD
            "error": "AI Provider belum dikonfigurasi."
=======
            "error": "AI Provider belum dikonfigurasi." #Pastikan file .env sudah dibuat dengan benar.
>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
        }), 500
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Message tidak ditemukan dalam request"
            }), 400
        
        user_message = data['message'].strip()
<<<<<<< HEAD
        conversation_id = data.get('conversation_id')
        
        # Create new conversation if none
        if not conversation_id:
            conversation_id = db.create_conversation(user_message[:50])
        
        # Save user message to database
        db.add_message(conversation_id, 'user', user_message)
        
        # Get conversation history for context
        history_messages = db.get_messages(conversation_id)
        messages = []
        
        # System message
        messages.append({
            "role": "system",
            "content": "Anda adalah CHATdelon AI yang diciptkan Farhan Akmal."
                        "sifat anda membantu dan informatif."
                        "Anda ahli dalam berbagai topik dan dapat menganalisis file yang diupload."
                        "Berikan jawaban sesuai konteks percakapan sebelumnya dan sesuai pertanyaan user."
                        "Berikan jawaban dalam berbagai format seperti teks, daftar, tabel, kode, dll."
                        "Berikan jawaban yang jelas dan mudah dimengerti."
                        "Berikan jawaban sesuai bahasa yang user gunakan"
                        "Selain itu, berikan jawaban yang sopan dan profesional."
                        "Lebih penting lagi, berikan jawaban yang jujur dan akurat."
                        "Lalu setelah anda memberikan jawaban, berikan beberapa pertanyaan lalu berikan beberapa saran untuk percakapan selajutnya berdasarkan topik yang sedang dibahas. "
                        "Jika anda tidak tahu jawabannya, katakan maaf saya belum bisa menjawabnya karena saya masih dalam tahap pengembangan"
        })
        
        # Add history (last 10 messages for context)
        for msg in history_messages[-10:]:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        # Get AI response dengan max_tokens yang reasonable
        ai_response = ai_provider.generate_response(
            messages=messages,
            temperature=0.7,
            max_tokens=100000  # ✅ Fixed: reasonable token limit
        )
        
        # Save AI response to database
        db.add_message(conversation_id, 'assistant', ai_response)
        
        return jsonify({
            "success": True, 
            "response": ai_response,
            "conversation_id": conversation_id
        })
=======
        if not user_message:
            return jsonify({
                "success": False,
                "error": "Message tidak boleh kosong"
            }), 400
        
        # Ambil history jika ada
        conversation_history = data.get('history', [])
        messages = []

        # Pesan sistem (aturan AI)
        messages.append({
            "role": "system",
            "content": (
                "Anda adalah asisten AI bernama CHATdelon yang dibuat oleh Farhan Akmal. "
                "Anda ramah, informatif, punya pengetahuan luas dan ahli di berbagai bidang. "
                "Berikan jawaban yang jelas, spesifik, dan mudah dipahami dalam bahasa Indonesia."
                "Jika ditanya jawab dengan jujur sesuia pengetahuan anda, kalo tidak tau jawab jujur."
            )
        })

        # Tambahkan history & pesan user
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": user_message})

        # Dapatkan respons AI
        ai_response = ai_provider.generate_response(
            messages=messages,
            temperature=0.7,
            max_tokens=20000
        )

        return jsonify({"success": True, "response": ai_response})
>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
    
    except Exception as e:
        error_msg = str(e)
        print(f"Chat API Error: {error_msg}")
        return jsonify({
            "success": False,
<<<<<<< HEAD
            "error": f"Terjadi kesalahan: {error_msg}"
        }), 500

# ===== NEW API ENDPOINTS =====

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations"""
    try:
        print("🔍 Fetching conversations from database...")
        conversations = db.get_conversations()
        print(f"✅ Found {len(conversations)} conversations")
        return jsonify({"success": True, "conversations": conversations})
    except Exception as e:
        print(f"❌ Error in get_conversations: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Database error: {str(e)}"
        }), 500

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    """Create new conversation"""
    try:
        data = request.get_json()
        title = data.get('title', 'Obrolan Baru')
        conversation_id = db.create_conversation(title)
        return jsonify({
            "success": True, 
            "conversation_id": conversation_id,
            "title": title
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete conversation"""
    try:
        db.delete_conversation(conversation_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    """Get messages for a conversation"""
    try:
        messages = db.get_messages(conversation_id)
        return jsonify({"success": True, "messages": messages})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and analysis"""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
    
    conversation_id = request.form.get('conversation_id')
    if not conversation_id:
        return jsonify({"success": False, "error": "Conversation ID required"}), 400

    try:
        # Save file
        filename, filepath = file_processor.save_file(file)
        if not filename:
            return jsonify({"success": False, "error": "File type not allowed"}), 400
        
        # Analyze file
        analysis_result = file_processor.analyze_file(filepath, file.content_type)
        
        # Save to database
        db.add_message(
            conversation_id=conversation_id,
            role='user',
            content=f"[File: {filename}]",
            file_name=filename,
            file_path=filepath,
            file_type=file.content_type,
            analysis_result=analysis_result
        )
        
        # Get AI analysis
        if ai_provider:
            ai_analysis = ai_provider.generate_response([
                {"role": "system", "content": "Analisis file yang diupload dan berikan insight."},
                {"role": "user", "content": f"File: {filename}\nKonten: {analysis_result}"}
            ])
            
            db.add_message(
                conversation_id=conversation_id,
                role='assistant',
                content=ai_analysis
            )
            
            return jsonify({
                "success": True,
                "filename": filename,
                "analysis": analysis_result,
                "ai_response": ai_analysis
            })
        
        return jsonify({
            "success": True,
            "filename": filename,
            "analysis": analysis_result
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)
=======
            "error": f"Terjadi kesalahan: {error_msg[:200]}"
        }), 500

>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe

@app.route('/api/provider')
def get_provider_info():
    """API endpoint untuk mendapatkan info provider yang sedang digunakan"""
    provider_name = os.getenv('AI_PROVIDER', 'groq')
    return jsonify({
        "provider": provider_name,
        "status": "active" if ai_provider else "inactive"
    })

<<<<<<< HEAD
=======

>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.png',
        mimetype='image/png'
    )

<<<<<<< HEAD
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  
    app.run(host="0.0.0.0", port=port)
=======

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Gunakan PORT dari Railway
    app.run(host="0.0.0.0", port=port)
>>>>>>> 6c1e03e2678e28d40f49769e03bb2dbeb8697abe
