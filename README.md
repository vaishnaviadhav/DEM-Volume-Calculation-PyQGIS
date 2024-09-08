# Volume Calculation for DEM

This project contains Python scripts to calculate the volume of a heap based on a Digital Elevation Model (DEM) and a shapefile mask. The calculations include Cut Volume, Fill Volume, and Net Volume. The results are saved in a CSV file.

## Project Structure

- `VolumeCalculator1.py`: Contains the logic for calculating volumes from a DEM using a shapefile mask.
- `test.py`: Script to run the volume calculation and test the functionality.
- `VolumeCalculator.py`: Whole script in one file.
- `README.md`: This file.

## Requirements

- **QGIS**: Ensure QGIS is installed and properly configured.
- **Python**: Version 3.9+
- **QGIS Python API**: Required modules should be available in the QGIS Python environment.

## Setup

1. **Install QGIS**: Follow the installation guide for [QGIS](https://qgis.org/en/site/forusers/download.html).
2. **Configure Python Environment**: Make sure you are using the Python environment bundled with QGIS or have the necessary QGIS libraries available.

## Usage

### Volume Calculation

1. **Prepare Your Data**:
   - Ensure you have a DEM file and a shapefile to use as a mask.

2. **Update File Paths**:
   - Open `test.py` and set the paths to your DEM file and shapefile in the `projectPath`, `inputRasterDEM`, and `clipShapefile` variables.

3. **Run the Test Script**:
   - Execute `test.py` to perform the volume calculation.

   ```bash
   python test.py
