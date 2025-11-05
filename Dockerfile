# Gunakan image Python dasar yang stabil
FROM python:3.11-slim

# Tetapkan direktori kerja
WORKDIR /app

# Salin requirements.txt dan instal semua library 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin sisa kode aplikasi ke dalam container
COPY . .

# Jalankan aplikasi Anda dengan Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 main:app
