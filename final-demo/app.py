import streamlit as st
import numpy as np
import plotly.express as px
from tensorflow.keras.models import load_model
from streamlit_drawable_canvas import st_canvas

# Meta Data
st.set_page_config(
    page_title="STAT 4185: Final Project Demo" # For the Tab title
)

# Project Details 
st.write("""
# STAT 4185: Final Project Demo

*This is a demo of the final project. For the final project, you must create your project on Streamlit and host it on Heroku. Please include a brief project description, step-by-step instructions for using the app, and a link to the GitHub repository hosting the project's annotated source code somewhere in your app.*


This simple app turns numerical handwriting into predicted values. A CNN-Dense architectural model and the MNIST data set were utilized to train the tensorflow model that powers this app. The GitHub Repository for this project can be found [here](https://github.com/venkata14/stat4185-teaching-material) under the "final-demo" folder.

---
""")

# Load model
# @st.cache 
def load_tfmodel():
    path = "models/final_model.h5"
    return load_model(path)
model = load_tfmodel()

# Columns for the canvas and instructions
c_col1, c_col2 = st.columns(2, gap="large")

with c_col1:
    st.write(
        """
        ### Instructions 

        1. Choose an appropriate Stroke Width. 
            - Changes in Stroke Width can improve results.
        2. Draw a number on the canvas.
            - The best predictions come from drawings that are centered as the model is trained on centered images.
        3. Press "Predict" and scroll down to see the prediction curve. 
        """
    )
    # Changing Stroke Width can improve results
    stroke_width = st.slider("Stroke width: ", 15, 25, 21)
with c_col2:
    st.write(
        "### Draw a Number"
    )
    # Setting up the Canvas. https://github.com/andfanilo/streamlit-drawable-canvas
    canvas_result = st_canvas(
        stroke_width=stroke_width,
        stroke_color="white",
        background_color="#000000",
        height=280,
        width=280,
        drawing_mode="freedraw",
    )

# Displaying the altered Images when click predict
if st.button("Predict"):
    col1, col2 = st.columns([1,1])

    if canvas_result.json_data is not None:
        # Grayscale image
        with col1:
            st.write("# Full Image")
            st.write("The model is trained on 28 x 28 images. This image needs to be resized for proper prediction.")
            rgb_weights = [0.2989, 0.5870, 0.1140]
            grayscale_image = np.dot(canvas_result.image_data[...,:3], rgb_weights)
            gray_fig = px.imshow(grayscale_image, binary_string=True)
            st.plotly_chart(gray_fig, use_container_width=True)

        # Resize Image
        with col2:
            st.write("# Resized Image")
            st.write("This the the resulting image when resized with the max pooling method. ")
            M, N = grayscale_image.shape
            K = 10
            MK = M // K
            NK = N // K
            resize_image = grayscale_image[:MK*K, :NK*K].reshape(MK, K, NK, K).max(axis=(1, 3))
            resize_fig = px.imshow(resize_image, binary_string=True)
            st.plotly_chart(resize_fig, use_container_width=True)


        # Not Needed
        # # Sharpen the image Image
        # crisp_image = np.where(resize_image > 50, 255, 0)
        # crisp_fig = px.imshow(crisp_image, binary_string=True)
        # st.plotly_chart(crisp_fig)
        
        # Out the predicted Softmax probabilities
        resize_image = resize_image.reshape((-1, 28,28,1)) # Needs to me reshaped for 1) the -1 at the top shows that this is one of possible multiple images. Python will figure out how many images there are and 2) the 1 at the end is to show that this is gray scale.
        # Get model prediction
        org_prediction = model.predict(resize_image)
        org_prediction = org_prediction.tolist()
        # Graph the predictions
        prediction_fig = px.bar(
                            x=range(0,10), 
                            y=org_prediction
                            )
        prediction_fig.update_layout(
                            showlegend=False,
                            xaxis_title="Possible Values",
                            title="Predictions"
                            )
        prediction_fig.update_layout(
                            xaxis = dict(
                                tickmode = 'linear',
                            ),
                            yaxis = dict(
                                visible = False
                            )
                        )
        st.plotly_chart(prediction_fig, use_container_width=True)