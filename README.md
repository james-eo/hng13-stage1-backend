# String Analyzer Service

A RESTful API service that analyzes strings and stores their computed properties.

## Features

- Analyze string properties (length, palindrome check, character frequency, etc.)
- Store analyzed strings with SHA-256 hash identification
- Filter strings using various criteria
- Natural language query support
- Full CRUD operations on strings

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Local Development Setup

1. **Clone the repository**

   ```bash
   git clone git@github.com:james-eo/hng13-stage1-backend.git
   cd backend/stage1
   ```

2. **Create virtual environment** (recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   python3 -m app.main
   ```

   Or using uvicorn directly:

   ```bash
   uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - Base URL: `http://localhost:8000`
   - Interactive API docs: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

## API Endpoints

### 1. Create/Analyze String

```http
POST /strings
Content-Type: application/json

{
  "value": "string to analyze"
}
```

**Response (201 Created):**

```json
{
  "id": "sha256_hash_value",
  "value": "string to analyze",
  "properties": {
    "length": 17,
    "is_palindrome": false,
    "unique_characters": 12,
    "word_count": 3,
    "sha256_hash": "abc123...",
    "character_frequency_map": {
      "s": 2,
      "t": 3,
      "r": 2
    }
  },
  "created_at": "2025-10-21T10:00:00Z"
}
```

### 2. Get Specific String

```http
GET /strings/{string_value}
```

### 3. Get All Strings with Filtering

```http
GET /strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a
```

### 4. Natural Language Filtering

```http
GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings
```

### 5. Delete String

```http
DELETE /strings/{string_value}
```

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **Pydantic**: Data validation and settings management

## Testing

Run the test suite:

```bash
pip install pytest
pytest tests/test_api.py -v
```

## Environment Variables

No environment variables are required for basic operation. The application uses local file storage by default.

## Project Structure

```
backend/stage1/
├── app/
│   ├── __init__.py
│   ├── main.py           # Application entry point
│   ├── api.py            # FastAPI routes and endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── file_storage.py    # File-based storage implementation
│   │   └── string_model.py    # String data models
│   ├── services/
│   │   ├── __init__.py
│   │   └── analyzer.py        # String analysis logic
│   └── utils/
│       ├── __init__.py
│       └── nlp_parser.py      # Natural language query parser
├── data/
│   └── strings.json           # JSON file for data storage
├── tests/
│   └── test_api.py           # API endpoint tests
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Deployment

This application can be deployed on various platforms:

- **Railway**: `railway deploy`
- **Heroku**: Using Procfile and gunicorn
- **AWS**: Using Elastic Beanstalk or EC2
- **DigitalOcean App Platform**
- **Google Cloud Run**

### Example Procfile for Heroku:

```
web: uvicorn app.api:app --host 0.0.0.0 --port $PORT
```

## API Documentation

When running locally, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `422 Unprocessable Entity`: Invalid data types

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

## License

MIT License
