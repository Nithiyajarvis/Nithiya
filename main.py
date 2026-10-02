
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# Load environment variables
load_dotenv()


# -----------------------------------
# FastAPI Application
# -----------------------------------

app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="Google Gemini powered educational assistant",
    version="1.0.0"
)


# -----------------------------------
# Static Files
# -----------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# -----------------------------------
# HTML Templates
# -----------------------------------

templates = Jinja2Templates(
    directory="templates"
)


# -----------------------------------
# Request Models
# -----------------------------------

class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=50000
    )


# -----------------------------------
# Home Page
# -----------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


# -----------------------------------
# Health Check
# -----------------------------------

@app.get("/health")
async def health():
    return {
        "status": "running",
        "gemini_configured": bool(
            os.getenv("GEMINI_API_KEY")
        )
    }


# -----------------------------------
# Q&A API
# -----------------------------------

@app.post("/qa")
async def qa(request: QuestionRequest):
    try:
        answer = answer_question(
            request.question
        )

        return {
            "success": True,
            "result": answer
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------------
# Explanation API
# -----------------------------------

@app.post("/explain")
async def explain(request: TextRequest):
    try:
        explanation = explain_concept(
            request.text
        )

        return {
            "success": True,
            "result": explanation
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------------
# Quiz API
# -----------------------------------

@app.post("/quiz")
async def quiz(request: TextRequest):
    try:
        quiz = generate_quiz(
            request.text
        )

        return {
            "success": True,
            "result": quiz
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------------
# Summary API
# -----------------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        summary = summarize_text(
            request.text
        )

        return {
            "success": True,
            "result": summary
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# -----------------------------------
# Learning Path API
# -----------------------------------

@app.post("/learn/recommendations")
async def learning_path(request: TextRequest):
    try:
        recommendations = get_learning_recommendations(
            request.text
        )

        return {
            "success": True,
            "result": recommendations
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

