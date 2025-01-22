from fastapi import APIRouter, Depends
from semantic_kernel.agents import ChatCompletionAgent

from agents.agent_01 import get_agent_01
from agents.agent_02 import get_agent_02
from config.settings import settings
from models.prompt import PromptRequest, PromptResponse
from services.llm import generate_model_response

router: APIRouter = APIRouter()


async def get_agent():
    if "gemini" in settings.LLM_MODEL:
        return await get_agent_02()
    else:
        return await get_agent_01()


@router.post("/prompt", response_model=PromptResponse)
async def get_prompt_response(
    request: PromptRequest,
    agent: ChatCompletionAgent = Depends(get_agent),
) -> PromptResponse:
    result = await generate_model_response(agent, request.prompt, request.user_id)
    return PromptResponse(response=result)
