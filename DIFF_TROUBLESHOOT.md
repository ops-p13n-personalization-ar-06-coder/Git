# Patch Troubleshooting

## Error: "patch fragment without header"
Cause: A hunk (`@@ ... @@`) appears without a preceding `diff --git` + `---/+++` header.
Fix: Re-generate a single, contiguous diff via GitHub compare `.patch`.

## Error: "patch failed: context mismatch"
Cause: The diff lines don't match the base commit.
Fix: Ensure your compare is `<BASE_SHA>...<your-branch>` (not main…branch). Download new `.patch`.

## Error: "path not found"
Cause: Wrong file path or moved file.
Fix: Verify the exact relative path at the base commit page (Browse files).

## Windows line endings
Always download the `.patch` from GitHub compare; it avoids CRLF/EOL issues.
