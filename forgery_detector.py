# -*- coding: utf-8 -*-
"""spoof_sense.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tEwYv3cwnaBvyBjRH2PGqIlMsx583mDc
"""

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

#checking the dimension of an image from the dataset
from PIL import Image

# Open the image
image_path = "/content/a_0001.jpg"
image = Image.open(image_path)

# Get the size of the image
width, height = image.size

image_size = (width, height)

# Print the size
print("Image size: {}x{}".format(width, height))

# Close the image
image.close()

#connecting to my google drive, where I uploaded the dataset
from google.colab import drive
drive.mount('/content/drive')

#pre-processing the data
from PIL import Image
from keras.applications.vgg16 import VGG16, preprocess_input
import keras.utils as image
from tensorflow.keras.utils import img_to_array
import numpy as np
import os

# Load the pre-trained VGG16 model
model = VGG16(weights='imagenet', include_top=False)

# Define the input image size
input_size = (224, 224)

def preprocess_images(folder_path):
    preprocessed_images = []
    labels = []

    for label_idx, label in enumerate(['authentic', 'copy-moved', 'spliced']):
        subfolder_path = os.path.join(folder_path, label)

        # Skip if 'authentic' folder doesn't have 'images' subfolder
        images_folder = subfolder_path if label == 'authentic' else os.path.join(subfolder_path, 'images')

        for image_name in os.listdir(images_folder):
            image_path = os.path.join(images_folder, image_name)

            # Convert TIFF and PNG images to JPEG format
            if image_path.endswith('.tif') or image_path.endswith('.tiff') or image_path.endswith('.png'):
                jpeg_path = os.path.splitext(image_path)[0] + '.jpeg'

                if not os.path.exists(jpeg_path):
                    im = Image.open(image_path)
                    im.convert('RGB').save(jpeg_path, "JPEG")

                image_path = jpeg_path

            img = Image.open(image_path)
            img = img.resize(input_size)

            # Convert image to array and preprocess input
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            preprocessed_images.append(x)
            labels.append(label_idx)  # Assign label index

    # Add the following line to print the set of unique labels
    print("Unique labels:", set(labels))

    return np.array(preprocessed_images), np.array(labels)



# Path to train and test folders
train_folder_path = "/content/drive/MyDrive/spoofsenseyy/data/traindev"
test_folder_path = "/content/drive/MyDrive/spoofsenseyy/data/test"

# Preprocess images and labels for the train set
train_images, train_labels = preprocess_images(train_folder_path)

# Preprocess images and labels for the test set
test_images, test_labels = preprocess_images(test_folder_path)

# Print the shape of preprocessed images and labels for train and test sets
print("Train images shape:", train_images.shape)
print("Train labels shape:", train_labels.shape)
print("Test images shape:", test_images.shape)
print("Test labels shape:", test_labels.shape)

#feature extraction using VGG
import cv2
import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.preprocessing import image
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import os

vgg_model = VGG16(weights='imagenet', include_top=False)

# Function to extract VGG16 features from an image
def extract_vgg_features(image_path):
    # Load the image
    img = image.load_img(image_path, target_size=(224, 224))

    # Preprocess the image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Extract VGG16 features
    features = vgg_model.predict(x)

    # Flatten the features
    features = features.flatten()

    return features

#copy move forgery detection using block matching
def calculate_similarity(block, block_mask):
    block_gray = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
    mask_gray = cv2.cvtColor(block_mask, cv2.COLOR_BGR2GRAY)
    correlation = np.corrcoef(block_gray.flatten(), mask_gray.flatten())[0, 1]
    return correlation

def detect_copy_move_forgery(image_path, mask_path=None):
    image = cv2.imread(image_path)
    if mask_path is None:
        mask = np.zeros_like(image)
    else:
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    if mask is None:
        return False

    binary_mask = np.where(mask > 0, 255, 0).astype(np.uint8)
    block_size = 16
    stride = 8
    for y in range(0, image.shape[0] - block_size, stride):
        for x in range(0, image.shape[1] - block_size, stride):
            block = image[y:y+block_size, x:x+block_size]
            block_mask = binary_mask[y:y+block_size, x:x+block_size]
            similarity = calculate_similarity(block, block_mask)
            threshold = 0.9
            if similarity > threshold:
                return True
    return False

