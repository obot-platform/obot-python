# Obot Python Client

A Python client for interacting with the Obot API.

## Installation (in development, not published to PyPI)

```bash
poetry install
```

The following won't work until published to PyPI:

```bash
pip install obot-python
```

## Quick Start

```python
from obot.sync_client import ObotClient

client = ObotClient(
    base_url="http://localhost:8080",
    token="your-token"
)
```

## Chat

The chat interface provides a simple way to interact with agents:

```python
# Start a conversation
conv = client.chat("a18pjdh", "Hi there!")
print(conv)  # prints the agent's response

# Continue the conversation using the same thread
response = conv.chat("What's 2+2?")
print(response)

# Stream responses in real-time
for chunk in conv.chat("Tell me a story", stream=True):
    print(chunk, end="", flush=True)
```

### Async Support

For async applications:

```python
from obot.async_client import AsyncObotClient
import asyncio

async def main():
    client = AsyncObotClient(
        base_url="http://localhost:8080",
        token="your-token"
    )
    
    # Start a conversation
    conv = await client.chat("a18pjdh", "Hi there!")
    print(conv)  # prints response
    
    # Continue conversation
    response = await conv.achat("What's 2+2?")
    print(response)
    
    # Stream responses
    async for chunk in await conv.achat("Tell me a story", stream=True):
        print(chunk, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
```

## Tools

List all available tools and their categories:

```python
# List all tools
all_tools = client.tools()

# List all tool categories
categories = client.tools.categories()

# List tools in a specific category
slack_tools = client.tools(category="Slack")
```

## Models

Work with models and model providers:

```python
# List all model providers
providers = client.models.providers()

# List only configured providers
configured_providers = client.models.providers(configured=True)

# List all models
all_models = client.models()

# List active models from a specific provider
active_models = client.models(
    model_provider="openai-model-provider",
    active=True
)
```

## Agents

Create and manage agents:

```python
# List all agents
all_agents = client.agents()

# Get a specific agent
agent = client.agents.get("a1-obot")

# Create a new agent
new_agent = client.agents.create(
    name="Test Agent",
    description="A test agent",
    prompt="You are a helpful assistant",
    model="grok-beta",  # Will be converted to model ID
    tools=["google-search-bundle", "slack-send-message"]  # Tool IDs
)

# Update specific fields of an agent
updated_agent = client.agents.update(
    agent_id="a1-agent-id",
    name="New Name",  # Only updates the name
    tools=["google-search-bundle"]  # Only updates the tools
)
```

### Notes

- When creating or updating agents, model names are automatically converted to model IDs
- Tool IDs are validated to ensure they exist
- Updates only modify the specified fields, preserving other settings
- Chat responses can be streamed in real-time
- Both synchronous and asynchronous clients are supported
- Conversations maintain thread context automatically

## TODO

- Workflows API
- Credentials API
- Webhooks API
- Error handling documentation
- Rate limiting
- Pagination support
- OAuth support
- CLI tool
- Type hints documentation
- More examples and use cases
- Unit tests
- Integration tests

## Development

To contribute to this project:

1. Clone the repository
2. Install Poetry (if you haven't already): `curl -sSL https://install.python-poetry.org | python3 -`
3. Install dependencies: `poetry install`

You can also activate the virtual environment directly:

```bash
poetry shell
pytest
```
