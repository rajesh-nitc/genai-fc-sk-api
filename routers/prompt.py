from fastapi import APIRouter, Depends
from semantic_kernel.agents import ChatCompletionAgent

from agents.agent_01 import get_agent_01
from models.prompt import PromptRequest, PromptResponse
from services.llm import generate_model_response

router: APIRouter = APIRouter()


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest,
    agent: ChatCompletionAgent = Depends(get_agent_01),
) -> PromptResponse:
    result = await generate_model_response(agent, request.prompt, request.user_id)
    return PromptResponse(response=result)
