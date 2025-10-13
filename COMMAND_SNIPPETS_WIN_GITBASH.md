# Windows / Git Bash Quick Commands

# Validate patch (no build required)
git clone https://github.com/<owner>/<repo>
cd <repo>
git checkout <BASE_SHA>
git apply --check /path/to/solution.patch
git apply /path/to/solution.patch
git apply -R --check /path/to/solution.patch

# Undo applied patch (if needed)
git reset --hard
