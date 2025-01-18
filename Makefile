# Variables
APP_NAME=genai-function-calling-api-v2
GOOGLE_CLOUD_PROJECT=prj-bu1-d-sample-base-9208
LLM_CHAT_BUCKET=bkt-bu1-d-function-calling-api-chat

# Adding so that make does not conflict with files or directory with the same names as target
# For e.g. "make tests" won't work unless we add tests as a phony target
.PHONY: help gcp_app_auth gcp_gcloud_auth gcp_clear_history gcp_credentials_base64 \
run prompt tests precommit docker docker_clean

help: ## Self-documenting help command
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

check_venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Error: Virtual environment is not activated. Please activate it and try again."; \
		exit 1; \
	fi

gcp_app_auth: ## App Auth with gcp
	gcloud auth application-default login
	gcloud auth application-default set-quota-project $(GOOGLE_CLOUD_PROJECT)
	gcloud config set project $(GOOGLE_CLOUD_PROJECT)

gcp_gcloud_auth: ## gcloud sdk Auth (Required for gsutil command in gcp_clear_history)
	gcloud auth login

gcp_clear_history: ## Clear gcs bucket contents (To clear the history)
	gsutil -m rm -r gs://$(LLM_CHAT_BUCKET)/**

gcp_credentials_base64: ## Base64 encode JSON creds (Use this for Github Actions Repository secret)
	base64 ~/.config/gcloud/application_default_credentials.json > credentials.json.base64
	cat credentials.json.base64
	rm credentials.json.base64

run: check_venv ## Run the application locally
	bash ./start.sh

prompt: ## Send an api request (e.g., make prompt PROMPT='what is 1+1')
	curl -X 'POST' 'http://localhost:8000/api/prompt' \
  	-H 'Content-Type: application/json' \
  	-d '{ "prompt": "$(PROMPT)", "user_id": "rajesh-nitc" }'

# Run test cases with --test-cases="weather"
tests: check_venv ## Run integration tests
	pytest -m integration --test-cases="weather"

precommit: check_venv ## Run pre-commit checks
	pre-commit run --all-files

docker: ## Run in docker (Add Openai API key, OpenWeather API key and update other variables)
	sudo docker build -t $(APP_NAME) .
	sudo docker run -d -p 8000:8000 \
        -v ~/.config/gcloud/application_default_credentials.json:/tmp/keys/credentials.json \
        -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/keys/credentials.json \
        -e APP_NAME=$(APP_NAME) \
		-e AZURE_OPENAI_API_KEY="" \
		-e AZURE_OPENAI_ENDPOINT="https://oai-function-calling-api.openai.azure.com/" \
        -e ENV="local" \
        -e GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT) \
		-e GOOGLE_CLOUD_REGION="us-central1" \
		-e HTTP_CLIENT_BASE_URL="https://api.openweathermap.org" \
        -e LLM_CHAT_BUCKET="bkt-bu1-d-function-calling-api-chat" \
        -e LLM_MODEL="gemini-1.5-flash" \
        -e LLM_SYSTEM_INSTRUCTION="You are a helpful assistant." \
        -e LOG_LEVEL="INFO" \
		-e OPENWEATHER_API_KEY="" \
        --name $(APP_NAME) \
        $(APP_NAME)

docker_clean: ## Stop and remove the Docker container
	sudo docker stop $(APP_NAME)
	sudo docker rm $(APP_NAME)
