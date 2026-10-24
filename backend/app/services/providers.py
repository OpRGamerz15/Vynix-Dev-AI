"""
Provider adapter interface.
Implement concrete adapters (OllamaAdapter, etc.) when a free backend is available.
Never route to paid providers unless explicitly enabled with controls.
"""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any, List
from app.models import Model


class BaseProvider(ABC):
    @abstractmethod
    async def chat(self, model: Model, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Non-streaming completion. Must return OpenAI-compatible dict or raise."""
        pass

    @abstractmethod
    async def chat_stream(self, model: Model, messages: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        """Streaming chunks."""
        pass

    @abstractmethod
    async def health(self) -> bool:
        pass


class UnavailableProvider(BaseProvider):
    """Default provider used when no free backend is configured."""
    async def chat(self, model: Model, messages, **kwargs):
        raise RuntimeError(
            f"Model '{model.id}' has no configured free inference backend. "
            "Status is unavailable. Configure a self-hosted open-weight model to enable."
        )

    async def chat_stream(self, model: Model, messages, **kwargs):
        raise RuntimeError("Streaming unavailable — no backend configured.")
        yield  # pragma: no cover

    async def health(self) -> bool:
        return False


def get_provider_for_model(model: Model) -> BaseProvider:
    """Resolve provider. Currently always returns UnavailableProvider.
    Extend this when adding OllamaAdapter, vLLMAdapter, etc.
    """
    if model.status != "available" or not model.backend_type:
        return UnavailableProvider()
    # Future: if model.backend_type == "ollama": return OllamaAdapter(...)
    return UnavailableProvider()