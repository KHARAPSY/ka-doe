FROM nvidia/cuda:12.6.1-devel-ubuntu22.04

WORKDIR /ka-doe

COPY . .

RUN apt-get update && \
    apt-get install -y \
    python3 python3-pip \
    python3-venv build-essential \
    libbz2-dev libncurses5-dev \
    libreadline-dev libssl-dev \
    libsqlite3-dev tesseract-ocr \
    tesseract-ocr-tha ffmpeg \
    libmagic1 libxml2-dev \
    libxslt1-dev libjpeg-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]