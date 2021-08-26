import base64
import os
from io import BytesIO
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image


def get_input_image(method, upload_image):
    if method == "Upload":
        image = Image.open(upload_image).convert('RGB')
        return np.asarray(image)
    elif method == "Example":
        subpath = os.path.dirname(os.path.abspath(__file__))
        example = cv2.imread(f"{subpath}/images/20180408_175842.jpg")
        example = cv2.cvtColor(example, cv2.COLOR_BGR2RGB)
        return example


def get_image_download_link(img):
    """
    from https://discuss.streamlit.io/t/how-to-download-image/3358/4
    :param img:
    :param filename:
    :param text:
    :return:
    """
    img = Image.fromarray(img)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="cartoon.jpeg">cartoon</a>'
    return href


def generate_download_file(image):
    def download_file():
        components.html(
            f"""
            <html>
            <head>
            <title>Start Auto Download file</title>
            <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
            <script>
            $('{get_image_download_link(image)}')[0].click()
            </script>
            </head>
            </html>
            """
        )
    return download_file


def get_image_download_link_button(img):
    """
    Source: https://discuss.streamlit.io/t/a-download-button-with-custom-css/4220/19
    Generates a link to download the given object_to_download.

    """

    img = Image.fromarray(img)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    button_id = "Download-Button"
    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 

            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    return custom_css + f'<a download="cartoon.jpeg" id="{button_id}" href="data:file/txt;base64,{img_str}">Download generated Image</a>'
