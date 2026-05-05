# Steg Passphrase Encryption Design

**Date:** 2026-04-11

## Summary

Strengthen Steg by requiring a user-entered passphrase for every encoded message and for every decode attempt. The hidden payload stored in the image will no longer be plaintext. Instead, the web app will encrypt the message into a self-contained envelope before passing it to the steganography model.

`CHECK` must continue to work without a passphrase. It should detect whether an image contains a valid Steg encrypted payload envelope, but it must not reveal or decrypt any message.

## Goals

- require a passphrase when encoding
- require the same passphrase when decoding
- keep encoded images self-contained
- allow `CHECK` to work without a passphrase
- reject legacy plaintext payloads going forward
- avoid storing passphrases, keys, or messages server-side

## Chosen Approach

Use a stateless encrypted payload envelope carried entirely inside the hidden message.

The flow will be:

1. The user submits `image + message + passphrase` to encode.
2. The service derives a cryptographic key from the passphrase using a random salt.
3. The plaintext message is encrypted with an authenticated cipher.
4. The service serializes the encrypted payload into a versioned Steg envelope string.
5. The envelope string is encoded into the image with the existing SteganoGAN model.

Decode reverses the process:

1. The model extracts the hidden string from the image.
2. The service verifies it is a supported Steg encrypted envelope.
3. The service derives the key from the submitted passphrase and stored salt.
4. The service decrypts the envelope and returns the recovered plaintext on authenticated success.

`CHECK` only verifies whether the extracted hidden string is a valid Steg encrypted envelope. It does not require or use the passphrase.

## Why This Approach

This approach improves confidentiality without introducing server-side secret storage. The image remains portable because all cryptographic material required for decryption, except the passphrase itself, is embedded inside the hidden payload envelope.

SQLite is not required for this feature. A database would only add complexity and create server-side state that is unnecessary for this security model.

## Payload Format

The hidden payload must be explicitly versioned and machine-detectable. The recommended string format is:

`STEGv1:<encoded-envelope>`

Where the encoded envelope contains:

- `salt`
- `nonce`
- authenticated `ciphertext`

The implementation should use a compact serialized representation that is easy to parse and validate.

## Security Requirements

- Use a well-supported crypto library rather than custom cryptography.
- Derive the key from the passphrase with a modern KDF and a random per-message salt.
- Use authenticated encryption so wrong passphrases and tampered payloads fail safely.
- Never log passphrases, derived keys, or decrypted plaintext.
- Return generic decode failures such as `Invalid passphrase or corrupted payload.`
- Continue using random output identifiers instead of predictable IDs.

## Compatibility

The new web app behavior is forward-only:

- newly encoded images always contain encrypted Steg envelopes
- decode only accepts the new protected payload format
- legacy plaintext payloads are treated as unsupported and decode should fail
- `CHECK` only reports true for valid Steg encrypted envelopes

## API Changes

### `/api/encode`

Requires:

- `image`
- `message`
- `passphrase`

### `/api/decode`

Requires:

- `image`
- `passphrase`

### `/api/check`

Requires:

- `image`

No passphrase is required.

## UI Changes

### Encode

Add a required `PASSPHRASE` field beneath the message field.

### Decode

Add a required `PASSPHRASE` field.

### Check

No passphrase field.

The UI should make one thing explicit: if the passphrase is lost, the hidden message cannot be recovered.

## Files Likely To Change

- [webapp/main.py](/C:/Users/USER/Documents/Steganography/webapp/main.py)
- [webapp/services.py](/C:/Users/USER/Documents/Steganography/webapp/services.py)
- [webapp/config.py](/C:/Users/USER/Documents/Steganography/webapp/config.py)
- [webapp/templates/index.html](/C:/Users/USER/Documents/Steganography/webapp/templates/index.html)
- [webapp/static/app.js](/C:/Users/USER/Documents/Steganography/webapp/static/app.js)
- [tests/webapp/test_api.py](/C:/Users/USER/Documents/Steganography/tests/webapp/test_api.py)
- [tests/webapp/test_services.py](/C:/Users/USER/Documents/Steganography/tests/webapp/test_services.py)
- [README.md](/C:/Users/USER/Documents/Steganography/README.md)
- [requirements-web.txt](/C:/Users/USER/Documents/Steganography/requirements-web.txt)

## Verification

The feature should be considered complete only after all of the following are verified:

- encode rejects missing passphrases
- decode rejects missing passphrases
- decode succeeds with the correct passphrase
- decode fails with the wrong passphrase
- check returns true for encrypted Steg payloads
- check returns false for plain images and unsupported payloads
- the web UI submits and renders the new passphrase flow correctly
- `python -m pytest tests/webapp -v` passes

## Notes

- The cryptographic layer should live in the web app service layer, not inside the core SteganoGAN model implementation.
- The existing `SteganoGAN.encode()` and `SteganoGAN.decode()` methods can remain unchanged because they only need to carry opaque strings.
