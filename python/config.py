__author__ = 'jblin'

INPUT_DIR = '/data/jinbin.lin/data/similarity/original/'
OUTPUT_DIR = '/data/jinbin.lin/data/similarity/augmented'

IMAGE_LIST = '/data/jinbin.lin/data/similarity/augmented/image.list'
TRAIN_LIST = '/data/jinbin.lin/data/similarity/augmented/train.list'
VAL_LIST   = '/data/jinbin.lin/data/similarity/augmented/val.list'

DEBUG = False 

TARGET_WIDTH = 64
TARGET_HEIGHT = 64

RANDOM_ITER = 100 

# resize
RANDOM_RESIZE_LB = 0.8
RANDOM_RESIZE_UB = 1.2

# crop
RANDOM_CROP_LB = 0.8
RANDOM_CROP_UB = 1.0

# rotate
RANDOM_ROTATE_LB = -10
RANDOM_ROTATE_UB = 10

# blur
RANDOM_BLUR_RADIUS_LB = 2
RANDOM_BLUR_RADIUS_UB = 4

# papper salt
RANDOM_PEPPER_SALT_LB = 0.01
RANDOM_PEPPER_SALT_UB = 0.04

# train/val
TRAIN_RATIO = 0.9
VAL_RATIO   = 0.1

#
DEBUG_TEST_COUNT = 1
