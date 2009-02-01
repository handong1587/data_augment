__author__ = 'jblin'

import numpy
import random
from random import randint
from PIL import Image

# for perspective transform
# pb is the four vertices in the current plane
# pa contains four vertices in the resulting plane

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)

# not for use
def random_affine_transform(image):
    width, height = image.size

    m = -0.2
    xshift = abs(m) * width
    new_width = width + int(round(xshift))
    img_affine = image.transform((new_width, height),
                                    Image.AFFINE,
                                    (1, m, -xshift if m > 0 else 0, 0, 1, 0),
                                    Image.BICUBIC)

    n = 0.2
    yshift = abs(n) * height
    new_height = height + int(round(yshift))
    img_affine2 = image.transform((width, new_height),
                                    Image.AFFINE,
                                    (1, 0, 0, n, 1, -yshift if n > 0 else 0),
                                    Image.BICUBIC)

    return img_affine

def random_perspective_transform(image):
    width, height = image.size
    x_ratio, y_ratio = random.uniform(0, 0.1), random.uniform(0, 0.1)
    x_shift = x_ratio * width
    y_shift = y_ratio * height
    new_width = width + int(x_shift)
    new_height = height + int(y_shift)

    # randomly choose 4 corner points in origin plane, each point not exceeding 0.05*w(h) away from original corner point

    #random_topleft = (0, 0)
    #random_topright = (width, 0)
    #random_downleft = (0, height)
    #random_downright = (width, height)

    random_topleft = (random.randint(0, (int)(width * 0.1)), random.randint(0, (int)(height * 0.1)))
    random_topright = (width - random.randint(0, (int)(width * 0.1)), random.randint(0, (int)(height * 0.1)))
    random_downleft = (random.randint(0, (int)(width * 0.1)), height - random.randint(0, (int)(height * 0.1)))
    random_downright = (width - random.randint(0, (int)(width * 0.1)), height - random.randint(0, (int)(height * 0.1)))

    #print random_topleft, random_topright, random_downleft, random_downright

    coeffs = find_coeffs([(0, 0), (new_width, 0), (0, new_height), (new_width, new_height)], # four vertices in the resulting plane
                        [random_topleft, random_topright, random_downleft, random_downright]) # four vertices in the current plane
    img_transform = image.transform((new_width, new_height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

    return img_transform