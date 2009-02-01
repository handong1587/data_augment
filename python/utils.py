__author__ = 'jblin'

import config as cfg
import os
import os.path as osp
from PIL import Image

def resizeToTargetSize(image):
    return image.resize((cfg.TARGET_WIDTH, cfg.TARGET_HEIGHT), Image.BICUBIC)

def create_dir_recursive(target_dir):
    prev_dir = os.path.split(target_dir)[0]
    if os.path.exists(prev_dir):
        os.mkdir(target_dir)
    else:
        create_dir_recursive(prev_dir)
        os.mkdir(target_dir)

def checkFileExist(file_name):
    if not osp.isfile(file_name):
        raise IOError(('{:s} not found.\n').format(file_name))

def readList(file_name):
    checkFileExist(file_name)
    list_file = open(file_name, 'r')
    lists = [line.rstrip('\n') for line in list_file]
    list_file.close()

    return lists

def makeAllDirs():
    if osp.exists(cfg.OUTPUT_DIR) == False:
        os.mkdir(cfg.OUTPUT_DIR)