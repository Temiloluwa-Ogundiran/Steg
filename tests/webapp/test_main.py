def test_root_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "STEG" in response.text
    assert "Encode" in response.text
    assert "Decode" in response.text
    assert "Check" in response.text
    assert "// Hide signal" in response.text
    assert 'name="architecture"' not in response.text
    assert 'type="file"' in response.text
    assert 'name="message"' in response.text
    assert response.text.count('name="passphrase"') == 2
    assert response.text.count('minlength="12"') == 2
    assert 'id="terminal-body"' in response.text
    assert 'data-mode-target="encode"' in response.text
    assert 'data-mode-panel="encode"' in response.text
    assert "SYSTEM READY" in response.text
    assert "TERMINAL" in response.text
    assert "LISTENING" in response.text
    assert "01 // MODE" in response.text
    assert "02 // INPUT" in response.text
    assert "03 // PAYLOAD" in response.text
    assert "04 // KEY" in response.text
    assert "EXECUTE" in response.text
    assert "FASTAPI / READY" not in response.text
    assert "If the passphrase is lost" not in response.text
