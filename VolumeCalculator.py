from qgis.PyQt.QtCore import QVariant
import csv

# Python can not iterate with floats, therefore we define this function
def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

# Set the path to your folder, the DEM file, and the shapefile for clipping
projectPath = "C:/Users/vaish/Downloads/Aereo1"
inputRasterDEM = "C:/Users/vaish/Downloads/Aereo1/heap-dem.tif"
clipShapefile = "C:/Users/vaish/Downloads/Aereo1/heap/polygons.shp"

# Clip the DEM using the shapefile mask (using GDAL's clip algorithm)
clippedDEM = projectPath + "/clipped_dem.tif"
processing.run("gdal:cliprasterbymasklayer", {
    'INPUT': inputRasterDEM,
    'MASK': clipShapefile,
    'SOURCE_CRS': None,
    'TARGET_CRS': None,
    'NODATA': -9999,
    'ALPHA_BAND': False,
    'CROP_TO_CUTLINE': True,
    'KEEP_RESOLUTION': True,
    'OPTIONS': '',
    'DATA_TYPE': 0,  # Same as input
    'OUTPUT': clippedDEM
})

# Load the clipped DEM
demLayer = iface.addRasterLayer(clippedDEM, "Clipped DEM", "gdal")

# Calculate the statistics (min/max) of the clipped DEM
stats = demLayer.dataProvider().bandStatistics(1)
demMinimum = stats.minimumValue
demMaximum = stats.maximumValue
print("min:", demMinimum, "m")
print("max:", demMaximum, "m")

# Determine the range
demRange = demMaximum - demMinimum
print("Elevation Difference:", demRange, "m")

# Set the increment for the iteration at 10% of the range
increment = demRange / 10.0
print("Increment:", increment)

# Create an empty list for storing the volume data
volumeData = []

# Loop over the elevation range from the minimum to the maximum with the increment
for level in frange(demMinimum, demMaximum + 1, increment):
    # Run the raster surface volume tool with the clipped DEM
    result = processing.run("native:rastersurfacevolume", {
        'INPUT': demLayer,
        'BAND': 1,
        'LEVEL': level,
        'METHOD': 1,
        'OUTPUT_HTML_FILE': 'TEMPORARY_OUTPUT',
        'OUTPUT_TABLE': 'memory:'
    })
    
    # Extract volume data from the output table
    outputLayer = result['OUTPUT_TABLE']
    totalVolume = 0

    for feature in outputLayer.getFeatures():
        volume = feature["Volume"]
        if volume > 0:
            fillVolume = volume / 1000000000.0  # Convert to km³
            cutVolume = 0
        elif volume < 0:
            cutVolume = abs(volume) / 1000000000.0  # Convert to km³
            fillVolume = 0
        else:
            fillVolume = 0
            cutVolume = 0

        # Net Volume = Fill Volume - Cut Volume
        netVolume = fillVolume - cutVolume

        # Append the results to the list
        volumeData.append([level, fillVolume, cutVolume, netVolume])

# Save the volume data to a CSV file
csvFilePath = projectPath + '/volume_data.csv'
with open(csvFilePath, mode='w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    # Write headers
    writer.writerow(["Level (m)", "Fill Volume (km³)", "Cut Volume (km³)", "Net Volume (km³)"])
    # Write data rows
    for row in volumeData:
        writer.writerow(row)

print("Volume data saved to:", csvFilePath)