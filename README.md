# 🐾 Ka-Doe

**Ka-Doe** is a document processing and knowledge management service powered by FastAPI. It provides a robust API for managing knowledge bases, uploading documents, extracting content, and performing OCR-based document processing.

> "A soft-pawed tabby whose whispers tamed tempests, and whose radiant eyes kindled love amid flames."

---

## ✨ Features

- **Document Management**: Upload, retrieve, and delete documents from knowledge bases
- **Knowledge Base Management**: Create, list, delete, and manage multiple knowledge bases
- **Content Processing**: Extract and process document content with OCR support
- **User Authentication**: Secure JWT-based authentication with role-based access control
- **Multi-backend Storage**: Support for PostgreSQL (metadata), MongoDB (content), and MinIO (file storage)
- **RESTful API**: Clean, well-documented API with Swagger/OpenAPI documentation
- **Docker Support**: Production-ready Docker setup with CUDA support for GPU acceleration

## 🏗️ Architecture

### Core Components

- **FastAPI Application**: Modern async web framework with automatic API documentation
- **PostgreSQL**: Relational database for user and metadata management
- **MongoDB**: Document database for content storage
- **MinIO**: S3-compatible object storage for files
- **OCR/Document Processing**: Integration with Docling for advanced document understanding

### Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── api/                 # API routes and dependencies
│   ├── routes/
│   │   ├── auth/        # Authentication endpoints
│   │   ├── health_check.py
│   │   ├── job_status.py
│   │   └── v1/
│   │       └── knowledges/  # Knowledge base endpoints
│   └── deps.py          # Dependency injection
├── core/                # Core configuration and utilities
│   ├── config.py        # Settings and environment variables
│   ├── security.py      # JWT and security utilities
│   └── logger.py        # Logging setup
├── db/                  # Database connections
│   ├── postgres.py      # PostgreSQL connection
│   ├── mongo.py         # MongoDB connection
│   └── minio.py         # MinIO connection
├── models/              # SQLAlchemy ORM models
│   └── user.py          # User model
├── schemas/             # Pydantic request/response schemas
│   ├── knowledges.py
│   └── user.py
├── services/            # Business logic
│   └── user.py
└── utils/               # Utility functions
    └── startup.py       # Initialization tasks
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)
- CUDA 12.6+ (optional, for GPU support)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KHARAPSY/ka-doe.git
   cd ka-doe
   ```

2. **Set up environment variables**
   
   See template in `.env`

3. **Start the application with Docker**

   Production

   ```bash
   make prod
   ```

   Development
   ```bash
   make dev
   ```

   Run with local databases
   ```bash
   make dbs # for production
   make dev-dbs # for development
   ```

4. **Access the application**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Setup

   Production

   ```bash
   make run
   ```

   Development
   ```bash
   make run-dev
   ```

## 📄 License

MIT License. See [LICENSE](LICENSE) for more info.

## ❤️ Acknowledgements

Built with care, curiosity, and cat-like precision. Powered by Python, FastAPI, and modern cloud infrastructure.