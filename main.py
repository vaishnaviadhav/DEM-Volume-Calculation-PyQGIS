from qgis.core import QgsProcessingAlgorithm, QgsProcessingParameterRasterLayer, QgsProcessingParameterVectorLayer, QgsProcessingParameterFileDestination, QgsProcessingParameterNumber, QgsRasterLayer, QgsProcessingContext, QgsProcessingUtils
from qgis.PyQt.QtCore import QVariant
import csv
import processing

class CalculateVolume(QgsProcessingAlgorithm):
    DEM_LAYER = 'DEM_LAYER'
    HEAP_LAYER = 'HEAP_LAYER'
    OUTPUT_CSV = 'OUTPUT_CSV'
    STEP = 'STEP'

    def initAlgorithm(self, config=None):
        # DEM layer input
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.DEM_LAYER,
                "Input DEM Layer"
            )
        )

        # Polygon layer representing heaps
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.HEAP_LAYER,
                "Input Heap Polygon Layer"
            )
        )

        # Output CSV for volume data
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_CSV,
                "Output CSV File",
                fileFilter="CSV files (*.csv)"
            )
        )

        # Step for volume calculation
        self.addParameter(
            QgsProcessingParameterNumber(
                self.STEP,
                "Elevation Step",
                defaultValue=10.0
            )
        )

    def processAlgorithm(self, parameters, context: QgsProcessingContext, feedback):
        # Retrieve input data
        dem_layer = self.parameterAsRasterLayer(parameters, self.DEM_LAYER, context)
        heap_layer = self.parameterAsVectorLayer(parameters, self.HEAP_LAYER, context)
        output_csv = self.parameterAsFileOutput(parameters, self.OUTPUT_CSV, context)
        step = self.parameterAsDouble(parameters, self.STEP, context)

        # 1. Clip DEM by the polygon layer
        feedback.setProgressText("Clipping DEM...")
        clipped_dem = self.clip_dem_by_heap(dem_layer, heap_layer, context, feedback)

        # 2. Calculate the volume data at different levels
        feedback.setProgressText("Calculating Volume...")
        volume_data = self.calculate_volume(clipped_dem, step, context, feedback)

        # 3. Export the volume data to a CSV file
        feedback.setProgressText("Exporting data to CSV...")
        self.export_to_csv(volume_data, output_csv)

        return {
            self.OUTPUT_CSV: output_csv
        }

    def clip_dem_by_heap(self, dem_layer: QgsRasterLayer, heap_layer, context, feedback):
        # Clip DEM using the heap polygon shapefile
        clipped_output = QgsProcessingUtils.generateTempFilename('clipped_dem.tif')
        processing.run("gdal:cliprasterbymasklayer", {
            'INPUT': dem_layer,
            'MASK': heap_layer,
            'SOURCE_CRS': None,
            'TARGET_CRS': None,
            'NODATA': -9999,
            'ALPHA_BAND': False,
            'CROP_TO_CUTLINE': True,
            'KEEP_RESOLUTION': True,
            'OPTIONS': '',
            'DATA_TYPE': 0,  # Same as input
            'OUTPUT': clipped_output
        }, context=context, feedback=feedback)

        return clipped_output

    def calculate_volume(self, clipped_dem, step, context, feedback):
        # Load the clipped DEM
        dem_layer = QgsRasterLayer(clipped_dem, "Clipped DEM")
        stats = dem_layer.dataProvider().bandStatistics(1)

        dem_minimum = stats.minimumValue
        dem_maximum = stats.maximumValue
        dem_range = dem_maximum - dem_minimum

        # Create an empty list for storing the volume data
        volume_data = []

        # Loop over the elevation range from the minimum to the maximum with the increment
        for level in self.frange(dem_minimum, dem_maximum + 1, step):
            # Run the raster surface volume tool with the clipped DEM
            result = processing.run("native:rastersurfacevolume", {
                'INPUT': dem_layer,
                'BAND': 1,
                'LEVEL': level,
                'METHOD': 1,
                'OUTPUT_HTML_FILE': 'TEMPORARY_OUTPUT',
                'OUTPUT_TABLE': 'memory:'
            }, context=context, feedback=feedback)
            
            # Extract volume data from the output table
            output_layer = result['OUTPUT_TABLE']
            for feature in output_layer.getFeatures():
                volume = feature["Volume"]
                if volume > 0:
                    fill_volume = volume / 1000000000.0  # Convert to km³
                    cut_volume = 0
                elif volume < 0:
                    cut_volume = abs(volume) / 1000000000.0  # Convert to km³
                    fill_volume = 0
                else:
                    fill_volume = 0
                    cut_volume = 0

                # Net Volume = Fill Volume - Cut Volume
                net_volume = fill_volume - cut_volume

                # Append the results to the list
                volume_data.append([level, fill_volume, cut_volume, net_volume])

        return volume_data

    def export_to_csv(self, volume_data, csv_file_path):
        # Save the volume data to a CSV file
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write headers
            writer.writerow(["Level (m)", "Fill Volume (km³)", "Cut Volume (km³)", "Net Volume (km³)"])
            # Write data rows
            for row in volume_data:
                writer.writerow(row)

    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    def name(self):
        return "Calculate Heap Volume"

    def displayName(self):
        return "Calculate Heap Volume from DEM"

    def createInstance(self):
        return CalculateVolume()