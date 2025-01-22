from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.google.vertex_ai import (
    VertexAIChatCompletion,
    VertexAIChatPromptExecutionSettings,
)
from semantic_kernel.kernel import Kernel

from config.settings import settings
from plugins.add_plugins import add_plugins


async def get_agent_02():
    kernel = Kernel()
    add_plugins(kernel)

    agent_name = "agent_02"

    kernel.add_service(
        VertexAIChatCompletion(
            project_id=settings.GOOGLE_CLOUD_PROJECT,
            region=settings.GOOGLE_CLOUD_REGION,
            gemini_model_id=settings.LLM_MODEL,
        )
    )

    execution_settings = VertexAIChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    return ChatCompletionAgent(
        kernel=kernel,
        name=agent_name,
        instructions=settings.LLM_SYSTEM_INSTRUCTION,
        execution_settings=execution_settings,
    )
