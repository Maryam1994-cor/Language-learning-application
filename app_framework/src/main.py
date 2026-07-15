"""Entry point for the Language Learning Application."""

from __future__ import annotations

import json
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from application_name.presentation_layer.user_interface import UserInterface


def load_environment_file() -> None:
    """Load environment variables from the project-level .env file."""
    project_root = Path(__file__).resolve().parents[2]
    environment_file = project_root / ".env"

    if not environment_file.exists():
        raise FileNotFoundError(
            f"Environment file not found: {environment_file}. "
            "Copy .env.example to .env and configure the database values."
        )

    load_dotenv(dotenv_path=environment_file, override=False)


def load_config(config_path: str) -> dict[str, Any]:
    """Load and return application configuration from a JSON file."""
    path = Path(config_path).expanduser().resolve()

    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Configuration path is not a file: {path}")

    with path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    if "meta" not in config or "database" not in config:
        raise ValueError(
            "Configuration file must contain 'meta' and 'database' sections."
        )

    return config


def configure_and_parse_commandline_arguments() -> Namespace:
    """Configure and parse command-line arguments."""
    parser = ArgumentParser(
        prog="main.py",
        description="Start the Language Learning Application.",
        epilog="Use --configfile to provide the application JSON configuration.",
    )

    parser.add_argument(
        "-c",
        "--configfile",
        required=True,
        help="Path to the application JSON configuration file.",
    )

    return parser.parse_args()


def main() -> None:
    """Load configuration and start the application."""
    try:
        load_environment_file()

        arguments = configure_and_parse_commandline_arguments()
        config = load_config(arguments.configfile)

        user_interface = UserInterface(config)
        user_interface.start()

    except FileNotFoundError as error:
        print(f"File error: {error}")

    except json.JSONDecodeError as error:
        print(f"Invalid JSON configuration: {error}")

    except ValueError as error:
        print(f"Configuration error: {error}")

    except KeyboardInterrupt:
        print("\nApplication stopped by user.")

    except Exception as error:
        print(f"Application error: {error}")


if __name__ == "__main__":
    main()