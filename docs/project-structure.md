# Project Structure

Here’s a breakdown of Ka-Doe’s directory layout:

```plain
.
├── main.py # Entrypoint for the FastAPI app
├── api/ # Application logic
│ ├── helpers.py # Helper functions
│ ├── models.py # Data models
│ ├── loggings.py # Logging config
│ └── routes/ # API endpoints
│ └── v1/ # Version 1 routes
├── docs/ # MkDocs documentation
├── dockers/ # Docker and Compose files
├── requirements.txt # Python dependencies
├── settings.json # Editor settings
└── mkdocs.yml # MkDocs config
```