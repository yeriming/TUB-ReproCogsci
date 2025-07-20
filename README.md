# TUB-ReproCogsci - Gait Analysis Scripts

## Repository Creator Information
- **Name:** Yerim Lee
- **Institution:** TU Berlin
- **Email:** yerimisyerim@gmail.com
- **Course:** Seminar Digital Tools for Reproducible Research

## Contributors
- **Original Script Author:** Sein Jeung (sein.jeung@tu-berlin.de)
  - GitHub: [@sjeung](https://github.com/sjeung)
  - Created original analysis scripts based on Hausdorff, Ladin, and Wei (1995)
- **Repository Maintainer:** [Your Name]
  - Modified scripts for cross-platform compatibility
  - Implemented portable path handling using pathlib
  - Added automatic directory creation

## Project Description

This repository contains three Python scripts for processing and analyzing data files. The scripts are designed to work sequentially to extract features and generate visualizations.

### Scripts Overview

#### 1. `gaits_01_import.py`
**Purpose:** Data import and format conversion
- **Input:** Text files from `Data/00_source-data/` directory
- **Processing:** Extracts columns 0, 17, 18 (time, left_force, right_force) from source data
- **Output:** 
  - Processed files in `Data/01_raw-data/sub-{participant_ID}/beh/`
  - File naming: `sub-{participant_ID}_run-{rep}_task-gait_beh.tsv`
  - Visualizations in `Figures/01_raw-data/`

#### 2. `gaits_02_extract_features-2.py`
**Purpose:** Feature extraction using edge detection
- **Input:** Processed data from previous script
- **Processing:** 
  - Edge detection with rise_fall_edge = 500
  - Local minima detection with window = 33 samples
  - Final contact detection with offset_contact = 10
- **Output:**
  - Result files: `sub-{participant_ID}_strides.tsv` in `Results/` directory
  - Visualizations in `Figures/02_edge_detection/` and `Figures/03_final_contacts/`

#### 3. `gait_03_summary.py`
**Purpose:** Data aggregation and group comparison
- **Input:** Stride files from `Results/` directory
- **Processing:** Computes averages for participant groups "Co" and "Pt"
- **Output:** Summary statistics and comparison scatter plots

## Dataset Configuration

### Processing Parameters (from code)
- **subset_name:** "Ga" (code comments indicate alternatives: "Ju", "Si", "Ga")
- **participant_groups:** ("Co", "Pt")
- **max_n_participant:** 33
- **rep sessions:** ('01', '02', '10')

## Requirements

### Dependencies (from import statements)
- import os 
- import numpy as np 
- import matplotlib.pyplot as plt 
- from pathlib import Path

## Installation and Setup

1. **Clone the repository:**
- git clone https://github.com/[your-username]/TUB-ReproCogsci.git
cd TUB-ReproCogsci
2. **Install required packages:**
- pip install numpy matplotlib

## Usage Instructions

### Execution Order
Scripts must be run in sequence:
- Step 1: Process raw data files (gaits_01_import.py)

- Step 2: Extract features and calculate stride times (gaits_02_extract_features-2.py)

- Step 3: Generate summary analysis (gait_03_summary.py)

### Expected Input
- Source files should be placed in `Data/00_source-data/`
- File naming pattern: `{participant_ID}_{rep}.txt`
- Where participant_ID follows pattern: `{subset_name}{group}{number:02d}`
- Example: `GaCo01_01.txt`, `GaPt15_02.txt`

## Output Files

### Results Directory
- **File format:** Tab-separated values (.tsv)
- **Structure:** Two columns (left stride times, right stride times)
- **Data handling:** NaN padding when arrays have unequal lengths

### Figures Directory
- **Format:** PNG images saved for each processing stage
- **Naming patterns:** 
  - `raw_{participant_ID}_{rep}.png`
  - `edges_{participant_ID}_{rep}.png`
  - `fc_{participant_ID}_{rep}.png`

## Troubleshooting

## License

MIT license

## Contact

For questions about this implementation:
- **Repository Maintainer:** yerimisyerim@gmail.com
- **Original Author:** sein.jeung@tu-berlin.de
- **Course:** Digital Tools for Reproducible Research, TU Berlin

## Acknowledgments

- Original script methodology referenced from Hausdorff, Ladin, and Wei (1995) (noted in code comments)
- Course instruction by Sein Jeung, TU Berlin