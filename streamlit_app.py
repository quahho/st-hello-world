import streamlit as st
import tkinter as tk
from tkinter import filedialog
import matplotlib
matplotlib.use('Agg')

st.write('Hello world!')

# Set up tkinter
root = tk.Tk()

# Hide tkinter window
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

# Create folder selector button
if st.button('Choose Folder Containing CSV Subfolders'):

    # Opens file explorer for selection
    st.session_state.csv_folder_path = filedialog.askdirectory(master=root)

# Check the path variable
if len(st.session_state.csv_folder_path) > 0:

    # Print folder path if selected
    st.success(st.session_state.csv_folder_path)

    # List out subfolders in the folder
    st.text('')
    st.markdown('**Subfolders found in the folder:**')

else:
    # Informs if cancel selection
    st.info('No folder has been selected yet...')
