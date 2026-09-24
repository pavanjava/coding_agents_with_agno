import argparse
import os

import questionary
from dotenv import load_dotenv

from qdrant_agent.agent import PROVIDER_API_KEY_ENV, PROVIDER_MODELS, TAVILY_API_KEY_ENV, build_team

PROVIDERS = list(PROVIDER_MODELS)


def _pick(role: str) -> tuple[str, str]:
    provider = questionary.select(f"Provider for the {role} agent:", choices=PROVIDERS).ask()
    model = questionary.select(f"Model for the {role} agent:", choices=PROVIDER_MODELS[provider]).ask()
    return provider, model


def _ensure_key(env_var: str) -> None:
    if not os.getenv(env_var):
        os.environ[env_var] = questionary.password(f"{env_var} (not set — enter it now):").ask()


def _pick_qdrant_connection() -> str:
    kind = questionary.select(
        "Qdrant instance to connect to:",
        choices=["Local / Docker (host + port)", "Qdrant Cloud / custom URL"],
    ).ask()

    if kind == "Local / Docker (host + port)":
        host = questionary.text("Host:", default="localhost").ask()
        port = questionary.text("Port:", default="6333").ask()
        url = f"http://{host}:{port}"
    else:
        url = questionary.text("Qdrant URL (e.g. https://xyz.cloud.qdrant.io:6333):").ask()

    if questionary.confirm("Does this instance require an API key?", default=False).ask():
        os.environ["QDRANT_API_KEY"] = questionary.password("Qdrant API key:").ask()
        auth_note = "It requires an API key — read it from the QDRANT_API_KEY environment variable in code, never hardcode it."
    else:
        auth_note = "It does not require an API key."

    return f"Qdrant instance already confirmed by the user, do not ask again: {url}. {auth_note}"


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Qdrant coding agent")
    parser.add_argument("dir", nargs="?", default=".", help="Working directory for the agent")
    args = parser.parse_args()

    coder_provider, coder_model = _pick("coder")
    critic_provider, critic_model = _pick("critic")

    for provider in {coder_provider, critic_provider}:
        _ensure_key(PROVIDER_API_KEY_ENV[provider])
    _ensure_key(TAVILY_API_KEY_ENV)

    qdrant_context = _pick_qdrant_connection()

    team = build_team(args.dir, coder_provider, coder_model, critic_provider, critic_model, qdrant_context)
    team.cli_app(markdown=True)


if __name__ == "__main__":
    main()
