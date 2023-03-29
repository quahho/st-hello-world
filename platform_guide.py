
# Import libraries
import streamlit as st


# Function to display platform guide page
def showPlatformGuidePage() :

    # Set page title
    st.title('6sense Platform Guide:candle:')

    # Create space
    st.write('')
    st.write('')

    # Set paragraph for Step 1
    st.subheader(':one: Using The App (Enrich CSV)')
    st.write('')
    st.write('')

    st.write("Prepare a CSV file containing two columns; ***Campaign ID*** and ***Campaign Name***.")
    st.write("This CSV file will be known as the campaign list and will be uploaded at the beginning.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-upload-campaign-list.png", use_column_width='auto', caption='A CSV file containing a campaign list being uploaded')
    st.write('')
    st.write('')

    st.write("The dropdown in the next step will be populated with campaign names found in the campaign list.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-campaign-option.png", use_column_width='auto', caption='List of campaign names appears in the dropdown')
    st.write('')
    st.write('')

    st.write("To start the process, select a campaign from the dropdown and upload CSV files tied to that campaign.")
    st.write("Press the start button to begin the enrichment process.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-1st-start-process.png", use_column_width='auto', caption='Download option found in the list')
    st.write('')
    st.write('')

    st.write("When the enrichment is done, the file uploader clears itself in preparation for the process to repeat.")
    st.write("A summary of the enrichment is shown in an output table in two separate tabs.")
    st.write("One tab shows the category of data found in the enriched CSV.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-category-result.png", use_column_width='auto', caption='Categories found in the enriched CSV files shown in an output table')
    st.write('')
    st.write('')

    st.write("The second tab shows the campaigns that have selected for the enrichment process.")
    st.write("There is a counter too, to help keep track of the total campaigns that has been covered.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-track-selected-campaigns.png", use_column_width='auto', caption='Campaigns that have already been selected for enrichment will be shown')
    st.write('')
    st.write('')
    
    st.write("The process repeats itself; first selecting a different campaign in the dropdown.")
    st.write("And then uploading CSV files related to that campaign, and finally clicking the start button.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-2nd-start-process.png", use_column_width='auto', caption='Select a different campaign, upload files related to it, and press start, rinse and repeat')
    st.write('')
    st.write('')
    
    st.write("You can stop the process at any given time by jumping straight to compiling the reports.")
    st.write("But ideally, it would be best to continue until all campaigns have been covered.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-covered-all-campaigns.png", use_column_width='auto', caption='The counter reaching a fraction of 1, signalling all campaigns have been selected')
    st.write('')
    st.write('')
    
    st.write("When all campaigns have been covered, press the export button to obtain the download links.")
    st.write("There will be a download link for all categories of data found during the enrichment.")
    st.write("A refresh checkbox will appear at the end to reset the process and start from scratch.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-csv-export-reports.png", use_column_width='auto', caption='The Download buttons appear after the Compile button is pressed')
    st.write('')
    st.write('')

    st.write("""
    The categories of data found in **Enrich CSV** are listed below:
    - Target Accounts
    - Reached Accounts
    - Comparison Chart
    - Ads Overview
    - Job Levels & Functions
    - Buying Stage Accounts
    - Buying Stages
    """)
    st.write("🔗 [Sample Data](https://github.com/quahho/st-hello-world/tree/main/sample-data) | [Github Download Guide](https://blog.hubspot.com/website/download-from-github)")
    st.markdown("---")

    # Set paragraph for Step 2
    st.subheader(':two: Using The App (Extract HTML)')
    st.write('')
    st.write('')

    st.write("Upload saved web pages into the file uploader and press the start button to begin the extraction process.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-html-start-process.png", use_column_width='auto', caption='Uploaded HTML files ready to be processed')
    st.write('')
    st.write('')

    st.write("When the extraction is done, a summary of the extraction is shown in an output table.")
    st.write("Press the export button to obtain the download link for each category of data found.")
    st.write("A refresh checkbox will appear at the end to reset the process and start from scratch.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/pltf-html-export-reports.png", use_column_width='auto', caption='The Download buttons appear after the Compile button is pressed')
    st.write('')
    st.write('')
    
    st.write("""
    The categories of data found in **Extract HTML** are listed below:
    - Summary Data
    - Device Type Distribution
    """)
    st.write("🔗 [Sample Data](https://github.com/quahho/st-hello-world/tree/main/sample-data) | [Github Download Guide](https://blog.hubspot.com/website/download-from-github)")