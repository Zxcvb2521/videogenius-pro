FROM python:3.11

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        git \
        libgl1 \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install ./playht-sdk

RUN mkdir -p videos

# YouTube API конфиги будут монтироваться при запуске (если есть)
# Ничего не копируем — избегаем ошибок сборки

EXPOSE 7860

CMD ["python", "app.py"]