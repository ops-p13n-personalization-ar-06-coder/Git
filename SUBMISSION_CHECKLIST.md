# Submission Checklist (Tick All)

- [ ] File name is exactly **solution.patch**
- [ ] Only changes the intended library/source files (no tests, no Dockerfile, no CI)
- [ ] Generated against the **exact base SHA**
- [ ] `git apply --check` and reverse check pass (or patch was downloaded from GitHub compare `.patch`)
- [ ] Implements all Solution Criteria, preserves backward compatibility
- [ ] Diff is minimal, clean, and follows project style
- [ ] Shipd form:
  - “No Dockerfile/test changes” → **Yes**
  - “Patch generated correctly; apply + reverse-apply works” → **Yes**
  - “Solution fully addresses requirements & passes tests” → **Yes**
