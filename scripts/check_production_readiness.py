"""SupplyMind production-readiness checks."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path


# ---------------------------------------------------------
# Ensure repository root is importable when this file is run
# as:
#
#   python scripts/check_production_readiness.py
# ---------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from supplymind.shared.config.settings import get_settings


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def configured(value: object | None) -> bool:
    """Return True when a configuration value is present."""

    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    return True


# ---------------------------------------------------------
# Main readiness check
# ---------------------------------------------------------

def main() -> None:
    print("SupplyMind production readiness check")
    print()

    settings = get_settings()

    # -----------------------------------------------------
    # Runtime configuration
    # -----------------------------------------------------

    checks = {
        "OPENAI_API_KEY": getattr(
            settings,
            "openai_api_key",
            None,
        ),
        "LLM_MODEL": getattr(
            settings,
            "llm_model",
            None,
        ),
        "PINECONE_API_KEY": getattr(
            settings,
            "pinecone_api_key",
            None,
        ),
        "PINECONE_INDEX_HOST": getattr(
            settings,
            "pinecone_index_host",
            None,
        ),
    }

    missing = [
        name
        for name, value in checks.items()
        if not configured(value)
    ]

    if missing:
        print("Missing configuration:")

        for name in missing:
            print(f" - {name}")
    else:
        print("Required runtime configuration: OK")

    # -----------------------------------------------------
    # Database configuration
    # -----------------------------------------------------

    database_url = getattr(
        settings,
        "database_url",
        None,
    )

    print(
        "Database configuration:",
        "OK"
        if configured(database_url)
        else "MISSING",
    )

    # -----------------------------------------------------
    # Champion model artifacts
    # -----------------------------------------------------

    champion_model = (
        REPO_ROOT
        / "models"
        / "champion"
        / "model.joblib"
    )

    champion_metadata = (
        REPO_ROOT
        / "models"
        / "champion"
        / "metadata.json"
    )

    print(
        "Champion model:",
        "OK"
        if champion_model.exists()
        else "MISSING",
    )

    print(
        "Champion metadata:",
        "OK"
        if champion_metadata.exists()
        else "MISSING",
    )

    # -----------------------------------------------------
    # FastAPI import
    # -----------------------------------------------------

    try:
        importlib.import_module(
            "apps.api.main"
        )

        print("FastAPI import: OK")

    except Exception as exc:
        print("FastAPI import: FAILED")
        print(
            f"  {type(exc).__name__}: {exc}"
        )

        raise

    # -----------------------------------------------------
    # Final instructions
    # -----------------------------------------------------

    print()
    print("Local checks still required:")
    print("  pytest -q")
    print(
        "  cd apps/web && "
        "npm run build"
    )


if __name__ == "__main__":
    main()