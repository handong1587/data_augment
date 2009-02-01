__author__ = 'jblin'

import config as cfg
import utils
import os
from PIL import Image
import random
from random import shuffle
from random import randint
import image_process as ip
import perspective_transform as pt
import warp

ImageAugMethods = [  [ip.random_crop, 'random_crop'],
                     [ip.random_rotate, 'random_rotate'],
                     [ip.random_blur_2, 'random_blur'],
                     [ip.random_pepper_salt_2, 'random_pepper_salt'],
                     [pt.random_perspective_transform, 'random_perspective_transform'],
                     [warp.random_warp, 'random_warp'],
                  ]

def print_aug_methods(rand_aug_list):
    assert len(rand_aug_list) > 0, \
        'Augmentation list must not be none'
    print 'Augmentation list:'
    for aug_method, aug_name in rand_aug_list:
        print '  {}'.format(aug_name)

def random_augment(image):
    aug_num = len(ImageAugMethods)
    rand_aug_list = random.sample(ImageAugMethods, randint(1, aug_num))
    shuffle(rand_aug_list)

    if cfg.DEBUG == True:
        print_aug_methods(rand_aug_list)

    image_aug = image

    for rand_augment in rand_aug_list:
        image_aug = rand_augment[0](image_aug)

    rand_flip = bool(randint(0, 1))
    if rand_flip == True:
        image_aug = image_aug.transpose(Image.FLIP_LEFT_RIGHT)
    return image_aug

def traverse_dir(input_dir, output_dir, image_list):
    print 'Start traversing...'

    if os.path.exists(input_dir) == False:
        print 'Input directory do not exist: {}'.format(input_dir)
        return
    if os.path.exists(output_dir) == False:
        utils.create_dir_recursive(output_dir)

    test_count = 0
    aug_count = 0

    for list_dirs in os.listdir(input_dir):

        if cfg.DEBUG == True and test_count >= cfg.DEBUG_TEST_COUNT:
            print 'Debug halts.'
            break

        target_path = os.path.join(input_dir, list_dirs)
        if os.path.isdir(target_path):
            #output_path = '%s/%s' % (output_dir, os.path.split(target_path)[1])
            output_path = '{}/{}'.format(output_dir, os.path.split(target_path)[1])
            traverse_dir(target_path, output_path, image_list)
        else:
            image = Image.open(target_path)

            print 'target_path: {}'.format(target_path)

            file_name = os.path.split(target_path)[1]
            file_name, file_ext = file_name.split('.')
            #alpha_str = filter(str.isalpha, re.split('\\.', file_name)[0])
            #digit_str = filter(str.isdigit, re.split('\\.', file_name)[0])
            digit_str = filter(str.isdigit, file_name)
            label_id = int(digit_str) / 4

            #print '{} {} {}'.format(file_name, file_ext, digit_str)

            #repeat_times = cfg.RANDOM_ITER
            #acc_idx = file_id * repeat_times * len(process_image_list)

            for rand_i in range(cfg.RANDOM_ITER):
                image_aug = random_augment(image)
                #output_file_name = '%s/%s%010d%s' % (output_dir, alpha_str, acc_idx, '.jpg')
                #output_file_name = '{}/{}_{}{}'.format(output_dir, alpha_str, acc_idx, '.jpg')
                output_file_name = '{}/{}_{}.jpg'.format(output_dir, file_name, str(rand_i).zfill(4))

                image_resize = utils.resizeToTargetSize(image_aug)
                image_resize.save(output_file_name, "JPEG")
                #acc_idx = acc_idx + 1

                write_line = '{} {}\n'.format(output_file_name, label_id)
                image_list.write(write_line)

            aug_count += cfg.RANDOM_ITER
            test_count += 1

    print 'Image augmentation counts: {}'.format(aug_count)

def genTrainValList():
    train_list_file = open(cfg.TRAIN_LIST, 'w')
    val_list_file = open(cfg.VAL_LIST, 'w')

    image_list = utils.readList(cfg.IMAGE_LIST)
    shuffle(image_list)

    train_num = int(len(image_list) * cfg.TRAIN_RATIO)
    val_num = len(image_list) - train_num

    train_list = image_list[:train_num]
    val_list = image_list[train_num:]

    print 'Generating train list ...'
    for i in xrange(len(train_list)):
        write_line = '{}\n'.format(train_list[i])
        train_list_file.write(write_line)

    print 'Generating validation list ...'
    for i in xrange(len(val_list)):
        write_line = '{}\n'.format(val_list[i])
        val_list_file.write(write_line)

    train_list_file.close()
    val_list_file.close()

    print 'Generate train/val list completed.'

if __name__ == '__main__':
    utils.makeAllDirs()

    image_list = open(cfg.IMAGE_LIST, 'w')
    traverse_dir(cfg.INPUT_DIR, cfg.OUTPUT_DIR, image_list)
    image_list.close()

    genTrainValList()
