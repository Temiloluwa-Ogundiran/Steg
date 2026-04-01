from unittest.mock import MagicMock

from webapp import services


PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT"
    b"\x08\xd7c\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\xc9\xfe"
    b"\x92\xef\x00\x00\x00\x00IEND\xaeB`\x82"
)


def test_encode_endpoint_returns_json_payload(client, monkeypatch):
    encode_image = MagicMock(
        return_value={
            "ok": True,
            "output_id": "abc123",
            "download_url": "/api/download/abc123",
            "filename": "steg-cover.png",
            "architecture": "dense",
        }
    )
    monkeypatch.setattr(services, "encode_image", encode_image)

    response = client.post(
        "/api/encode",
        data={"message": "secret message"},
        files={"image": ("cover.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "output_id": "abc123",
        "download_url": "/api/download/abc123",
        "filename": "steg-cover.png",
        "architecture": "dense",
    }
    _, kwargs = encode_image.call_args
    assert kwargs["architecture"] == "dense"
    assert kwargs["filename"] == "cover.png"
    assert kwargs["message"] == "secret message"
    assert hasattr(kwargs["upload"], "filename")
    assert kwargs["upload"].filename == "cover.png"
    assert hasattr(kwargs["upload"], "file")


def test_decode_endpoint_returns_json_payload(client, monkeypatch):
    decode_image = MagicMock(
        return_value={
            "ok": True,
            "message": "hello",
            "architecture": "dense",
        }
    )
    monkeypatch.setattr(services, "decode_image", decode_image)

    response = client.post(
        "/api/decode",
        files={"image": ("encoded.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "message": "hello",
        "architecture": "dense",
    }
    _, kwargs = decode_image.call_args
    assert kwargs["architecture"] == "dense"
    assert kwargs["filename"] == "encoded.png"
    assert hasattr(kwargs["upload"], "filename")
    assert kwargs["upload"].filename == "encoded.png"
    assert hasattr(kwargs["upload"], "file")


def test_check_endpoint_returns_json_payload(client, monkeypatch):
    check_image = MagicMock(
        return_value={
            "ok": True,
            "hidden_data": False,
            "message": "No hidden data found.",
            "architecture": "dense",
        }
    )
    monkeypatch.setattr(services, "check_image", check_image)

    response = client.post(
        "/api/check",
        files={"image": ("plain.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 200
    assert response.json() == {
        "ok": True,
        "hidden_data": False,
        "message": "No hidden data found.",
        "architecture": "dense",
    }
    _, kwargs = check_image.call_args
    assert kwargs["architecture"] == "dense"
    assert kwargs["filename"] == "plain.png"
    assert hasattr(kwargs["upload"], "filename")
    assert kwargs["upload"].filename == "plain.png"
    assert hasattr(kwargs["upload"], "file")


def test_download_endpoint_streams_output_file(client, monkeypatch, tmp_path):
    output_path = tmp_path / "abc123.png"
    output_path.write_bytes(b"encoded-image")
    get_output_path = MagicMock(return_value=output_path)
    monkeypatch.setattr(services, "get_output_path", get_output_path)

    response = client.get("/api/download/abc123")

    assert response.status_code == 200
    assert response.content == b"encoded-image"
    assert "attachment;" in response.headers["content-disposition"]
    assert "abc123.png" in response.headers["content-disposition"]
    get_output_path.assert_called_once_with("abc123")


def test_encode_endpoint_translates_validation_errors_to_400(client, monkeypatch):
    encode_image = MagicMock(side_effect=services.ServiceValidationError("Unsupported architecture."))
    monkeypatch.setattr(services, "encode_image", encode_image)

    response = client.post(
        "/api/encode",
        data={"message": "secret message"},
        files={"image": ("cover.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported architecture."}


def test_decode_endpoint_translates_processing_errors_to_500(client, monkeypatch):
    decode_image = MagicMock(side_effect=services.ProcessingError("Decoding failed."))
    monkeypatch.setattr(services, "decode_image", decode_image)

    response = client.post(
        "/api/decode",
        files={"image": ("encoded.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 500
    assert response.json() == {"detail": "Decoding failed."}


def test_download_endpoint_returns_404_for_missing_output(client, monkeypatch):
    get_output_path = MagicMock(side_effect=services.OutputNotFoundError("Missing output."))
    monkeypatch.setattr(services, "get_output_path", get_output_path)

    response = client.get("/api/download/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "Missing output."}
