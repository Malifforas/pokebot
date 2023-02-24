import cv2
import numpy as np


def preprocess(image):
    # Convert the image to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the image
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)

    # Apply binary thresholding to the image
    _, thresholded = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY)

    return thresholded


def compare_images(image1, image2):
    # Compute the mean squared error (MSE) between the two images
    mse = np.mean((image1 - image2) ** 2)

    # If the MSE is less than 500, the images are considered to be the same
    return mse < 500
