from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.contents.chat_history import ChatHistory


async def invoke_agent(
    agent: ChatCompletionAgent, prompt: str, chat: ChatHistory
) -> str:
    """
    Invoke the agent with the user prompt.
    """
    chat.add_user_message(prompt)

    streaming = False
    response_content = ""

    if streaming:
        contents = []
        async for content in agent.invoke_stream(chat):
            content.name
            contents.append(content)
        response_content = "".join([content.content for content in contents])
        chat.add_assistant_message(response_content)
    else:
        async for content in agent.invoke(chat):
            response_content = content.content
        chat.add_message(content)
    return response_content
