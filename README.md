# AI_USIA - Multi-Provider AI Chat Application

Aplikasi web Flask untuk mengecek usia dan mendapatkan fakta menarik menggunakan berbagai provider AI seperti ChatGPT, Gemini, DeepSeek, Groq, dan Claude.

## Fitur

- ✅ Mendukung multiple AI providers:
  - **OpenAI** (ChatGPT) - GPT-3.5, GPT-4
  - **Google Gemini** - Gemini Pro
  - **DeepSeek** - DeepSeek Chat
  - **Groq** - Llama 3.1, Mixtral (Default)
  - **Anthropic** (Claude) - Claude 3.5 Sonnet

- ✅ Mudah mengganti provider melalui file `.env`
- ✅ Fleksibel dalam memilih model untuk setiap provider

## Instalasi

1. Clone atau download repository ini

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Buat file `.env` berdasarkan `env.example`:
```bash
cp env.example .env
```

4. Edit file `.env` dan isi dengan API key provider yang ingin Anda gunakan.

## Konfigurasi

Edit file `.env` dan set konfigurasi berikut:

### Pilih Provider
```env
AI_PROVIDER=groq  # Pilih: openai, gemini, deepseek, groq, atau anthropic
```

### OpenAI (ChatGPT)
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-3.5-turbo
```

### Google Gemini
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
```

### DeepSeek
```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_MODEL=deepseek-chat
```

### Groq (Default)
```env
GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

### Anthropic (Claude)
```env
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

## Cara Mendapatkan API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Gemini**: https://makersuite.google.com/app/apikey
- **DeepSeek**: https://platform.deepseek.com/
- **Groq**: https://console.groq.com/keys
- **Anthropic**: https://console.anthropic.com/

## Menjalankan Aplikasi

```bash
python main.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Model yang Didukung

### OpenAI
- `gpt-3.5-turbo` (default)
- `gpt-4`
- `gpt-4-turbo`

### Gemini
- `gemini-pro` (default)
- `gemini-pro-vision`

### DeepSeek
- `deepseek-chat` (default)
- `deepseek-coder`

### Groq
- `llama-3.1-8b-instant` (default)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`

### Anthropic
- `claude-3-5-sonnet-20241022` (default)
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`

## Struktur Project

```
chat_delon/
├── main.py              # Flask application
├── ai_providers.py      # AI provider abstraction layer
├── requirements.txt     # Python dependencies
├── env.example          # Template konfigurasi .env
├── templates/           # HTML templates
└── static/              # CSS, images
```

## License

MIT