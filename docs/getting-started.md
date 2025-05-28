# Getting Started

Welcome to **Ka-Doe** 🐾 — let’s get your environment up and running!

This guide walks you through the installation steps, runtime requirements, and how to launch the API locally.

---

## 🛠 Requirements

Before you begin, ensure the following dependencies are installed:

- **Python 3.12.4** – Core language runtime
- **Tesseract OCR** – For image-based text extraction
- **Poppler** – For PDF parsing and rendering
- **PurrfectKit** – Utility toolkit powering internal workflows

---

## 📦 Installation

### 1. System Dependencies

Install the required system packages:

```bash
sudo apt-get update
sudo apt-get install \
  tesseract-ocr \
  tesseract-ocr-tha \
  poppler-utils \
  ffmpeg \
  libmagic1
```

### 2. Python Packages

Install the Python dependencies using pip:

```bash
pip install fastapi uvicorn python-multipart \
    git+https://github.com/suwalutions/PurrfectKit.git@meow

```

## 🚦 Run the Application

Once everything is installed, start the Ka-Doe server with:

```bash
uvicorn main:app
```

Your API will be available at:

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

This endpoint provides an interactive Swagger UI for exploring the API.

## 🧪 Need Help?

Check the [Project Structure](project-structure.md) for more insights, or visit the [API Reference](api-intro.md) for usage examples.