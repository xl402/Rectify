from skimage import data, io, filters
import time

image = io.imread("test.jpg")

coordinate_list = [[1000, 1200, 300, 800], [700, 1200, 100, 500], [500, 1000, 400, 1200]]
for i in range(len(coordinate_list)):
    coordinates = coordinate_list[i]
    cropped = image[coordinates[0]:coordinates[1], coordinates[2]:coordinates[3]]
    io.imshow(cropped)
    im_name = "test_" + str(i) + ".jpg"
    io.imsave(im_name, cropped)
    print("yo")
