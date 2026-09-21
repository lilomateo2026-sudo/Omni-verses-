# TOSH/OMNI GitHub App Integration — O21

## Purpose

This specification defines the repository-facing trust boundary for TOSH/OMNI GitHub integration. Repository access is not considered verified merely because a repository can be listed. The integration advances only through explicit evidence gates.

## State machine

```text
O21.1 AUTHORIZATION
  -> O21.2 VISIBILITY + WRITABILITY PROBE
  -> O21.3 REPO-READY INTEGRATION PATCH
  -> O21.4 CI QUALIFICATION
  -> O21.5 CONTINUATION / PROMOTION
```

## O21.1 — Authorization

A repository is authorized when the connected GitHub App installation can enumerate the exact repository and expose its effective repository permissions.

Required evidence:

- exact repository full name
- visibility
- default branch
- effective pull/push permission state

## O21.2 — Non-destructive write probe

The writability probe MUST:

1. start from the exact current default-branch commit;
2. create a dedicated probe branch;
3. write one disposable UTF-8 probe file;
4. read the file back through the same connected GitHub surface;
5. verify exact content equality and record the returned blob SHA;
6. delete the temporary file;
7. prove the cleanup tree SHA equals the original base tree SHA;
8. leave the default branch untouched.

The canonical evidence packet is `evidence/GITHUB_APP_INTEGRATION_O21_2.json`.

A permission declaration such as `push=true` is necessary but not sufficient. O21.2 is PASS only after the full create/read/delete round trip succeeds.

## O21.3 — Repo-ready integration patch

The repository must preserve:

- this specification;
- the O21.2 evidence packet;
- a machine-readable evidence schema;
- deterministic tests that fail on missing probe evidence, failed cleanup, changed base tree, or absent push permission.

This stage does not merge itself into `main`. Promotion remains a separate human-controlled repository action.

## O21.4 — CI qualification

The existing repository CI must execute the deterministic evidence tests on the integration pull request. Passing local structure alone does not qualify the patch.

## O21.5 — Continuation

After CI passes, continuation work may build higher-level GitHub automation only behind these invariants:

- least authority;
- exact repository identity;
- explicit target branch;
- read-before-update for existing files;
- no silent default-branch mutation;
- commit/blob provenance retained for every write;
- rollback or compensating cleanup recorded when a probe is temporary.

## Current evidence

O21.2 passed on the isolated branch `integration/github-o21-verification`.

- base commit: `b79c6c8fc2f7f9572e5f46dc1844f350c680922b`
- write commit: `07206bc73f5df7a1900643c6e3f5f8e5429cb58f`
- probe blob: `5a91ca6f336159fe1e04fa4a239cca2c2210714b`
- cleanup commit: `7c8c71f6d78baefe96db451fd2a7ef08b6b1912e`
- base/cleanup tree: `d6188708618091b8b785ab9e931f8ec5574278fd`

The equal base and cleanup tree SHAs establish that the temporary probe left no net repository-tree change.
