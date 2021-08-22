import streamlit as stl
import cv2
import os
# from input import image_input, webcam_input
from cartoonize_functions import to_cartoon
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

stl.title("Neural Style Transfer")
stl.sidebar.title('Navigation')
method = stl.sidebar.radio('Go To ->', options=['Webcam', 'Image'])
transformation = stl.sidebar.selectbox("Select the transfomation method: ", ["Classic", "Transformer"])
stl.sidebar.header('Options')


color_space = stl.sidebar.select_slider('Color Discretisation', list(range(8, 256, 4)), value=64)
down_scaling_factor = stl.sidebar.select_slider('Downscaling Factor', list(range(1, 5, 1)), value=2)
bilateral_filter_steps = stl.sidebar.select_slider('bilateral_filter_steps', list(range(1, 50, 1)), value=1)

# style_model_name = stl.sidebar.selectbox("Choose the style model: ", style_models_name)


subpath=os.path.dirname(os.path.abspath(__file__))
uni=mpimg.imread(f"{subpath}/images/20180408_175842.jpg")
#uni=cv2.imread(f"{subpath}/images/20180408_175842.jpg")
to_cartoon(uni, color_space, down_scaling_factor, bilateral_filter_steps)
#if method == 'Image':
#    image_input(style_model_name)
#else:
#    webcam_input(style_model_name)
