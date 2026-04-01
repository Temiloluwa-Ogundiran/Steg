from io import BytesIO
import os
from pathlib import Path
from unittest.mock import MagicMock
from uuid import UUID
from time import time

import pytest
from PIL import Image

from webapp import services


def make_png_bytes(color=(19, 81, 170)):
    image = Image.new("RGB", (8, 8), color=color)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def make_image_bytes(size=(8, 8), mode="RGB", color=(19, 81, 170), format="PNG"):
    image = Image.new(mode, size, color=color)
    buffer = BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()


@pytest.fixture(autouse=True)
def clear_model_cache():
    services._load_model.cache_clear()
    yield
    services._load_model.cache_clear()


def test_get_model_caches_by_architecture(monkeypatch):
    model = object()
    load = MagicMock(return_value=model)
    monkeypatch.setattr(services.SteganoGAN, "load", load)

    first = services.get_model("dense")
    second = services.get_model("dense")

    assert first is model
    assert second is model
    load.assert_called_once_with(architecture="dense", cuda=False, verbose=False)


def test_get_model_rejects_unsupported_architecture():
    with pytest.raises(services.ServiceValidationError):
        services.get_model("unknown")


def test_get_model_normalizes_architecture_before_caching(monkeypatch):
    model = object()
    load = MagicMock(return_value=model)
    monkeypatch.setattr(services.SteganoGAN, "load", load)

    first = services.get_model("  Dense  ")
    second = services.get_model("dense")

    assert first is model
    assert second is model
    load.assert_called_once_with(architecture="dense", cuda=False, verbose=False)


def test_optimization_defaults_are_defined():
    assert services.MAX_IMAGE_DIMENSION == 2048
    assert services.OUTPUT_RETENTION_SECONDS > 0


