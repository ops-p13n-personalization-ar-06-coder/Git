#!/usr/bin/env python3
import os, sys, re
from pathlib import Path

def die(msg, code=1):
    print(f"[ERROR] {msg}")
    sys.exit(code)

patch_path = Path(sys.argv[1] if len(sys.argv) > 1 else "/app/artifacts/solution.patch")
if not patch_path.exists() or patch_path.stat().st_size == 0:
    die(f"missing or empty patch: {patch_path}")

raw = patch_path.read_bytes()
if b"\r" in raw:
    die("CRLF line endings found; use LF only")
try:
    txt = raw.decode("ascii", "strict")
except UnicodeDecodeError:
    die("non-ASCII bytes found in patch")

allowed_env = os.environ.get("TARGET_FILES_CSV", "").strip()
if not allowed_env:
    die("TARGET_FILES_CSV not set in env")
allowed = [p.strip() for p in allowed_env.split(",") if p.strip()]

paths = []
for line in txt.splitlines():
    if line.startswith("diff --git "):
        parts = line.split()
        if len(parts) >= 4:
            b = parts[3]
            if b.startswith("b/"):
                b = b[2:]
            paths.append(b)

if not paths:
    die("no changed files detected in patch")

deny = [
    r"(^|/)(tests?|mars_new|mars_base_ok)/",
    r"(^|/)test\.sh$",
    r"(^|/)Dockerfile$",
    r"(^|/)pyproject\.toml$",
    r"(^|/)setup\.(py|cfg)$",
    r"(^|/)__init__\.py$",
]
for p in paths:
    for pat in deny:
        if re.search(pat, p):
            die(f"forbidden path in patch: {p}")

bad = [p for p in paths if p not in allowed]
if bad:
    die("disallowed file(s) in patch: " + ", ".join(bad))

print("OK files:", ", ".join(paths))
print("OK allowed:", ", ".join(allowed))
print("OK patch format and paths")
