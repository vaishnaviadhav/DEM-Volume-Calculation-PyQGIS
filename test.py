from VolumeCalculator1 import volume_calculator
import traceback

# Set the path to your folder, the DEM file, and the shapefile for clipping
projectPath = "C:/Users/vaish/Downloads/Aereo1"
inputRasterDEM = "C:/Users/vaish/Downloads/Aereo1/heap-dem.tif"
clipShapefile = "C:/Users/vaish/Downloads/Aereo1/heap/polygons.shp"

def main():
    try:
        volume_calculator(projectPath, inputRasterDEM, clipShapefile)
        print("Completed")
    except Exception as e:
        print(f"main(): Error - {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()