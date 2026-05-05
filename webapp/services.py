from base64 import b64decode, urlsafe_b64encode
from binascii import Error as BinasciiError
from functools import lru_cache
from io import BytesIO
import os
import warnings
from os import urandom
from pathlib import Path
from time import time
from uuid import uuid4

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from PIL import Image, UnidentifiedImageError
import torch
from torch.serialization import SourceChangeWarning

from steganogan import SteganoGAN
from webapp.config import (
    ENCRYPTED_PAYLOAD_PREFIX,
    ENCRYPTION_NONCE_BYTES,
    KDF_SALT_BYTES,
    MAX_IMAGE_DIMENSION,
    OUTPUT_DIR,
    OUTPUT_RETENTION_SECONDS,
    PASSPHRASE_MIN_LENGTH,
    UPLOAD_DIR,
)

SUPPORTED_ARCHITECTURES = ("basic", "dense", "residual")
EXPECTED_DECODE_FAILURE_MESSAGE = "Failed to find message."
DERIVED_KEY_BYTES = 32
PAYLOAD_SEGMENT_COUNT = 3
SCRYPT_COST = 2 ** 14
SCRYPT_BLOCK_SIZE = 8
SCRYPT_PARALLELIZATION = 1
_TORCH_CONFIGURED = False

warnings.filterwarnings("ignore", category=SourceChangeWarning)

try:
    _RESAMPLE_FILTER = Image.Resampling.LANCZOS
except AttributeError:  # pragma: no cover - Pillow compatibility fallback
    _RESAMPLE_FILTER = Image.LANCZOS


class ServiceValidationError(ValueError):
    """Raised when user input is invalid for the web service."""


class OutputNotFoundError(FileNotFoundError):
    """Raised when a generated output cannot be found."""


class ProcessingError(RuntimeError):
    """Raised when model processing fails unexpectedly."""


def _env_int(name):
    value = os.getenv(name)
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer.") from exc


def configure_torch():
    global _TORCH_CONFIGURED
    if _TORCH_CONFIGURED:
        return

    num_threads = _env_int("TORCH_NUM_THREADS")
    if num_threads is not None:
        if num_threads < 1:
            raise RuntimeError("TORCH_NUM_THREADS must be >= 1.")
        torch.set_num_threads(num_threads)

    interop_threads = _env_int("TORCH_NUM_INTEROP_THREADS")
    if interop_threads is not None:
        if interop_threads < 1:
            raise RuntimeError("TORCH_NUM_INTEROP_THREADS must be >= 1.")
        torch.set_num_interop_threads(interop_threads)

    _TORCH_CONFIGURED = True


def _urlsafe_b64encode_bytes(value):
    return urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _urlsafe_b64decode_text(value):
    padding = "=" * (-len(value) % 4)
    return b64decode(value + padding, altchars=b"-_", validate=True)


def _validate_passphrase(passphrase):
    candidate = (passphrase or "").strip()
    if not candidate:
        raise ServiceValidationError("Passphrase is required.")
    if len(candidate) < PASSPHRASE_MIN_LENGTH:
        raise ServiceValidationError(
            f"Passphrase must be at least {PASSPHRASE_MIN_LENGTH} characters."
        )

    return candidate


def _derive_key(passphrase, salt):
    kdf = Scrypt(
        salt=salt,
        length=DERIVED_KEY_BYTES,
        n=SCRYPT_COST,
        r=SCRYPT_BLOCK_SIZE,
        p=SCRYPT_PARALLELIZATION,
    )
    return kdf.derive(passphrase.encode("utf-8"))


def _is_supported_payload(payload):
    candidate = (payload or "").strip()
    if not candidate.startswith(ENCRYPTED_PAYLOAD_PREFIX):
        return False

    segments = candidate[len(ENCRYPTED_PAYLOAD_PREFIX):].split(".")
    if len(segments) != PAYLOAD_SEGMENT_COUNT or not all(segments):
        return False

    try:
        salt, nonce, ciphertext = [_urlsafe_b64decode_text(segment) for segment in segments]
    except (BinasciiError, ValueError, TypeError):
        return False

    return (
        len(salt) == KDF_SALT_BYTES
        and len(nonce) == ENCRYPTION_NONCE_BYTES
        and len(ciphertext) > 0
    )


def _encrypt_message(message, passphrase):
    validated_passphrase = _validate_passphrase(passphrase)
    salt = urandom(KDF_SALT_BYTES)
    nonce = urandom(ENCRYPTION_NONCE_BYTES)
    key = _derive_key(validated_passphrase, salt)
    ciphertext = AESGCM(key).encrypt(nonce, message.encode("utf-8"), None)
    segments = (
        _urlsafe_b64encode_bytes(salt),
        _urlsafe_b64encode_bytes(nonce),
        _urlsafe_b64encode_bytes(ciphertext),
    )
    return f"{ENCRYPTED_PAYLOAD_PREFIX}{'.'.join(segments)}"


def _parse_encrypted_payload(payload):
    if not _is_supported_payload(payload):
        raise ServiceValidationError("Invalid passphrase or corrupted payload.")

    encoded_segments = payload[len(ENCRYPTED_PAYLOAD_PREFIX):].split(".")
    try:
        salt, nonce, ciphertext = [_urlsafe_b64decode_text(
            segment) for segment in encoded_segments]
    except (BinasciiError, ValueError, TypeError):
        raise ServiceValidationError("Invalid passphrase or corrupted payload.") from None

    return salt, nonce, ciphertext


def _decrypt_message(payload, passphrase):
    validated_passphrase = _validate_passphrase(passphrase)
    salt, nonce, ciphertext = _parse_encrypted_payload(payload)

    try:
        key = _derive_key(validated_passphrase, salt)
        plaintext = AESGCM(key).decrypt(nonce, ciphertext, None)
        return plaintext.decode("utf-8")
    except (InvalidTag, ValueError, TypeError, UnicodeDecodeError):
        raise ServiceValidationError("Invalid passphrase or corrupted payload.") from None


def _ensure_runtime_dirs():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _normalize_architecture(architecture):
    normalized = (architecture or "").strip().lower()
    if normalized not in SUPPORTED_ARCHITECTURES:
        raise ServiceValidationError("Unsupported architecture.")

    return normalized


def _remove_path(path):
    if path and path.exists():
        path.unlink(missing_ok=True)


def _resolve_upload_source(upload=None, contents=None):
    if upload is not None:
        source = getattr(upload, "file", upload)
        if hasattr(source, "seek"):
            source.seek(0)
        return source

    if contents is None:
        raise ServiceValidationError("Missing upload contents.")

    return BytesIO(contents)


def _normalize_image(upload=None, contents=None):
    source = _resolve_upload_source(upload, contents)
    try:
        with Image.open(source) as image:
            image.load()
            normalized = image.convert("RGB")
            if max(normalized.size) > MAX_IMAGE_DIMENSION:
                normalized.thumbnail((MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION), _RESAMPLE_FILTER)
            return normalized
    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise ServiceValidationError("The uploaded file is not a readable image.") from error


def _write_upload(upload=None, contents=None, filename=None):
    _ensure_runtime_dirs()
    input_id = uuid4().hex
    input_path = UPLOAD_DIR / f"{input_id}.png"
    normalized = _normalize_image(upload=upload, contents=contents)
    normalized.save(input_path, format="PNG")
    return input_path


def _cleanup_expired_outputs(now=None):
    _ensure_runtime_dirs()
    now = now or time()
    cutoff = now - OUTPUT_RETENTION_SECONDS

    for output_path in OUTPUT_DIR.glob("*.png"):
        try:
            if output_path.stat().st_mtime < cutoff:
                output_path.unlink(missing_ok=True)
        except FileNotFoundError:
            continue


