**Image Forgery Detection with VGG16 and SVM**

**Overview**
This project is aimed at building an image forgery detection system that can accurately distinguish between authentic and forged images. The forgery methods primarily focused on are copy-move and splicing.

The copy-move forgery detection algorithm identifies regions within an image that have been copied and pasted elsewhere in the same image. The splice forgery detection algorithm identifies regions that have been cut from one image and pasted into another.


**Methodology**
We employ a two-step process that consists of feature extraction using VGG16 and then classification using a Support Vector Machine (SVM).


**Feature Extraction**
The VGG16 model, pre-trained on the ImageNet dataset, is used for feature extraction. This Convolutional Neural Network (CNN) model is known for its robustness in detecting a variety of features from input images. The model's architecture allows us to extract high-level features that are then flattened to create a feature vector for each image.


**Classification**
The feature vectors extracted from the VGG16 model are used as input for an SVM classifier. The SVM, which is trained on these feature vectors and their corresponding labels, is responsible for the final classification of the images.


**Prerequisites:**
The project uses Python and requires the following packages:

OpenCV (cv2)
NumPy
Keras
scikit-learn
PIL


**Running the Classifier:**
 To use the classifier, run the classifier.py Python script.


**Challenges and Solutions**
Extracting robust and informative features from images was a critical challenge. The VGG16 model, renowned for its excellent performance in a variety of image recognition tasks, provided an efficient solution. \Training deep learning models requires significant computational resources, which can be a limiting factor, especially when running the model on personal computers. To work around this, we used transfer learning from a pre-trained VGG16 model, which significantly reduced the computational resources needed while maintaining a high level of accuracy.


**Results**
The SVM classifier, once trained, is used to predict the labels of the images in the test set. The performance of the model is then evaluated using metrics such as accuracy and the confusion matrix.

The obtained accuracy and confusion matrix on the test dataset are as follows:




