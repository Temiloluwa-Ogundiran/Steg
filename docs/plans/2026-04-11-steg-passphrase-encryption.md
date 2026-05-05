# Steg Passphrase Encryption Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add passphrase-protected message encryption to the Steg web app so encoded payloads require the correct passphrase to decode while `CHECK` still works without a passphrase.

**Architecture:** Keep encryption in the FastAPI web app service layer rather than modifying the steganography model internals. Encode will wrap plaintext into a versioned encrypted envelope before calling `SteganoGAN.encode`, decode will require a passphrase to decrypt that envelope after `SteganoGAN.decode`, and check will validate the presence of the envelope format without decryption.

**Tech Stack:** Python, FastAPI, Jinja2, vanilla JavaScript, pytest, cryptography

---

### Task 1: Add Crypto Dependency and Configuration

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/requirements-web.txt`
- Modify: `C:/Users/USER/Documents/Steganography/webapp/config.py`
- Test: `C:/Users/USER/Documents/Steganography/tests/webapp/test_services.py`

**Step 1: Write the failing test**

Add a service test that asserts the encryption configuration constants exist and the payload prefix is defined, for example:

```python
def test_encryption_defaults_are_defined():
    assert services.ENCRYPTED_PAYLOAD_PREFIX == "STEGv1:"
    assert services.PASSPHRASE_MIN_LENGTH >= 1
```

**Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest tests/webapp/test_services.py::test_encryption_defaults_are_defined -v
```

Expected: FAIL because the new constants are not defined yet.

**Step 3: Write minimal implementation**

- add `cryptography` to `requirements-web.txt`
- add config constants in `webapp/config.py` for:
  - encrypted payload prefix
  - KDF salt length
  - nonce length
  - minimum passphrase length

**Step 4: Run test to verify it passes**

Run:

```powershell
python -m pytest tests/webapp/test_services.py::test_encryption_defaults_are_defined -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add requirements-web.txt webapp/config.py tests/webapp/test_services.py
git commit -m "chore: add passphrase encryption configuration"
```

### Task 2: Add Encrypted Envelope Helpers in the Service Layer

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/webapp/services.py`
- Test: `C:/Users/USER/Documents/Steganography/tests/webapp/test_services.py`

**Step 1: Write the failing tests**

Add focused tests for helper behavior, for example:

```python
def test_encrypt_message_creates_prefixed_payload():
    payload = services._encrypt_message("secret", "passphrase")
    assert payload.startswith("STEGv1:")


def test_decrypt_message_round_trips_with_correct_passphrase():
    payload = services._encrypt_message("secret", "passphrase")
    assert services._decrypt_message(payload, "passphrase") == "secret"


def test_decrypt_message_rejects_wrong_passphrase():
    payload = services._encrypt_message("secret", "passphrase")
    with pytest.raises(services.ServiceValidationError):
        services._decrypt_message(payload, "wrong-passphrase")


def test_is_supported_payload_detects_only_new_envelopes():
    assert services._is_supported_payload("STEGv1:abc") is True
    assert services._is_supported_payload("legacy-text") is False
```

**Step 2: Run test to verify they fail**

Run:

```powershell
python -m pytest tests/webapp/test_services.py -k "encrypt_message or decrypt_message or supported_payload" -v
```

Expected: FAIL because the helper functions do not exist yet.

**Step 3: Write minimal implementation**

In `webapp/services.py`:

- import the crypto primitives from `cryptography`
- add helper functions to:
  - validate a passphrase is non-empty
  - derive a key from passphrase + salt
  - encrypt plaintext into a versioned envelope
  - parse the envelope safely
  - decrypt the envelope with authenticated verification
  - identify whether a decoded payload matches the new Steg format

Keep failures generic: `Invalid passphrase or corrupted payload.`

**Step 4: Run test to verify they pass**

Run:

```powershell
python -m pytest tests/webapp/test_services.py -k "encrypt_message or decrypt_message or supported_payload" -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add webapp/services.py tests/webapp/test_services.py
git commit -m "feat: add encrypted payload envelope helpers"
```

### Task 3: Update Encode, Decode, and Check Service Behavior

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/webapp/services.py`
- Test: `C:/Users/USER/Documents/Steganography/tests/webapp/test_services.py`

**Step 1: Write the failing tests**

Add service tests that prove the new behavior:

```python
def test_encode_image_rejects_empty_passphrase(...):
    with pytest.raises(services.ServiceValidationError):
        services.encode_image(..., message="secret", passphrase="  ")


def test_decode_image_requires_passphrase(...):
    with pytest.raises(services.ServiceValidationError):
        services.decode_image(..., passphrase="  ")


def test_decode_image_decrypts_message_with_correct_passphrase(...):
    ...


def test_decode_image_rejects_legacy_payload(...):
    ...


def test_check_image_is_true_for_supported_encrypted_payload(...):
    ...


def test_check_image_is_false_for_legacy_payload(...):
    ...
```

Use mocked model outputs so the tests focus on web service behavior rather than model internals.

**Step 2: Run test to verify they fail**

Run:

```powershell
python -m pytest tests/webapp/test_services.py -k "passphrase or legacy_payload or check_image_is_true_for_supported_encrypted_payload" -v
```

Expected: FAIL because `encode_image`, `decode_image`, and `check_image` do not yet support passphrases and encrypted envelopes.

