from functools import lru_cache
from io import BytesIO
from pathlib import Path
from time import time
from uuid import uuid4

from PIL import Image, UnidentifiedImageError

from steganogan import SteganoGAN
from webapp.config import MAX_IMAGE_DIMENSION, OUTPUT_DIR, OUTPUT_RETENTION_SECONDS, UPLOAD_DIR

SUPPORTED_ARCHITECTURES = ("basic", "dense", "residual")
EXPECTED_DECODE_FAILURE_MESSAGE = "Failed to find message."

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
    return SteganoGAN.load(architecture=architecture, cuda=False, verbose=False)


def get_model(architecture):
    normalized = _normalize_architecture(architecture)
    return _load_model(normalized)


def encode_image(*, architecture, filename=None, upload=None, contents=None, message):
    normalized = _normalize_architecture(architecture)
    if not message or not message.strip():
        raise ServiceValidationError("Message is required for encoding.")

    _cleanup_expired_outputs()
    input_path = None
    output_id = uuid4().hex
    output_path = OUTPUT_DIR / f"{output_id}.png"

    try:
        input_path = _write_upload(upload=upload, contents=contents, filename=filename)
        model = get_model(normalized)
        model.encode(str(input_path), str(output_path), message.strip())
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


def decode_image(*, architecture, filename=None, upload=None, contents=None):
    normalized = _normalize_architecture(architecture)
    input_path = None

    try:
        input_path = _write_upload(upload=upload, contents=contents, filename=filename)
        model = get_model(normalized)
        message = model.decode(str(input_path))
    except ValueError as error:
        if str(error) == EXPECTED_DECODE_FAILURE_MESSAGE:
            result = {
                "ok": False,
                "message": "No hidden message found.",
                "architecture": normalized,
            }
            return result
        raise ProcessingError("Decoding failed.") from error
    except ProcessingError:
        raise
    except Exception as error:
        raise ProcessingError("Decoding failed.") from error
    finally:
        _remove_path(input_path)

    return {
        "ok": True,
        "message": message,
        "architecture": normalized,
    }


def check_image(*, architecture, filename=None, upload=None, contents=None):
    decoded = decode_image(
        architecture=architecture,
        filename=filename,
        upload=upload,
        contents=contents,
    )

    if decoded["ok"]:
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
