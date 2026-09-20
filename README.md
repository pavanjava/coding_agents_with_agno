# qdrant-agent

A CLI coding agent for Qdrant only. Backed by an Agno team of two models (OpenAI + Claude) with file/shell tools, reasoning, web search, and vendored Qdrant skills.

## Install

```bash
uv venv
uv pip install -e .
```

(Or `pip install -e .` if you're not using `uv`.)

## Configure keys

Export the keys in your shell, or copy `.env.example` to `.env` and fill them in:

```bash
cp .env.example .env
```

```
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
TAVILY_API_KEY=...
```

Exported shell env vars always take priority over `.env`.

### Exporting the keys in your shell

Run these once per shell session:

```bash
export OPENAI_API_KEY=your-openai-key
export ANTHROPIC_API_KEY=your-anthropic-key
export TAVILY_API_KEY=your-tavily-key
```

To persist them across sessions, add the same three lines to your shell profile (`~/.zshrc` for zsh, `~/.bashrc` for bash) and restart your shell or run `source ~/.zshrc`.

## Run

```bash
qdrant-agent [dir]
```

`dir` is the working directory the agent can read/write/run shell commands in (defaults to the current directory). This starts an interactive session — the agent will ask which Qdrant instance (local, Docker, Cloud, or a host/URL) to target before writing any code.

## Memory

Conversation history is remembered within a run and across separate `qdrant-agent` runs in the same directory (e.g. the Qdrant instance and task you already described won't need to be repeated). It's stored per-directory in `~/.qdrant_agent/sessions.json`. Delete that file, or the folder, to reset all memory.
