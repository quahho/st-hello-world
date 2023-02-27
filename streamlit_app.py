import yaml
import streamlit as st
import streamlit_authenticator as stauth

# # Test code
# st.write('Hello world!')

# hashed_passwords = stauth.Hasher(['The6thSense']).generate()
# st.write(hashed_passwords)

# Import the YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# Create the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


# col1, col2, col3 = st.columns([1, 2, 1])

# with col2:
#    name, authentication_status, email = authenticator.login('Login', 'main')



# Render the login widget by providing a name for the form and its location
name, authentication_status, email = authenticator.login('Login', 'sidebar')


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.title('Some content')

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] == None:
    st.sidebar.warning('Please enter your username and password')
