# Python 3.10 bazaviy imijidan foydalanamiz
FROM python:3.10-slim

# Ishlash katalogini belgilaymiz
WORKDIR /app

# Kerakli fayllarni ko'chiramiz
COPY . .

# Talablar faylidan kerakli kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
# Botni ishga tushiramiz
CMD ["python3", "app.py"]
