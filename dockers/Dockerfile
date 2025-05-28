FROM python:3.12.4

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    tesseract-ocr \
    tesseract-ocr-tha \
    poppler-utils \
    ffmpeg \
    libmagic1 \
    && rm -rf var/lib/apt/lists/*

WORKDIR /app

COPY ../api ./api
COPY ../main.py ./main.py
COPY ../requirements.txt ./requirements.txt
COPY ../settings.json ./settings.json

RUN pip install --no-cache-dir -r requirements.txt