import streamlit as stl
from cartoonize_functions import build_style_gan, build_to_cartoon_function, build_to_cartoon
from data_io import get_input_image, get_image_download_link_button
from settings import INPUT_METHODS, style_models_name

stl.set_page_config(layout="wide")
stl.title("Cartoonize Style Transfer")

# Sidebar
stl.sidebar.title('Cartoonize Options')
transformations = stl.sidebar.multiselect("Select the transfomation method: ", ["Classic", "Transformer", "Style Gan"],["Classic"])
# resize_option = stl.sidebar.radio("Select Resize Option: ", ("None", "Shrink", "Shrink and Grow"))
# stl.sidebar.write("For Large Images ")
stl.sidebar.header('Classic Cartoonize')


color_space = stl.sidebar.select_slider('Color Discretisation', list(range(4, 128, 4)), value=64)
# down_scaling_factor = stl.sidebar.select_slider('Downscaling Factor', list(range(1, 5, 1)), value=1)
bilateral_filter_steps = stl.sidebar.select_slider('bilateral_filter_steps', list(range(1, 50, 1)), value=2)
eliptic_kernal = stl.sidebar.select_slider('eliptic_kernal', list(range(1, 50, 1)), value=3)
quadrativ_kernal = stl.sidebar.select_slider('quadrativ_kernal', list(range(1, 50, 1)), value=2)
neighbourhood = stl.sidebar.select_slider('pixel_neighbourhood', list(range(3, 25, 2)), value=9)

stl.sidebar.header('Style Gan Cartoonize')
model_name = stl.sidebar.selectbox("Choose the style model: ", style_models_name)
# MainFrame

method = stl.radio('Input option', options=INPUT_METHODS, index=1)
uploaded_image = stl.file_uploader('Upload your image here', type=['jpg', 'jpeg', 'png'])

image = get_input_image(method, uploaded_image)
TRANSFORMATIONS_MAP = {"Classic": build_to_cartoon(bilateral_filter_steps, color_space, eliptic_kernal, quadrativ_kernal, neighbourhood), "Transformer": build_style_gan(model_name), "Style Gan": build_style_gan(model_name)}
func = build_to_cartoon_function(transformations,TRANSFORMATIONS_MAP)
down_scaling_factor = 1
# generated = to_cartoon(image, down_scaling_factor, bilateral_filter_steps, color_space, eliptic_kernal, quadrativ_kernal, neighbourhood)
generated = func(image)
col1, col2 = stl.columns(2)
with col1:
    stl.image(image, channels='RGB')
with col2:
    stl.image(generated, channels='RGB', clamp=True)
stl.markdown(get_image_download_link_button(generated), unsafe_allow_html=True)