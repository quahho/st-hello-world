
# Import libraries
import streamlit as st


# ====================================================================================================


# Function to handle Home option
def selectOption0() :
    
    # Set the checkbox values
    st.session_state['option_0'] = 1
    st.session_state['option_1'] = 0
    st.session_state['option_2'] = 0
    st.session_state['option_3'] = 0
    st.session_state['option_4'] = 0
    st.session_state['option_5'] = 0


# Function to handle Platform CSV option
def selectOption1() :
    
    # Set the checkbox values
    st.session_state['option_0'] = 0
    st.session_state['option_1'] = 1
    st.session_state['option_2'] = 0
    st.session_state['option_3'] = 0
    st.session_state['option_4'] = 0
    st.session_state['option_5'] = 0


# Function to handle Platform HTML option
def selectOption2() :

    # Set the checkbox values
    st.session_state['option_0'] = 0
    st.session_state['option_1'] = 0
    st.session_state['option_2'] = 1
    st.session_state['option_3'] = 0
    st.session_state['option_4'] = 0
    st.session_state['option_5'] = 0


# Function to handle Platform Guide option
def selectOption3() :

    # Set the checkbox values
    st.session_state['option_0'] = 0
    st.session_state['option_1'] = 0
    st.session_state['option_2'] = 0
    st.session_state['option_3'] = 1
    st.session_state['option_4'] = 0
    st.session_state['option_5'] = 0


# Function to handle Email EML option  
def selectOption4() :

    # Set the checkbox values
    st.session_state['option_0'] = 0
    st.session_state['option_1'] = 0
    st.session_state['option_2'] = 0
    st.session_state['option_3'] = 0
    st.session_state['option_4'] = 1
    st.session_state['option_5'] = 0


# Function to handle Email Guide option  
def selectOption5() :

    # Set the checkbox values
    st.session_state['option_0'] = 0
    st.session_state['option_1'] = 0
    st.session_state['option_2'] = 0
    st.session_state['option_3'] = 0
    st.session_state['option_4'] = 0
    st.session_state['option_5'] = 1


# Function to display navigation bar
def showNavigationBar() :

    # Initialize session variables for checkbox values
    if 'option_0' not in st.session_state :

        # Set the checkbox values
        st.session_state['option_0'] = 1
        st.session_state['option_1'] = 0
        st.session_state['option_2'] = 0
        st.session_state['option_3'] = 0
        st.session_state['option_4'] = 0
        st.session_state['option_5'] = 0

    # Set clout tag
    st.sidebar.caption('By [Vincent Quah](https://bit.ly/3BvREYT) | Handmade in Klang.')

    # Set sidebar title
    st.sidebar.title('Navigation :world_map:')

    # Create home page checkbox
    main_menu = st.sidebar.checkbox(
        label = 'Home :house:', 
        value = st.session_state['option_0'], 
        key = 'Option 0',
        on_change = selectOption0
    )
    
    # Create separation line
    st.sidebar.write('---')

    # Set sidebar header
    st.sidebar.header('6sense Platform :round_pushpin:')

    # Create platform related checkboxes
    platform_csv = st.sidebar.checkbox(
        label = 'Enrich CSV', 
        value = st.session_state['option_1'], 
        key = 'Option 1',
        on_change = selectOption1
    )

    platform_html = st.sidebar.checkbox(
        label = 'Extract HTML', 
        value = st.session_state['option_2'], 
        key = 'Option 2',
        on_change = selectOption2
    )

    platform_guide = st.sidebar.checkbox(
        label = 'Guide', 
        value = st.session_state['option_3'], 
        key = 'Option 3',
        on_change = selectOption3
    )

    # Create separation line
    st.sidebar.write('---')

    # Set sidebar header
    st.sidebar.header('Email Alert :round_pushpin:')

    # Create email related checkboxes
    email_eml = st.sidebar.checkbox(
        label = 'Extract EML', 
        value = st.session_state['option_4'], 
        key = 'Option 4',
        on_change = selectOption4
    )

    email_guide = st.sidebar.checkbox(
        label = 'Guide', 
        value = st.session_state['option_5'], 
        key = 'Option 5',
        on_change = selectOption5
    )

    # Add padding in sidebar
    st.write(
        """
        <style>
        [data-testid="stSidebar"] {
            padding: 0 1vw;
        }
        a {
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

