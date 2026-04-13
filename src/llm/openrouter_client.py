"""OpenRouter LLM Integration using LangChain."""

import os
from pathlib import Path
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, BaseMessage

# Try to load .env file
def _load_env():
    """Load .env file from project root."""
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
        except ImportError:
            # dotenv not installed, skip loading
            pass

_load_env()


class OpenRouterClient:
    """Client for interacting with OpenRouter API via LangChain."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "anthropic/claude-3.5-sonnet",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        base_url: str = "https://openrouter.ai/api/v1",
    ):
        """
        Initialize the OpenRouter client.

        Args:
            api_key: OpenRouter API key. Falls back to OPENROUTER_API_KEY env var.
            model: Model identifier (default: anthropic/claude-3.5-sonnet)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            base_url: OpenRouter API endpoint
        """
        self.api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided or set via OPENROUTER_API_KEY environment variable"
            )

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url

        self._llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            base_url=self.base_url,
            api_key=self.api_key,
            # OpenRouter requires custom headers
            default_headers={
                "HTTP-Referer": "https://github.com/master-thesis-prototype",
                "X-Title": "DCAT-AP.de Quality Analyzer",
            },
        )

    def generate(
        self,
        prompt: str,
        system_message: Optional[str] = None,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: User prompt
            system_message: Optional system message for context

        Returns:
            LLM response as string
        """
        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))
        messages.append(HumanMessage(content=prompt))

        response = self._llm.invoke(messages)
        return response.content

    def generate_with_messages(
        self,
        messages: list[BaseMessage],
    ) -> str:
        """
        Generate a response with explicit message list.

        Args:
            messages: List of BaseMessage objects (SystemMessage, HumanMessage)

        Returns:
            LLM response as string
        """
        response = self._llm.invoke(messages)
        return response.content

    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "base_url": self.base_url,
        }


def create_client(
    api_key: Optional[str] = None,
    model: str = "anthropic/claude-3.5-sonnet",
    **kwargs
) -> OpenRouterClient:
    """
    Factory function to create an OpenRouter client.

    Args:
        api_key: OpenRouter API key
        model: Model identifier
        **kwargs: Additional arguments passed to OpenRouterClient

    Returns:
        Configured OpenRouterClient instance
    """
    return OpenRouterClient(
        api_key=api_key,
        model=model,
        **kwargs
    )


# Example usage
if __name__ == "__main__":
    # Set API key via environment variable
    # export OPENROUTER_API_KEY="your-api-key"

    try:
        client = create_client(model="anthropic/claude-3.5-sonnet")

        # Simple generation
        response = client.generate(
            system_message="You are a helpful assistant.",
            prompt="Explain DCAT-AP.de in one sentence."
        )
        print(f"Response: {response}")

        # Get model info
        print(f"Model Info: {client.get_model_info()}")

    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")