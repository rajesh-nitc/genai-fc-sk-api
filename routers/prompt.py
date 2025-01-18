from fastapi import APIRouter, Depends
from semantic_kernel.agents import ChatCompletionAgent

from agents.func_calling import get_agent
from models.prompt import PromptRequest, PromptResponse
from services.llm import generate_model_response

router: APIRouter = APIRouter()


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest,
    agent: ChatCompletionAgent = Depends(get_agent),
) -> PromptResponse:
    result = await generate_model_response(agent, request.prompt, request.user_id)
    return PromptResponse(response=result)
