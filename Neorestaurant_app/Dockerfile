# ใช้ Python 3.10 แบบ slim เพื่อลดขนาด image
FROM python:3.10-slim

# ตั้ง working directory
WORKDIR /app

# ป้องกัน Python cache
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ติดตั้ง dependency ของระบบ (ถ้าจำเป็น)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt และติดตั้ง
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code ทั้งหมดเข้า container
COPY . .

# Flask รันที่ port 5000
EXPOSE 5000

# คำสั่งเริ่มต้น (ใช้ flask run หรือ python app.py ก็ได้)
CMD ["python", "app.py"]
