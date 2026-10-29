import os
from ollama import AsyncClient

async_client = AsyncClient()

async def call_local_llm(
        prompt: str, system_prompt: str, max_tokens: int, temperature: float):
    try:
        response = await async_client.chat(
            model="gemma3:4b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            options={
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        return {"text": response["message"]["content"], "model": "gemma-local", "tokens": len(prompt.split()) + len(response["message"]["content"].split())}
    except Exception as e:
        raise RuntimeError(f"Ollama Error server Error(Is 'ollama serve' running?): {str(e)}"
    
)