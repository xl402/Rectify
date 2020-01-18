from image_cut import image_cut_saver
from multiple_detection import get_boxes
from multiple_predictor import multiple_predict

def get_object_list(image_dir):

    # Get locations of all objects
    locs = get_boxes(image_dir)

    # Extract each object into its own image
    image_cut_saver(locs, image_dir)

    # Get a class prediction for each image
    # Set percentage threshold
    THRESHOLD = 95
    objects = multiple_predict(THRESHOLD)

    return objects
