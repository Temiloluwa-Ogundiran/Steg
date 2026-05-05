from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from webapp import services
from webapp.config import PASSPHRASE_MIN_LENGTH
from webapp.config import (
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    DEFAULT_ARCHITECTURE,
    STATIC_DIR,
    TEMPLATE_DIR,
)

app = FastAPI(title=APP_TITLE, version=APP_VERSION, description=APP_DESCRIPTION)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "app_title": APP_TITLE,
            "app_version": APP_VERSION,
            "default_architecture": DEFAULT_ARCHITECTURE,
        },
    )


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.post("/api/encode")
async def encode_image(
    image: UploadFile = File(...),
    message: str = Form(...),
    passphrase: str | None = Form(None),
):
    if not message or not message.strip():
        raise HTTPException(status_code=400, detail="Message is required for encoding.")
    if not passphrase or not passphrase.strip():
        raise HTTPException(status_code=400, detail="Passphrase is required for encoding.")
    if len(passphrase.strip()) < PASSPHRASE_MIN_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Passphrase must be at least {PASSPHRASE_MIN_LENGTH} characters for encoding.",
        )

    try:
        return services.encode_image(
            architecture=DEFAULT_ARCHITECTURE,
            filename=image.filename or "image.png",
            upload=image,
            message=message,
            passphrase=passphrase,
        )
    except services.ServiceValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except services.ProcessingError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        await image.close()


@app.post("/api/decode")
async def decode_image(
    image: UploadFile = File(...),
    passphrase: str | None = Form(None),
):
    if not passphrase or not passphrase.strip():
        raise HTTPException(status_code=400, detail="Passphrase is required for decoding.")
    if len(passphrase.strip()) < PASSPHRASE_MIN_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Passphrase must be at least {PASSPHRASE_MIN_LENGTH} characters for decoding.",
        )

    try:
        return services.decode_image(
            architecture=DEFAULT_ARCHITECTURE,
            filename=image.filename or "image.png",
            upload=image,
            passphrase=passphrase,
        )
    except services.ServiceValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except services.ProcessingError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        await image.close()


@app.post("/api/check")
async def check_image(
    image: UploadFile = File(...),
):
    try:
        return services.check_image(
            architecture=DEFAULT_ARCHITECTURE,
            filename=image.filename or "image.png",
            upload=image,
        )
    except services.ServiceValidationError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except services.ProcessingError as error:
        raise HTTPException(status_code=500, detail=str(error)) from error
    finally:
        await image.close()


@app.get("/api/download/{output_id}")
def download_image(output_id: str):
    try:
        output_path = services.get_output_path(output_id)
    except services.OutputNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    return FileResponse(output_path, filename=output_path.name)
