FROM python:3.9

# Cài đặt thư viện
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy mã nguồn bot
COPY . .

# Chạy bot và server FastAPI
CMD ["python", "app.py"]