import os
import cv2
import numpy as np
import matplotlib.image as mpimg

from app import style_models_name, style_models_file


def to_cartoon( inital, down=2,bi=25, color_space =16, eliptic_kernal=3,quadrativ_kernal=2,neighbourhood=9):
    """

    :param inital: intital image
    :param down: downsampling steps
    :param bi: bilateral filtering steps
    :param color_space: number of colors in the cartoon image
    :return:
    """

    # bilateral filter
    colour = inital
    height, width, chennel = colour.shape
    # for _ in range(down):
    #     height, width = int(height/2), int(width/2)
    #     colour = cv2.pyrDown(colour, dst=(height, width))
    for _ in range(bi):
        colour = cv2.bilateralFilter(colour, d=neighbourhood, sigmaColor=neighbourhood, sigmaSpace=7)
    # for _ in range(down):
    #     height, width = int(height * 2), int(width * 2)
    #     colour = cv2.pyrUp(colour, dst=(height,width))

    # creating blur & edges
    grey = cv2.cvtColor(inital, cv2.COLOR_RGB2GRAY)
    for _ in range(bi):
        blur = cv2.bilateralFilter(grey, neighbourhood, neighbourhood, 7)
    edge = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=neighbourhood, C=3)
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)

    colour = colour[0:len(inital), 0:len(inital[0])]
    edge = edge[0:len(inital), 0:len(inital[0])]

    # assable cartoon:
    cartoon = cv2.bitwise_and(colour, edge)
    # Reduce color space
    cartoon = np.array(np.floor(cartoon/color_space)*color_space, dtype=np.uint8)
    # morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (eliptic_kernal, eliptic_kernal))
    cartoon2 = cv2.morphologyEx(cartoon, cv2.MORPH_CLOSE, kernel)
    kernel2 = np.ones((quadrativ_kernal,quadrativ_kernal),np.uint8)
    cartoon2 = cv2.dilate(cartoon2,kernel2,iterations = 1)

    return cartoon2


def build_to_cartoon(bi=25, color_space =16, eliptic_kernal=3,quadrativ_kernal=2,neighbourhood=9):
    def to_cartoon(inital):
        """

         :param inital: intital image
         :param down: downsampling steps
         :param bi: bilateral filtering steps
         :param color_space: number of colors in the cartoon image
         :return:
         """

        # bilateral filter
        colour = inital
        height, width, chennel = colour.shape
        # for _ in range(down):
        #     height, width = int(height/2), int(width/2)
        #     colour = cv2.pyrDown(colour, dst=(height, width))
        for _ in range(bi):
            colour = cv2.bilateralFilter(colour, d=neighbourhood, sigmaColor=neighbourhood, sigmaSpace=7)
        # for _ in range(down):
        #     height, width = int(height * 2), int(width * 2)
        #     colour = cv2.pyrUp(colour, dst=(height,width))

        # creating blur & edges
        grey = cv2.cvtColor(inital, cv2.COLOR_RGB2GRAY)
        for _ in range(bi):
            blur = cv2.bilateralFilter(grey, neighbourhood, neighbourhood, 7)
        edge = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize=neighbourhood, C=3)
        edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB)

        colour = colour[0:len(inital), 0:len(inital[0])]
        edge = edge[0:len(inital), 0:len(inital[0])]

        # assable cartoon:
        cartoon = cv2.bitwise_and(colour, edge)
        # Reduce color space
        cartoon = np.array(np.floor(cartoon / color_space) * color_space, dtype=np.uint8)
        # morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (eliptic_kernal, eliptic_kernal))
        cartoon2 = cv2.morphologyEx(cartoon, cv2.MORPH_CLOSE, kernel)
        kernel2 = np.ones((quadrativ_kernal, quadrativ_kernal), np.uint8)
        cartoon2 = cv2.dilate(cartoon2, kernel2, iterations=1)

        return cartoon2
    return to_cartoon


def build_style_gan(model_name):

    model_path = 'models'

    style_models_dict = {name: os.path.join(model_path, file) for name, file in
                         zip(style_models_name, style_models_file)}
    model = cv2.dnn.readNet(style_models_dict[model_name])

    def style_transfer(image):
        (h, w) = image.shape[:2]
        oversize_factor = limit_image_size(h, w)
        if oversize_factor > 1:
            image = cv2.resize(np.array(image),(w/oversize_factor, h/oversize_factor))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        blob = cv2.dnn.blobFromImage(image, 1.0, (w, h), (0, 0, 0), swapRB=False, crop=False)
        model.setInput(blob)
        output = model.forward()

        output = output.reshape((3, output.shape[2], output.shape[3]))
        output = output.transpose(1, 2, 0)
        output = cv2.cvtColor(np.array(output), cv2.COLOR_BGR2RGB)
        output = np.clip(output, 0.0, 255.0)
        output = np.array(output, dtype=np.uint8)
        if oversize_factor > 1:
            output = cv2.resize(np.array(image), (w , h ))
        return output
    return style_transfer


def build_to_cartoon_function(transformations,TRANSFORMATIONS_MAP):
    def transform(image):
        for transformation in transformations:
            image=TRANSFORMATIONS_MAP[transformation](image)
        return image
    return transform


def limit_image_size(h, w):
    FULL_HD = (1920, 1080)
    return max(FULL_HD[1]/h, FULL_HD[0]/w)


if __name__ == "__main__":
    subpath = os.path.dirname(os.path.abspath(__file__))
    uni = mpimg.imread(f"{subpath}/images/20180408_175842.jpg")
    uni = cv2.resize(uni, (2016, 1512), interpolation=cv2.INTER_AREA)
    to_cartoon(uni)