# genai-function-calling-api-v2

This API uses the Microsoft Semantic Kernel framework. It supports function calling with both Azure OpenAI models and Gemini models on Vertex AI. The model is provided with the day's chat history to maintain multi-turn context.

## Models Tested

- **gpt-4**
- **gpt-4o**
- **gpt-4o-mini**
- **gemini-1.5-pro**

## Features

1. **Generation with APIs** (e.g., `get_location_coordinates_func`, `get_weather_by_coordinates_func`)

## Getting Started 🚀

### Prerequisites

1. **Azure Authentication**:

```
echo 'export AZURE_OPENAI_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

2. **GCP Authentication**:

```
make gcp_app_auth
make gcp_gcloud_auth
```

3. **OpenWeather Authentication**:

```
echo 'export OPENWEATHER_API_KEY=YOUR_API_KEY_HERE' >> ~/.zshrc
```

4. **Application Settings**: Update variables in `config/settings.py` and `Makefile`.

5. **Additional Notes**:

- Dev Containers require Linux or WSL on Windows, along with VS Code (with the Dev Containers extension) and Docker Desktop.
- After updating environment variables in steps 1 and 3, open a new terminal to ensure the changes take effect.

- Makefile help:

```
make help
```

### Run

```
# Run Locally (Without Docker)
make run

# Run Locally (With Docker)
make docker

```

### Test

```
# Generation with APIs
make prompt PROMPT='what is 1+1 and how is the weather in bengaluru and mumbai?'

```
