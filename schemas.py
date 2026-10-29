from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    prompt: str = Field(
        ..., min_length=1, description="The input prompt for the model"
    )
    system_prompt: str = Field(
        "You are a helpful AI engineer assistant.",
        description="System context",
    )
    max_tokens: int = Field(
        200, ge=10, le=2000, description="Max tokens to generate"
    )
    temperature: float = Field(
        0.7, ge=0.0, le=2.0, description="Sampling temperature"
    )

class LLMResponse(BaseModel):
    response_text: str
    model_used: str
    tokens_consumed: int