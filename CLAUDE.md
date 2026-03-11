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
- **Figure Font Standards (MANDATORY for all generated figures)**:
  - Chinese text: **SimSun (宋体)** — required for all Chinese labels, titles, and annotations
  - English text and mathematical symbols: **Times New Roman** — required for all English/math content
  - These two fonts must be explicitly requested when using generate-image or any figure generation tool
  - This applies to all diagrams in `Img/` directory

- **Mathematical Symbols (Strict Compliance with Small Paper)**:
  - Hessian block matrices: $\mathbf{H}_{pp}, \mathbf{H}_{pm}, \mathbf{H}_{pm}^{\mathrm{T}}, \mathbf{H}_{mm}$ (subscripts: $pp, pm, mm$ without \text).
  - State increments: $\Delta\mathbf{X}$ and $\Delta\mathbf{X}_p$ (X must be **bold and uppercase**).
  - Right-hand side (gradient) vectors: $\mathbf{b}, \mathbf{b}_p, \mathbf{b}_m$.
  - Schur complement operator: $\mathbf{S}$ (bold and uppercase).
  - Schur equation: $\mathbf{S} = \mathbf{H}_{pp} - \mathbf{H}_{pm}\mathbf{H}_{mm}^{-1}\mathbf{H}_{pm}^{\mathrm{T}}$.
  - Gradient update: $\mathbf{b}'_p = \mathbf{b}_p - \mathbf{H}_{pm}\mathbf{H}_{mm}^{-1}\mathbf{b}_m$.
  - All matrices and vectors must use `\mathbf{}`.

## Bibliography Management Tools

The project includes automated tools in the `scripts/` directory for fetching BibTeX entries from academic databases.

### Quick Usage

**Recommended: CrossRef Tool (No VPN Required)**

```bash
cd scripts

# Query by paper title
python3 fetch_bibtex_crossref.py "ORB-SLAM: a Versatile and Accurate Monocular SLAM System"

# Query by DOI (fastest and most accurate)
python3 fetch_bibtex_crossref.py --doi "10.1109/TRO.2015.2463671"

# Save to file
python3 fetch_bibtex_crossref.py "Paper Title" -o output.bib

# Append directly to ref.bib
python3 fetch_bibtex_crossref.py "Paper Title" >> ../Biblio/ref.bib
```

**Alternative: Google Scholar Tool (for arXiv preprints)**

```bash
# Basic usage
python3 fetch_bibtex.py "Paper Title"

# With proxy (if blocked)
python3 fetch_bibtex.py --proxy "Paper Title"
```

### Tool Selection Guide

- **Use CrossRef** (`fetch_bibtex_crossref.py`) for:
  - Journal articles (IEEE TRO, IJCV, etc.)
  - Conference papers (CVPR, ICCV, ICRA, etc.)
  - Papers with DOI
  - **Advantages**: Fast, stable, no anti-bot restrictions, no VPN needed

- **Use Google Scholar** (`fetch_bibtex.py`) for:
  - arXiv preprints
  - Technical reports without DOI
  - Papers not indexed in CrossRef
  - **Note**: Requires VPN for China users, may encounter rate limiting

### Tested Papers

The following papers have been successfully tested with CrossRef:
- ORB-SLAM (IEEE TRO 2015)
- VINS-Mono (IEEE TRO 2018)
- DTAM (ICCV 2011)

For detailed documentation, see `scripts/README.md`.

## Bibliography and Citation Standards (CRITICAL)

**STRICTLY ENFORCE THESE RULES FOR ALL REFERENCES:**

1. **Zero Tolerance for Fabricated References**:
   - **NEVER** create, invent, or fabricate any bibliography entries.
   - Every single reference must be verifiable on Google Scholar or other academic databases.
   - If you cannot verify a reference exists, DO NOT include it in the paper.

2. **Verification Requirement**:
   - Before adding or citing any reference, you MUST verify its existence through:
     - Google Scholar search (scholar.google.com)
     - PubMed, IEEE Xplore, ACM Digital Library, or arXiv
   - Record the exact title, authors, venue, and year from the verified source.

3. **Accuracy Requirements**:
   - **Authors**: Must match exactly (correct names, order, and affiliations).
   - **Title**: Must be character-accurate including capitalization.
   - **Venue**: Conference/journal name must be official and complete.
   - **Year**: Must be the actual publication year, not estimated.
   - **Affiliations**: When mentioning research institutions, verify author affiliations from the paper.

4. **Common Errors to Avoid**:
   - ❌ Inventing paper titles or DOIs
   - ❌ Misattributing works to wrong institutions (e.g., claiming Tsinghua work as from PKU)
   - ❌ Confusing similar paper titles or authors
   - ❌ Using outdated or retracted papers
   - ❌ Citing papers that exist in preprint but not peer-reviewed venues

5. **Recommended Workflow**:
   - When writing research status sections (e.g., Chapter 1.2), use verified survey papers as primary sources.
   - Cross-reference claims with multiple reliable sources.
   - Prefer citing well-established works over obscure or unverifiable sources.
   - Use reference paper: `/Users/byheng/Dissertation/ref_paper/视觉SLAM机器人中光束法平差优化芯片研究综述_莫霄睿.pdf` as authoritative source for BA accelerator research status.

6. **Documentation**:
   - When adding references to `Biblio/ref.bib`, include a comment with verification source:
     ```bibtex
     % Verified: Google Scholar, 2025-03-06
     @article{example2025,
       title={...},
       ...
     }
     ```

**VIOLATION CONSEQUENCES**: Fabricated references undermine academic integrity and can result in paper rejection or retraction. When in doubt, omit the reference or ask the user for verification.
