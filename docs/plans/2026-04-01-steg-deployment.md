# Steg Deployment Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a production-ready Docker deployment path for the Steg FastAPI web app using Gunicorn with Uvicorn workers.

**Architecture:** The container should install a deployment-specific dependency set, copy the repository into the image, and run `webapp.main:app` behind Gunicorn with Uvicorn workers. This avoids the current `setup.py` packaging issues while keeping the runtime simple and portable.

**Tech Stack:** Docker, Python, FastAPI, Gunicorn, Uvicorn, Jinja2, PyTorch

---

### Task 1: Add Deployment Dependency Manifest

**Files:**
- Create: `C:/Users/USER/Documents/Steganography/requirements-web.txt`

**Step 1: Verify the deployment manifest does not exist yet**

Run:

```powershell
Test-Path 'C:\Users\USER\Documents\Steganography\requirements-web.txt'
```

Expected: `False`

**Step 2: Create the deployment dependency file**

Add a focused runtime dependency list that includes:

```text
fastapi>=0.110,<1.0
gunicorn>=21.2,<22.0
uvicorn>=0.29,<1.0
jinja2>=3.1,<4.0
python-multipart>=0.0.9,<1.0
pillow>=10.0,<11.0
numpy>=1.26,<3.0
scipy>=1.11,<2.0
imageio>=2.34,<3.0
reedsolo==0.3
tqdm>=4.66,<5.0
torch
torchvision
```

**Step 3: Review the file for deployment scope only**

Confirm it includes web runtime and model dependencies, but does not depend on editable installation via `setup.py`.

**Step 4: Commit**

```bash
git add requirements-web.txt
git commit -m "chore: add web deployment requirements"
```

### Task 2: Add Docker Context Exclusions

**Files:**
- Create: `C:/Users/USER/Documents/Steganography/.dockerignore`

**Step 1: Verify the file does not exist yet**

Run:

```powershell
Test-Path 'C:\Users\USER\Documents\Steganography\.dockerignore'
```

Expected: `False`

**Step 2: Create the Docker ignore file**

Add exclusions for:

```text
.git
.gitignore
.pytest_cache
.playwright-cli
.omx
__pycache__/
*.py[cod]
*.log
docs/plans
tests
training
output
webapp/runtime
```

**Step 3: Review the ignore list**

Confirm it excludes local artifacts and non-runtime directories without excluding `webapp`, `steganogan`, or root project files required for the app.

**Step 4: Commit**

```bash
git add .dockerignore
git commit -m "chore: add docker ignore rules"
```

### Task 3: Add Production Dockerfile

**Files:**
- Create: `C:/Users/USER/Documents/Steganography/Dockerfile`

**Step 1: Verify Docker build currently fails because no Dockerfile exists**

Run:

```powershell
docker build -t steg:test 'C:\Users\USER\Documents\Steganography'
```

Expected: FAIL because `Dockerfile` is missing

**Step 2: Create the Dockerfile**

Add a production Dockerfile along these lines:

```dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV WEB_CONCURRENCY=2
ENV TIMEOUT=120

WORKDIR /app

COPY requirements-web.txt /app/requirements-web.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements-web.txt

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "gunicorn webapp.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT} --workers ${WEB_CONCURRENCY} --timeout ${TIMEOUT}"]
```

**Step 3: Build the image**

Run:

```powershell
docker build -t steg:test 'C:\Users\USER\Documents\Steganography'
```

Expected: PASS with a successfully tagged local image

**Step 4: Run the container**

Run:

```powershell
docker run --rm -d --name steg-test -p 8000:8000 steg:test
```

Expected: container starts successfully

**Step 5: Verify the home page responds**

Run:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8000/' | Select-Object -ExpandProperty StatusCode
```

Expected: `200`

**Step 6: Stop the test container**

Run:

```powershell
docker stop steg-test
```

Expected: container stops cleanly

**Step 7: Commit**

```bash
git add Dockerfile
git commit -m "feat: add production dockerfile"
```

### Task 4: Document Docker Usage

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/README.md`

**Step 1: Add a Docker section**

Document:

- how to build the image
- how to run the container
- the default port
- optional environment variables such as `PORT`, `WEB_CONCURRENCY`, and `TIMEOUT`

Suggested commands:

```powershell
docker build -t steg .
docker run --rm -p 8000:8000 steg
```

**Step 2: Review the README flow**

Make sure the Docker instructions sit near the Quick Start section and read cleanly for a web-app-first audience.

**Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add docker deployment instructions"
```

### Task 5: Final Verification

**Files:**
- Verify: `C:/Users/USER/Documents/Steganography/Dockerfile`
- Verify: `C:/Users/USER/Documents/Steganography/.dockerignore`
- Verify: `C:/Users/USER/Documents/Steganography/requirements-web.txt`
- Verify: `C:/Users/USER/Documents/Steganography/README.md`

**Step 1: Build the final image fresh**

Run:

```powershell
docker build --no-cache -t steg:final 'C:\Users\USER\Documents\Steganography'
```

Expected: PASS

**Step 2: Run the final container**

Run:

```powershell
docker run --rm -d --name steg-final -p 8000:8000 steg:final
```

Expected: container starts successfully

**Step 3: Verify the app responds**

Run:

```powershell
Invoke-WebRequest -Uri 'http://127.0.0.1:8000/' | Select-Object StatusCode, StatusDescription
```

Expected: `200 OK`

**Step 4: Verify logs are clean enough to serve requests**

Run:

```powershell
docker logs steg-final
```

Expected: Gunicorn/Uvicorn startup logs without fatal import or dependency errors

**Step 5: Stop the final container**

Run:

```powershell
docker stop steg-final
```

Expected: container stops cleanly

**Step 6: Commit**

```bash
git add Dockerfile .dockerignore requirements-web.txt README.md
git commit -m "chore: prepare steg for container deployment"
```
