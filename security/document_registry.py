import json
import os


REGISTRY_PATH = "data/document_registry.json"


def load_registry():
    """Load trusted document records."""

    if not os.path.exists(REGISTRY_PATH):
        return {}

    with open(REGISTRY_PATH, "r") as file:
        return json.load(file)


def save_registry(registry):
    """Persist document registry."""

    os.makedirs(
        os.path.dirname(REGISTRY_PATH),
        exist_ok=True,
    )

    with open(REGISTRY_PATH, "w") as file:
        json.dump(registry, file, indent=4)


def check_document_version(
    document_id: str,
    document_hash: str,
):
    """
    Compare an incoming document against the trusted registry.

    Returns:
        status:
            NEW
            SAME
            CHANGED

        version:
            current/new proposed version
    """

    registry = load_registry()

    existing = registry.get(document_id)

    # First time seeing this document
    if existing is None:
        return {
            "status": "NEW",
            "version": 1,
            "previous_hash": None,
        }

    previous_hash = existing["document_hash"]
    previous_version = existing["version"]

    # Exact same document
    if previous_hash == document_hash:
        return {
            "status": "SAME",
            "version": previous_version,
            "previous_hash": previous_hash,
        }

    # Same document ID, but contents changed
    return {
        "status": "CHANGED",
        "version": previous_version + 1,
        "previous_hash": previous_hash,
    }


def register_trusted_document(
    document_id: str,
    document_hash: str,
    version: int,
    owner_id: str,
):
    """Register an approved/trusted document version."""

    registry = load_registry()

    registry[document_id] = {
        "document_hash": document_hash,
        "version": version,
        "owner_id": owner_id,
        "status": "approved",
    }

    save_registry(registry)