import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from datetime import datetime
from dotenv import load_dotenv
from ai_providers import get_ai_provider

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Inisialisasi AI provider
try:
    ai_provider = get_ai_provider()
    print(f"✅ AI Provider berhasil dimuat: {os.getenv('AI_PROVIDER', 'groq')}")
except Exception as e:
    print(f"⚠️  Warning: {str(e)}")
    ai_provider = None


# ===== ROUTES =====

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat_api():
    """
    API endpoint untuk chat dengan AI
    Menerima JSON dengan format: {"message": "user message"}
    """
    if not ai_provider:
        return jsonify({
            "success": False,
            "error": "AI Provider belum dikonfigurasi. Pastikan file .env sudah dibuat dengan benar."
        }), 500
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Message tidak ditemukan dalam request"
            }), 400
        
        user_message = data['message'].strip()
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
                "Anda ramah, informatif, dan ahli di berbagai bidang. "
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
    
    except Exception as e:
        error_msg = str(e)
        print(f"Chat API Error: {error_msg}")
        return jsonify({
            "success": False,
            "error": f"Terjadi kesalahan: {error_msg[:200]}"
        }), 500


@app.route('/api/provider')
def get_provider_info():
    """API endpoint untuk mendapatkan info provider yang sedang digunakan"""
    provider_name = os.getenv('AI_PROVIDER', 'groq')
    return jsonify({
        "provider": provider_name,
        "status": "active" if ai_provider else "inactive"
    })


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.png',
        mimetype='image/png'
    )


if __name__ == "__main__":
    # Port disesuaikan untuk Railway
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8059)))
