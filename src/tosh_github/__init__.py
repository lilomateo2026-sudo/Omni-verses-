"""TOSH/OMNI GitHub integration guard package."""

from .integration_guard import (
    PRODUCTION_WRITES_ENABLED,
    WritePlan,
    authorize_write,
    validate_write_plan,
)

__all__ = [
    "PRODUCTION_WRITES_ENABLED",
    "WritePlan",
    "authorize_write",
    "validate_write_plan",
]
