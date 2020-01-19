from skimage import data, io, filters
import time
import glob
import os

# Clear existing images
files = glob.glob('adian/*')
for f in files:
    os.remove(f)

def image_cut_saver(coordinate_list, image_dir):
    image = io.imread(image_dir)
    for i in range(len(coordinate_list)):
        coordinates = coordinate_list[i]
        cropped = image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]
        if cropped.shape[0]!=0:
            im_name = "adian/test" + str(i) + ".jpg"
            io.imsave(im_name, cropped)