**Step 3: Write minimal implementation**

Update `webapp/services.py` so that:

- `encode_image(...)` accepts `passphrase`, validates it, encrypts `message`, and passes the encrypted envelope to the model
- `decode_image(...)` accepts `passphrase`, validates it, decrypts only supported `STEGv1:` payloads, and rejects legacy payloads
- `check_image(...)` reads the model output and returns `hidden_data=True` only for supported encrypted envelopes

Preserve temp-file cleanup and existing output-download behavior.

**Step 4: Run test to verify they pass**

Run:

```powershell
python -m pytest tests/webapp/test_services.py -k "passphrase or legacy_payload or check_image_is_true_for_supported_encrypted_payload" -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add webapp/services.py tests/webapp/test_services.py
git commit -m "feat: require passphrases for steg payloads"
```

### Task 4: Update FastAPI Routes and API Tests

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/webapp/main.py`
- Modify: `C:/Users/USER/Documents/Steganography/tests/webapp/test_api.py`

**Step 1: Write the failing tests**

Add API tests for:

```python
def test_encode_endpoint_passes_passphrase_to_service(...):
    ...


def test_decode_endpoint_passes_passphrase_to_service(...):
    ...


def test_encode_endpoint_rejects_missing_passphrase(...):
    ...


def test_decode_endpoint_rejects_missing_passphrase(...):
    ...
```

**Step 2: Run test to verify they fail**

Run:

```powershell
python -m pytest tests/webapp/test_api.py -k "passphrase" -v
```

Expected: FAIL because the routes do not yet accept or validate passphrases.

**Step 3: Write minimal implementation**

Update `webapp/main.py` so that:

- `/api/encode` accepts `passphrase: str = Form(...)`
- `/api/decode` accepts `passphrase: str = Form(...)`
- both routes reject blank passphrases with `400`
- the service calls include the passphrase argument
- `/api/check` remains unchanged with no passphrase

**Step 4: Run test to verify they pass**

Run:

```powershell
python -m pytest tests/webapp/test_api.py -k "passphrase" -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add webapp/main.py tests/webapp/test_api.py
git commit -m "feat: require passphrases in steg api routes"
```

### Task 5: Update the Web UI and Client-Side Flow

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/webapp/templates/index.html`
- Modify: `C:/Users/USER/Documents/Steganography/webapp/static/app.js`
- Test: `C:/Users/USER/Documents/Steganography/tests/webapp/test_main.py`

**Step 1: Write the failing test**

Add a route/template test that checks the rendered page includes passphrase inputs for encode and decode, for example:

```python
def test_root_contains_passphrase_fields(client):
    response = client.get("/")
    html = response.text
    assert 'name="passphrase"' in html
```

**Step 2: Run test to verify it fails**

Run:

```powershell
python -m pytest tests/webapp/test_main.py::test_root_contains_passphrase_fields -v
```

Expected: FAIL because the template does not yet render passphrase fields.

**Step 3: Write minimal implementation**

Update the template and client script so that:

- encode form includes a required passphrase field
- decode form includes a required passphrase field
- check form stays image-only
- the client-side validation blocks blank passphrases before submit
- decode result copy and encode result copy remain consistent with the current poster-style UI
- add a visible note that lost passphrases cannot be recovered

**Step 4: Run test to verify it passes**

Run:

```powershell
python -m pytest tests/webapp/test_main.py::test_root_contains_passphrase_fields -v
```

Expected: PASS

**Step 5: Commit**

```bash
git add webapp/templates/index.html webapp/static/app.js tests/webapp/test_main.py
git commit -m "feat: add passphrase fields to steg ui"
```

### Task 6: Update Documentation and Full Verification

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/README.md`
- Verify: `C:/Users/USER/Documents/Steganography/webapp/main.py`
- Verify: `C:/Users/USER/Documents/Steganography/webapp/services.py`
- Verify: `C:/Users/USER/Documents/Steganography/webapp/templates/index.html`
- Verify: `C:/Users/USER/Documents/Steganography/webapp/static/app.js`
- Verify: `C:/Users/USER/Documents/Steganography/tests/webapp/test_api.py`
- Verify: `C:/Users/USER/Documents/Steganography/tests/webapp/test_main.py`
- Verify: `C:/Users/USER/Documents/Steganography/tests/webapp/test_services.py`

**Step 1: Update README**

Document that:

- encode now requires a passphrase
- decode requires the same passphrase
- check does not require a passphrase
- legacy non-encrypted payloads are no longer supported by the web app

**Step 2: Run the full web app test suite**

Run:

```powershell
python -m pytest tests/webapp -v
```

Expected: PASS

**Step 3: Run a browser verification flow**

Run the web app locally and verify:

1. encode with an image, message, and passphrase
2. decode succeeds with the correct passphrase
3. decode fails with the wrong passphrase
4. check returns true for the encoded image

Use Playwright as required by the repo instructions.

**Step 4: Commit**

```bash
git add README.md webapp/main.py webapp/services.py webapp/templates/index.html webapp/static/app.js tests/webapp/test_api.py tests/webapp/test_main.py tests/webapp/test_services.py requirements-web.txt webapp/config.py
git commit -m "feat: add passphrase-protected steg messages"
```
