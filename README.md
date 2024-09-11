# Volume Calculation for DEM

This project contains Python scripts to calculate the volume of a heap based on a Digital Elevation Model (DEM) and a shapefile mask. The calculations include Cut Volume, Fill Volume, and Net Volume. The results are saved in a CSV file.

## Problem
In GIS, calculating the volume of terrain features such as heaps, pits, or other earthworks based on a Digital Elevation Model (DEM) is crucial for many applications in civil engineering, mining, and environmental management. Manually calculating these volumes can be complex and time-consuming, especially when considering large datasets and multiple features.

## Solution
This script automates the volume calculation process for selected heaps using a DEM and a clipping shapefile. It calculates:
- Cut Volume (Material below a reference plane)
- Fill Volume (Material above a reference plane)
- Net Volume (Difference between cut and fill volumes)
The service outputs the results to a CSV file with detailed volume data for various elevation levels within the selected area.

Cut Volume (Material below a reference plane)
Fill Volume (Material above a reference plane)
Net Volume (Difference between cut and fill volumes)
The service outputs the results to a CSV file with detailed volume data for various elevation levels within the selected area.

## Project Structure

- `VolumeCalculator1.py`: Contains the logic for calculating volumes from a DEM using a shapefile mask.
- `test.py`: Script to run the volume calculation and test the functionality.
- `VolumeCalculator.py`: Whole script in one file.
- `main.py`: Processing tool creation in QGIS.
- `README.md`: This file.

## Prerequisites

- **QGIS 3.20+**: Ensure that QGIS is installed and configured on your machine.
- **Python 3.6+**: Required for running the scripts.
- **Required Python Packages**: See the requirements.txt for the necessary dependencies.

## Setup

1. Clone or Download the repository containing the project files.
   `git clone https://github.com/your-username/volume-calculation.git`
2. Install Dependencies: Ensure you're using the QGIS Python environment, and install the required dependencies:
   `pip install -r requirements.txt`
3. **Install QGIS**: Follow the installation guide for [QGIS](https://qgis.org/en/site/forusers/download.html).
4. **Configure Python Environment**: Make sure you are using the Python environment bundled with QGIS or have the necessary QGIS libraries available.

## Usage

### Volume Calculation

1. **Prepare Your Data**:
   - A DEM file (.tif format) representing the heap area.
   - A shapefile (.shp) representing the clipping area around the heap.

2. **Update File Paths**:
   - Open `test.py` and set the paths to your DEM file and shapefile in the `projectPath`, `inputRasterDEM`, and `clipShapefile` variables.

3. **Run the Test Script**:
   - Execute `test.py` to perform the volume calculation.

   ```bash
   python test.py

## Reasoning Behind Technical Choices
**QGIS & GDAL**
The combination of QGIS and GDAL was chosen because:
QGIS provides an extensive set of geospatial processing tools that are highly flexible and customizable for handling complex spatial data such as DEMs.
GDAL is a powerful library for geospatial data manipulation, particularly useful for raster operations like clipping and volume calculations.
**PyQt5**
Since QGIS is built on the Qt framework, PyQt5 is necessary for interacting with QGIS's API and ensures that the script can manage data layers and other elements seamlessly.

**CSV for Output**
CSV was selected for output due to its simplicity and wide compatibility with different software. It can easily be imported into GIS systems, spreadsheet programs, or other analytical tools.

**Modularity**
The project is split into two scripts:
`VolumeCalculator1.py` for the core volume calculation logic.
`test.py` for testing and execution.
This separation allows easier maintenance and reuse of the codebase.

## Trade-offs and Future Considerations
**Trade-offs**
Performance vs. Precision: The current volume calculations use a 10% increment of the total elevation range. This is a balance between computational speed and precision. Finer increments could increase the precision of the volume results but would result in longer processing times.
Data Type Handling: To handle large datasets, the system uses floating-point operations, which might introduce some minor rounding errors in very large or small numbers. However, these errors are negligible for most practical applications.

**Future Enhancements**
Multi-threading: The current implementation is single-threaded, which may slow down for large DEMs. Implementing multi-threading would improve performance for high-resolution datasets.
UI Integration: A potential improvement could be integrating the script into a QGIS Plugin with a graphical user interface (GUI), allowing users to interact with the service more intuitively.
Additional Outputs: Adding support for more output formats (e.g., GeoJSON, shapefiles) could extend the service's usability.