def test_write_upload_normalizes_and_resizes_oversized_images(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    upload_path = services._write_upload(
        contents=make_image_bytes(size=(4096, 1024), mode="RGBA", color=(19, 81, 170, 120)),
        filename="cover.png",
    )

    assert upload_path.exists()
    with Image.open(upload_path) as image:
        assert image.mode == "RGB"
        assert image.size == (2048, 512)


def test_write_upload_preserves_small_image_dimensions(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    upload_path = services._write_upload(
        contents=make_image_bytes(size=(128, 96), mode="RGBA", color=(19, 81, 170, 120)),
        filename="cover.png",
    )

    with Image.open(upload_path) as image:
        assert image.mode == "RGB"
        assert image.size == (128, 96)


def test_encode_image_persists_input_and_returns_download_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    model = MagicMock()

    def encode_side_effect(input_path, output_path, message):
        assert Path(input_path).exists()
        assert message == "secret message"
        Path(output_path).write_bytes(b"encoded")

    model.encode.side_effect = encode_side_effect
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    result = services.encode_image(
        architecture="dense",
        filename="cover.png",
        contents=make_png_bytes(),
        message="secret message",
    )

    assert result["ok"] is True
    assert result["output_id"]
    assert result["download_url"].startswith("/api/download/")
    assert result["filename"].endswith(".png")
    model.encode.assert_called_once()


def test_encode_image_cleans_temp_upload_and_stale_outputs(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "outputs"
    monkeypatch.setattr(services, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(services, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(services, "OUTPUT_RETENTION_SECONDS", 60)

    stale_output = output_dir / "stale.png"
    stale_output.parent.mkdir(parents=True, exist_ok=True)
    stale_output.write_bytes(b"old")
    old_timestamp = time() - 120
    os.utime(stale_output, (old_timestamp, old_timestamp))

    model = MagicMock()

    def encode_side_effect(input_path, output_path, message):
        Path(output_path).write_bytes(b"encoded")

    model.encode.side_effect = encode_side_effect
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    result = services.encode_image(
        architecture="dense",
        filename="cover.png",
        contents=make_png_bytes(),
        message="secret message",
    )

    assert result["ok"] is True
    assert not list(upload_dir.glob("*"))
    assert not stale_output.exists()
    assert Path(output_dir / f"{result['output_id']}.png").exists()


def test_encode_image_rejects_empty_message(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    with pytest.raises(services.ServiceValidationError):
        services.encode_image(
            architecture="dense",
            filename="cover.png",
            contents=make_png_bytes(),
            message="   ",
        )


def test_encode_image_cleans_temp_upload_on_processing_error(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "outputs"
    monkeypatch.setattr(services, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(services, "OUTPUT_DIR", output_dir)

    model = MagicMock()
    model.encode.side_effect = RuntimeError("boom")
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    with pytest.raises(services.ProcessingError):
        services.encode_image(
            architecture="dense",
            filename="cover.png",
            contents=make_png_bytes(),
            message="secret message",
        )

    assert not list(upload_dir.glob("*"))


def test_decode_image_returns_message(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    model = MagicMock()
    model.decode.return_value = "hello"
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    result = services.decode_image(
        architecture="residual",
        filename="encoded.png",
        contents=make_png_bytes(),
    )

    assert result == {"ok": True, "message": "hello", "architecture": "residual"}
    assert not list((tmp_path / "uploads").glob("*"))


def test_decode_image_returns_controlled_negative_result(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    model = MagicMock()
    model.decode.side_effect = ValueError("Failed to find message.")
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    result = services.decode_image(
        architecture="basic",
        filename="encoded.png",
        contents=make_png_bytes(),
    )

    assert result["ok"] is False
    assert result["architecture"] == "basic"
    assert "No hidden message" in result["message"]
    assert not list((tmp_path / "uploads").glob("*"))


def test_decode_image_raises_processing_error_for_unexpected_value_error(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    model = MagicMock()
    model.decode.side_effect = ValueError("something else went wrong")
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    with pytest.raises(services.ProcessingError):
        services.decode_image(
            architecture="basic",
            filename="encoded.png",
            contents=make_png_bytes(),
        )

    assert not list((tmp_path / "uploads").glob("*"))


def test_check_image_is_true_only_when_decode_succeeds(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    mock_decode = MagicMock(side_effect=[
        {"ok": True, "message": "secret", "architecture": "dense"},
        {"ok": False, "message": "No hidden message found.", "architecture": "dense"},
    ])
    monkeypatch.setattr(services, "decode_image", mock_decode)

    found = services.check_image(
        architecture="dense",
        filename="encoded.png",
        contents=make_png_bytes(),
    )
    missing = services.check_image(
        architecture="dense",
        filename="plain.png",
        contents=make_png_bytes(color=(0, 0, 0)),
    )

    assert found == {
        "ok": True,
        "hidden_data": True,
        "message": "Hidden data found.",
        "architecture": "dense",
    }
    assert missing == {
        "ok": True,
        "hidden_data": False,
        "message": "No hidden data found.",
        "architecture": "dense",
    }


def test_check_image_cleans_temp_upload_on_failure(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "outputs"
    monkeypatch.setattr(services, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(services, "OUTPUT_DIR", output_dir)

    model = MagicMock()
    model.decode.side_effect = ValueError("something else went wrong")
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    with pytest.raises(services.ProcessingError):
        services.check_image(
            architecture="dense",
            filename="encoded.png",
            contents=make_png_bytes(),
        )

    assert not list(upload_dir.glob("*"))


def test_encode_image_generates_unique_output_ids(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "UPLOAD_DIR", tmp_path / "uploads")
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    def fake_write_upload(upload=None, contents=None, filename=None):
        upload_dir = tmp_path / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        upload_path = upload_dir / f"{Path(filename).stem}.png"
        upload_path.write_bytes(contents)
        return upload_path

    monkeypatch.setattr(services, "_write_upload", fake_write_upload)
    monkeypatch.setattr(services, "uuid4", MagicMock(side_effect=[UUID(int=1), UUID(int=2)]))

    model = MagicMock()

    def encode_side_effect(input_path, output_path, message):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(b"encoded")

    model.encode.side_effect = encode_side_effect
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    first = services.encode_image(
        architecture="dense",
        filename="cover.png",
        contents=make_png_bytes(),
        message="first secret",
    )
    second = services.encode_image(
        architecture="dense",
        filename="cover.png",
        contents=make_png_bytes(),
        message="second secret",
    )

    assert first["output_id"] != second["output_id"]
    assert first["download_url"] != second["download_url"]
    assert first["output_id"] == UUID(int=1).hex
    assert second["output_id"] == UUID(int=2).hex


def test_encode_image_removes_expired_outputs_before_creating_new_one(tmp_path, monkeypatch):
    upload_dir = tmp_path / "uploads"
    output_dir = tmp_path / "outputs"
    monkeypatch.setattr(services, "UPLOAD_DIR", upload_dir)
    monkeypatch.setattr(services, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(services, "OUTPUT_RETENTION_SECONDS", 60)

    stale_output = output_dir / "stale.png"
    stale_output.parent.mkdir(parents=True, exist_ok=True)
    stale_output.write_bytes(b"old")
    old_timestamp = time() - 120
    os.utime(stale_output, (old_timestamp, old_timestamp))

    model = MagicMock()

    def encode_side_effect(input_path, output_path, message):
        Path(output_path).write_bytes(b"encoded")

    model.encode.side_effect = encode_side_effect
    monkeypatch.setattr(services, "get_model", MagicMock(return_value=model))

    services.encode_image(
        architecture="dense",
        filename="cover.png",
        contents=make_png_bytes(),
        message="secret message",
    )

    assert not stale_output.exists()


def test_get_output_path_raises_for_unknown_id(tmp_path, monkeypatch):
    monkeypatch.setattr(services, "OUTPUT_DIR", tmp_path / "outputs")

    with pytest.raises(services.OutputNotFoundError):
        services.get_output_path("missing")


def test_get_output_path_removes_expired_output(tmp_path, monkeypatch):
    output_dir = tmp_path / "outputs"
    monkeypatch.setattr(services, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(services, "OUTPUT_RETENTION_SECONDS", 60)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "expired.png"
    output_path.write_bytes(b"encoded")
    old_timestamp = time() - 120
    os.utime(output_path, (old_timestamp, old_timestamp))

    with pytest.raises(services.OutputNotFoundError):
        services.get_output_path("expired")

    assert not output_path.exists()


def test_get_output_path_returns_existing_file(tmp_path, monkeypatch):
    output_dir = tmp_path / "outputs"
    monkeypatch.setattr(services, "OUTPUT_DIR", output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "abc123.png"
    output_path.write_bytes(b"encoded")

    assert services.get_output_path("abc123") == output_path
