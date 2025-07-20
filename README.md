# TUB Reproducible Research Portfolio - Gait Analysis

## Repository Creator Information
- **Name:** Yerim Lee
- **Institution:** TU Berlin
- **Email:** yerimisyerim@gmail.com
- **Course:** Digital Tools for Reproducible Research

## Contributors
- **Original Script Author:** Sein Jeung (sein.jeung@tu-berlin.de)
  - GitHub: [@sjeung](https://github.com/sjeung)
  - Created original analysis scripts for gait data processing
- **Repository Maintainer:** Yerim Lee
  - Modified scripts for cross-platform compatibility and reproducibility
  - Implemented portable path handling and documentation

## Project Description

This repository contains Python scripts for analyzing gait data from the physionet database. The analysis focuses on extracting stride times from ground reaction force data and comparing gait patterns between control and patient groups.

### Scripts Overview

#### 1. `gaits_01_import.py`
**Purpose:** Data import and preprocessing
- Loads raw gait data from source files
- Extracts time, left foot force, and right foot force data
- Converts data to BIDS-compliant format
- Generates visualization of raw force signals
- **Output:** Processed data files in `Data/01_raw-data/` directory

#### 2. `gaits_02_extract_features-2.py`
**Purpose:** Feature extraction and stride time calculation
- Detects rising and falling edges in force signals
- Identifies local minima and final contact points
- Calculates stride times for left and right feet
- Based on methodology from Hausdorff, Ladin, and Wei (1995)
- **Output:** Stride time data in `Results/` directory and analysis figures

#### 3. `gait_03_summary.py`
**Purpose:** Group analysis and visualization
- Loads individual participant stride data
- Computes group averages for control and patient populations
- Generates scatter plots comparing groups
- **Output:** Summary statistics and comparison visualizations

## Dataset Information

**Data Source:** Gait analysis data from physionet database
- **Subset Used:** "Ga" (one of Ju, Si, Ga subsets)
- **Groups:** 
  - Control group (Co): Healthy participants
  - Patient group (Pt): Participants with gait disorders
- **Measurements:** Ground reaction forces for left and right feet
- **Sampling:** Up to 33 participants per group, multiple recording sessions

**Data Structure:**
- Raw data contains time series of vertical ground reaction forces
- Analysis focuses on stride time extraction and group comparisons
- Results include individual stride times and group statistics

## Requirements

### Python Dependencies
- numpy
- matplotlib
- pathlib (built-in)
- os (built-in)

### System Requirements
- Python 3.6+
- Cross-platform compatible (Windows, macOS, Linux)

## Installation and Setup

1. **Clone the repository:**
- git clone https://github.com/[your-username]/TUB-ReproCogsci.git
cd TUB-ReproCogsci
2. **Install dependencies:**
- pip install numpy matplotlib
3. **Prepare data structure:**
The scripts will automatically create the following directories:
- `Data/` - Raw and processed data files
- `Results/` - Analysis output files
- `Figures/` - Generated visualizations

## Usage Instructions

### Step 1: Data Import
- python gaits_01_import.py
- Processes raw data files from `Data/00_source-data/`
- Creates BIDS-formatted files in `Data/01_raw-data/`
- Generates force signal visualizations

### Step 2: Feature Extraction
- python gaits_02_extract_features-2.py
- Analyzes processed data to extract stride times
- Creates result files in `Results/` directory
- Generates edge detection and contact point visualizations

### Step 3: Summary Analysis
- python gait_03_summary.py
- - Loads all participant data for group analysis
- Creates summary statistics and comparison plots
- Outputs group comparison visualizations


## Key Improvements Made

### Reproducibility Enhancements
- **Portable Path Handling:** Replaced hardcoded absolute paths with relative paths using `pathlib`
- **Automatic Directory Creation:** Scripts automatically create required directories
- **Cross-Platform Compatibility:** Code works on Windows, macOS, and Linux without modification
- **Error Handling:** Improved exception handling with informative error messages

### Code Quality Improvements
- Consistent use of `pathlib.Path` for all file operations
- Removal of system-specific path separators
- Enhanced documentation and comments
- Standardized variable naming conventions

## Methodology

The gait analysis follows established biomechanical principles:

1. **Force Signal Processing:** Raw ground reaction forces are filtered and processed
2. **Edge Detection:** Rising and falling edges identify foot contact phases
3. **Stride Time Calculation:** Time between consecutive foot contacts defines stride duration
4. **Group Comparison:** Statistical comparison between control and patient populations

## Troubleshooting

### Common Issues
- **File Not Found Errors:** Ensure source data files are in `Data/00_source-data/` directory
- **Permission Errors:** Check write permissions for output directories
- **Import Errors:** Verify all required Python packages are installed

### Debug Mode
To debug file processing issues, check the console output for specific error messages and file paths.

## License

MIT License

## Contact

For questions about this implementation or the course assignment:
- Repository Maintainer: yerimisyerim@gmail.com
- Original Author: sein.jeung@tu-berlin.de
- Course: Seminar Digital Tools for Reproducible Research, TU Berlin

## Acknowledgments

- Original analysis methodology based on Hausdorff, Ladin, and Wei (1995)
- Course instruction and guidance by Sein Jeung
- Physionet database for providing the gait analysis dataset