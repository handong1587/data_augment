__author__ = 'jblin'
# http://svn.navi.cx/misc/trunk/pycaptcha/Captcha/Visual/Distortions.py

import math
import random
from PIL import Image

def get_transform(image):
    return lambda x, y: (x, y)

def get_sine_warp_transform(image):
    #amplitudeRange = (2, 4)
    amplitudeRange = (1, 3)
    #periodRange    = (0.04, 0.1)
    periodRange    = (0.04, 0.1)
    amplitude = random.uniform(*amplitudeRange)
    period = random.uniform(*periodRange)
    offset = (random.uniform(0, math.pi * 2 / period),
              random.uniform(0, math.pi * 2 / period))

    return (lambda x, y,
                   a = amplitude,
                   p = period,
                   o = offset:
            (math.sin( (y+o[0])*p )*a + x,
             math.sin( (x+o[1])*p )*a + y))

def random_warp(image):
    #resolution = 10
    resolution = random.randint(2,10)
    filtering = Image.BILINEAR

    r = resolution
    xPoints = image.size[0] / r + 2
    yPoints = image.size[1] / r + 2
    # f = getTransform(image)
    f = get_sine_warp_transform(image)

    # Create a list of arrays with transformed points
    xRows = []
    yRows = []
    for j in xrange(yPoints):
        xRow = []
        yRow = []
        for i in xrange(xPoints):
            x, y = f(i*r, j*r)

            # Clamp the edges so we don't get black undefined areas
            x = max(0, min(image.size[0]-1, x))
            y = max(0, min(image.size[1]-1, y))

            xRow.append(x)
            yRow.append(y)
        xRows.append(xRow)
        yRows.append(yRow)

    # Create the mesh list, with a transformation for
    # each square between points on the grid
    mesh = []
    for j in xrange(yPoints-1):
        for i in xrange(xPoints-1):
            mesh.append((
                # Destination rectangle
                (i*r, j*r,
                 (i+1)*r, (j+1)*r),
                # Source quadrilateral
                (xRows[j  ][i  ], yRows[j  ][i  ],
                 xRows[j+1][i  ], yRows[j+1][i  ],
                 xRows[j+1][i+1], yRows[j+1][i+1],
                 xRows[j  ][i+1], yRows[j  ][i+1]),
                ))

    image_warp = image.transform(image.size, Image.MESH, mesh, filtering)

    return image_warp

def random_wiggle_blocks(image):
    blockSize=16
    sigma=0.01
    iterations=300
    seed = random.random()

    image_wiggle = image

    r = random.Random(seed)
    for i in xrange(iterations):
        # Select a block
        bx = int(r.uniform(0, image_wiggle.size[0]-blockSize))
        by = int(r.uniform(0, image_wiggle.size[1]-blockSize))
        block = image_wiggle.crop((bx, by, bx+blockSize-1, by+blockSize-1))

        # Figure out how much to move it.
        # The call to floor() is important so we always round toward
        # 0 rather than to -inf. Just int() would bias the block motion.
        mx = int(math.floor(r.normalvariate(0, sigma)))
        my = int(math.floor(r.normalvariate(0, sigma)))

        # Now actually move the block
        image_wiggle.paste(block, (bx+mx, by+my))

    return image_wiggle