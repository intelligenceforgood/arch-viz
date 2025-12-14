# Architecture Visualization

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Graphviz](https://img.shields.io/badge/Tool-Graphviz-orange.svg)](https://graphviz.org/)
[![Make](https://img.shields.io/badge/Build-Makefile-informational.svg)](Makefile)

This repository contains the "Diagrams as Code" source for the i4g platform architecture.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    (Note: Requires Graphviz installed on your system, e.g., `brew install graphviz`)

## Usage

To generate all diagrams:

```bash
make all
```

This will:
1.  Run the Python scripts in `src/views/`.
2.  Output SVG files to `output/`.

## Workflow

1.  Edit the Python scripts in `src/views/` to update the diagrams.
2.  Run `make all` to regenerate the SVGs.
3.  Copy the generated SVGs to the main documentation repo:
    ```bash
    cp output/*.svg ../docs/book/assets/architecture/
    ```

## Directory Structure

*   `src/views/`: Python scripts defining the diagrams.
    *   `system_topology.py`: Level 1 "Metro Map".
    *   `data_pipeline.py`: Level 2 Data Ingestion & Processing.
    *   `security_model.py`: Level 2 Auth & Encryption.
*   `output/`: Generated SVG/PNG files (gitignored).
