from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI OpenAI Project"),
    description="A FastAPI project with OpenAI GPT-4o-mini integration",
    version="1.0.0"
)

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key or openai_api_key == "your_openai_api_key_here":
    logger.warning("OpenAI API key not properly configured!")
    openai_client = None
else:
    try:
        openai_client = OpenAI(api_key=openai_api_key)
        logger.info("OpenAI client initialized successfully!")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {str(e)}")
        openai_client = None

# Pydantic models
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main HTML page"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "app_name": os.getenv("APP_NAME", "FastAPI OpenAI Project"),
        "openai_configured": openai_client is not None
    })

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question to GPT-4o-mini"""
    if not openai_client:
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."
        )
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": request.question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return QuestionResponse(answer=response.choices[0].message.content)
    
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        # If gpt-4o-mini is not available, try gpt-3.5-turbo
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": request.question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return QuestionResponse(answer=response.choices[0].message.content)
        except Exception as e2:
            logger.error(f"Fallback OpenAI API error: {str(e2)}")
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    debug_mode = os.getenv("DEBUG", "True").lower() == "true"
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=debug_mode
    )