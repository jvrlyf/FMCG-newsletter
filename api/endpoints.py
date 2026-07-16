from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from api.pipeline import run_pipeline
from api.models import NewsletterRequest, NewsletterResponse, StatusResponse
from LLM.ollama import is_ollama_running, list_model_names

router = APIRouter()


@router.post("/generate", response_model=NewsletterResponse)
async def generate_newsletter(request: NewsletterRequest):
    try:
        html = await run_in_threadpool(
            run_pipeline, request.topic, request.region, request.date
        )
        return NewsletterResponse(success=True, html=html)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status", response_model=StatusResponse)
async def status():
    return StatusResponse(
        ollama_running=is_ollama_running(),
        models=list_model_names(),
    )
