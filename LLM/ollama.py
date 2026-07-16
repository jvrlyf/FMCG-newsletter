import os
import requests
from typing import Optional


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "minimax-m3:cloud")
OLLAMA_API = f"{OLLAMA_HOST}/api"


def is_ollama_running() -> bool:
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def list_model_names() -> list[str]:
    if not is_ollama_running():
        return []
    resp = requests.get(f"{OLLAMA_API}/tags", timeout=5)
    resp.raise_for_status()
    return [m["name"] for m in resp.json().get("models", [])]


def generate(
    prompt: str,
    model: Optional[str] = None,
    system: Optional[str] = None,
    temperature: float = 0.7,
) -> str:
    """Call Ollama with prompt, return response text."""
    if not is_ollama_running():
        raise RuntimeError("Ollama not running. Start with `ollama serve` or open GUI.")
    
    model = model or OLLAMA_MODEL
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    
    resp = requests.post(
        f"{OLLAMA_API}/chat",
        json={"model": model, "messages": messages, "stream": False, "options": {"temperature": temperature}},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]
