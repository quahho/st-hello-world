
# Import libraries
import bcrypt
import streamlit as st
from home import showHomePage

# Set tab info
st.set_page_config(
    page_title="2X | 6sense",
    page_icon="🎏"
)

# ====================================================================================================

# Initialize session variables

# Variable to check user is logged in
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False

# Variable to check user is logged in
if 'failed_attempt' not in st.session_state:
    st.session_state['failed_attempt'] = False

# Variable to set input text field instruction
if 'text_value' not in st.session_state:
    st.session_state['text_value'] = 'Type here'

# Variable to store input text submitted value
if 'code' not in st.session_state:
    st.session_state['code'] = ''


# ====================================================================================================

# Function to handle submitted text
def submitText():

    # Pass the submitted text to session variable
    st.session_state['code'] = st.session_state['text_input']

    # Check the submitted text for a match
    checkCode(st.session_state['code'])


# Function to check if code matches
def checkCode(text_input) :

    # Set real password's hash
    hash = b'$2b$12$ZeHtfYRuDZMwjkCbJWwe7enHtBAOAUnK1O2w/ZxLEK9w6to0TEVhm'

    # Encode the input text
    encoded_text_input = text_input.encode('utf-8')

    # Compare encoded input text with hash
    matched = bcrypt.checkpw(encoded_text_input, hash)

    # Set path for post checking action
    if matched :

        # Change login status for matched
        st.session_state['login_status'] = True
    
    else : 

        # Clear the input text box
        st.session_state['text_input'] = ''

        # Keep login status as before
        st.session_state['login_status'] = False

        # Trigger failed attempt 
        st.session_state['failed_attempt'] = True

        
# Function to display login page
def showLoginPage() :

    # Vertically centre the content of the page 
    st.write(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            padding: 10vh 1vw
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Set the content alignment
    left_space, content, right_space = st.columns([1, 3, 1])

    # Define content
    with content :
    
        # Set logo
        st.image('alt-logo.png')

        # Set the inner content alignment
        inner_left_space, inner_content, inner_right_space = st.columns([1, 3, 1])
        
        # Define inner content
        with inner_content:

            # Create space below picture
            st.write('')

            # Set input text box
            text_input = st.text_input(
                label = 'Enter some text 👇',
                key = 'text_input', 
                type = 'password',
                autocomplete = None,
                on_change = submitText,
                placeholder = st.session_state['text_value'],
                label_visibility = 'collapsed'
            )

            # Show message below input text box
            if not st.session_state['failed_attempt'] :

                # Display guide message
                st.info('Enter access code above.')

            else :
                
                # Display error message
                st.error('Invalid code, try again.')


# ====================================================================================================

# Run main workflow of the page

# Check login status
if not st.session_state['login_status'] :

    # Display login page when not logged in
    showLoginPage()

else :

    # Display home page when logged in
    showHomePage()


# Hide the hamburger icon and "Made with Streamlit" footer
st.write(
    """
    <style>
    # #MainMenu {
    #     visibility: hidden;
    # }
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

