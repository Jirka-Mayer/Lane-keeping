"""
    Deforms images to account for different car shift and rotation
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt

# skew is in [-1, 1]
# this is mapping to percentage of image width
SKEW_SCALE = 500 / 1920 # 500px in a 1920x1080 image

# same as skew
ROTATION_SCALE = 500 / 1920

# skew ground
def shiftCar(image, skew):
    rows, cols, ch = image.shape

    # transform bottom half (ground)
    pts1 = np.float32([[0, rows/2], [cols, rows/2], [0, rows]])
    pts2 = np.float32([[0, 0], [cols, 0], [skew * SKEW_SCALE * cols, rows/2]])
    M = cv2.getAffineTransform(pts1,pts2)
    ground = cv2.warpAffine(image, M, (cols, int(rows/2)))

    # overlay bottom half
    image[int(rows/2):,:,:] = ground

    return image


# shift sky sideways, drag ground
def rotateCar(image, rotation):
    rows, cols, ch = image.shape
    offset = rotation * ROTATION_SCALE * cols

    # transform bottom half (ground)
    pts1 = np.float32([[0, rows], [cols, rows], [0, rows/2]])
    pts2 = np.float32([[0, rows/2], [cols, rows/2], [offset, 0]])
    M = cv2.getAffineTransform(pts1,pts2)
    ground = cv2.warpAffine(image, M, (cols, int(rows/2)))

    # shift image sideways (top part mainly)
    pts1 = np.float32([[0, 0], [0, 100], [100, 100]])
    pts2 = np.float32([[0+offset, 0], [0+offset, 100], [100+offset, 100]])
    M = cv2.getAffineTransform(pts1,pts2)
    image = cv2.warpAffine(image, M, (cols, rows))

    # overlay bottom half
    image[int(rows/2):,:,:] = ground

    return image


if __name__ == "__main__":
    image = cv2.imread("recording-center/frame-584.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = rotateCar(image, -1)
    plt.imshow(image)
    plt.show()