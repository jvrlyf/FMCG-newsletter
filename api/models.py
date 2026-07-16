from pydantic import BaseModel
from typing import List, Optional

class NewsletterRequest(BaseModel):
    topic: str = "ma-funding"
    region: str = "india"
    date: str = "today"

class NewsletterResponse(BaseModel):
    success: bool
    html: Optional[str] = None
    error: Optional[str] = None

class StatusResponse(BaseModel):
    ollama_running: bool
    models: List[str]
