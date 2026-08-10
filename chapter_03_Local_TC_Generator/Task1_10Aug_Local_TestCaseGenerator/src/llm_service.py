"""LLM service layer — abstracts local Ollama and cloud Groq providers."""
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


# ── Abstract Provider ──────────────────────────────────────────────
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Return the LLM response for the given prompt."""
        ...


# ── Ollama (Local) ─────────────────────────────────────────────────
class OllamaProvider(LLMProvider):
    def __init__(self, model=None, base_url=None):
        import ollama
        self._ollama = ollama
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self._client = ollama.Client(host=self.base_url)
        configured = model or os.getenv("OLLAMA_MODEL", "").strip().strip('"')
        # Auto-detect: use configured model if available, otherwise first installed model
        try:
            installed = [m["name"] for m in self._client.list().get("models", [])]
        except Exception:
            installed = []
        if configured and any(configured in m for m in installed):
            self.model = configured
        elif installed:
            self.model = installed[0]
            print(f"[Ollama] Model '{configured}' not found, using '{self.model}' instead")
        else:
            self.model = configured or "llama3"

    def generate(self, prompt: str) -> str:
        response = self._client.generate(model=self.model, prompt=prompt)
        return response.get("response", "")

    def list_models(self):
        """Return available local models."""
        return self._client.list()


# ── Groq (Cloud) ───────────────────────────────────────────────────
class GroqProvider(LLMProvider):
    def __init__(self, api_key=None, model=None):
        from groq import Groq
        self.api_key = api_key or os.getenv("GROQ_API_TOKEN")
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        if not self.api_key:
            raise ValueError("GROQ_API_TOKEN not set in .env")
        self._client = Groq(api_key=self.api_key)

    def generate(self, prompt: str) -> str:
        completion = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a Senior QA Engineer."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=4096,
        )
        return completion.choices[0].message.content


# ── Service Factory ────────────────────────────────────────────────
class LLMService:
    """Selects the LLM provider based on configuration."""

    @staticmethod
    def get_provider(provider: str = "groq") -> LLMProvider:
        providers = {
            "groq": GroqProvider,
            "ollama": OllamaProvider,
        }
        cls = providers.get(provider.lower())
        if cls is None:
            raise ValueError(f"Unknown provider: {provider}. Use 'groq' or 'ollama'.")
        return cls()

    @staticmethod
    def generate(prompt: str, provider: str = "groq") -> str:
        return LLMService.get_provider(provider).generate(prompt)

    @staticmethod
    def test_ollama() -> tuple[bool, str]:
        """Test Ollama connection — returns (success, message)."""
        try:
            provider = OllamaProvider()
            response = provider.generate("Say OK in one word.")
            return True, f"✅ Connected — model: {provider.model}"
        except Exception as e:
            return False, f"❌ Ollama Error: {e}"

    @staticmethod
    def test_groq() -> tuple[bool, str]:
        """Test Groq connection — returns (success, message)."""
        try:
            provider = GroqProvider()
            response = provider.generate("Say OK in one word.")
            return True, f"✅ Connected — model: {provider.model}"
        except Exception as e:
            return False, f"❌ Groq Error: {e}"