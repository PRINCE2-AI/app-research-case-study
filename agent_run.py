#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent


def main():
    sdk_status = "installed"
    composio_version = "unknown"
    try:
        import composio
        from composio import Composio
        composio_version = getattr(composio, "__version__", "unknown")
    except Exception as exc:
        result = {
            "status": "sdk_unavailable",
            "error": type(exc).__name__,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        (ROOT / "agent_run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result))
        return

    api_key = os.getenv("COMPOSIO_API_KEY")
    if not api_key:
        result = {
            "status": "skipped_no_api_key",
            "sdk_status": sdk_status,
            "composio_version": composio_version,
            "live_tool_calls": 0,
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "reason": "No credentials were supplied, so no paid-account or live MCP test was fabricated.",
        }
        (ROOT / "agent_run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result))
        return

    try:
        client = Composio(api_key=api_key)
        result = {
            "status": "sdk_initialized",
            "sdk_status": sdk_status,
            "composio_version": composio_version,
            "live_tool_calls": 0,
            "session_api_available": hasattr(client, "sessions"),
            "tool_router_available": hasattr(client, "tool_router"),
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "note": "SDK initialized; live provider research requires explicit tool/session configuration.",
        }
    except Exception as exc:
        result = {
            "status": "sdk_initialization_failed",
            "sdk_status": sdk_status,
            "composio_version": composio_version,
            "live_tool_calls": 0,
            "error": type(exc).__name__,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    (ROOT / "agent_run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
