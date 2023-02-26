import streamlit as st

# Hide the default footer
hide_footer_style = '''
<style>
.reportview-container .main footer {visibility: hidden;}
'''

st.markdown(hide_footer_style, unsafe_allow_html=True)

# Hide the default hamburger menu
hide_menu_style = '''
<style>
#MainMenu {visibility: hidden;}
</style>
'''

st.markdown(hide_menu_style, unsafe_allow_html=True)

# Test code
st.write('Hello world!')
