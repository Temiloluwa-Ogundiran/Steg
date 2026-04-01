# Steg Webapp Optimization Design

**Date:** 2026-04-01

## Goal

Optimize the Steg web application for lower CPU, RAM, and disk usage without changing the visible product flow. The optimized app should keep the same encode, decode, check, and download user journeys while handling large images more efficiently.

## Approved Product Decisions

- Oversized images should be automatically resized before encode, decode, or check.
- The max image dimension should be `2048px` on the longest side.
- Temporary uploads should be deleted immediately after processing.
- Generated outputs should remain downloadable for a short retention window, then expire automatically.

## Recommended Optimization Approach

Use a balanced optimization pass focused on the webapp boundary:

- stream uploads instead of buffering full files in request handlers
- normalize and resize oversized images before model processing
- remove temp uploads immediately after use
- delete expired generated outputs on a lightweight cleanup pass

This keeps the existing UI and API contract intact while reducing per-request RAM pressure, reducing CPU load on oversized images, and bounding disk growth in `webapp/runtime`.

## Behavioral Design

### Upload Handling

The current routes read uploaded files fully into memory before passing them into the service layer. That should be replaced with streamed persistence into the managed upload directory.

The service layer should:

- persist the raw upload to disk in chunks
- validate that it is a readable image
- normalize it into an RGB image
- resize it only if the longest side exceeds `2048px`
- save the normalized image back to the managed upload path

The user should not need to make any new choices in the UI.

### Resize Policy

Resize only when necessary:

- if longest side is `<= 2048`, keep the current dimensions
- if longest side is `> 2048`, scale down proportionally so the longest side becomes `2048`

This preserves aspect ratio and keeps behavior predictable.

### Temp File Lifecycle

Temporary uploads should be removed in all cases:

- after successful encode
- after successful decode
- after successful check
- after validation or processing errors

This cleanup should happen in a `finally` path so temp files do not accumulate after failures.

### Generated Output Retention

Encoded outputs should remain available for download after creation, but not indefinitely.

The webapp should:

- keep generated outputs in the managed output directory
- define a retention window in config
- remove expired output files based on last-modified or creation time
- run cleanup before creating or serving outputs

This allows normal user downloads while limiting long-term disk growth.

## Technical Scope

This optimization should stay inside the webapp layer:

- `webapp/main.py`
- `webapp/services.py`
- `webapp/config.py`
- `tests/webapp/*`

The core `steganogan` model code should remain functionally unchanged.

## Testing Strategy

The optimization should be verified through webapp-focused tests:

- oversized images are resized down to `2048px`
- smaller images are left unchanged
- temp uploads are removed after processing
- expired outputs are cleaned up while fresh outputs remain
- API routes still return the same response structure
- encode/decode/check still work end-to-end through the webapp

## Verification Expectations

Final verification should include:

- `python -m pytest tests/webapp -v`
- a browser-based encode/decode/check run
- an oversized image path verification

## Constraints

- This workspace is not a Git repository, so design-plan commits are blocked.
- The optimization should preserve the current dense-only webapp behavior.

