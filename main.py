from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from schemas import LLMRequest, LLMResponse
from services import async_client, call_local_llm  # Updated import
app=FastAPI(title="Local AI Engineering Gateway", version="1.0", description="FastAPI backend powered by local LLM",)

@app.get("/", response_class=HTMLResponse)
def get_index():
    with open("index.html", "r") as f:
        return f.read()
def health_check():
    return {"status": "online", "engineer": "EVARIST-DEV AI ENGINEER", "backend": "Local Ollama (gemma3:4b)",}

@app.post("/v1/generate", response_model=LLMResponse)
async def generate_text(payload: LLMRequest):
    try:
        result = await call_local_llm(
            prompt=payload.prompt,
            system_prompt=payload.system_prompt,
            max_tokens=payload.max_tokens,
            temperature=payload.temperature,
        )
        return LLMResponse(
            response_text=result["text"],
            model_used=result["model"],
            tokens_consumed=result["tokens"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def token_generator(payload: LLMRequest):
    stream = await async_client.chat(
      model="gemma3:4b",
      messages=[
          {"role": "system", "content": payload.system_prompt},
          {"role": "user", "content": payload.prompt},
      ],
      options={"temperature": payload.temperature},
      stream=True,
  )
    
    async for chunk in stream:
        yield chunk["message"]["content"]
        if delta:
            yield f"data: {delta}\n\n"

@app.post("/v1/stream")
async def stream_test(payload: LLMRequest):
 return StreamingResponse(token_generator(payload), media_type="text/event-stream")