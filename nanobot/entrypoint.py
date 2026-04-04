#!/usr/bin/env python3
"""
Nanobot Docker entrypoint.

Resolves environment variables into the config at runtime,
then launches nanobot gateway.
"""

import json
import os
from pathlib import Path


def main():
    """Main entrypoint function."""
    # Paths
    base_dir = Path("/app/nanobot")
    config_path = base_dir / "config.json"
    # Write resolved config to /tmp to avoid permission issues with mounted volumes
    resolved_config_path = Path("/tmp/nanobot.config.resolved.json")
    workspace_path = base_dir / "workspace"

    # Create writable directories in /tmp for cron and memory to avoid permission issues
    cron_dir = Path("/tmp/nanobot/cron")
    cron_dir.mkdir(parents=True, exist_ok=True)
    memory_dir = Path("/tmp/nanobot/memory")
    memory_dir.mkdir(parents=True, exist_ok=True)

    # Read the base config
    with open(config_path, "r") as f:
        config = json.load(f)

    # Set environment variable for cron store path before nanobot initializes
    os.environ["NANOBOT_CRON_STORE_PATH"] = str(cron_dir / "jobs.json")

    # Inject environment variables
    # LLM provider settings
    if "LLM_API_KEY" in os.environ:
        config["providers"]["custom"]["apiKey"] = os.environ["LLM_API_KEY"]
    if "LLM_API_BASE_URL" in os.environ:
        config["providers"]["custom"]["apiBase"] = os.environ["LLM_API_BASE_URL"]
    if "LLM_API_MODEL" in os.environ:
        config["agents"]["defaults"]["model"] = os.environ["LLM_API_MODEL"]

    # Gateway settings
    if "NANOBOT_GATEWAY_CONTAINER_ADDRESS" in os.environ:
        config["gateway"]["host"] = os.environ["NANOBOT_GATEWAY_CONTAINER_ADDRESS"]
    if "NANOBOT_GATEWAY_CONTAINER_PORT" in os.environ:
        config["gateway"]["port"] = int(os.environ["NANOBOT_GATEWAY_CONTAINER_PORT"])

    # Webchat channel settings
    if "channels" not in config:
        config["channels"] = {}
    if "webchat" not in config["channels"]:
        config["channels"]["webchat"] = {"enabled": True, "allowFrom": ["*"]}

    if "NANOBOT_WEBCHAT_CONTAINER_ADDRESS" in os.environ:
        config["channels"]["webchat"]["host"] = os.environ[
            "NANOBOT_WEBCHAT_CONTAINER_ADDRESS"
        ]
    if "NANOBOT_WEBCHAT_CONTAINER_PORT" in os.environ:
        config["channels"]["webchat"]["port"] = int(
            os.environ["NANOBOT_WEBCHAT_CONTAINER_PORT"]
        )

    # MCP server environment variables for LMS
    if "tools" not in config:
        config["tools"] = {}
    if "mcpServers" not in config["tools"]:
        config["tools"]["mcpServers"] = {}
    if "lms" not in config["tools"]["mcpServers"]:
        config["tools"]["mcpServers"]["lms"] = {
            "command": "python",
            "args": ["-m", "mcp_lms"],
        }

    # Ensure env section exists for LMS MCP server
    if "env" not in config["tools"]["mcpServers"]["lms"]:
        config["tools"]["mcpServers"]["lms"]["env"] = {}

    if "NANOBOT_LMS_BACKEND_URL" in os.environ:
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = (
            os.environ["NANOBOT_LMS_BACKEND_URL"]
        )
    if "NANOBOT_LMS_API_KEY" in os.environ:
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = os.environ[
            "NANOBOT_LMS_API_KEY"
        ]

    # Add webchat MCP server for structured UI
    if "webchat" not in config["tools"]["mcpServers"]:
        config["tools"]["mcpServers"]["webchat"] = {
            "command": "python",
            "args": ["-m", "mcp_webchat"],
            "env": {},
        }

    # Ensure env section exists for webchat MCP server
    if "env" not in config["tools"]["mcpServers"]["webchat"]:
        config["tools"]["mcpServers"]["webchat"]["env"] = {}

    if "NANOBOT_WEBCHAT_UI_RELAY_URL" in os.environ:
        config["tools"]["mcpServers"]["webchat"]["env"][
            "NANOBOT_WEBCHAT_UI_RELAY_URL"
        ] = os.environ["NANOBOT_WEBCHAT_UI_RELAY_URL"]
    if "NANOBOT_WEBCHAT_UI_RELAY_TOKEN" in os.environ:
        config["tools"]["mcpServers"]["webchat"]["env"][
            "NANOBOT_WEBCHAT_UI_RELAY_TOKEN"
        ] = os.environ["NANOBOT_WEBCHAT_UI_RELAY_TOKEN"]

    # Add observability MCP server
    if "obs" not in config["tools"]["mcpServers"]:
        config["tools"]["mcpServers"]["obs"] = {
            "command": "python",
            "args": ["-m", "mcp_obs"],
            "env": {},
        }

    # Ensure env section exists for obs MCP server
    if "env" not in config["tools"]["mcpServers"]["obs"]:
        config["tools"]["mcpServers"]["obs"]["env"] = {}

    if "NANOBOT_VICTORIALOGS_URL" in os.environ:
        config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIALOGS_URL"] = (
            os.environ["NANOBOT_VICTORIALOGS_URL"]
        )
    if "NANOBOT_VICTORIATRACES_URL" in os.environ:
        config["tools"]["mcpServers"]["obs"]["env"]["NANOBOT_VICTORIATRACES_URL"] = (
            os.environ["NANOBOT_VICTORIATRACES_URL"]
        )

    # Write the resolved config
    with open(resolved_config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Using config: {resolved_config_path}")

    # Launch nanobot gateway
    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--config",
            str(resolved_config_path),
            "--workspace",
            str(workspace_path),
        ],
    )


if __name__ == "__main__":
    main()
