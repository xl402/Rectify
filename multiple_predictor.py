from imageai.Prediction import ImagePrediction
import os
import shutil

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
        #print("-----------------------")

    # Remove duplicates
    #objects = list(dict.fromkeys(objects))
    objects = list(set(objects))
    supported_list = ['banana', 'orange', 'mixing_bowl', 'soup_bowl', 'washbowl', 'washbasin', 'handbasin', 'lavabo', 'wash-hand basin', 'custard apple','pomegranate', 'beer_bottle', 'pop_bottle', 'soda_bottle', 'water_bottle', 'wine_bottle', 'sundial', 'bathtub']
    objects = [i for i in objects if i in supported_list]
    objects = [i if i not in ['pomegranate', 'custard apple', 'sundial'] else 'apple' for i in objects]
    objects = [i if i not in ['pop_bottle', 'soda_bottle', 'wine_bottle'] else 'water_bottle' for i in objects]
    objects = [i if i not in ['soup_bowl', 'washbowl', 'washbasin', 'handbasin', 'bathtub'] else 'mixing_bowl' for i in objects]
    objects = list(set(objects))
    
    return objects
