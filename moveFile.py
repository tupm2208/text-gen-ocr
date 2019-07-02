import os
import random

folders = [os.path.join('out', folder) for folder in os.listdir('out')]
os.makedirs('test', exist_ok=True)

for e in folders:
    if e == 'out/labels.txt':
        continue
    os.makedirs(e.replace('out', 'test'), exist_ok=True)
    images = [os.path.join(e, image) for image in os.listdir(e)]
    random.shuffle(images)
    for i in range(0, int(len(images)/5)):
        os.rename(images[i], images[i].replace('out', 'test'))

    os.makedirs(e.replace('out', 'val'), exist_ok=True)
    for i in range(int(len(images)/5), int(len(images)/5) + int(len(images)/25)):
        os.rename(images[i], images[i].replace('out', 'val'))
