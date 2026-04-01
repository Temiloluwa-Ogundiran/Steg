# Steg Webapp Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Optimize the Steg web application so uploads use less memory, oversized images are resized to a max `2048px` longest side, temp uploads are cleaned up immediately, and generated outputs expire automatically after a short retention window.

**Architecture:** Keep the optimization inside the FastAPI webapp layer. Add config values for upload normalization and output retention, move request handling toward streamed file persistence, and centralize normalization, cleanup, and retention logic in the webapp service layer so the UI and API contract stay stable.

**Tech Stack:** FastAPI, Starlette uploads, Pillow, pytest, existing `steganogan` integration.

---

### Task 1: Add Optimization Config and Retention Defaults

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\config.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Add service-focused tests that expect configuration-backed behavior for:

- max image dimension set to `2048`
- output retention window value exists and is used by cleanup logic entry points

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because retention and resize settings are not fully represented in the service contract yet.

**Step 3: Write minimal implementation**

- add `MAX_IMAGE_DIMENSION = 2048`
- add `OUTPUT_RETENTION_SECONDS` with a short-window default
- keep existing runtime directory constants intact

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add webapp optimization config`

### Task 2: Normalize and Resize Uploaded Images in the Service Layer

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\services.py`
- Modify: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Add tests for:

- an oversized image being resized so the longest side becomes `2048`
- a smaller image remaining unchanged
- normalized saved upload remaining readable by downstream processing

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because uploads are currently only validated and written, not normalized and resized.

**Step 3: Write minimal implementation**

- add helper(s) to open the upload with Pillow
- convert to RGB
- resize proportionally when needed
- save normalized output back to the upload path

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: normalize and resize web uploads`

### Task 3: Add Immediate Temp Upload Cleanup

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\services.py`
- Modify: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Add tests verifying upload temp files are removed:

- after successful encode
- after successful decode
- after successful check
- after processing failure

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because temp uploads currently remain on disk after processing.

**Step 3: Write minimal implementation**

- wrap processing paths in `try/finally`
- delete upload temp files when they exist
- keep generated outputs intact for encode success

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: clean up temp uploads after processing`

### Task 4: Add Output Expiration Cleanup

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\services.py`
- Modify: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Add tests that verify:

- expired output files are deleted
- fresh output files are preserved
- cleanup runs before output lookup and before generating new encoded outputs

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because output expiry cleanup is not implemented yet.

**Step 3: Write minimal implementation**

- add an output cleanup helper
- compare file age against `OUTPUT_RETENTION_SECONDS`
- invoke cleanup before serving outputs and before encode output creation

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: expire stale generated outputs`

### Task 5: Reduce Request-Side Memory Pressure

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\main.py`
- Modify: `C:\Users\USER\Documents\Steganography\tests\webapp\test_api.py`

**Step 1: Write the failing test**

Add route tests that still verify the same response shapes and status codes after request-handling changes.

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_api.py -v`

Expected: FAIL once the route-side assumptions are updated for the new upload path handling.

**Step 3: Write minimal implementation**

- reduce direct buffering in request handlers where practical
- preserve existing route signatures and response contracts
- keep dense-only behavior intact

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_api.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `refactor: reduce webapp upload memory pressure`

### Task 6: Re-verify the Full Webapp Surface

**Files:**
- Modify only if verification reveals issues.

**Step 1: Run the full webapp test suite**

Run: `python -m pytest tests/webapp -v`

Expected: PASS

**Step 2: Start the local app**

Run: `python -m uvicorn webapp.main:app --host 127.0.0.1 --port 8000`

Expected: app starts successfully.

**Step 3: Perform browser verification**

Use Playwright to verify:

- normal encode still generates a downloadable file
- decode still recovers the expected message
- check still returns correct positive and negative states
- oversized image path succeeds after resize

**Step 4: Record residual risks**

Document any remaining caveats, such as route-side upload buffering that could not be removed cleanly without a larger refactor.

**Step 5: Commit**

Commit message: `chore: verify webapp optimization pass`

