# Notes: OrdinalEncoder `categories="frequency"`

## Expected behavior
- When `categories="frequency"`: order categories by **descending frequency** with **lexicographic tie-break**.
- Trailing `NaN` (if present) remains last.
- When `categories="auto"`: original lexicographic ordering.
- When `categories` is an explicit list: never re-order.

## Safe implementation pattern
- Add `"frequency"` to `_parameter_constraints` for `OrdinalEncoder`.
- Implement ordering inside `_BaseEncoder._fit` so infrequent/missing logic still works.
- Use `_unique(..., return_counts=True)` → `np.lexsort((values, -counts))`.
- Split NaN vs non-NaN only to append NaN last.

## Self-check
- New behavior only triggers for `"frequency"`.
- No change for `"auto"` or explicit lists.
- No tests/Dockerfile in `solution.patch`.
