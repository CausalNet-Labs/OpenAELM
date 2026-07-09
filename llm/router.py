"""Optional LLM chat router.

This is the ONLY module in AELM that touches the network, and it is
entirely optional. It activates only when the user provides a token via
the AELM_HF_TOKEN environment variable (an OpenAI-compatible endpoint
can be pointed at with AELM_API_URL, including a local server such as
llama.cpp or Ollama for a fully self-hosted setup).
"""

from ..config import CONFIG
from ..session import session
from .system_prompt import SYSTEM_PROMPT


def chat_available() -> bool:
    return bool(CONFIG.api_token)


def chat(prompt: str) -> str:
    if not chat_available():
        raise RuntimeError(
            "Chat is disabled. Set the AELM_HF_TOKEN environment variable "
            "(and optionally AELM_API_URL to use a local model server)."
        )

    try:
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "Chat requires the optional 'requests' package "
            "(pip install requests)."
        ) from exc

    session.conversation.append({"role": "user", "content": prompt})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(session.conversation[-CONFIG.max_history:])

    try:
        response = requests.post(
            CONFIG.api_url,
            headers={
                "Authorization": f"Bearer {CONFIG.api_token}",
                "Content-Type": "application/json",
            },
            json={
                "model": CONFIG.model,
                "messages": messages,
                "temperature": CONFIG.temperature,
                "max_tokens": CONFIG.max_tokens,
            },
            timeout=CONFIG.timeout,
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception:
        session.conversation.pop()  # keep history consistent on failure
        raise

    session.conversation.append({"role": "assistant", "content": reply})
    return reply
