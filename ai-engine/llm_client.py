import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def call_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()
    return response.json()["response"]

def call_llm_json(prompt: str) -> dict:
    raw = call_llm(prompt)

    # Attempt to extract JSON safely
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to fix common formatting issues
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(raw[start:end])
            except:
                pass

        raise ValueError("LLM did not return valid JSON")