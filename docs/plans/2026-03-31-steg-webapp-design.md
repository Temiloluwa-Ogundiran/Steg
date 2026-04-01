# Steg Webapp Design

**Date:** 2026-03-31

## Goal

Build **Steg**, a FastAPI-based web application for the existing steganography project. The app should let users:

- encode a message into an image
- download the encoded image
- decode a message from an image
- check whether an image contains hidden data

The UI should be a dedicated tool interface rather than a marketing landing page, and it should follow a poster-modernist visual system inspired by the provided references.

## Product Decisions

- Frontend approach: FastAPI-rendered pages with HTML/CSS and lightweight JavaScript.
- Product shape: a dedicated tool interface, not a separate marketing site.
- Hidden-data check behavior: strict yes/no based on whether a valid message can be recovered.
- Model controls: expose architecture selection to users with `basic`, `dense`, and `residual`.

## Experience Direction

The interface should feel technical, editorial, and structured rather than decorative. The page will use:

- a strict 12-column grid
- cream background (`#E3E2DE`)
- black primary text (`#141414`)
- cobalt accent (`#1351AA`)
- thin gray borders (`#C7C7C7`)
- high-contrast sans-serif typography with oversized headlines
- zero-radius controls and flat surfaces
- sticky sidebar labels for major sections

The result should feel like a product workspace built from a design system, not a generic SaaS dashboard.

## Layout

### Top Bar

- 80px tall sticky navigation bar
- left: `STEG`
- center: system/version or status text
- right: compact utility/status area
- 1px bottom border and lightly translucent cream background

### Main Workspace

The first viewport should act like a poster-style tool surface:

- large headline with one cobalt-highlighted word
- a short supporting paragraph explaining the tool
- mode switcher for `ENCODE`, `DECODE`, and `CHECK`
- the active tool displayed immediately beneath the headline

### Grid Structure

- columns 1-3: metadata/sidebar labels
- columns 4-12: primary content
- horizontal rules separate major areas
- labels such as `WORKSPACE`, `INPUT`, `PAYLOAD`, and `RESULT` stay visible as structural anchors

## Feature Flows

### Encode

User flow:

1. Upload a cover image.
2. Select architecture: `basic`, `dense`, or `residual`.
3. Enter the message to hide.
4. Submit the form.
5. View the encoded image preview.
6. Download the generated image.

Expected output:

- success message
- image preview
- file metadata where helpful
- download action for the generated image

### Decode

User flow:

1. Upload an image.
2. Select architecture.
3. Submit the form.
4. View the recovered message or a controlled failure state.

Expected output:

- recovered text in a prominent result panel
- clear failure message if decoding fails

### Check

User flow:

1. Upload an image.
2. Select architecture.
3. Submit the form.
4. Receive a strict binary result.

Expected output:

- `HIDDEN DATA FOUND` only when a valid message can actually be recovered
- otherwise `NO HIDDEN DATA FOUND`

This feature should not expose heuristic confidence scores.

## Backend Design

The web application will wrap the existing `SteganoGAN` package rather than replacing any steganography logic.

### FastAPI Responsibilities

- render the main page
- accept uploaded files
- validate image inputs
- call the model service for encode/decode/check operations
- return structured JSON for interactive updates
- stream generated files for download

### Planned Routes

- `GET /`: render the application shell
- `POST /api/encode`: upload image, message, and architecture; return encoded result metadata and download URL
- `GET /api/download/{id}`: download generated encoded image
- `POST /api/decode`: upload image and architecture; return recovered message
- `POST /api/check`: upload image and architecture; return strict yes/no hidden-data result

### Service Layer

A dedicated service module should:

- cache loaded pretrained models by architecture
- write uploads to temporary files
- call the existing `SteganoGAN.load`, `encode`, and `decode` methods
- encapsulate strict check logic by attempting a real decode
- manage output file retention and cleanup

## Frontend Design

The frontend should use server-rendered HTML with static CSS and a small JavaScript layer for interaction.

### JavaScript Responsibilities

- switch between modes
- preview selected filenames or images where useful
- submit forms with `fetch`
- render success, negative, and error states inline
- update the result panel without a full page reload

### Visual Components

- poster-style mode switcher
- file input blocks with strong labels
- architecture selector
- message textarea for encode
- output rail for result states
- download button with hard rectangular treatment

## Error Handling

Errors should be explicit and controlled rather than decorative.

Examples:

- unreadable image: explain that the file could not be processed
- missing encode message: block submission or return a precise validation error
- decode failure: report that no valid message was found
- backend failure: return a concise technical error without exposing a traceback

## Testing Strategy

The implementation should include:

- FastAPI route tests for page rendering and API endpoints
- service-layer tests for model selection, temp-file handling, and strict check behavior
- frontend smoke tests for mode switching and result rendering
- browser-based verification of the main workflows after implementation

## Constraints and Notes

- The repo currently contains the core steganography library but no web stack yet.
- The existing project directory is not currently a Git repository in this environment, so any commit step is blocked unless the repo metadata is restored elsewhere.
- The current package already includes pretrained model loading, which should be reused for the app.

