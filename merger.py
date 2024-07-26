import os
import sys
import re
import numpy as np
import random


def merge_files(folder):
    files = os.listdir(folder)
    files = [f for f in files if f.endswith('.npy')]
    if len(files) == 0:
        return

    # sort the files
    files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    merged = []
    for f in files:
        data = np.load(os.path.join(folder, f))
        merged.append(data)

    # convert to numpy array
    merged = np.array(merged)

    # Keep only the middle 18 frames
    total_frames = merged.shape[0]
    start_frame = (total_frames - 18) // 2
    end_frame = start_frame + 18

    merged = merged[start_frame:end_frame]

    # Apply random crop to the merged video
    height, width = merged.shape[1], merged.shape[2]
    crop_size = 64  # 64x64 crop
    min_x = crop_size // 2
    min_y = crop_size // 2
    max_x = width - crop_size // 2
    max_y = height - crop_size // 2
    crop_x = random.randint(min_x, max_x)
    crop_y = random.randint(min_y, max_y)

    merged = merged[:, crop_y - crop_size // 2:crop_y + crop_size // 2,
                    crop_x - crop_size // 2:crop_x + crop_size // 2]

    return merged


if __name__ == '__main__':
    super_merged = []
    # folders = [f for f in os.listdir('./data') if os.path.isdir(f)]
    folders = [os.path.join('./data', f) for f in os.listdir('./data') if os.path.isdir(os.path.join('./data', f))]

    # sort the folders
    folders.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    for folder in folders:
        merged = merge_files(folder)
        if merged is not None:
            print(folder, merged.shape)
            super_merged.append(merged)

    super_merged = np.array(super_merged)
    print(super_merged.shape)

    # (batches, channels, frames, height, width)
    super_merged = super_merged.transpose(0, 4, 1, 2, 3)
    print(super_merged.shape)

    np.save('./merged.npy', super_merged)
