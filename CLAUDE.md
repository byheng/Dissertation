# CLAUDE.md

## Build & Compile
The project uses `artratex.sh` (macOS/Linux) or `artratex.bat` (Windows) for compilation.

- **Check Usage:** `./artratex.sh`
- **XeLaTeX + BibTeX (Recommended):** `./artratex.sh xa Thesis.tex`
- **PDFLaTeX + BibTeX:** `./artratex.sh pa Thesis.tex`
- **LuaLaTeX + Biber:** `./artratex.sh lb Thesis.tex`

The script automatically creates a `Tmp/` directory for auxiliary files and opens the PDF upon completion.

## Project Structure
- `Thesis.tex`: Main entry point (master document).
- `Tex/`: LaTeX source files for chapters and front/back matter.
- `Style/`: Custom styles (`.sty`), document class (`.cls`), and config (`.cfg`).
- `Img/`: Image assets and figures.
- `Biblio/`: Bibliography database (`.bib`) and citation styles (`.bst`).
- `Tmp/`: Build artifacts and auxiliary files (safe to delete).

## Project Status & Progress
- **Dissertation Title**: 基于 FPGA 的 SLAM 后端软硬协同加速器设计与实现
- **Last Updated**: 2026-02-12
- **Current Completion**:
  - [x] GitHub repository setup and codebase initialization.
  - [x] CLAUDE.md persistence document created with methodology.
  - [x] Frontinfo updated with author and supervisor details.
  - [x] Chapter 1: Introduction (Expanded with domestic/foreign research status and citations).
  - [x] Chapter 2: Methodology (Expanded with camera models, NLS, Schur theory and citations).
  - [x] Chapter 3: System Architecture (Expanded with data flow, protocols, and detailed SOB logic).
  - [x] Chapter 4: Hardware Design (Jacobi engine, SOB gating, memory optimization, Schur core).
  - [ ] Chapter 5: Evaluation (Pending).

## Research Methodology (Core Knowledge)
The dissertation focuses on an FPGA-based hardware/software co-designed SLAM backend accelerator (Schur Kernel).

### Software Algorithm Architecture
- **Framework**: Based on SchurVINS and SVO 2.0.
- **CPU Tasks (ARM)**: State management, visual tracking, EKF pose update (incremental update instead of full LM iteration), and covariance management.
- **Core Strategy**: Uses Schur complement elimination to decouple pose and landmark optimization, then applies EKF for lightweight updates.

### Hardware Infrastructure (FPGA)
- **Jacobi Engine**: 5-stage deep pipeline (Coordinate Transform -> Residual Calculation -> Jacobian Generation -> Hessian Accumulation).
- **SOB Encoding (Sparse Observation Bitmap)**: 8-bit bitmap representing observations across 4 sliding window states and stereo cameras.
- **Dynamic Gating**: High-efficiency mechanism using SOB to skip null calculations (State-level bypass and Camera-level clock gating).
- **Storage**: Compact data stream storing only non-zero Hessian blocks with implicit indexing to save BRAM (optimized to ~67 KB).
- **Schur Module**: Parallelized Hmm inversion ($3 \times 3$), intermediate product caching, and symmetric Hessian update.

### Key Performance Metrics
- **Speedup**: ~3.74x acceleration compared to ARM CPU.
- **Real-time Performance**: Backend optimization frequency > 25 Hz.
- **Accuracy**: Maintains parity with full software implementations on EuRoC and TUM-VI datasets.

## External Reference Materials
- **Small paper (implementation details & figures)**: `/Users/byheng/JQR_LaTeX_Template-0507`

## Code Conventions
- **Source Files**: Organize main content in the `Tex/` directory.
- **Bibliography**: Add entries to `Biblio/ref.bib`.
- **Custom Styles**: Add user-defined commands to `Style/artracom.sty` or directly in `Thesis.tex`.
- **Paths**: Use relative paths. The build script sets `TEXINPUTS` to search subdirectories recursively.
- **Workflow**: Always compile from the root directory using the provided scripts to ensure paths are handled correctly.
- **Mathematical Symbols (Strict Compliance with Small Paper)**:
  - Hessian block matrices: $\mathbf{H}_{pp}, \mathbf{H}_{pm}, \mathbf{H}_{pm}^{\mathrm{T}}, \mathbf{H}_{mm}$ (subscripts: $pp, pm, mm$ without \text).
  - State increments: $\Delta\mathbf{X}$ and $\Delta\mathbf{X}_p$ (X must be **bold and uppercase**).
  - Right-hand side (gradient) vectors: $\mathbf{b}, \mathbf{b}_p, \mathbf{b}_m$.
  - Schur complement operator: $\mathbf{S}$ (bold and uppercase).
  - Schur equation: $\mathbf{S} = \mathbf{H}_{pp} - \mathbf{H}_{pm}\mathbf{H}_{mm}^{-1}\mathbf{H}_{pm}^{\mathrm{T}}$.
  - Gradient update: $\mathbf{b}'_p = \mathbf{b}_p - \mathbf{H}_{pm}\mathbf{H}_{mm}^{-1}\mathbf{b}_m$.
  - All matrices and vectors must use `\mathbf{}`.
