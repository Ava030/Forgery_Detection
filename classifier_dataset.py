# -*- coding: utf-8 -*-
"""classifier_dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FzZsze2CqupBxOUlP7ApLUfy_avnOrFZ
"""

import os
import cv2
import numpy as np
from sklearn.svm import SVC
from keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.metrics import accuracy_score, confusion_matrix
from joblib import load

# Load the trained SVM model
svm_classifier = load('/path/to/your/svm_model.joblib')

# Load VGG16 model
vgg_model = VGG16(weights='imagenet', include_top=False)

# Define labels and their corresponding index
label_dict = {0: 'authentic', 1: 'copy-moved', 2: 'spliced'}

# Function to extract VGG16 features from an image
def extract_vgg_features(image_path):
    # Load the image
    img = load_img(image_path, target_size=(224, 224))

    # Preprocess the image
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Extract VGG16 features
    features = vgg_model.predict(x)

    # Flatten the features
    features = features.flatten()

    return features

# Define your test directory
test_directory = "/path/to/your/test/directory"

# Initialize list to store the classification results
results = []

# Loop over all subdirectories in the test directory
for label in os.listdir(test_directory):
    subfolder_path = os.path.join(test_directory, label)
    images_folder = subfolder_path if label == 'authentic' else os.path.join(subfolder_path, 'images')

    # Loop over all images in the subdirectory
    for filename in os.listdir(images_folder):
        # Only process files with the following extensions
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Get the full path of the image
            image_path = os.path.join(images_folder, filename)

            # Extract features and reshape to the expected format
            features = extract_vgg_features(image_path)
            features = features.reshape(1, -1)

            # Make a prediction
            prediction = svm_classifier.predict(features)

            # Add the classification result to the results list
            results.append((filename, label_dict[prediction[0]]))

# Print the classification results
for filename, label in results:
    print("Image", filename, "is classified as", label)

