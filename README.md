# Steg

Steg is a FastAPI web application for image steganography. It gives you a clean browser-based workspace to hide messages inside images, download the encoded output, decode hidden messages from existing images, and check whether an image contains recoverable hidden data.

Under the hood, the app uses the original `steganogan` package in this repository, which is based on deep-learning steganography models.

## Features

- Encode a message into an image
- Protect every hidden message with a user-provided passphrase
- Download the generated encoded image
- Decode hidden text from an image with the correct passphrase
- Check whether an image contains a supported encrypted Steg payload without the passphrase
- Poster-style web interface built with FastAPI, Jinja templates, CSS, and vanilla JavaScript
- Dense architecture fixed as the default processing model in the web app
- Upload normalization and automatic resizing for oversized images

## Quick Start

### 1. Install dependencies

```powershell
pip install -r requirements-web.txt
```

This installs the web app runtime and model dependencies without relying on the legacy editable package setup.

### 2. Start the web app

From the project root:

```powershell
python -m uvicorn webapp.main:app --host 127.0.0.1 --port 8000 --reload
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Run with Docker

Build the image from the project root:

```powershell
docker build -t steg .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 steg
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Optional runtime settings:

- `PORT`: container port to bind Gunicorn to. Default: `8000`
- `WEB_CONCURRENCY`: number of Gunicorn workers. Default: `2`
- `TIMEOUT`: worker timeout in seconds. Default: `120`
- `TORCH_NUM_THREADS`: PyTorch intra-op CPU threads. Default: PyTorch default.
- `TORCH_NUM_INTEROP_THREADS`: PyTorch inter-op CPU threads. Default: PyTorch default.

Example with custom settings:

```powershell
docker run --rm -p 8000:8000 -e WEB_CONCURRENCY=1 -e TIMEOUT=180 -e TORCH_NUM_THREADS=4 -e TORCH_NUM_INTEROP_THREADS=1 steg
```

## Using the Web App

### Encode

1. Upload a source image.
2. Enter the message you want to hide.
3. Enter a passphrase that is at least `12` characters long.
4. Submit the form.
5. Download the generated encoded image from the result panel.

### Decode

1. Upload an image that may contain hidden data.
2. Enter the same passphrase used during encoding.
3. Submit the form.
4. Read the recovered message if decoding succeeds.

### Check

1. Upload an image.
2. Submit the form.
3. Steg will report whether a supported encrypted Steg payload was found.

## Web App Notes

- The web app uses the `dense` architecture for all encode, decode, and check operations.
- Encode and decode require a user-provided passphrase.
- Passphrases must be at least `12` characters long.
- `CHECK` does not require the passphrase and only detects the Steg encrypted payload format.
- Uploaded images are normalized to RGB and resized if their longest side exceeds `2048px`.
- Generated outputs are stored temporarily and are cleaned up automatically after a short retention window.
- The app currently runs model inference on the server process, so very large or frequent requests may still be compute-heavy.
- The model is loaded on startup per worker to avoid per-request load overhead.
- If the passphrase is lost, the hidden message cannot be recovered.

## Project Structure

```text
Steganography/
|-- webapp/                 FastAPI app, templates, static assets, runtime files
|-- steganogan/             Core steganography library and model code
|-- tests/                  Legacy tests and web app tests
|   `-- webapp/             API and service tests for the FastAPI app
|-- training/               Training scripts and notebooks for model work
|-- docs/plans/             Design and implementation planning documents
|-- setup.py                Package metadata and dependencies
`-- README.md               Project overview and usage guide
```

## Developer Usage

The original `steganogan` package is still available if you want to work with the library directly.

### Python API

```python
from steganogan import SteganoGAN

model = SteganoGAN.load(architecture="dense", cuda=False, verbose=False)
model.encode("input.png", "encoded.png", "secret-message")
message = model.decode("encoded.png")
print(message)
```

### CLI

After installation, the package exposes the `steganogan` command:

```powershell
steganogan encode -i input.png -o encoded.png -m "secret-message"
steganogan decode -i encoded.png
```

CLI behavior depends on the original package implementation in [steganogan/cli.py](/C:/Users/USER/Documents/Steganography/steganogan/cli.py).

## Testing

Run the web app test suite with:

```powershell
python -m pytest tests/webapp -v
```

Run the broader test suite with:

```powershell
python -m pytest tests -v
```

The web app suite is the best signal for the FastAPI product. Some legacy tests in the original package may still reflect upstream assumptions and older environment behavior.

## Implementation Overview

The web app lives in [webapp/main.py](/C:/Users/USER/Documents/Steganography/webapp/main.py) and routes requests to [webapp/services.py](/C:/Users/USER/Documents/Steganography/webapp/services.py), which:

- validates uploads
- normalizes and resizes images
- caches the loaded steganography model
- performs encode, decode, and check operations
- manages temporary download outputs

The actual steganography logic comes from [steganogan/models.py](/C:/Users/USER/Documents/Steganography/steganogan/models.py) and related modules in [steganogan](/C:/Users/USER/Documents/Steganography/steganogan).

## Limitations

- The web app is currently fixed to the `dense` model architecture.
- The web app only supports the new passphrase-protected Steg payload format and does not decode legacy plaintext payloads.
- The decode and check paths still rely on the upstream library's decode-failure behavior for plain images with no hidden message.
- The original project has older package constraints and research-oriented training code that may need modernization for newer Python and PyTorch stacks.

## License

This project inherits the original MIT licensing from the upstream SteganoGAN package. See the package metadata in [setup.py](/C:/Users/USER/Documents/Steganography/setup.py).
