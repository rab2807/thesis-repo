import time
import ee
import numpy as np
import rasterio

# Authenticate and initialize Google Earth Engine
ee.Authenticate()
ee.Initialize()

# Define the latitude and longitude of the region of interest
latitude = 37.7749
longitude = -122.4194
# Define the region of interest (example: a 150x150 px box around the point)
region = ee.Geometry.Rectangle([longitude - 0.01, latitude - 0.01,
                                longitude + 0.01, latitude + 0.01])

# Define the date range
start_date = '2022-01-01'
end_date = '2022-01-31'

# Load Sentinel-2 image collection
sentinel2 = ee.ImageCollection('COPERNICUS/S2') \
    .filterDate(start_date, end_date) \
    .filterBounds(region) \
    .sort('CLOUD_COVER') \
    .first()  # Get the least cloudy image

# Select bands
bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6',
         'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']
image = sentinel2.select(bands)

# Define the region to export (same as region of interest)
region = image.geometry()

# Export the image to Google Drive (as an example)
task = ee.batch.Export.image.toDrive(
    image=image,
    description='Sentinel2Bands',
    scale=10,
    region=region,
    fileFormat='GeoTIFF',
    folder='Sentinel_Export',
    fileNamePrefix='Sentinel2_Bands'
)

task.start()
print('Exporting image to Google Drive...')

# Monitor the task until it is complete
while task.status()['state'] in ['READY', 'RUNNING']:
    print('Current status:', task.status())
    time.sleep(10)
print('Final status:', task.status())

# Once the file is exported, download it from Google Drive
# Alternatively, download from Earth Engine directly if you prefer

# Assume the file is downloaded as 'Sentinel2_Bands.tif' from Google Drive
tif_file = 'Sentinel2_Bands.tif'

# Read the GeoTIFF file and convert to NumPy array
with rasterio.open(tif_file) as src:
    data = src.read()  # Read all bands into a 3D numpy array

# Save the NumPy array to a file
np.save('Sentinel2_Bands.npy', data)
print('Saved bands to Sentinel2_Bands.npy')
