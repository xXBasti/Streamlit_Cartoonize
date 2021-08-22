from sklearn.cluster import KMeans
import cv2
from matplotlib import pyplot as plt
import numpy as np


def to_cartoon( inital, down=2,bi=25, color_space =64 ):
    """

    :param inital: intital image
    :param down: downsampling steps
    :param bi: bilateral filtering steps
    :param color_space: number of colors in the cartoon image
    :return:
    """

    # bilateral filter
    colour = inital
    for _ in range(down):
        colour = cv2.pyrDown(colour)
    for _ in range(bi):
        colour = cv2.bilateralFilter(colour, d=9, sigmaColor=9, sigmaSpace=7)
    for _ in range(down):
        colour = cv2.pyrUp(colour)

    # creating blur & edges
    grey = cv2.cvtColor(inital, cv2.COLOR_RGB2GRAY)
    for _ in range(bi):
        blur = cv2.bilateralFilter(grey, 9, 9, 7)
    edge = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=9, C=3)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)

    colour = colour[0:len(inital), 0:len(inital[0])]
    edge = edge[0:len(inital), 0:len(inital[0])]

    # assable cartoon:
    cartoon = cv2.bitwise_and(colour, edge)
    # Reduce color space
    cartoon=np.array(np.floor(cartoon/color_space)*color_space, dtype=np.uint8)
    # morphology
    kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    cartoon2 = cv2.morphologyEx(cartoon, cv2.MORPH_CLOSE, kernel)
    kernel2 = np.ones((2,2),np.uint8)
    cartoon2 = cv2.dilate(cartoon2,kernel2,iterations = 1)

    return cartoon2;
