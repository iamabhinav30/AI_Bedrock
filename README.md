# Claude in Amazon Bedrock

Hands-on practice notebooks for the **Claude in Amazon Bedrock** course by [Anthropic](https://www.anthropic.com/) on [Skilljar](https://skilljar.com/).

## Overview

This repository contains Jupyter notebooks that explore using Claude via the Amazon Bedrock Converse API — covering API requests, multi-turn conversations, and system messages.

## Notebooks

| # | Notebook | Description |
|---|----------|-------------|
| 1 | `src/001_Api_requests.ipynb` | Basic API calls, multi-turn chat, and an interactive chatbot loop |
| 2 | `src/002_System_messages.ipynb` | Using system messages to control Claude's behavior |

## Prerequisites

- Python 3.8+
- AWS account with Amazon Bedrock access
- Anthropic model access enabled in Bedrock (use case form submitted)

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

4. **Run the notebooks** using VS Code or JupyterLab.

## Course

- **Course**: Claude in Amazon Bedrock
- **Provider**: Anthropic × AWS (via Skilljar)
- **Topics**: Bedrock Converse API, prompt engineering, system messages, multi-turn conversations

## Notes

- The model used is `apac.anthropic.claude-sonnet-4-20250514-v1:0` (APAC cross-region inference profile)
- Type `exit` in the interactive chat cell to end the conversation loop
