import os
import random

flds = [os.path.join('val', folder) for folder in os.listdir('val')]
for e in flds:
    images = [os.path.join(e, image) for image in os.listdir(e)]
    for i in range(0, len(images)):
        os.rename(images[i], images[i].replace('val', 'out'))

folders = [os.path.join('out', folder) for folder in os.listdir('out')]
os.makedirs('test', exist_ok=True)

for e in folders:

    os.makedirs(e.replace('out', 'val'), exist_ok=True)
    images = [os.path.join(e, image) for image in os.listdir(e)]
    random.shuffle(images)
    for i in range(0, int(len(images)/20)):
        os.rename(images[i], images[i].replace('out', 'val'))
