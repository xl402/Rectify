from imageai.Prediction import ImagePrediction
import os

def multiple_predict(threshold):

    execution_path = os.getcwd()
    multiple_prediction = ImagePrediction()
    multiple_prediction.setModelTypeAsInceptionV3()
    multiple_prediction.setModelPath(os.path.join(execution_path, "inception_v3_weights_tf_dim_ordering_tf_kernels.h5"))
    multiple_prediction.loadModel()
    all_images_array = []
    all_files = os.listdir(execution_path+"/adian")
    for each_file in all_files:
        if(each_file.endswith(".jpg") or each_file.endswith(".png")):
            all_images_array.append("adian/"+each_file)
    results_array = multiple_prediction.predictMultipleImages(all_images_array, result_count_per_image=1)

    objects = []
    for each_result in results_array:
        predictions, percentage_probabilities = each_result["predictions"], each_result["percentage_probabilities"]
        for index in range(len(predictions)):
            print(predictions[index] , " : " , percentage_probabilities[index])
            prob = percentage_probabilities[index]
            if prob > threshold:
                objects.append(predictions[index])
        print("-----------------------")

    # Remove duplicates
    objects = list(dict.fromkeys(objects))
    return objects
