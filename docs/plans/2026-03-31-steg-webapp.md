# Steg Webapp Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a FastAPI web application called Steg that lets users encode, download, decode, and strictly check images for hidden data using the existing SteganoGAN codebase.

**Architecture:** Add a new `webapp` package that contains the FastAPI app, a service layer for invoking SteganoGAN safely, server-rendered templates, static assets, and route tests. Keep the steganography logic in the existing `steganogan` package and build a focused UI with poster-modernist styling and lightweight JavaScript interactions.

**Tech Stack:** FastAPI, Jinja2 templates, Starlette static files, pytest, existing `steganogan` package, Playwright for final browser verification.

---

### Task 1: Add Web Dependencies and App Skeleton

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\setup.py`
- Create: `C:\Users\USER\Documents\Steganography\webapp\__init__.py`
- Create: `C:\Users\USER\Documents\Steganography\webapp\main.py`
- Create: `C:\Users\USER\Documents\Steganography\webapp\config.py`
- Create: `C:\Users\USER\Documents\Steganography\tests\webapp\__init__.py`
- Create: `C:\Users\USER\Documents\Steganography\tests\webapp\conftest.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_main.py`

**Step 1: Write the failing test**

Write a route test that imports the FastAPI app and expects `GET /` to return HTTP 200.

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: FAIL because the `webapp` package and app entry point do not exist yet.

**Step 3: Write minimal implementation**

- add FastAPI and Jinja2 to install requirements
- create the `webapp` package
- create a minimal FastAPI app with a placeholder `/` route
- add a test client fixture

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add FastAPI app skeleton`

### Task 2: Add the Base Template and Static Asset Structure

**Files:**
- Create: `C:\Users\USER\Documents\Steganography\webapp\templates\index.html`
- Create: `C:\Users\USER\Documents\Steganography\webapp\static\styles.css`
- Create: `C:\Users\USER\Documents\Steganography\webapp\static\app.js`
- Modify: `C:\Users\USER\Documents\Steganography\webapp\main.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_main.py`

**Step 1: Write the failing test**

Extend the page test so `GET /` asserts that the HTML contains:

- `STEG`
- the three mode labels `ENCODE`, `DECODE`, `CHECK`
- a headline fragment such as `Hide Signal`

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: FAIL because the placeholder route does not yet render the designed template.

**Step 3: Write minimal implementation**

- mount a static files directory
- configure Jinja2 templates
- render a poster-style base page
- create CSS variables and layout primitives matching the approved visual system
- add a minimal JS file placeholder

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add Steg application shell`

### Task 3: Add a SteganoGAN Service Layer with Model Caching

**Files:**
- Create: `C:\Users\USER\Documents\Steganography\webapp\services.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Write tests for a service class or module that:

- loads a model for a selected architecture
- caches it across repeated calls
- rejects unsupported architectures

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because the service module does not exist.

**Step 3: Write minimal implementation**

- create a supported-architecture constant
- implement a cached loader around `SteganoGAN.load`
- normalize and validate architecture input

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add SteganoGAN web service layer`

### Task 4: Add Temporary File Management for Uploads and Outputs

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\config.py`
- Modify: `C:\Users\USER\Documents\Steganography\webapp\services.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Write tests that verify:

- uploaded files are written into a configured temp directory
- generated encoded files receive unique IDs
- download lookup only returns files from the managed output directory

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because temp storage behavior is not implemented yet.

**Step 3: Write minimal implementation**

- define app temp directories in config
- add helpers to persist uploads and generated outputs
- return safe metadata objects containing IDs and absolute paths

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add safe temp storage for web processing`

### Task 5: Implement Encode Service Behavior

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\services.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Write a service test that:

- saves an uploaded image
- invokes the selected SteganoGAN model’s `encode` method with input path, output path, and message
- returns download metadata for the generated file

Use mocks around model loading and image processing boundaries so the test focuses on service behavior.

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because encode processing is not implemented.

**Step 3: Write minimal implementation**

- implement an `encode_image` service function
- validate that the message is not empty
- call the cached model’s `encode` method
- return a structured result with output ID and download URL

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add encode processing service`

### Task 6: Implement Decode and Strict Check Service Behavior

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\services.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`

