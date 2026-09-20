import hashlib
import os
from pathlib import Path

from agno.agent import Agent
from agno.db.json import JsonDb
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from agno.skills import LocalSkills, Skills
from agno.team import Team
from agno.tools.coding import CodingTools
from agno.tools.tavily import TavilyTools

from qdrant_agent.instructions import CODER_INSTRUCTIONS, CRITIC_INSTRUCTIONS, TEAM_INSTRUCTIONS

SKILLS_DIR = Path(__file__).parent / "skills"
SESSIONS_DB_PATH = Path.home() / ".qdrant_agent" / "sessions.json"

OPENAI_MODEL = os.getenv("QDRANT_AGENT_OPENAI_MODEL", "gpt-5")
CLAUDE_MODEL = os.getenv("QDRANT_AGENT_CLAUDE_MODEL", "claude-sonnet-5")


def _session_id_for(base_dir: str) -> str:
    resolved = str(Path(base_dir).resolve())
    return "dir-" + hashlib.sha256(resolved.encode()).hexdigest()[:16]


def build_team(base_dir: str) -> Team:
    skills = Skills(loaders=[LocalSkills(path=str(SKILLS_DIR))])

    # coder writes the deliverable; critic can only read/run, never write/edit it
    coder_tools = [CodingTools(base_dir=base_dir, all=True), TavilyTools()]
    critic_tools = [
        CodingTools(
            base_dir=base_dir,
            enable_read_file=True,
            enable_edit_file=False,
            enable_write_file=False,
            enable_run_shell=True,
            enable_grep=True,
            enable_find=True,
            enable_ls=True,
        ),
        TavilyTools(),
    ]

    claude_agent = Agent(
        name="qdrant-claude",
        model=Claude(id=CLAUDE_MODEL),
        tools=coder_tools,
        skills=skills,
        instructions=CODER_INSTRUCTIONS,
    )
    openai_agent = Agent(
        name="qdrant-openai",
        model=OpenAIChat(id=OPENAI_MODEL),
        tools=critic_tools,
        skills=skills,
        instructions=CRITIC_INSTRUCTIONS,
    )

    return Team(
        members=[claude_agent, openai_agent],
        model=Claude(id=CLAUDE_MODEL),
        instructions=TEAM_INSTRUCTIONS,
        db=JsonDb(db_path=str(SESSIONS_DB_PATH)),
        session_id=_session_id_for(base_dir),
        add_history_to_context=True,
        num_history_runs=20,
    )
