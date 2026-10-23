# shared/registries/tools/data_steward_tool_registry.py
#
# The missing piece that ties the other 3 modules together for Data-Steward:
#
#   agent.json (ExtendedAgentCard)
#       │  x-artifacts: skill/task/tool/handler/messageType per capability
#       │  (all 5 existing tool artifacts use path="/" → internal, skipped)
#       ▼
#   NEW_TOOL_ARTIFACTS  ──patched in──▶  extended_card["x-artifacts"]
#       (Paubox, RingCentral — real external providers, real paths)
#       ▼
#   bootstrap_tools.build_tool_registry(extended_card)  →  ToolRegistry
#       ▼
#   ToolInvocationManager(registry)  →  audited, dry-run-aware invoke()
#
# Why Paubox/RingCentral actually get loaded where the other 5 don't:
#   bootstrap_tools._load_one_tool() skips any artifact with path == "/" or "".
#   The 5 built-in tool artifacts (Phone.Call, Phone.Answer, Data-Request.Govern,
#   Email.Read, Email.Send) are all internal capability dispatches — path="/" —
#   so they never reach the adapter-resolution step.
#   Paubox and RingCentral are real external HTTP providers, so they're given
#   real paths (/paubox_email.py, /ringcentral_voice.py) and real provider
#   config. Neither "Paubox" nor "RingCentral" is in bootstrap_tools'
#   _ADAPTER_CLASS_REGISTRY, so both fall through to the safe default,
#   HttpToolAdapter — which is correct, since both are REST/HTTP APIs.
#
# Drop this file at: /shared/registries/tools/data_steward_tool_registry.py

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Optional

from tools.bootstrap_tools import build_tool_registry
from tools.tool_invocation_manager import ToolInvocationManager
from tools.tool_registry import ToolRegistry
from core.observability.logging.platform_logger import get_platform_logger

LOG = get_platform_logger("data_steward_tool_registry")

# ── Location of the Data-Steward ExtendedAgentCard ─────────────────────────
# Adjust if the card lives elsewhere in your deployment.
DEFAULT_CARD_PATH = Path(__file__).resolve().parent / "agent.json"


# ── New external tool artifacts ─────────────────────────────────────────────
# Real providers, real paths (never "/") so bootstrap_tools treats them as
# external adapters rather than internal capability dispatches.

PAUBOX_TOOL_ARTIFACT = {
    "name": "Paubox",
    "version": "1.0.0",
    "artifactType": "tool",
    "description": "Send and receive HIPAA-compliant encrypted email via Paubox, backing the Email.Send / Email.Read skills.",
    "capabilities": ["send", "read"],
    "path": "/paubox_email.py",
    "provider": {
        "name": "Paubox",
        "brand": "Paubox",
        "product": "Email API",
        "version": "1.0.0",
        "license": "Commercial",
        "url": "https://www.paubox.com/docs/api",
        "config": {
            "baseUrl": "https://api.paubox.net/v1",
            "apiKeyEnv": "PAUBOX_API_KEY",
        },
    },
    "inputSchema": {"$ref": "#/schemas/Paubox.Input"},
    "outputSchema": {"$ref": "#/schemas/Paubox.Output"},
    "auth": "apiKey",
}

RINGCENTRAL_TOOL_ARTIFACT = {
    "name": "RingCentral",
    "version": "1.0.0",
    "artifactType": "tool",
    "description": "Place and receive voice calls via the RingCentral Voice API, backing the Phone.Call / Phone.Answer skills.",
    "capabilities": ["call", "answer"],
    "path": "/ringcentral_voice.py",
    "provider": {
        "name": "RingCentral",
        "brand": "RingCentral",
        "product": "Voice API",
        "version": "1.0.0",
        "license": "Commercial",
        "url": "https://developers.ringcentral.com/api-reference/Call-Control",
        "config": {
            "baseUrl": "https://platform.ringcentral.com/restapi/v1.0",
            "clientIdEnv": "RINGCENTRAL_CLIENT_ID",
            "clientSecretEnv": "RINGCENTRAL_CLIENT_SECRET",
        },
    },
    "inputSchema": {"$ref": "#/schemas/RingCentral.Input"},
    "outputSchema": {"$ref": "#/schemas/RingCentral.Output"},
    "auth": "oauth2",
}

NEW_TOOL_ARTIFACTS = [PAUBOX_TOOL_ARTIFACT, RINGCENTRAL_TOOL_ARTIFACT]


# ── Card loading / patching ─────────────────────────────────────────────────

def load_extended_card(card_path: Path | str = DEFAULT_CARD_PATH) -> dict:
    with open(card_path, "r") as f:
        return json.load(f)


def with_new_tools(extended_card: dict) -> dict:
    # ── Returns a copy of extended_card with Paubox + RingCentral injected ──
    # Idempotent: re-running this does not create duplicate artifacts.
    patched = copy.deepcopy(extended_card)
    artifacts = patched.setdefault("x-artifacts", [])

    existing_names = {
        a.get("name")
        for a in artifacts
        if isinstance(a, dict) and a.get("artifactType") == "tool"
    }

    for tool_artifact in NEW_TOOL_ARTIFACTS:
        if tool_artifact["name"] in existing_names:
            LOG.write(
                event_type="data_steward_tool_registry.AlreadyPresent",
                payload={"tool_name": tool_artifact["name"]},
                context=None,
            )
            continue
        artifacts.append(copy.deepcopy(tool_artifact))
        LOG.write(
            event_type="data_steward_tool_registry.ToolArtifactAdded",
            payload={"tool_name": tool_artifact["name"]},
            context=None,
        )

    return patched


# ── Public API ───────────────────────────────────────────────────────────────

def build_data_steward_registry(
    card_path: Path | str = DEFAULT_CARD_PATH,
) -> ToolRegistry:
    # ── Resurrects the Data-Steward's ToolRegistry with Paubox + RingCentral ─
    extended_card = load_extended_card(card_path)
    patched_card = with_new_tools(extended_card)
    registry = build_tool_registry(patched_card)

    LOG.write(
        event_type="data_steward_tool_registry.Built",
        payload={"tools": registry.list_tools()},
        context=None,
    )
    return registry


def build_data_steward_tool_manager(
    card_path: Path | str = DEFAULT_CARD_PATH,
) -> ToolInvocationManager:
    return ToolInvocationManager(build_data_steward_registry(card_path))


# ── Module-level singletons ─────────────────────────────────────────────────
# Lazily built on first access so importing this module has no side effects
# (and so tests can call build_data_steward_registry() directly with a
# custom card_path instead of relying on the singleton).

_registry: Optional[ToolRegistry] = None
_tool_manager: Optional[ToolInvocationManager] = None


def get_registry() -> ToolRegistry:
    global _registry
    if _registry is None:
        _registry = build_data_steward_registry()
    return _registry


def get_tool_manager() -> ToolInvocationManager:
    global _tool_manager
    if _tool_manager is None:
        _tool_manager = ToolInvocationManager(get_registry())
    return _tool_manager


# ── Standalone CLI ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    card_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CARD_PATH
    registry = build_data_steward_registry(card_path)
    tools = registry.list_tools()

    if tools:
        print(f"Data-Steward tools loaded ({len(tools)}):")
        for name in tools:
            print(f"  - {name}")
    else:
        print("No tools loaded.")
