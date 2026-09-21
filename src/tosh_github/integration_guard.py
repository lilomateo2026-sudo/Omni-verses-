"""Deterministic guardrails for TOSH/OMNI GitHub write plans.

This module performs no network calls. It is intentionally disabled for
production writes until an explicit higher-level activation step is supplied.
"""

from dataclasses import dataclass
from typing import Optional, Tuple


PRODUCTION_WRITES_ENABLED = False
ALLOWED_OPERATIONS = {"create", "update", "delete"}


@dataclass(frozen=True)
class WritePlan:
    repository: str
    branch: str
    operation: str
    path: str
    expected_blob_sha: Optional[str] = None
    temporary: bool = False
    cleanup_required: bool = False


def validate_write_plan(
    plan: WritePlan,
    *,
    exact_repository: str,
    default_branch: str,
) -> Tuple[str, ...]:
    errors = []

    if plan.repository != exact_repository:
        errors.append("repository_mismatch")

    if not plan.branch:
        errors.append("explicit_branch_required")
    elif plan.branch == default_branch:
        errors.append("default_branch_write_forbidden")

    if plan.operation not in ALLOWED_OPERATIONS:
        errors.append("unsupported_operation")

    if not plan.path or plan.path.startswith("/") or ".." in plan.path.split("/"):
        errors.append("unsafe_repository_path")

    if plan.operation in {"update", "delete"} and not plan.expected_blob_sha:
        errors.append("read_before_write_blob_sha_required")

    if plan.temporary and not plan.cleanup_required:
        errors.append("temporary_write_requires_cleanup")

    return tuple(errors)


def authorize_write(
    plan: WritePlan,
    *,
    exact_repository: str,
    default_branch: str,
    human_activated: bool = False,
) -> Tuple[bool, Tuple[str, ...]]:
    errors = list(
        validate_write_plan(
            plan,
            exact_repository=exact_repository,
            default_branch=default_branch,
        )
    )

    if not PRODUCTION_WRITES_ENABLED:
        errors.append("production_writes_disabled")

    if not human_activated:
        errors.append("human_activation_required")

    return not errors, tuple(errors)
