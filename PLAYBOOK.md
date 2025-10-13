# Shipd Solver Playbook (Zero-Setup, Windows-Friendly)

## Goal
Ship a single `solution.patch` against a pinned base commit. No tests or Dockerfile changes in the patch.

## Workflow (Browser-First)
1) Open the problem page → note repo URL + **base commit SHA**.
2) **Fork** the repo on GitHub.
3) Open the base commit page (the exact SHA) → click **Browse files**.
4) Navigate to the file(s) you need → click the **pencil** → edit in browser.
5) Commit to a new branch on your fork.
6) Open the **compare** URL:  
   `https://github.com/<you>/<repo>/compare/<BASE_SHA>...<your-branch>`
7) Append **`.patch`** to the compare URL → save the page as **`solution.patch`** (UTF-8).
8) Upload **`solution.patch`** to Shipd. Mark all checks “Yes”.

## Core Rules
- Patch must only touch library/source files required to solve the issue.
- Never include tests, Dockerfile, CI, or `test.sh` in `solution.patch`.
- Patch must apply cleanly to the exact base commit.

## If “patch failed to apply”
- Re-generate from GitHub compare using the base SHA (step 6–7).
- Ensure paths match exactly and there are no empty hunks (like `@@ -0,0 +1,0 @@`).

## Quality Bar (for yourself)
- Backward compatible unless the problem says otherwise.
- Deterministic behavior that matches problem criteria.
- Minimal, focused diff; follow the project style.