#splice forgery detection
from skimage.feature import local_binary_pattern

def local_binary_patterns(image, radius, points):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lbp = local_binary_pattern(gray, points, radius, method='uniform')
    return lbp.astype(np.uint8)

def calculate_texture_consistency(lbp_image):
    variance = np.var(lbp_image)
    normalized_variance = variance / (lbp_image.max() - lbp_image.min())
    texture_consistency = 1 - normalized_variance
    return texture_consistency

def detect_splice_forgery(image_path, mask_path=None):
    image = cv2.imread(image_path)

    if mask_path is None:
        mask = np.zeros_like(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    else:
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    if mask is None:
        return False

    binary_mask = np.where(mask > 0, 255, 0).astype(np.uint8)
    lbp_radius = 1
    lbp_points = 8
    lbp_image = local_binary_patterns(image, lbp_radius, lbp_points)
    masked_lbp_image = cv2.bitwise_and(lbp_image, binary_mask)
    texture_consistency = calculate_texture_consistency(masked_lbp_image)
    threshold = 0.8

    if texture_consistency < threshold:
        return True
    return False

#training the SVM classifier and evaluating the model
import os
import cv2
import numpy as np
from sklearn.svm import SVC
from keras.applications.vgg16 import VGG16, preprocess_input
import keras.utils as image
from tensorflow.keras.utils import img_to_array
from sklearn.metrics import accuracy_score, confusion_matrix
from tensorflow.keras.layers import Input
from tensorflow.keras.utils import load_img

# Initialize VGG16 model with pre-trained ImageNet weights
vgg_model = VGG16(weights='imagenet', include_top=False)

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

# Define train and test folders
train_folder = "/content/drive/MyDrive/spoofsenseyy/data/traindev"
test_folder = "/content/drive/MyDrive/spoofsenseyy/data/test"

# Define labels and their corresponding index
label_dict = {'authentic': 0, 'copy-moved': 1, 'spliced': 2}

# Initialize the train and test features and labels
train_features = []
train_labels = []
test_features = []
test_labels = []

# Extract features and labels for training data
for label in ['authentic', 'copy-moved', 'spliced']:
    subfolder_path = os.path.join(train_folder, label)
    images_folder = subfolder_path if label == 'authentic' else os.path.join(subfolder_path, 'images')

    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        vgg_features = extract_vgg_features(image_path)
        train_features.append(vgg_features)
        train_labels.append(label_dict[label])

# Extract features and labels for test data
for label in ['authentic', 'copy-moved', 'spliced']:
    subfolder_path = os.path.join(test_folder, label)
    images_folder = subfolder_path if label == 'authentic' else os.path.join(subfolder_path, 'images')

    for image_name in os.listdir(images_folder):
        image_path = os.path.join(images_folder, image_name)
        vgg_features = extract_vgg_features(image_path)
        test_features.append(vgg_features)
        test_labels.append(label_dict[label])

# Convert lists to numpy arrays
train_features = np.array(train_features)
train_labels = np.array(train_labels)
test_features = np.array(test_features)
test_labels = np.array(test_labels)

# Train SVM classifier
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(train_features, train_labels)

# Predict on test set
test_predictions = svm_classifier.predict(test_features)

# Print accuracy
accuracy = accuracy_score(test_labels, test_predictions)
print("Accuracy: {:.2f}%".format(accuracy * 100))

# Print confusion matrix
confusion_mat = confusion_matrix(test_labels, test_predictions)
print("Confusion Matrix:")
print(confusion_mat)

#saving the classifier
import pickle

# Save the trained model to disk
pickle.dump(svm_classifier, open("svm_classifier.pkl", 'wb'))

from joblib import dump
dump(svm_classifier, 'svm_model.joblib')

