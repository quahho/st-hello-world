
# Import libraries
import streamlit as st


# ====================================================================================================


# Function to display home page
def showHomePage() :

    # Welcome message
    st.title('Hello, *World!* :sunglasses:')

    # Create space
    st.write('')

    # Intro message
    st.write('Welcome to the one-stop place for prepping 6sense data prior to upload.')

    st.write('If your data comes from...')

    # Create space
    st.write('')

    # First subheader for 6sense platform
    st.subheader(':one: 6sense Platform')

    # Create space
    st.write('')

    # Set directional message
    st.write('And if the data are **exported reports**, then you can **enrich** them in the `Enrich CSV` section.')

    st.write('Else if the data are **saved web pages**, then you can **extract** their content in the `Extract HTML` section.')
    
    # Create space
    st.write('')

    # Continuation message
    st.write('Else if your data comes from...')

    # Create space
    st.write('')

    # Second subheader for 6sense platform
    st.subheader(':two: Email Alert')

    # Create space
    st.write('')

    # Set directional message
    st.write('Then you can **extract** the content of the **saved emails** in the `Extract EML` section.')

    # Create space
    st.write('')

    # Set directional message
    st.write('For further information to go about each section, head over to their respective `Guide` section.')