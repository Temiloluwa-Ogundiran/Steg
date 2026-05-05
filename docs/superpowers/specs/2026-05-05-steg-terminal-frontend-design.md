# Steg Terminal UI Design Spec

**Date:** 2026-05-05
**Topic:** steg-terminal-frontend-redesign
**Approach:** A — Segmented Mode Grid + Terminal Results

---

## Overview

Replace the current poster-style Steg web interface with a stark, utilitarian terminal-aesthetic design. The goal is to reduce on-screen text, increase information density, and create a developer-first workspace that feels fast and focused.

---

## Style System

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--bg-primary` | `#111111` | Page background |
| `--bg-terminal` | `#050505` | Right sidebar background |
| `--bg-surface` | `#1A1A1A` | Hover states, subtle elevation |
| `--border` | `#333333` | All borders, dividers |
| `--text-title` | `#FFFFFF` | Headings, active mode text |
| `--text-body` | `#E5E5E5` | Body text, filenames |
| `--text-muted` | `#555555` | Labels, disabled states, line numbers |
| `--accent-success` | `#4ADE80` | Success states, listening indicator |
| `--accent-error` | `#F87171` | Error states |
| `--accent-warn` | `#FACC15` | Processing / pending states |
| `--accent-purple` | `#C084FC` | Terminal keywords |
| `--accent-blue` | `#60A5FA` | Terminal variables |
| `--accent-green-light` | `#BBF7D0` | Terminal strings |

### Typography

| Role | Font | Weight | Size | Transform |
|---|---|---|---|---|
| H1 (Brand) | Space Grotesk | 700 | 24px | uppercase |
| H2 (Section) | JetBrains Mono | 700 | 10px | uppercase |
| Body | JetBrains Mono | 400 | 12px | none |
| Button | Space Grotesk | 700 | 12px | uppercase |
| Terminal | JetBrains Mono | 400 | 11px | none |
| Terminal Header | JetBrains Mono | 400 | 10px | uppercase |
| Metrics | JetBrains Mono | 400 | 10px | none |

### Effects & Grid

- **Background grid:** 40px × 40px, 1px lines at `rgba(255,255,255,0.03)`, masked with bottom fade
- **Border radius:** `0px` everywhere — no exceptions
- **Cursor:** `crosshair` globally
- **Transitions:** `0.05s linear` or none. Mechanical, instant state changes
- **Shadows / gradients:** None. Depth achieved through borders and hex color shifts only

---

## Layout

### Two-Pane Structure

```
+--------------------------------------------------+
| HEADER                                           |
| [■] STEG v0.1.0 [BUILD 001]        // SYSTEM READY |
+--------------------------------+-----------------+
| MAIN WORKSPACE                 | TERMINAL (340px) |
|                                |                  |
| STEG                           | TERMINAL // :8000|
| // Hide signal. Reveal truth.  | ● LISTENING      |
|                                |                  |
| 01 // MODE                     | [syntax output]  |
| [ENCODE][DECODE][CHECK]        |                  |
|                                |                  |
| 02 // INPUT                    |                  |
| [FILE] cover.png     8x8 PX    |                  |
|                                |                  |
| 03 // PAYLOAD                  |                  |
| Enter hidden message...        |                  |
|                                |                  |
| 04 // KEY                      |                  |
| ••••••••••••                   |                  |
|                                |                  |
|                    [EXECUTE >] |                  |
|                                |                  |
+--------------------------------+-----------------+
```

### Header

- Compressed height (~40px)
- `#333333` bottom border
- Left cluster: 8px white square + version string in 10px mono uppercase
- Right cluster: `// SYSTEM READY` in 10px mono `#555555`

### Main Workspace (left, flex:1)

#### Brand Block
- H1: `STEG` — Space Grotesk 24px, weight 700, uppercase, letter-spacing `-0.02em`
- Subline: `// Hide signal. Reveal truth.` — JetBrains Mono 10px, `#555555`

#### 01 // MODE — Segmented Calibration Grid
- Section label: `01 // MODE` — 10px mono uppercase, `#555555`
- Grid: 3 equal columns, 1px `#333333` borders
- Each segment: 10px uppercase mono text, centered, padding `12px`
- **Inactive:** bg `#111111`, text `#555555`
- **Hover:** bg `#1A1A1A`, text `#E5E5E5`
- **Active:** bg `#FFFFFF`, text `#000000`, font-weight 700
- Internal borders: `1px solid #333333`

#### 02 // INPUT — File Field
- Section label: `02 // INPUT`
- Container: `1px solid #333333`, padding `12px`, flex row
- Content: `[FILE]` prefix (mono, `#555555`) + filename (mono, `#E5E5E5`) + dimensions (mono, `#555555`, right-aligned)
- Hidden native `<input type="file">` triggered by click on container

#### 03 // PAYLOAD — Textarea
- Section label: `03 // PAYLOAD`
- Visible only in **Encode** mode
- Container: `1px solid #333333`, padding `12px`, min-height `120px`
- Textarea: no border, bg transparent, color `#E5E5E5`, placeholder `#555555`

#### 04 // KEY — Passphrase
- Section label: `04 // KEY`
- Visible in **Encode** and **Decode** modes
- Container: `1px solid #333333`, padding `12px`
- Input: `type="password"`, no border, bg transparent, color `#E5E5E5`

