
# Import libraries
import streamlit as st


# Function to display email guide page
def showEmailGuidePage() :

    # Set page title
    st.title('Email Alert Guide:candle:')

    # Create space
    st.write('')
    st.write('')

    # Set paragraph for Step 1
    st.subheader(':one: Download Email From Outlook’s Web Version')
    st.write('')
    st.write('')

    st.write("Proceed to [Outlook Web](https://outlook.office.com/mail/) and sign in to your email account on the site if you haven’t already.")

    st.write("In the inbox section, select the email that you want to download.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-inbox.png", use_column_width='auto', caption='An email being selected in the inbox')
    st.write('')
    st.write('')

    st.write("In the email section, at the top-right corner, click the three dots.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-dots.png", use_column_width='auto', caption='The triple dot being selected at the top right corner of the email')
    st.write('')
    st.write('')

    st.write("In the menu that opens, choose “Download”.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-download.png", use_column_width='auto', caption='Download option found in the list')
    st.write('')
    st.write('')

    st.write("The downloaded email, having the EML extension, will appear in the Downloads folder.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-email-output.png", use_column_width='auto', caption='Downloaded emails in the Downloads folder')
    st.markdown("---")

    # Set paragraph for Step 2
    st.subheader(':two: Convert Email to Web Page Using Online Converter')
    st.write('')
    st.write('')

    st.write("Proceed to [Online Converter](https://www.aconvert.com/document/eml-to-html/) and turn off any ad-blocker to prevent limited usage of the site's services.")

    st.write("In the center of the site, choose the downloaded email to be converted through the 'Choose Files' button.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-choose-file.png", use_column_width='auto', caption='Choose Files button being selected')
    st.write('')
    st.write('')

    st.write("It is possible to choose one or more file(s) at one go in the file explorer that pops out.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-choose-email.png", use_column_width='auto', caption='Downloaded emails being selected')
    st.write('')
    st.write('')

    st.write("After selection of files, click the 'Convert Now' button to start the conversion process.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-convert.png", use_column_width='auto', caption='Convert Now button being selected')
    st.write('')
    st.write('')

    st.write("The converted emails, now as web pages and having the HTML extension, will appear in a result table.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-conversion-result.png", use_column_width='auto', caption='Converted files listed in a table')
    st.markdown("---")

    # Set paragraph for Step 3
    st.subheader(':three: Download Web Page From Generated URL Link')
    st.write('')
    st.write('')

    st.write("In the result table, the generated URL links of the web pages are beside their respective file names.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-generated-link.png", use_column_width='auto', caption='Generated links in the result table')
    st.write('')
    st.write('')

    st.write("To download the web page, right click the generated URL link and select 'Save Link As...' option.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-save-link.png", use_column_width='auto', caption='The Save Link As option being selected')
    st.write('')
    st.write('')

    st.write("In the file explorer that pops out, ensure that the 'Save as type' option is 'HTML Documents (*.html)'.")
    st.write("Before clicking the 'Save' button, rename the file accordingly for ease of identifying it later.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-save-webpage.png", use_column_width='auto', caption='The web page being downloaded')
    st.write('')
    st.write('')

    st.write("The downloaded web pages, having the HTML extension, will appear in the Downloads folder.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-webpage-output.png", use_column_width='auto', caption='Downloaded web pages in the Downloads folder')
    st.markdown("---")

    # Set paragraph for Step 4
    st.subheader(':four: Using The App (Extract EML)')
    st.write('')
    st.write('')

    st.write("With the downloaded web pages ready, proceed to upload them in the file uploader.")
    st.write("Press the start button to begin the extraction process.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-start-process.png", use_column_width='auto', caption='Uploaded HTML files ready to be processed')
    st.write('')
    st.write('')

    st.write("When the extraction is done, a summary of the extraction is shown in an output table.")
    st.write("Press the export button to obtain the download link for the compiled top accounts data.")
    st.write("A refresh checkbox will appear at the end to reset the process and start from scratch.")
    st.image("https://raw.githubusercontent.com/quahho/st-hello-world/main/images/eml-export-report.png", use_column_width='auto', caption='The Download button appears after the Compile button is pressed')
    st.write('')
    st.write('')

    st.write("""
    The categories of data found in **Extract EML** are listed below:
    - Top Accounts
    """)
    st.write("🔗 [Sample Data](https://github.com/quahho/st-hello-world/tree/main/sample-data) | [Github Download Guide](https://blog.hubspot.com/website/download-from-github)")