import streamlit as st
import numpy as np
import pandas as pd
import keras
from keras.utils.np_utils import to_categorical
from keras.models import Sequential, load_model
from keras import backend as K
import os
import time
import io
from PIL import Image
import plotly.express as px

MODELSPATH = './models/'
DATAPATH = './static/'


def render_header():
    st.write("""
        <p align="center"> 
            <H1> Skin cancer Analyzer 
        </p>

    """, unsafe_allow_html=True)


@st.cache
def load_mekd():
    img = Image.open(DATAPATH + '/ISIC_0024312.jpg')
    return img


@st.cache
def data_gen(x):
    img = np.asarray(Image.open(x).resize((28, 28)))
    x_test = np.asarray(img.tolist())
    x_test_mean = np.mean(x_test)
    x_test_std = np.std(x_test)
    x_test = (x_test - x_test_mean) / x_test_std
    x_validate = x_test.reshape(1, 28, 28, 3)

    return x_validate


@st.cache
def data_gen_(img):
    img = img.reshape(28, 28)
    x_test = np.asarray(img.tolist())
    x_test_mean = np.mean(x_test)
    x_test_std = np.std(x_test)
    x_test = (x_test - x_test_mean) / x_test_std
    x_validate = x_test.reshape(1, 28, 28, 3)

    return x_validate


def load_models():

    model = load_model(MODELSPATH + 'best_model.h5')
    return model


@st.cache
def predict(x_test, model):
    Y_pred = model.predict(x_test)
    #ynew = model.predict_proba(x_test)
    K.clear_session()
    #ynew = np.round(ynew, 2)
    #ynew = ynew*100
    #y_new = ynew[0].tolist()
    K.clear_session()
    #return y_new, Y_pred_classes

    return Y_pred[0]



@st.cache
def display_prediction(Y_pred_classes):
#def display_prediction(y_new):
    """Display image and preditions from model"""

    result = pd.DataFrame({'Probability%': Y_pred_classes}, index=np.arange(7))
    result = result.reset_index()
    result.columns = ['Classes', 'Probability%']
    lesion_type_dict = {2: 'Benign keratosis-like lesions', 4: 'Melanocytic nevi', 3: 'Dermatofibroma',
                        5: 'Melanoma', 6: 'Vascular lesions', 1: 'Basal cell carcinoma', 0: 'Actinic keratoses'}
    result["Classes"] = result["Classes"].map(lesion_type_dict)
    return result


def main():
    st.sidebar.header('Skin cancer Analyzer')
    st.sidebar.subheader('Choose a page to proceed:')
    page = st.sidebar.selectbox("", ["Sample Data", "Upload Your Image"])

    if page == "Sample Data":
        st.header("Sample Data Prediction for Skin Cancer")
        st.markdown("""
        **Now, this is probably why you came here. Let's get you some Predictions**

        You need to choose Sample Data
        """)

        base = ['Sample Data I']
        sample_data = st.multiselect('Choose Sample Data', base)

        if len(sample_data) > 1:
            st.error('Please select Sample Data')
        if len(sample_data) == 1:
            st.success("You have selected Sample Data")
        else:
            st.info('Please select Sample Data')

        if len(sample_data) == 1:
            if st.checkbox('Show Sample Data'):
                st.info("Showing Sample data---->>>")
                image = load_mekd()
                st.image(image, caption='Sample Data', use_column_width=True)
                st.subheader("Click Predict to move forward")
                if st.checkbox('Predict'):
                    model = load_models()
                    st.success("Hooray !! Model Loaded!")
                    if st.checkbox('Show Prediction Probablity on Sample Data'):
                        x_test = data_gen(DATAPATH + '/ISIC_0024312.jpg')
                        Y_pred_classes = predict(x_test, model)*100
                        #y_new, Y_pred_classes = predict(x_test, model)
                        result = display_prediction(Y_pred_classes)
                        st.write(result)
                        if st.checkbox('Display Probability% Graph'):
                            fig = px.bar(result, x="Classes",
                                         y="Probability%", color='Classes')
                            st.plotly_chart(fig, use_container_width=True)

    if page == "Upload Your Image":

        st.header("Upload Your Image")

        file_path = st.file_uploader('Upload an image', type=['png', 'jpg'])

        if file_path is not None:
            x_test = data_gen(file_path)
            image = Image.open(file_path)
            img_array = np.array(image)

            st.success('File Upload Success!!')
        else:
            st.info('Please upload Image file')

        if st.checkbox('Show Uploaded Image'):
            st.info("Showing Uploaded Image ---->>>")
            st.image(img_array, caption='Uploaded Image',
                     use_column_width=True)
            st.subheader("Click Predict to move forward")
            if st.checkbox('Predict'):
                model = load_models()
                st.success("Hooray !! Model Loaded!")
                if st.checkbox('Show Prediction Probablity for Uploaded Image'):
                    Y_pred_classes = predict(x_test, model)*100
                    #y_new, Y_pred_classes = predict(x_test, model)
                    result = display_prediction(Y_pred_classes)
                    st.write(result)
                    if st.checkbox('Display Probability% Graph'):
                        fig = px.bar(result, x="Classes",
                                     y="Probability%", color='Classes')
                        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
