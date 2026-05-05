# Steg Final Year Report Design

**Date:** 2026-04-12

## Summary

Revise the existing final year project report so it accurately presents the work as an original secure steganography software suite, not as a wrapper or adaptation of another repository. The completed report must extend from the current partial draft through Chapters Three, Four, and Five, while also correcting and aligning Chapters One and Two with the actual system that was built.

## Core Positioning

The report should frame the project as:

- an original secure steganography software suite
- focused on resilient hidden communication in digital images
- using adversarial-network-based image steganography as the core embedding strategy
- strengthened with software-level security controls, especially passphrase-protected decoding
- evaluated against conventional steganography approaches that are less effective against modern steganalysis

SteganoGAN and its paper should be treated only as scholarly and technical references that informed the project, not as the identity of the project itself.

## Editorial Goals

The revised report must:

- preserve the current citation style already used in the document
- retain the student's general writing voice while improving technical accuracy, coherence, and scholarly quality
- align every chapter with the implemented Steg system
- be strong enough in structure, explanation, and evaluation to support journal-quality refinement later

## Chapter-Level Design

### Chapter One: Introduction

This chapter must be revised so that:

- the background reflects the evolution from classical steganography to steganalysis-aware deep learning methods
- the statement of problem focuses on the lack of practical secure software suites that combine modern steganographic embedding with usable security controls
- the aim and objectives are clearly measurable
- the methodology reflects the actual design, implementation, testing, and evaluation workflow
- significance, scope, and chapter outline match the final system

### Chapter Two: Literature Review

This chapter should retain its broad review purpose but be tightened to:

- compare classical spatial-domain and transform-domain methods
- explain steganalysis, especially machine-learning-based steganalysis
- discuss GAN-based or adversarial steganography as a response to stronger detectors
- review practical tools and systems
- identify the research gap that motivates the proposed secure software suite

It should explicitly compare adversarial-network-based steganography with weaker conventional methods such as:

- Least Significant Bit substitution
- transform-domain methods such as DCT/JPEG-based embedding
- traditional steganography tools such as OpenStego and Steghide where relevant

### Chapter Three: System Analysis and Design

This chapter should follow the stronger FYP patterns seen in the provided examples and include:

- preamble
- overview of the system
- requirements analysis
- functional requirements
- non-functional requirements
- dataset description
- physical/system architecture
- logical design
- use case / activity / sequence flow
- security design
- mathematical formulation and evaluation metrics

The design must reflect the actual Steg application:

- web frontend
- FastAPI backend
- image encode/decode/check workflow
- passphrase-protected payload handling
- runtime flow between input image, secure payload envelope, embedding, extraction, and validation

### Chapter Four: System Implementation and Evaluation

This chapter should present:

- hardware and software requirements
- implementation tools
- dataset preparation
- training/deployment context where relevant
- application modules and interfaces
- evaluation setup
- results and discussion
- comparison with traditional methods

The results section should include:

- image quality metrics
- security and detection discussion
- comparative tables
- screenshots and figures where useful

### Chapter Five: Summary, Recommendations and Conclusion

This chapter should conclude the project with:

- summary
- recommendations
- conclusion
- limitations and future work if needed by departmental convention

## Use of Sources

The following sources should inform the final report:

- the current report draft
- the original SteganoGAN paper in [1901.03892v2.pdf](/C:/Users/USER/Documents/Steganography/report/1901.03892v2.pdf)
- the official SteganoGAN documentation and repository as technical references
- the two previous final year reports for chapter organization and academic style expectations
- the actual codebase and implemented Steg web application
- the dataset acquisition notes supplied by the user for DIV2K and MSCOCO

## Figures and Formulae

Use figures and formulas where they add academic value, especially:

- system architecture diagram
- workflow diagram for encode/decode/check
- use case or activity diagram
- dataset or module illustration if useful
- equations for MSE, PSNR, SSIM, and related evaluation measures
- tables comparing adversarial steganography to classical methods

## Style Guidance

The final writing should:

- stay close to the student's existing voice
- reduce repetition and awkward phrasing
- avoid sounding copied from papers or generated from disconnected sources
- read as one coherent report written by a single author

## Deliverable

The final artifact should be an updated version of:

[SECURE STEGANOGRAPHY SOFTWARE SUITE RESILIENT TO STEGANALYSIS (OGUNDIRAN)  (Repaired).docx](/C:/Users/USER/Documents/Steganography/report/SECURE%20STEGANOGRAPHY%20SOFTWARE%20SUITE%20RESILIENT%20TO%20STEGANALYSIS%20%28OGUNDIRAN%29%20%20%28Repaired%29.docx)

with revised Chapters One and Two and completed Chapters Three, Four, and Five.
