import logging

from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)
from semantic_kernel.connectors.ai.google.vertex_ai import (
    VertexAIChatCompletion,
    VertexAIChatPromptExecutionSettings,
)
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.kernel import Kernel

from config.settings import settings
from plugins.add_plugins import add_plugins

logger = logging.getLogger(__name__)


async def get_agent():
    kernel = Kernel()
    add_plugins(kernel)

    service_id = "agent"

    if "gpt" in settings.LLM_MODEL:
        kernel.add_service(
            AzureChatCompletion(
                service_id=service_id,
                api_key=settings.AZURE_OPENAI_API_KEY,
                endpoint=settings.AZURE_OPENAI_ENDPOINT,
                deployment_name=settings.LLM_MODEL,
            )
        )

        execution_settings = kernel.get_prompt_execution_settings_from_service_id(
            service_id=service_id
        )
        execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
        return ChatCompletionAgent(
            service_id=service_id,
            kernel=kernel,
            name=settings.APP_NAME,
            instructions=settings.LLM_SYSTEM_INSTRUCTION,
            execution_settings=execution_settings,
        )

    elif "gemini" in settings.LLM_MODEL:
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
            name=settings.APP_NAME,
            instructions=settings.LLM_SYSTEM_INSTRUCTION,
            execution_settings=execution_settings,
        )
    else:
        raise ValueError(f"Unsupported model type: {settings.LLM_MODEL}")


async def invoke_agent(
    agent: ChatCompletionAgent, prompt: str, chat: ChatHistory
) -> str:
    """
    Invoke the agent with the user prompt.
    """
    agent = await get_agent()
    chat.add_user_message(prompt)
    print(f"# {AuthorRole.USER}: '{prompt}'")

    streaming = False
    response_content = ""

    if streaming:
        contents = []
        content_name = ""
        async for content in agent.invoke_stream(chat):
            content_name = content.name
            contents.append(content)
        response_content = "".join([content.content for content in contents])
        print(f"# {content.role} - {content_name or '*'}: '{response_content}'")
        chat.add_assistant_message(response_content)
    else:
        async for content in agent.invoke(chat):
            response_content = content.content
            print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        chat.add_message(content)
    return response_content
