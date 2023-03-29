
# Import libraries
import streamlit as st
import extract_eml as exeml 
from random import randint


# =====================================================================================================================


# Function to display email eml page
def showEmailEMLPage() :


    # Adjust length of button
    st.write(
        """
        <style>
        [class="row-widget stButton"] button {
            width: 100%;
            background-color: #FD6767;
        }
        [class="row-widget stDownloadButton"] button {
            width: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # =====================================================================================================================

    # To store file uploader widget key value
    if 'eml_randomizer' not in st.session_state: 
        st.session_state['eml_randomizer'] = str(randint(1000, 100000000))

    # To store disable triggers for start button
    if 'eml_disable_start' not in st.session_state :
        st.session_state['eml_disable_start'] = True
    
    # To store disable triggers for export button
    if 'eml_disable_export' not in st.session_state :
        st.session_state['eml_disable_export'] = True
    
    # To store output table
    if 'eml_output_table' not in st.session_state:
        st.session_state['eml_output_table'] = []

    # To store top accounts dataframe
    if 'eml_top_accounts' not in st.session_state:
        st.session_state['eml_top_accounts'] = []
    
    # To store show export buttons boolean
    if 'eml_show_export' not in st.session_state :
        st.session_state['eml_show_export'] = False


    # =====================================================================================================================


    # Set page title
    st.title('Extract EML :e-mail:')

    # Create space
    st.write('')


    # =====================================================================================================================


    # First step -- Convert Email
    st.subheader(':one: Convert EML Files')

    # Create space
    st.write('')

    # 
    st.write(':link: *Download emails from [Outlook Web](https://outlook.office.com/mail/) , and convert them \
             to web pages using [Online Converter](https://www.aconvert.com/document/eml-to-html/) .*')
    
    # Create space
    st.write('')


    # =====================================================================================================================


    # Second step -- Select Extract Date
    st.subheader(':two: Select Date')

    # Create space
    st.write('')

    # Create date picker for extract date
    extract_date = st.date_input(
        label = 'Date',
        on_change = exeml.clearStoredData,
        label_visibility = 'collapsed'
    )

    # Create space
    st.write('')


    # =====================================================================================================================


    # Third step -- Upload Converted EML files
    st.subheader(':three: Upload HTML Files')
    
    # Create space
    st.write('')
    
    # Create file uploader for HTML files
    eml_uploaded_files = st.file_uploader(
        label = 'Upload HTML files', 
        type = 'html',
        accept_multiple_files = True,
        key = st.session_state['eml_randomizer'],
        on_change = exeml.clearStoredData,
        label_visibility = 'collapsed'
    )

    # When there are uploaded files
    if not eml_uploaded_files :

        # Disable buttons
        st.session_state['eml_disable_start'] = True
        st.session_state['eml_disable_export'] = True
        st.session_state['eml_show_export'] = False

        # Clear out stored data
        st.session_state['eml_output_table'] = []
        st.session_state['eml_top_accounts'] = []

    
    # Create space
    st.write('')
    

    # =====================================================================================================================


    # Fourth step -- Start Extraction
    st.subheader(':four: Start Process')
    
    # Create space
    st.write('')
    
    # Create button for starting process
    start_button = st.button(
        label = '**Extract From All HTML Files**',
        type = 'primary',
        on_click = exeml.showOutput,
        disabled = st.session_state['eml_disable_start']
    )
    
    # When button is pressed
    if start_button :

        # Create spinner for loading
        with st.spinner('In progress...'):

            # Enrich data
            exeml.extractData(eml_uploaded_files, extract_date)
    
    # Create space
    st.write('')

    # There should be categorized files to show any output
    has_output = len(st.session_state['eml_output_table']) > 0

    # When there are output data
    if has_output :

        # Get output table dataframe
        output_df = st.session_state['eml_output_table']

        # Set index to start from 1
        output_df.index += 1

        # Display dataframe
        st.dataframe(output_df, use_container_width = True)


    # Create space
    st.write('')


    # =====================================================================================================================


    # When output data exists 
    if (len(st.session_state['eml_top_accounts']) > 0) :

        # Set compile report button to be in the opposite state of upload csv button
        st.session_state['eml_disable_export'] = not st.session_state['eml_disable_start']

        # Fourth step -- Export All Reports
        st.subheader(':four: Export Compiled Report')
        
        # Create space
        st.write('')

        # Create compile reports button
        compile_button = st.button(
            label = '**Compile All HTML Files**',
            type = 'primary',
            disabled = st.session_state['eml_disable_export']
        )

        # Create space
        st.write('')

        # When compile button pressed
        if compile_button :

            # Enable the download button to be shown
            st.session_state['eml_show_export'] = True
        
        # When compile button not pressed and is in disabled state
        elif st.session_state['eml_disable_export'] :

            # Enable the download button to be shown
            st.session_state['eml_show_export'] = False

        # When allowed to show download button
        if st.session_state['eml_show_export'] :

            # Compile reports and display download button
            exeml.compileReports(extract_date)

            # Create space
            st.write('')

            # Create checkbox for restart
            if st.checkbox(':arrows_counterclockwise: Restart') :

                # Change the key of the file uploader
                st.session_state['eml_randomizer'] = str(randint(1000, 100000000))

                # Disable buttons
                st.session_state['eml_disable_start'] = True
                st.session_state['eml_disable_export'] = True
                st.session_state['eml_show_export'] = False

                # Clear out stored data
                st.session_state['eml_output_table'] = []
                st.session_state['eml_top_accounts'] = []

                # Rerun the page
                st.experimental_rerun()


