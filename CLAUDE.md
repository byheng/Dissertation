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
- **Last Updated**: 2026-02-11
- **Current Completion**:
  - [x] GitHub repository setup and codebase initialization.
  - [x] CLAUDE.md persistence document created with methodology.
  - [x] Frontinfo updated with author and supervisor details.
  - [ ] Chapter 1: Introduction (In progress - placeholders existing).
  - [ ] Chapter 2: Methodology (Pending).

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

## Code Conventions
- **Source Files**: Organize main content in the `Tex/` directory.
- **Bibliography**: Add entries to `Biblio/ref.bib`.
- **Custom Styles**: Add user-defined commands to `Style/artracom.sty` or directly in `Thesis.tex`.
- **Paths**: Use relative paths. The build script sets `TEXINPUTS` to search subdirectories recursively.
- **Workflow**: Always compile from the root directory using the provided scripts to ensure paths are handled correctly.
