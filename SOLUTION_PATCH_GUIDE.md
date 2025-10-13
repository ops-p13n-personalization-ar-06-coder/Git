# Solution Patch Guide (No Local Build Needed)

## Make the change in GitHub
1) Fork the repo.
2) Open the base commit: `https://github.com/<owner>/<repo>/commit/<BASE_SHA>`
3) Click **Browse files**.
4) Edit the target file(s) via the web editor.
5) Commit to a new branch on your fork.

## Generate a guaranteed-clean patch
1) Compare base → branch:
   `https://github.com/<you>/<repo>/compare/<BASE_SHA>...<your-branch>`
2) Append **`.patch`** to the URL.
3) Save the page content as **`solution.patch`** (UTF-8).

> This `.patch` is aligned to the pinned commit and only includes your changes.

## Optional: quick validation (Git Bash on Windows)
```bash
git clone https://github.com/<owner>/<repo>
cd <repo>
git checkout <BASE_SHA>
git apply --check /path/to/solution.patch
git apply /path/to/solution.patch
git apply -R --check /path/to/solution.patch
```
All three should be silent (no errors).
