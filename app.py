import streamlit as stl
# from input import image_input, webcam_input
from cartoonize_functions import to_cartoon
from data_io import get_input_image, get_image_download_link, generate_download_file, get_image_download_link_button
from settings import INPUT_METHODS

stl.set_page_config(layout="wide")
stl.title("Neural Style Transfer")

# Sidebar
stl.sidebar.title('Cartoonize Options')
transformations = stl.sidebar.multiselect("Select the transfomation method: ", ["Classic", "Transformer", "Style Gan"],["Classic"])
stl.sidebar.header('Classic Cartoonize')


color_space = stl.sidebar.select_slider('Color Discretisation', list(range(4, 128, 4)), value=64)
# down_scaling_factor = stl.sidebar.select_slider('Downscaling Factor', list(range(1, 5, 1)), value=1)
bilateral_filter_steps = stl.sidebar.select_slider('bilateral_filter_steps', list(range(1, 50, 1)), value=2)
eliptic_kernal = stl.sidebar.select_slider('eliptic_kernal', list(range(1, 50, 1)), value=3)
quadrativ_kernal = stl.sidebar.select_slider('quadrativ_kernal', list(range(1, 50, 1)), value=2)
neighbourhood = stl.sidebar.select_slider('pixel_neighbourhood', list(range(3, 25, 2)), value=9)

stl.sidebar.header('Style Gan Cartoonize')
# style_model_name = stl.sidebar.selectbox("Choose the style model: ", style_models_name)

# MainFrame

method = stl.radio('Input option', options=INPUT_METHODS, index=1)
uploaded_image = stl.file_uploader('Upload your image here', type=['jpg', 'jpeg', 'png'])


# uni=mpimg.imread(f"{subpath}/images/20180408_175842.jpg")
# uni = cv2.resize(uni, (51,32), interpolation = cv2.INTER_AREA)

image = get_input_image(method, uploaded_image)

down_scaling_factor = 1
generated = to_cartoon(image, down_scaling_factor, bilateral_filter_steps, color_space, eliptic_kernal, quadrativ_kernal, neighbourhood)

col1, col2 = stl.columns(2)
with col1:
    stl.image(image, channels='RGB')
with col2:
    stl.image(generated, channels='RGB', clamp=True)
stl.markdown(get_image_download_link_button(generated), unsafe_allow_html=True)