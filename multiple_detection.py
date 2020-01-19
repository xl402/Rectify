from imageai.Detection import ObjectDetection
import os


def get_boxes(image_dir):
    execution_path = os.getcwd()

    detector = ObjectDetection()


    # Choose Model type
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))

    custom = detector.CustomObjects(handbag = True, tie = True, frisbee = True, bottle = True, cup = True, fork = True, knife = True, spoon = True, bowl = True, banana = True, apple = True, sandwich = True, orange = True, broccoli = True, carrot = True, scissors = True, toothbrush = True, book = True, vase = True)

    detector.loadModel()
    detections = detector.detectCustomObjectsFromImage(custom_objects=custom, input_image=os.path.join(execution_path , image_dir), output_image_path=os.path.join(execution_path , "dontcare.jpg"), minimum_percentage_probability=5)

    locs = []
    for eachObject in detections:
        #print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
        locs.append(eachObject["box_points"])
    return locs
