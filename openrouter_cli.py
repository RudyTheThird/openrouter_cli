import requests
import time
import argparse
import json
import os

# Constants
OPENROUTER_API_URL = "https://openrouter.ai/api/v1"
API_KEY = os.getenv("OPENROUTER_API_KEY")  # Store your API key in an environment variable

# Supported Models and Costs
MODELS = {
    "gpt-4": {"name": "openai/gpt-4", "cost_per_1k_tokens": 0.03},
    "claude-3": {"name": "anthropic/claude-3", "cost_per_1k_tokens": 0.015},
    "claude-3.5-haiku": {"name": "anthropic/claude-3.5-haiku", "cost_per_1k_tokens": 0.000004}
}

# Rate limiting
RATE_LIMIT_WAIT = 2  # seconds


def chat_completion(model, user_input):
    """Interact with the chat completion endpoint."""
    url = f"{OPENROUTER_API_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": user_input}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        content = data['choices'][0]['message']['content']
        token_usage = data.get('usage', {}).get('total_tokens', 0)
        cost = (token_usage / 1000) * MODELS.get(model, {}).get('cost_per_1k_tokens', 0)
        
        print(f"\nResponse:\n{content}")
        print(f"\nTokens used: {token_usage}, Estimated Cost: ${cost:.4f}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error during chat completion: {e}")
    except KeyError as e:
        print(f"Unexpected response structure: {e}")
    
    time.sleep(RATE_LIMIT_WAIT)


def embedding(model, text):
    """Interact with the embedding endpoint."""
    url = f"{OPENROUTER_API_URL}/embeddings"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "input": text
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        embedding_vector = data['data'][0]['embedding']
        token_usage = data.get('usage', {}).get('total_tokens', 0)
        cost = (token_usage / 1000) * MODELS.get(model, {}).get('cost_per_1k_tokens', 0)
        
        print(f"\nEmbedding Vector (first 5 dimensions): {embedding_vector[:5]}")
        print(f"\nTokens used: {token_usage}, Estimated Cost: ${cost:.4f}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error during embedding: {e}")
    except KeyError as e:
        print(f"Unexpected response structure: {e}")
    
    time.sleep(RATE_LIMIT_WAIT)


def main():
    parser = argparse.ArgumentParser(description="OpenRouter API CLI Interface")
    parser.add_argument('--mode', choices=['chat', 'embedding'], required=True, help="Select API mode: chat or embedding")
    parser.add_argument('--model', choices=MODELS.keys(), required=True, help="Choose the LLM model")
    parser.add_argument('--input', type=str, required=True, help="User input for chat or embedding")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: OPENROUTER_API_KEY is not set. Please set it as an environment variable.")
        return

    model_name = MODELS[args.model]['name']

    if args.mode == 'chat':
        chat_completion(model_name, args.input)
    elif args.mode == 'embedding':
        embedding(model_name, args.input)


if __name__ == "__main__":
    main()
