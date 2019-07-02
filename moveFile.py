import os
import random

folders = [os.path.join('out', folder) for folder in os.listdir('out')]
os.makedirs('test', exist_ok=True)
f1 = open(os.path.join('out', 'labels.txt'), 'w+')
f2 = open(os.path.join('test', 'labels.txt'), 'w+')
for e in folders:
    if e == 'out/labels.txt':
        continue
    os.makedirs(e.replace('out', 'test'), exist_ok=True)
    images = [os.path.join(e, image) for image in os.listdir(e)]
    random.shuffle(images)
    for i in range(0, int(len(images)/5)):
        os.rename(images[i], images[i].replace('out', 'test'))

        texts = images[i].split('/')
        f2.write("%s %s\n" % (texts[2], texts[1]))

    for i in range(int(len(images)/5), len(images)):

        texts = images[i].split('/')
        f1.write("%s %s\n" % (texts[2], texts[1]))

f1.close()
f2.close()