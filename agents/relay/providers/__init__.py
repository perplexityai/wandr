"""Provider implementations live in provider-owned modules."""
from relay.core import EndpointFactory, RelayError
from relay.providers.anthropic import AnthropicManagedEndpoint
from relay.providers.exa import ExaAgentEndpoint
from relay.providers.gemini import GeminiDeepResearchEndpoint
from relay.providers.openai import OpenAIResponsesEndpoint
from relay.providers.parallel import ParallelTaskEndpoint
from relay.providers.perplexity import PerplexityAgentAPIEndpoint

PROVIDERS: dict[str, EndpointFactory] = {
    "anthropic": AnthropicManagedEndpoint,
    "exa": ExaAgentEndpoint,
    "gemini": GeminiDeepResearchEndpoint,
    "openai": OpenAIResponsesEndpoint,
    "parallel": ParallelTaskEndpoint,
    "perplexity": PerplexityAgentAPIEndpoint,
}


def endpoint_factory(provider: str) -> EndpointFactory:
    try:
        return PROVIDERS[provider]
    except KeyError as exc:
        raise RelayError(f"Unknown relay provider: {provider}") from exc
