import os
import json

jsons = os.listdir('jsons')

for json_file in jsons:
    # get the object from file
    with open(f'jsons/{json_file}', 'r') as f:
        data = json.load(f)
    # get the center coordinates
    center_coords = data['features'][0]['geometry']['coordinates'][0]

    # get mean x and mean y
    mean_x = 0
    mean_y = 0
    for coords in center_coords:
        mean_x += coords[0]
        mean_y += coords[1]
    mean_x /= len(center_coords)
    mean_y /= len(center_coords)

    # append the coords to the json and save it
    data['center_coords'] = [mean_x, mean_y]
    with open(f'jsons/{json_file}', 'w') as f:
        json.dump(data, f)

print('done')
