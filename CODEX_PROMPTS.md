# Codex Prompts (Copy/Paste)

## 1) Generate a single-file patch
Return **only** a file named `solution.patch` (no explanations).
It is a unified diff that modifies **only**:
`<relative/path/to/source_file>`
Implement: <very short feature spec>.
Do not include tests or Dockerfile. Keep existing behaviors unchanged.

## 2) Clean a messy patch
Return **only** a file named `solution.patch` (no explanations).
Unify to a single `diff --git` header for each file.
Remove empty hunks like `@@ -0,0 +1,0 @@`.
Restrict changes to `<relative/path/to/source_file>`.
Ensure paths/line numbers match base commit `<BASE_SHA>`.

## 3) Behavior confirmation (short note)
Confirm the code orders categories by decreasing frequency with lexicographic tie-break.
If `categories` is an explicit list, bypass frequency ordering.
If `categories="auto"`, preserve original lexicographic behavior.