@lru_cache(maxsize=3)
def _load_model(architecture):
    configure_torch()
    return SteganoGAN.load(architecture=architecture, cuda=False, verbose=False)


def get_model(architecture):
    normalized = _normalize_architecture(architecture)
    return _load_model(normalized)


def _extract_hidden_payload(*, architecture, filename=None, upload=None, contents=None):
    normalized = _normalize_architecture(architecture)
    input_path = None

    try:
        input_path = _write_upload(upload=upload, contents=contents, filename=filename)
        model = get_model(normalized)
        payload = model.decode(str(input_path))
    except ValueError as error:
        if str(error) == EXPECTED_DECODE_FAILURE_MESSAGE:
            return {
                "ok": False,
                "payload": None,
                "architecture": normalized,
            }
        raise ProcessingError("Decoding failed.") from error
    except ProcessingError:
        raise
    except Exception as error:
        raise ProcessingError("Decoding failed.") from error
    finally:
        _remove_path(input_path)

    return {
        "ok": True,
        "payload": payload,
        "architecture": normalized,
    }


def encode_image(*, architecture, filename=None, upload=None, contents=None, message, passphrase):
    normalized = _normalize_architecture(architecture)
    if not message or not message.strip():
        raise ServiceValidationError("Message is required for encoding.")

    validated_passphrase = _validate_passphrase(passphrase)
    _cleanup_expired_outputs()
    input_path = None
    output_id = uuid4().hex
    output_path = OUTPUT_DIR / f"{output_id}.png"

    try:
        input_path = _write_upload(upload=upload, contents=contents, filename=filename)
        model = get_model(normalized)
        encrypted_payload = _encrypt_message(message.strip(), validated_passphrase)
        model.encode(str(input_path), str(output_path), encrypted_payload)
        if not output_path.exists():
            raise ProcessingError("Encoded output was not generated.")
    except ServiceValidationError:
        raise
    except ProcessingError:
        raise
    except Exception as error:
        raise ProcessingError("Encoding failed.") from error
    finally:
        _remove_path(input_path)

    return {
        "ok": True,
        "output_id": output_id,
        "download_url": f"/api/download/{output_id}",
        "filename": f"steg-{Path(filename or 'image').stem}.png",
        "architecture": normalized,
    }


def decode_image(*, architecture, filename=None, upload=None, contents=None, passphrase):
    validated_passphrase = _validate_passphrase(passphrase)
    decoded = _extract_hidden_payload(
        architecture=architecture,
        filename=filename,
        upload=upload,
        contents=contents,
    )

    if not decoded["ok"]:
        return {
            "ok": False,
            "message": "No hidden message found.",
            "architecture": decoded["architecture"],
        }

    if not _is_supported_payload(decoded["payload"]):
        raise ServiceValidationError("Unsupported encrypted payload.")

    return {
        "ok": True,
        "message": _decrypt_message(decoded["payload"], validated_passphrase),
        "architecture": decoded["architecture"],
    }


def check_image(*, architecture, filename=None, upload=None, contents=None):
    decoded = _extract_hidden_payload(
        architecture=architecture,
        filename=filename,
        upload=upload,
        contents=contents,
    )

    if decoded["ok"] and _is_supported_payload(decoded["payload"]):
        return {
            "ok": True,
            "hidden_data": True,
            "message": "Hidden data found.",
            "architecture": decoded["architecture"],
        }

    return {
        "ok": True,
        "hidden_data": False,
        "message": "No hidden data found.",
        "architecture": decoded["architecture"],
    }


def get_output_path(output_id):
    _cleanup_expired_outputs()
    candidate = (output_id or "").strip().lower()
    if not candidate.isalnum():
        raise OutputNotFoundError("Missing output.")

    output_path = OUTPUT_DIR / f"{candidate}.png"
    if not output_path.exists():
        raise OutputNotFoundError("Missing output.")

    return output_path
