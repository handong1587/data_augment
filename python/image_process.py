# first version: 2015/01/30
# second version: 2015/12/17

import math
import random
from PIL import Image
from PIL import ImageFilter
import config as cfg

# default interpolation method: image.BICUBIC

def random_resize(image):
    ratio_lb = cfg.RANDOM_RESIZE_LB
    ratio_ub = cfg.RANDOM_RESIZE_UB
    [width, height] = image.size
    ratio_h = random.uniform(ratio_lb, ratio_ub)
    ratio_w = random.uniform(ratio_lb, ratio_ub)
    resize_h = int(height * ratio_h)
    resize_w = int(width * ratio_w)
    image_resize = image.resize((resize_w, resize_h), Image.BICUBIC)
    return image_resize

def random_crop(image):
    ratio_lb = cfg.RANDOM_CROP_LB
    ratio_ub = cfg.RANDOM_CROP_UB
    [width, height] = image.size
    ratio_h = random.uniform(ratio_lb, ratio_ub)
    ratio_w = random.uniform(ratio_lb, ratio_ub)
    crop_h = int(height * ratio_h)
    crop_w = int(width * ratio_w)
    x_start = random.randint(0, width-crop_w-1)
    y_start = random.randint(0, height-crop_h-1)
    image_crop = image.crop((x_start, y_start, x_start+crop_w, y_start+crop_h))

    return image_crop

def random_rotate(image):
    angle_lb = cfg.RANDOM_ROTATE_LB
    angle_ub = cfg.RANDOM_ROTATE_UB
    [w, h] = image.size
    rotate_angle = random.randint(angle_lb, angle_ub)
    image_rotate = image.rotate(rotate_angle, Image.BICUBIC)
    remove_w = (int)(math.ceil(abs(h/2 * math.tan(rotate_angle * math.pi/180))))
    remove_h = (int)(math.ceil(abs(w/2 * math.tan(rotate_angle * math.pi/180))))
    image_crop = image_rotate.crop((remove_w, remove_h, w-remove_w-1, h-remove_w-1))

    return image_crop

def random_crop_resize(image):
    image_crop = random_crop(image)
    image_resize = random_resize(image_crop)
    return image_resize

def random_rotate_resize(image):
    image_rotate = random_rotate(image)
    image_resize = random_resize(image_rotate)
    return  image_resize

def random_blur(image):
    image_blur = image.filter(ImageFilter.BLUR)
    return image_blur

def random_blur_2(image):
    random_radius = random.randint(cfg.RANDOM_BLUR_RADIUS_LB, cfg.RANDOM_BLUR_RADIUS_UB)
    image_blur = image.filter(ImageFilter.GaussianBlur(random_radius))
    return image_blur

# pepper & salt noise
def random_pepper_salt(image):
    ratio_lb = cfg.RANDOM_PEPPER_SALT_LB
    ratio_ub = cfg.RANDOM_PEPPER_SALT_UB
    image_noising = image.copy()
    [w, h] = image_noising.size
    noise_ratio = random.uniform(ratio_lb, ratio_ub)
    max_noise_pixel_cnt = (int)(w * h * noise_ratio)
    noise_pixel_cnt = 0
    pix = image_noising.load()
    for x in range(w):
        if noise_pixel_cnt >= max_noise_pixel_cnt:
            break
        for y in range(h):
            if noise_pixel_cnt >= max_noise_pixel_cnt:
                break

            if random.randint(0,(int)(1/noise_ratio)) != 0: # simulate noise_ratio probability
                continue
            random_value = random.randint(0,1) * 255
            pix[x, y] = (random_value, random_value, random_value)
            noise_pixel_cnt = noise_pixel_cnt + 1

    return image_noising

def random_pepper_salt_2(image):
    ratio_lb = cfg.RANDOM_PEPPER_SALT_LB
    ratio_ub = cfg.RANDOM_PEPPER_SALT_UB
    image_noising = image.copy()
    [w, h] = image_noising.size
    noise_ratio = random.uniform(ratio_lb, ratio_ub)
    threshold  = 1 - noise_ratio/2
    noise_pixel_cnt = 0
    pix = image_noising.load()
    for x in range(w):
        #if noise_pixel_cnt >= max_noise_pixel_cnt:
         #   break
        for y in range(h):
          #  if noise_pixel_cnt >= max_noise_pixel_cnt:
           #     break

            random_value = random.random()
            if random_value < noise_ratio/2:
                pix[x, y] = (0, 0, 0)
                noise_pixel_cnt += 1
            elif random_value > threshold:
                pix[x, y] = (255, 255, 255)
                noise_pixel_cnt += 1
            else:
                continue

    return image_noising
