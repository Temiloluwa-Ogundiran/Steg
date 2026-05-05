def test_root_returns_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "STEG" in response.text
    assert "ENCODE" in response.text
    assert "DECODE" in response.text
    assert "CHECK" in response.text
    assert "Hide Signal" in response.text
    assert "DENSE" in response.text
    assert 'name="architecture"' not in response.text
    assert 'type="file"' in response.text
    assert 'name="message"' in response.text
    assert response.text.count('name="passphrase"') == 2
    assert response.text.count('minlength="12"') == 2
    assert "If the passphrase is lost" in response.text
    assert 'id="result-panel"' in response.text
    assert 'data-mode-target="encode"' in response.text
    assert 'data-mode-panel="encode"' in response.text
    assert "FASTAPI / READY" not in response.text
