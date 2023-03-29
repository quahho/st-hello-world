
# Import libraries
import streamlit as st
import enrich_csv as encsv
from random import randint


# =====================================================================================================================


# Function to display platform csv page
def showPlatformCSVPage() :

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

    # =================================================================================

    # To store disable triggers for steps in the process
    if 'pltf_disabled' not in st.session_state :
        st.session_state['pltf_disable_step_2_and_3'] = True
        st.session_state['pltf_disable_step_4'] = True
        st.session_state['pltf_disable_step_5'] = True

    # To store random uploader widget key value for clearing uploaded csv files
    if 'pltf_campaign_list_randomizer' not in st.session_state: 
        st.session_state['pltf_campaign_list_randomizer'] = str(randint(1000, 100000000))

    # To store random uploader widget key value for clearing uploaded csv files
    if 'pltf_csv_files_randomizer' not in st.session_state: 
        st.session_state['pltf_csv_files_randomizer'] = str(randint(1000, 100000000))

    # To store problematic file check boolean
    if 'pltf_any_problematic_files' not in st.session_state: 
        st.session_state['pltf_any_problematic_files'] = False

    # To store show export buttons boolean
    if 'pltf_show_export' not in st.session_state :
        st.session_state['pltf_show_export'] = False

    # =================================================================================

    # To store list of enriched file name
    if 'pltf_file_history' not in st.session_state :
        st.session_state['pltf_file_history'] = []
    
    # To store list of selected campaign
    if 'pltf_campaign_history' not in st.session_state :
        st.session_state['pltf_campaign_history'] = []

    # To store list of found category
    if 'pltf_category_history' not in st.session_state :
        st.session_state['pltf_category_history'] = []
    
    # To store list of batch number
    if 'pltf_batch_history' not in st.session_state :
        st.session_state['pltf_batch_history'] = []

    # To store current iteration of the process
    if 'pltf_batch_number' not in st.session_state :
        st.session_state['pltf_batch_number'] = 1

    # =================================================================================

    # To store list of valid category
    if 'pltf_valid_category' not in st.session_state :
        st.session_state['pltf_valid_category'] = []

    # To store compiled dataframe of target accounts
    if 'pltf_target_accounts' not in st.session_state :
        st.session_state['pltf_target_accounts'] = []

    # To store compiled dataframe of reached accounts
    if 'pltf_reached_accounts' not in st.session_state :
        st.session_state['pltf_reached_accounts'] = []
    
    # To store compiled dataframe of comparison chart
    if 'pltf_comparison_chart' not in st.session_state :
        st.session_state['pltf_comparison_chart'] = []
    
    # To store compiled dataframe of job level function
    if 'pltf_job_level_function' not in st.session_state :
        st.session_state['pltf_job_level_function'] = []
    
    # To store compiled dataframe of ads overview
    if 'pltf_ads_overview' not in st.session_state :
        st.session_state['pltf_ads_overview'] = []
    
    # To store compiled dataframe of buying stage accounts
    if 'pltf_buying_stage_accounts' not in st.session_state :
        st.session_state['pltf_buying_stage_accounts'] = []
    
    # To store compiled dataframe of buying stage
    if 'pltf_buying_stage' not in st.session_state :
        st.session_state['pltf_buying_stage'] = []


    # =====================================================================================================================


    # Set page title
    st.title('Enrich CSV :card_file_box:')

    # Create space
    st.write('')


    # =====================================================================================================================


    # First step -- Upload Campaign List
    st.subheader(':one: Upload Campaign List')

    # Create space
    st.write('')

    # Create file uploader for campaign list
    campaign_list = st.file_uploader(
        label = 'Upload CSV file', 
        type = 'csv',
        key = st.session_state['pltf_campaign_list_randomizer'],
        label_visibility = 'collapsed'
    )

    # Once campaign list is uploaded
    if campaign_list :

        # Check uploaded campaign list and obtain campaign table
        campaign_df = encsv.checkCampaignList(campaign_list)

    # When there is no uploaded campaign list
    else :

        # Disable other widgets in the page
        st.session_state['pltf_disable_step_2_and_3'] = True

        # Clear session variables involved in output log
        st.session_state['pltf_file_history'] = []
        st.session_state['pltf_campaign_history'] = []
        st.session_state['pltf_category_history'] = []
        st.session_state['pltf_batch_history'] = []
        st.session_state['pltf_batch_number'] = 1

        # Clear session variables involved in compiled export
        st.session_state['pltf_valid_category'] = []
        st.session_state['pltf_target_accounts'] = []
        st.session_state['pltf_reached_accounts'] = []
        st.session_state['pltf_comparison_chart'] = []
        st.session_state['pltf_job_level_function'] = []
        st.session_state['pltf_ads_overview'] = []
        st.session_state['pltf_buying_stage_accounts'] = []
        st.session_state['pltf_buying_stage'] = []

        # Hide the download buttons
        st.session_state['pltf_show_export'] = False

    # Create space
    st.write('')


    # =====================================================================================================================


    # Second step -- Select Campaign Name and Extract Date
    st.subheader(':two: Select Campaign and Date')

    # Create equal size columns 
    column_1, column_2 = st.columns([1, 1])

    # In the first column
    with column_1 :

        # When no proper campaign list found
        if st.session_state['pltf_disable_step_2_and_3'] :

            # No options should be available
            campaign_option = []
        
        # When there is a proper campaign list 
        else :

            # Use the list of campaign name
            campaign_option = list(campaign_df['Campaign Name'])

        # Create select box for campaign options
        campaign_choice = st.selectbox(
            label = 'Campaign :',
            options = campaign_option,
            disabled = st.session_state['pltf_disable_step_2_and_3']
        )

        # When there is a campaign selected
        if campaign_choice :

            # Get the selected campaign's info
            campaign_info = encsv.getCampaignInfo(campaign_df, campaign_choice)
        
        # When no campaign is selected
        else :
            
            # Set an empty dictionary
            campaign_info = {}

    # In the second column
    with column_2 :

        # Create date picker for extract date
        extract_date = st.date_input(
            label = 'Date :',
            disabled = st.session_state['pltf_disable_step_2_and_3']
        )

    # Create space
    st.write('')


    # =====================================================================================================================


    # Third step -- Upload CSV files
    st.subheader(':three: Upload CSV Files')
    
    # Create space
    st.write('')
    
    # Create file uploader for CSV files
    uploaded_files = st.file_uploader(
        label = 'Upload CSV files', 
        type = 'csv',
        accept_multiple_files = True,
        key = st.session_state['pltf_csv_files_randomizer'],
        disabled = st.session_state['pltf_disable_step_2_and_3'],
        label_visibility = 'collapsed'
    )

    # When csv files are uploaded
    if uploaded_files :

        # Check uploaded files and obtain file names and cleaned dataframes
        file_names, dataframes = encsv.checkCSVFiles(uploaded_files)

        # If there are any problematic files found
        if st.session_state['pltf_any_problematic_files'] :

            # Disable start process button
            st.session_state['pltf_disable_step_4'] = True

        else :
            # Enable start process button
            st.session_state['pltf_disable_step_4'] = False
    
    # When no file is uploaded
    else :

        # Set the argument lists to empty list
        file_names = []
        dataframes = []

        # Disable start process button
        st.session_state['pltf_disable_step_4'] = True

    # Create space
    st.write('')
    

    # =====================================================================================================================


    # Fourth step -- Start Enrichment
    st.subheader(':four: Start Process')
    
    # Create space
    st.write('')

    # Create button for starting process
    start_button = st.button(
        label = '**Enrich All CSV Files**',
        type = 'primary',
        on_click = encsv.startProcess,
        args = (file_names, dataframes, campaign_info, extract_date),
        disabled = st.session_state['pltf_disable_step_4']
    )

    # There should be categorized files to show any output
    has_output = len(st.session_state['pltf_category_history']) > 0
    
    # When there are output data
    if has_output :

        # Get upload history dataframe
        process_log = encsv.getProcessHistory()

        # Hide uploaded files log
        with st.expander('*View uploaded and processed CSV files*'):
            
            # Display dataframe
            st.dataframe(process_log)

        # Get category aggregate dataframe
        category_aggregate = encsv.getCategoryAggregate(process_log)

        # Set category aggregate label; include the number of valid category files
        category_aggregate_label = 'Total Working Files Processed : **' + str(len(st.session_state['pltf_valid_category'])) + '**'

        # Get campaign aggregate dataframe
        campaign_aggregate = encsv.getCampaignAggregate(process_log)

        # Set campaign aggregate label; include the number of selected campaigns and the total campaigns uploaded
        campaign_aggregate_label = 'Total Unique Campaigns Selected : **' + str(len(campaign_aggregate)) + ' / ' + str(len(campaign_df)) + '**'

        # Create tabs
        tab1, tab2 = st.tabs([category_aggregate_label, campaign_aggregate_label])

        # In the first tab
        with tab1:

            # Display category aggregate dataframe
            st.dataframe(category_aggregate)

        # In the second tab
        with tab2:
            
            # Display campaign aggregate dataframe
            st.dataframe(campaign_aggregate)
    
    # Create space
    st.write('')


    # =====================================================================================================================


    # When valid category exists for export and no new csv files being uploaded
    if (len(st.session_state['pltf_valid_category']) > 0) :

        # Set compile report button to be in the opposite state of upload csv button
        st.session_state['pltf_disable_step_5'] = not st.session_state['pltf_disable_step_4']

        # Fifth step -- Export All Reports
        st.subheader(':five: Export Compiled Reports')
        
        # Create space
        st.write('')

        # Set fine print warning
        st.code('# Repeat steps 2 + 3 + 4 until all campaigns are covered before proceeding.')

        # Create compile reports button
        compile_button = st.button(
            label = '**Compile All CSV Files By Category**',
            type = 'primary',
            disabled = st.session_state['pltf_disable_step_5']
        )

        # Create space
        st.write('')

        # When compile button pressed
        if compile_button :

            # Enable the download buttons to be shown
            st.session_state['pltf_show_export'] = True
        
        # When compile button not pressed and is in disabled state
        elif st.session_state['pltf_disable_step_5'] :

            # Enable the download buttons to be shown
            st.session_state['pltf_show_export'] = False

        # When allowed to show download buttons
        if st.session_state['pltf_show_export'] :

            # Compile reports and display download buttons
            encsv.compileReports(extract_date)

            # Create space
            st.write('')

            # Create checkbox for restart
            if st.checkbox(':arrows_counterclockwise: Restart') :

                # Change the key of the file uploader
                st.session_state['pltf_campaign_list_randomizer'] = str(randint(1000, 100000000))

                # Disable other widgets in the page
                st.session_state['pltf_disable_step_2_and_3'] = True

                # Clear session variables involved in output log
                st.session_state['pltf_file_history'] = []
                st.session_state['pltf_campaign_history'] = []
                st.session_state['pltf_category_history'] = []
                st.session_state['pltf_batch_history'] = []
                st.session_state['pltf_batch_number'] = 1

                # Clear session variables involved in compiled export
                st.session_state['pltf_valid_category'] = []
                st.session_state['pltf_target_accounts'] = []
                st.session_state['pltf_reached_accounts'] = []
                st.session_state['pltf_comparison_chart'] = []
                st.session_state['pltf_job_level_function'] = []
                st.session_state['pltf_ads_overview'] = []
                st.session_state['pltf_buying_stage_accounts'] = []
                st.session_state['pltf_buying_stage'] = []

                # Hide the download buttons
                st.session_state['pltf_show_export'] = False

                # Rerun the page
                st.experimental_rerun()


