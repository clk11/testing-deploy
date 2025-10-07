# FastAPI OpenAI Project

A simple FastAPI application with OpenAI GPT-4o-mini integration and a web interface for asking questions.

## Features

- FastAPI web framework with HTML template serving
- OpenAI GPT-4o-mini integration for question answering
- Interactive web interface at the root endpoint
- Environment variable configuration
- Proper error handling and logging

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the `.env` file and add your OpenAI API key:

```bash
# Edit .env file
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

You can get your OpenAI API key from: https://platform.openai.com/api-keys

### 3. Run the Application

```bash
# Using Python directly
python main.py

# Or using uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative API docs**: http://localhost:8000/redoc

## API Endpoints

### GET `/`
Serves the interactive HTML page where you can ask questions to GPT-4o-mini.

### POST `/ask`
API endpoint for asking questions to GPT-4o-mini.

**Request Body:**
```json
{
  "question": "Your question here"
}
```

**Response:**
```json
{
  "answer": "GPT-4o-mini response here"
}
```

## Example Usage

### Web Interface (Recommended):
1. Open your browser and go to http://localhost:8000
2. Enter your question in the text field
3. Click "Ask Question" or press Enter
4. View the GPT-4o-mini response

### Using curl:
```bash
# Ask a question via API
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the capital of France?"}'
```

### Using Python requests:
```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "Tell me a joke"}
)
print(response.json())
```

## Project Structure

```
testing_project/
├── main.py           # FastAPI application
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (add your API key here)
├── .gitignore       # Git ignore rules
├── templates/        # HTML templates
│   └── index.html   # Main web interface
└── README.md        # This file
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `APP_NAME`: Application name (optional, defaults to "FastAPI OpenAI Project")
- `DEBUG`: Debug mode (optional, defaults to True)

## Development

The application runs in debug mode by default with auto-reload enabled. This means the server will restart automatically when you make changes to the code.

## Error Handling

The application includes proper error handling for:
- Missing or invalid OpenAI API key
- OpenAI API errors
- Invalid request data

## Security Notes

- Never commit your `.env` file with real API keys to version control
- The `.env` file is already included in `.gitignore`
- Consider using environment-specific configuration for production deployments