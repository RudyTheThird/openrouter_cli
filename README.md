
# OpenRouter API CLI Tool

This script interacts with OpenRouter's API to perform chat completions with LLMs.

## Setup Instructions

1. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/openrouter_cli.git
   cd openrouter_cli
   ```

2. Install Dependencies:
   ```bash
   pip install requests
   ```

3. Set API Key:
   ```bash
   export OPENROUTER_API_KEY="your_api_key_here"
   ```

4. Run the Script:
   ```bash
   python openrouter_cli.py --mode chat --model gpt-4 --input "Hello!"
   ```

## Supported Models
- GPT-4
- Claude-3

## License
MIT License
