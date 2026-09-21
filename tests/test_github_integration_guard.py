import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from tosh_github.integration_guard import WritePlan, authorize_write, validate_write_plan  # noqa: E402


REPOSITORY = "lilomateo2026-sudo/Omni-verses-"


def test_isolated_create_plan_is_structurally_valid():
    plan = WritePlan(
        repository=REPOSITORY,
        branch="integration/example",
        operation="create",
        path="evidence/example.txt",
    )
    assert validate_write_plan(
        plan,
        exact_repository=REPOSITORY,
        default_branch="main",
    ) == ()


def test_default_branch_write_is_rejected():
    plan = WritePlan(
        repository=REPOSITORY,
        branch="main",
        operation="create",
        path="README.md",
    )
    errors = validate_write_plan(
        plan,
        exact_repository=REPOSITORY,
        default_branch="main",
    )
    assert "default_branch_write_forbidden" in errors


def test_update_requires_read_before_write_blob_sha():
    plan = WritePlan(
        repository=REPOSITORY,
        branch="integration/example",
        operation="update",
        path="README.md",
    )
    errors = validate_write_plan(
        plan,
        exact_repository=REPOSITORY,
        default_branch="main",
    )
    assert "read_before_write_blob_sha_required" in errors


def test_temporary_write_requires_cleanup():
    plan = WritePlan(
        repository=REPOSITORY,
        branch="integration/example",
        operation="create",
        path="evidence/probe.txt",
        temporary=True,
        cleanup_required=False,
    )
    errors = validate_write_plan(
        plan,
        exact_repository=REPOSITORY,
        default_branch="main",
    )
    assert "temporary_write_requires_cleanup" in errors


def test_runtime_authorization_remains_disabled_by_default():
    plan = WritePlan(
        repository=REPOSITORY,
        branch="integration/example",
        operation="create",
        path="evidence/example.txt",
    )
    allowed, errors = authorize_write(
        plan,
        exact_repository=REPOSITORY,
        default_branch="main",
        human_activated=True,
    )
    assert allowed is False
    assert "production_writes_disabled" in errors
