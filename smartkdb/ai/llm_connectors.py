import os
from typing import Optional

class LLMConnector:
    def __init__(self, provider: str = "openai", api_key: str = None):
        self.provider = provider
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def query(self, prompt: str) -> str:
        if self.provider == "openai":
            return self._query_openai(prompt)
        elif self.provider == "local":
            return self._query_local(prompt)
        else:
            return "Provider not supported."

    def _query_openai(self, prompt: str) -> str:
        # Stub for OpenAI API
        if not self.api_key:
            return "Error: No API Key provided."
        return f"[OpenAI Stub] Response to: {prompt}"

    def _query_local(self, prompt: str) -> str:
        # Stub for Local LLM (e.g., Llama.cpp)
        return f"[Local LLM Stub] Response to: {prompt}"
