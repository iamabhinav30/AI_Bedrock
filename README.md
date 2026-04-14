# Claude in Amazon Bedrock

Hands-on practice notebooks for the **Claude in Amazon Bedrock** course by [Anthropic](https://www.anthropic.com/) on [Skilljar](https://skilljar.com/).

## Overview

This repository contains Jupyter notebooks that explore using Claude via the Amazon Bedrock Converse API � covering API requests, multi-turn conversations, system messages, streaming, and controlling model output.

## Project Structure

```
AI_Bedrock/
+-- .env                          # AWS credentials (not committed)
+-- src/
�   +-- bedrock_client.py         # Shared AWS Bedrock client + model ID
�   +-- bedrock_helpers.py        # Shared helper functions (add_user_message, chat, etc.)
�   +-- working-with-api/
�       +-- 001_Api_requests.ipynb        # Basic API calls and multi-turn chat
�       +-- 002_System_messages.ipynb     # System prompts to control behavior
�       +-- 003_Streaming.ipynb           # Streaming responses with converse_stream
�       +-- 004_Controlling_output.ipynb  # Temperature, maxTokens, topP, stop sequences
```

## Notebooks

| # | Notebook | Description |
|---|----------|-------------|
| 1 | `001_Api_requests.ipynb` | Basic Converse API calls, multi-turn chat, interactive chatbot loop |
| 2 | `002_System_messages.ipynb` | Using system prompts to define Claude's persona and restrict topics |
| 3 | `003_Streaming.ipynb` | Streaming responses with `converse_stream`, handling all stream events |
| 4 | `004_Controlling_output.ipynb` | Controlling output via temperature, maxTokens, topP, and stop sequences |

## Shared Modules

| File | Purpose |
|------|---------|
| `src/bedrock_client.py` | Initializes the `boto3` Bedrock client and sets the `model_id_sonnet4` |
| `src/bedrock_helpers.py` | `add_user_message()`, `add_assistant_message()`, `chat_sonnet4()` (reusable across notebooks) |

Every notebook imports from these shared modules:
```python
from bedrock_client import client, model_id_sonnet4
from bedrock_helpers import add_user_message, add_assistant_message, chat_sonnet4
```

## Prerequisites

- Python 3.8+
- AWS account with Amazon Bedrock access
- Anthropic model access enabled (use case form submitted in Bedrock console)

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/iamabhinav30/AI_Bedrock.git
   cd AI_Bedrock
   ```

2. **Install dependencies**
   ```bash
   pip install boto3 python-dotenv
   ```

3. **Configure environment variables**

   Create a `.env` file in the root directory:
   ```env
   AWS_REGION=your-region
   AWS_ACCESS_KEY_ID=your-access-key-id
   AWS_SECRET_ACCESS_KEY=your-secret-access-key
   ```

4. **Open the notebooks** in VS Code and run from `src/working-with-api/`.

## Course

- **Course**: Claude in Amazon Bedrock
- **Provider**: Anthropic � AWS (via Skilljar)
- **Topics**: Bedrock Converse API, system messages, streaming, output control, multi-turn conversations

## Notes

- Model used: `apac.anthropic.claude-sonnet-4-20250514-v1:0` (APAC cross-region inference profile)
- Default `temperature` is `0.3` for consistent, focused responses
- Type `exit` in any interactive chat cell to end the conversation loop