**Step 1: Write the failing test**

Write tests that verify:

- `decode_image` returns recovered text from the selected model
- decode failures produce controlled error values
- `check_image` returns `true` only when `decode_image` succeeds with a valid message

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: FAIL because decode and check behavior are missing.

**Step 3: Write minimal implementation**

- implement `decode_image`
- implement strict `check_image` on top of the decode result
- normalize error messages so route handlers can distinguish expected failure from server errors

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_services.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add decode and strict check services`

### Task 7: Implement API Endpoints

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\main.py`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_api.py`

**Step 1: Write the failing test**

Write route tests for:

- `POST /api/encode`
- `POST /api/decode`
- `POST /api/check`
- `GET /api/download/{id}`

Assert status codes, JSON shapes, and file download headers using mocked service functions.

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_api.py -v`

Expected: FAIL because the endpoints do not exist yet.

**Step 3: Write minimal implementation**

- add form/file endpoints
- validate required inputs
- translate service results into JSON responses
- stream generated files using Starlette responses

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_api.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add Steg API endpoints`

### Task 8: Build the Poster-Modernist Tool Interface

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\templates\index.html`
- Modify: `C:\Users\USER\Documents\Steganography\webapp\static\styles.css`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_main.py`

**Step 1: Write the failing test**

Extend HTML assertions so the rendered page includes:

- left-column sidebar labels
- architecture selector
- upload controls
- encode message field
- result panel container

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: FAIL because the page shell does not yet include the full tool workspace.

**Step 3: Write minimal implementation**

- create the full 12-column layout
- add the top bar, headline, and mode switcher
- add structured sections for input and results
- style controls to match the approved visual language
- make the layout responsive on mobile without losing hierarchy

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: build Steg workspace UI`

### Task 9: Add Frontend Interactions

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\webapp\static\app.js`
- Modify: `C:\Users\USER\Documents\Steganography\webapp\templates\index.html`
- Test: `C:\Users\USER\Documents\Steganography\tests\webapp\test_main.py`

**Step 1: Write the failing test**

Add assertions that the page contains:

- mode toggle hooks
- form identifiers
- result target regions
- download link placeholder

These server-rendered hooks are what the JS will depend on.

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: FAIL because the hook structure is incomplete.

**Step 3: Write minimal implementation**

- implement mode switching
- implement fetch-based submit handlers
- render encode/decode/check results inline
- show controlled error states
- update the download link after encode success

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp/test_main.py -v`

Expected: PASS

**Step 5: Commit**

Commit message: `feat: add Steg frontend interactions`

### Task 10: Add End-to-End Route and Service Integration Coverage

**Files:**
- Modify: `C:\Users\USER\Documents\Steganography\tests\webapp\test_api.py`
- Modify: `C:\Users\USER\Documents\Steganography\tests\webapp\test_services.py`
- Create: `C:\Users\USER\Documents\Steganography\tests\webapp\fixtures\sample.png`

**Step 1: Write the failing test**

Add focused tests for:

- missing message validation on encode
- unsupported architecture handling
- download of unknown output ID returning 404
- decode/check expected-negative responses

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/webapp -v`

Expected: FAIL because edge-case handling is incomplete.

**Step 3: Write minimal implementation**

- tighten validation and error responses
- ensure negative decode/check outcomes are reported consistently
- make unknown downloads return 404 cleanly

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/webapp -v`

Expected: PASS

**Step 5: Commit**

Commit message: `test: cover Steg web edge cases`

### Task 11: Verify the Full Application

**Files:**
- No code changes required unless verification reveals issues.

**Step 1: Run backend tests**

Run: `python -m pytest tests/webapp -v`

Expected: all webapp tests pass.

**Step 2: Run broader regression tests**

Run: `python -m pytest tests -v`

Expected: existing project tests remain green or any known incompatibilities are documented.

**Step 3: Run the application locally**

Run: `uvicorn webapp.main:app --reload`

Expected: app starts and serves the Steg interface.

**Step 4: Perform browser verification**

Use Playwright to verify:

- the page loads
- all three modes are accessible
- encode shows a download action
- decode and check display clear result states
- layout holds together on desktop and mobile widths

**Step 5: Commit**

Commit message: `chore: verify Steg webapp`

