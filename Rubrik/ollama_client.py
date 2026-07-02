import os
import requests

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama.ai-platform.svc.cluster.local:11434/api/generate"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "tinyllama:latest"
)


def ask_ollama(prompt):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]
