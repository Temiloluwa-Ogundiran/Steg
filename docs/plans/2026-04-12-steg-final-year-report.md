# Steg Final Year Report Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Complete and revise the final year project report so it accurately presents Steg as an original secure steganography software suite and extends the document through Chapter Five.

**Architecture:** The work should proceed in two layers: first extract and analyze the existing report, example FYP documents, original paper, and implemented codebase; then rewrite Chapters One and Two and author Chapters Three to Five in the report’s existing citation style and adapted student voice. The final output must be a polished `.docx` document with proper structure, figures/tables/formulae where necessary, and consistent academic formatting.

**Tech Stack:** DOCX editing, python-docx, PDF/document extraction, repository analysis, academic technical writing

---

### Task 1: Extract Structure, Voice, and Source Material

**Files:**
- Read: `C:/Users/USER/Documents/Steganography/report/SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx`
- Read: `C:/Users/USER/Documents/Steganography/report/example1.docx`
- Read: `C:/Users/USER/Documents/Steganography/report/example2.docx`
- Read: `C:/Users/USER/Documents/Steganography/report/1901.03892v2.pdf`
- Read: `C:/Users/USER/Documents/Steganography/README.md`
- Read: `C:/Users/USER/Documents/Steganography/webapp/main.py`
- Read: `C:/Users/USER/Documents/Steganography/webapp/services.py`

**Step 1: Extract the current report outline and sample prose**

Capture:

- current chapter headings
- current subsections
- representative writing samples from Chapters One and Two
- citation patterns already in use

**Step 2: Extract the chapter pattern from previous FYPs**

Identify the expected structure for:

- Chapter Three
- Chapter Four
- Chapter Five

**Step 3: Extract technical evidence from the codebase and SteganoGAN paper**

Build notes for:

- actual system architecture
- implemented features
- security model
- dataset usage
- evaluation metrics
- relevant formulas and comparisons

**Step 4: Write a working outline**

Produce a concrete section map for revised Chapter One, revised Chapter Two, and new Chapters Three to Five.

**Step 5: Commit**

```bash
git add notes-or-plan-files-if-created
git commit -m "docs: map report structure and source material"
```

### Task 2: Revise Chapter One to Match the Actual Project

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/report/SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx`

**Step 1: Rewrite the chapter sections**

Revise:

- Background Information
- Statement of Problem
- Aim and Objectives
- Methodology
- Significance of the Study
- Chapter Outline

The rewrite must:

- remove wording that implies the project is a wrapper or reproduction
- frame the work as an original secure software suite
- align objectives with the actual system and evaluation

**Step 2: Keep citation style consistent**

Preserve the in-text citation style already present in the document.

**Step 3: Review for voice consistency**

Match the student’s tone while tightening technical accuracy and academic flow.

**Step 4: Save and visually inspect the revised chapter**

Render or inspect the document to ensure formatting remains intact.

**Step 5: Commit**

```bash
git add report/"SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx"
git commit -m "docs: revise chapter one for final report"
```

### Task 3: Revise Chapter Two with Stronger Comparative Literature Framing

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/report/SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx`

**Step 1: Rewrite the literature framing**

Revise Chapter Two so it clearly covers:

- cryptography
- steganography
- spatial-domain techniques
- transform-domain techniques
- steganalysis
- machine learning in steganalysis
- adversarial/GAN-based steganography
- review of tools and systems
- research gaps
- proposed system

**Step 2: Strengthen the comparison with conventional methods**

Add a clear comparison between:

- adversarial-network-based image steganography
- LSB-based methods
- transform-domain/JPEG/DCT methods
- traditional tool-based workflows such as OpenStego and Steghide where appropriate

**Step 3: Align the proposed system section with the actual Steg implementation**

Make sure the chapter leads naturally into the design of the secure software suite.

**Step 4: Save and visually inspect**

Review chapter formatting after revision.

**Step 5: Commit**

```bash
git add report/"SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx"
git commit -m "docs: strengthen chapter two literature review"
```

### Task 4: Write Chapter Three - System Analysis and Design

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/report/SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx`

**Step 1: Add Chapter Three structure**

Write sections such as:

- Preamble
- Overview of the System
- Requirements Analysis
- Functional Requirements
- Non-Functional Requirements
- Dataset Description
- Physical Design / System Architecture
- Logical Design
- Security Design
- Summary

**Step 2: Add technical diagrams and tables where necessary**

Include or prepare:

- system architecture diagram
- workflow diagram
- requirements table

**Step 3: Add formulas and explanatory technical content**

Where relevant, include formulas for:

- MSE
- PSNR
- SSIM
- embedding capacity or related metrics

**Step 4: Visually inspect the chapter layout**

Ensure headings, spacing, tables, and equations render cleanly.

**Step 5: Commit**

```bash
git add report/"SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx"
git commit -m "docs: add chapter three system analysis and design"
```

### Task 5: Write Chapter Four - Implementation and Evaluation

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/report/SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx`

**Step 1: Add implementation sections**

Write:

- Preamble
- System Requirements
- Hardware Requirements
- Software Requirements
- Implementation Tools
- Program Modules and Interfaces

**Step 2: Add evaluation design**

Document:

- dataset preparation using DIV2K and MSCOCO
- experimental setup
- evaluation metrics
- baseline comparison strategy

**Step 3: Write comparative evaluation**

Compare the adversarial-network method with traditional approaches in terms of:

- imperceptibility
- resistance to steganalysis
- payload security
- practical usability

**Step 4: Add screenshots, tables, and discussion**

Use the actual Steg interface and implementation evidence where relevant.

**Step 5: Visually inspect the chapter**

Re-render and check pagination, figure placement, and tables.

**Step 6: Commit**

```bash
git add report/"SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx"
git commit -m "docs: add chapter four implementation and evaluation"
```

### Task 6: Write Chapter Five - Summary, Recommendations, and Conclusion

**Files:**
- Modify: `C:/Users/USER/Documents/Steganography/report/SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx`

**Step 1: Write the closing chapter**

Include:

- Summary
- Recommendations
- Conclusion

Optionally include limitations or future work if they fit the faculty pattern and existing report style.

**Step 2: Ensure the conclusion matches the actual contributions**

The conclusion must reflect:

- secure passphrase-protected message workflow
- adversarial-network-based embedding approach
- comparison with weaker traditional methods
- practical software delivery as a suite

**Step 3: Visually inspect the final chapter**

Confirm formatting and continuity.

**Step 4: Commit**

```bash
git add report/"SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx"
git commit -m "docs: add chapter five conclusion sections"
```

### Task 7: Final Document Review and Rendering

**Files:**
- Verify: `C:/Users/USER/Documents/Steganography/report/SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx`

**Step 1: Perform a full document review**

Check:

- chapter numbering
- heading consistency
- table and figure references
- citation consistency
- tone consistency
- grammar and academic flow

**Step 2: Render and inspect the document**

Use the DOCX workflow to render pages and inspect layout visually.

**Step 3: Fix final formatting defects**

Correct any pagination, spacing, or table/figure issues found during rendering.

**Step 4: Produce the final deliverable**

Save the updated document in place or to a clearly named final copy if needed.

**Step 5: Commit**

```bash
git add report/"SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx"
git commit -m "docs: finalize full final year report"
```
