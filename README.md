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

## TODO

- Threads API
- Workflows API
- Credentials API
- Webhooks API
- Async client support
- Error handling documentation
- Rate limiting
- Pagination support
- OAuth support
- Streaming responses
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
