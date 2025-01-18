import json
import logging

from google.cloud import storage
from semantic_kernel.contents.chat_message_content import ChatMessageContent

from config.settings import settings
from utils.date import get_today_date

LLM_CHAT_BUCKET = settings.LLM_CHAT_BUCKET

logger = logging.getLogger(__name__)


def get_gcs_client() -> storage.Client:
    """
    Get a Google Cloud Storage client
    """
    try:
        return storage.Client(project=settings.GOOGLE_CLOUD_PROJECT)
    except Exception as e:
        logger.error(f"Failed to initialize GCS client: {e}")
        raise


def get_file_path(user_id: str) -> str:
    """
    Generate day's GCS file path
    """
    today, _ = get_today_date()
    return f"{user_id}/{today}.json"


def get_chat_messages(user_id: str) -> list[ChatMessageContent]:
    """
    Retrieve day's chat history
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(LLM_CHAT_BUCKET)
        file_path = get_file_path(user_id)

        blob = bucket.blob(file_path)
        if blob.exists():
            messages = json.loads(blob.download_as_text())
            # Convert dicts to ChatMessage instances
            chat_messages = [ChatMessageContent(**msg) for msg in messages]
        else:
            chat_messages = []

        return chat_messages

    except Exception as e:
        logger.error(f"Error fetching chat messages for user {user_id}: {e}")
        raise


def append_chat_message_to_gcs(user_id: str, message: ChatMessageContent) -> None:
    """
    Append a new message to day's chat history.
    """
    try:
        client = get_gcs_client()
        bucket = client.bucket(LLM_CHAT_BUCKET)
        file_path = get_file_path(user_id)
        blob = bucket.blob(file_path)
        if blob.exists():
            # Download the existing file
            messages = json.loads(blob.download_as_text())
        else:
            # Start with an empty list if the file does not exist
            messages = []

        messages.append(message.model_dump())

        # Upload the updated list back to GCS
        blob.upload_from_string(json.dumps(messages), content_type="application/json")
    except Exception as e:
        logger.error(f"Error appending chat message for user {user_id}: {e}")
        raise
