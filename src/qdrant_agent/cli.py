import argparse

from dotenv import load_dotenv

from qdrant_agent.agent import build_team


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Qdrant coding agent")
    parser.add_argument("dir", nargs="?", default=".", help="Working directory for the agent")
    args = parser.parse_args()

    team = build_team(args.dir)
    team.cli_app(markdown=True)


if __name__ == "__main__":
    main()
