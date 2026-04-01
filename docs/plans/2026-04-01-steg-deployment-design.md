# Steg Deployment Design

**Date:** 2026-04-01

## Summary

Prepare Steg for container-based deployment by adding a production-oriented Docker setup for the FastAPI web app. The deployment target is a single container that runs the app behind Gunicorn with Uvicorn workers.

## Chosen Approach

Use one production container with:

- a Python slim base image
- Gunicorn as the process manager
- `uvicorn.workers.UvicornWorker` for serving the FastAPI app
- a deployment-specific Python requirements file instead of `pip install -e .`

This avoids being blocked by the repository's current packaging issues while keeping deployment simple for container hosts.

## Why This Approach

This repository mixes a legacy Python package and a newer FastAPI web app. The web app is the product surface we want to deploy, but the root packaging is not deployment-safe yet because:

- [setup.py](/C:/Users/USER/Documents/Steganography/setup.py) still expects a missing `HISTORY.md`
- [setup.py](/C:/Users/USER/Documents/Steganography/setup.py) includes an old malformed `numpy` version constraint

Using a clean runtime requirements file keeps deployment focused on the app that actually needs to run.

## Deployment Shape

The container will:

- start [webapp/main.py](/C:/Users/USER/Documents/Steganography/webapp/main.py)
- bind to `0.0.0.0`
- expose port `8000`
- accept environment-driven runtime settings such as `PORT`, `WEB_CONCURRENCY`, and `TIMEOUT`
- keep temporary upload/output files inside the container's existing runtime directories under [webapp](/C:/Users/USER/Documents/Steganography/webapp)

## Files To Add

- `Dockerfile`
- `.dockerignore`
- `requirements-web.txt`

## Files To Update

- [README.md](/C:/Users/USER/Documents/Steganography/README.md)

## Runtime Dependencies

The deployment requirements file should include the packages needed to run:

- FastAPI
- Gunicorn
- Uvicorn
- Jinja2
- python-multipart
- Pillow
- PyTorch
- torchvision
- imageio
- reedsolo
- scipy
- tqdm
- numpy

## Scope

### In Scope

- add a production Dockerfile
- add a `.dockerignore`
- add a deployment-oriented Python requirements file
- document Docker build and run usage in the README

### Out of Scope

- rewriting the legacy package metadata
- adding Docker Compose
- adding Nginx or another reverse proxy
- changing the FastAPI architecture
- changing the steganography model behavior

## Verification

Deployment prep should be verified by:

1. building the Docker image locally
2. starting the container locally
3. opening the app in a browser
4. confirming the home page loads successfully
5. optionally exercising one app flow after startup

## Notes

- The app currently performs inference in-process, so worker count should stay modest unless runtime characteristics are measured.
- Container hosts with ephemeral filesystems are acceptable because generated downloads are already temporary.
