from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

from agents.invoke import invoke_agent
from utils.gcs import append_chat_message_to_gcs, get_chat_messages


async def generate_model_response(
    agent: ChatCompletionAgent, prompt: str, user_id: str
) -> str:
    """ """
    history = get_chat_messages(user_id)
    chat = ChatHistory(messages=history)
    response = await invoke_agent(agent, prompt, chat)
    append_chat_message_to_gcs(
        user_id, ChatMessageContent(role=AuthorRole.USER, content=prompt)
    )
    append_chat_message_to_gcs(
        user_id, ChatMessageContent(role=AuthorRole.ASSISTANT, content=response)
    )
    return response
