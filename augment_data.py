from __future__ import print_function
from __future__ import division
import os
import shutil
import Augmentor
from tqdm import tqdm

image_dir_path = '/media/trongpq/HDD/ai_data/text-gen-ocr/single_front_rgb'

image_dirs = os.listdir(image_dir_path)
image_dirs.sort()
for images_dir in image_dirs:
    images_dir = os.path.join(image_dir_path, images_dir)
    p = Augmentor.Pipeline(images_dir)
    p.crop_centre(probability=0.5, percentage_area=0.9)
    p.sample(360)
    p = Augmentor.Pipeline(images_dir)
    p.rotate(probability=0.5, max_left_rotation=5, max_right_rotation=5)
    p.sample(360)
    p = Augmentor.Pipeline(images_dir)
    p.random_distortion(probability=0.5, grid_width=5, grid_height=5, magnitude=5)
    p.sample(360)
    output_augment_dir = os.path.join(images_dir, 'output')
    list_dirs = os.listdir(output_augment_dir)
    for _dir in list_dirs:
        shutil.move(os.path.join(output_augment_dir, _dir), os.path.join(images_dir, _dir))
    os.rmdir(output_augment_dir)