#### Action Footer
- Right-aligned within main workspace
- Button: `EXECUTE >`
  - bg `#FFFFFF`, text `#000000`
  - Space Grotesk 12px, weight 700, uppercase
  - Padding `12px 24px`
  - No border radius
  - Hover: bg `#E5E5E5`
  - Active/pressed: bg `#CCCCCC`

### Terminal Sidebar (right, 340px fixed)

- Background: `#050505`
- Left border: `1px solid #333333`
- Padding: `16px`
- Display: flex column

#### Terminal Header
- Flex row, space-between
- Left: `TERMINAL // :8000` — 10px mono uppercase, `#555555`
- Right: `● LISTENING` — 10px mono, `#4ADE80`, pulsing dot

#### Terminal Body
- Flex:1, overflow-y: auto
- Line numbers: `#333333`, 10px mono, right-aligned, min-width `24px`
- Content lines: 11px mono

**Syntax highlighting rules:**

| Context | Color | Example |
|---|---|---|
| Comments | `#555555` | `// Awaiting input...` |
| Keywords | `#C084FC` | `ERROR`, `SUCCESS`, `STATUS` |
| Strings | `#BBF7D0` | decoded message text |
| Variables | `#60A5FA` | `download_url`, `message` |
| Prompt | `#FACC15` | `>` |
| Error values | `#F87171` | error details |

**State outputs:**

- **Idle:**
  ```
  01  // Awaiting input...
  02  
  03  Select mode and submit.
  ```

- **Processing:**
  ```
  01  > Processing request...
  02  
  03  architecture: dense
  04  mode: encode
  ```

- **Encode Success:**
  ```
  01  STATUS ok
  02  download_url: "/api/download/abc123"
  03  filename: "steg-cover.png"
  04  
  05  [image preview rendered here]
  ```

- **Decode Success:**
  ```
  01  STATUS ok
  02  message: "the secret text"
  03  architecture: dense
  ```

- **Check Result:**
  ```
  01  STATUS ok
  02  hidden_data: true
  03  architecture: dense
  ```

- **Error:**
  ```
  01  ERROR Processing halted.
  02  
  03  Invalid passphrase or corrupted payload.
  ```

#### Terminal Footer
- Border-top: `1px solid #333333`
- Padding-top: `8px`
- Flex row, space-between
- Content: `RAM: --%` / `CPU: --%` — 10px mono, `#555555`
- (Static placeholder for now; no live system metrics)

---

## Interaction States

### Mode Switching
- Clicking a mode segment instantly swaps the visible form
- No transition animation
- Active segment receives white bg + black text immediately
- Form fields that don't apply to the selected mode are hidden (`display:none`)

### File Selection
- Clicking the input container triggers hidden file input
- On selection: filename and dimensions replace placeholder text
- File type validation happens server-side; no client-side preview beyond filename

### Form Submission
- Button text changes to `PROCESSING...` (no spinner, text-only)
- Button disabled during processing
- Terminal body clears and shows processing state immediately
- On completion: terminal updates to result state
- On error: terminal updates to error state

### Result States

| State | Terminal Output | Sidebar BG |
|---|---|---|
| Idle | Gray comment | `#050505` |
| Processing | Yellow prompt + vars | `#050505` |
| Encode success | Green strings + preview | `#050505` |
| Decode success | Green plain text | `#050505` |
| Check found | Green `true` | `#050505` |
| Check missing | Gray `false` | `#050505` |
| Error | Red keywords + details | `#050505` |

---

## Responsive Behavior

### Breakpoint: < 900px

- Two-pane collapses to single column
- Terminal sidebar drops below main workspace, full width
- Mode grid stays horizontal (3 columns)
- All padding reduces by ~30%

### Breakpoint: < 480px

- Mode grid stacks vertically (1 column per mode)
- Section labels remain visible
- Terminal sidebar scrolls independently if needed

---

## Component Inventory

| Component | File | Notes |
|---|---|---|
| Global styles | `styles.css` | Grid background, tokens, resets |
| App logic | `app.js` | Mode switching, form handling, terminal rendering |
| Main template | `index.html` | Jinja2 template, all markup |

No new dependencies. Uses existing FastAPI + Jinja2 + vanilla JS stack.

---

## Text Reduction Plan

Current UI has ~30 visible text elements (labels, descriptions, helper copy). New UI reduces to ~12:

- **Removed:** All descriptive paragraphs, architecture static fields, "If passphrase is lost" warning, mode panel headers, result panel copy
- **Kept:** Section labels (`01 // MODE`, etc.), button labels, terminal output, minimal placeholders
- **Replaced:** Result panel with terminal syntax output

---

## Assets

- **Fonts:** Space Grotesk (Google Fonts), JetBrains Mono (Google Fonts)
- **Icons:** None required. Uses ASCII/terminal symbols: `>`, `//`, `●`, `[`, `]`
- **Images:** No external images. Favicon can be a data-URI SVG square.

---

## Accessibility Notes

- Mode segments are `<button>` elements with `aria-pressed`
- File input has associated `<label>` via `for` attribute
- Terminal output uses `aria-live="polite"` region for screen readers
- Color is not the sole indicator of state (text content differs per state)
- Focus states: `outline: 1px solid #FFFFFF` on all interactive elements

---

## Out of Scope

- Live RAM/CPU metrics (static placeholder)
- Real-time websocket terminal (HTTP polling/fetch only)
- Dark/light mode toggle (terminal aesthetic is permanently dark)
- Custom scrollbar styling (use browser default)
