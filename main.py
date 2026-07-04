from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

# The internal DNS routing directly to your vLLM pod(s)
# Format: http://<service-name>:<port>/v1
LLM_BASE_URL = os.getenv("LLM_INTERNAL_URL", "http://llm-service:8000/v1")

# Initialize the client. The API key is required by the SDK but ignored by vLLM.
client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key="not-needed"
)

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat_with_model(request: ChatRequest):
    try:
        # The model name must exactly match what you passed in the vLLM deployment arguments
        response = client.chat.completions.create(
            model="Qwen/Qwen1.5-0.5B-Chat",
            messages=[
                {"role": "system", "content": "You are a highly capable and concise AI assistant."},
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "FastAPI is running and ready to proxy to the LLM"}
