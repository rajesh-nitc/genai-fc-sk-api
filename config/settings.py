from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings

from utils.text import dedent_and_strip


class Settings(BaseSettings):
    APP_NAME: str = Field(
        "genai-function-calling-api-v2", description="Name of the application."
    )
    AZURE_OPENAI_API_KEY: str = Field(
        ...,  # Required field (this means it must be provided through env)
        json_schema_extra={"env": "AZURE_OPENAI_API_KEY"},
        description="Azure OpenAI API key.",
    )
    AZURE_OPENAI_ENDPOINT: str = Field(
        "https://oai-function-calling-api-06.openai.azure.com/",
        description="Azure OpenAI endpoint.",
    )
    ENV: Literal["local", "dev", "npr", "prd"] = Field(
        "local", description="Application environment."
    )
    GOOGLE_CLOUD_PROJECT: str = Field(
        "prj-bu1-d-sample-base-9208", description="The Google Cloud project ID."
    )
    GOOGLE_CLOUD_REGION: Literal["us-central1"] = Field(
        "us-central1", description="The GCP region."
    )
    HTTP_CLIENT_BASE_URL: str = Field(
        "https://api.openweathermap.org", description="OpenWeather API base url"
    )
    LLM_CHAT_BUCKET: str = Field(
        "bkt-bu1-d-function-calling-api-chat",
        description="Bucket for storing chat history.",
    )
    LLM_MODEL: Literal[
        "gpt-4",
        "gpt-4o",
        "gpt-4o-mini",
        "gemini-1.5-flash",
    ] = Field("gemini-1.5-flash", description="The foundation model to use.")
    LLM_SYSTEM_INSTRUCTION: str = Field(
        dedent_and_strip(
            """
            You are a helpful assistant.
        """
        ),
        description="System instruction for the Model.",
    )
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        "INFO", description="Logging level."
    )
    OPENWEATHER_API_KEY: str = Field(
        ...,  # Required field (this means it must be provided through env)
        json_schema_extra={"env": "OPENWEATHER_API_KEY"},
        description="OpenWeather API key.",
    )


settings = Settings()  # type: ignore
