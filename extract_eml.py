
# Import libraries
import copy
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup


# =====================================================================================================================


# Function to clear stored data whenever file upload changes
def clearStoredData() :
    
    # Set process to end
    st.session_state['eml_disable_start'] = False
    
    # Disable buttons
    st.session_state['eml_disable_export'] = True

    # Clear out stored data
    st.session_state['eml_output_table'] = []
    st.session_state['eml_top_accounts'] = []


# Function to disable start button at the end of process
def showOutput() :

    # Disable start button
    st.session_state['eml_disable_start'] = True


# Function to extract data from html files
def extractData(uploaded_files, extract_date) :

    # Loop through each file
    for file in uploaded_files :

        # Initialize session variables
        refreshStorageVariables()

        # Pass file to parser 
        soup = BeautifulSoup(file, "lxml")

        # Get top accounts
        getTopAccounts(soup, extract_date, file.name)


# Function to reset session variables for result data
def refreshStorageVariables() :

    # Intro page variables
    st.session_state['timeframe'] = ''
    st.session_state['segment'] = ''

    # Company info variables
    st.session_state['account_list'] = []
    st.session_state['6QA_list'] = []
    st.session_state['domain_list'] = []
    st.session_state['country_list'] = []
    st.session_state['category_list'] = []

    # 6sense info variables
    st.session_state['buying_stage_list'] = []
    st.session_state['profile_fit_list'] = []
    st.session_state['account_reach_list'] = []

    # Stats info variables
    st.session_state['active_contact_list'] = []
    st.session_state['web_visit_count_list'] = []
    st.session_state['known_contact_count_list'] = []
    st.session_state['anonymous_count_list'] = []
    st.session_state['web_url_list'] = []
    st.session_state['keyword_list'] = []
    st.session_state['bombora_topic_list'] = []
    

# Function to get top accounts
def getTopAccounts(soup, extract_date, file_name) :

    # Get main content html block
    content_table_html = getMainContent(soup)

    # When main_content is found
    if content_table_html != '' :

        # Get intro page related fields
        found_intro_page = getIntroPageContent(content_table_html)

        # Get profile page related fields
        found_profile_page = getProfilePageContent(content_table_html)

        # When both pages are found
        if found_intro_page and found_profile_page :

            # Create dictionary of list for top accounts
            result_dict = {
                'Account Name': st.session_state['account_list'],
                'Is 6QA': st.session_state['6QA_list'],
                'Domain': st.session_state['domain_list'],
                'Country': st.session_state['country_list'],
                'Category': st.session_state['category_list'],
                'Buying Stage': st.session_state['buying_stage_list'],
                'Profile Fit': st.session_state['profile_fit_list'],
                'Account Reach': st.session_state['account_reach_list'],
                'Active Contact': st.session_state['active_contact_list'],
                'Web Visit Count': st.session_state['web_visit_count_list'],
                'Known Contact Count': st.session_state['known_contact_count_list'],
                'Anonymous Count': st.session_state['anonymous_count_list'],
                'Web URLs': st.session_state['web_url_list'],
                'Keywords': st.session_state['keyword_list'],
                'Bombora Company Surge Topics': st.session_state['bombora_topic_list']
            }

            # Create dataframe for top accounts
            result_df = pd.DataFrame(result_dict)
            
            # Add suplementary fields
            result_df['Extract Date'] = extract_date
            result_df['Timeframe'] = st.session_state['timeframe']
            result_df['Segment Name'] = st.session_state['segment']

            # Create dictionary of list for output table
            output_dict = {
                'File Name': [file_name],
                'Segment Name': [st.session_state['segment']],
                'Total Top Accounts': [len(result_df)]
            }

            # Create dataframe for top accounts
            output_df = pd.DataFrame(output_dict)

            # When there are top accounts found
            if len(result_df) > 0 :

                # When there is no data for top accounts
                if len(st.session_state['eml_top_accounts']) == 0 :

                    # Assign the first dataframe
                    st.session_state['eml_top_accounts'] = result_df

                # When there is data for top accounts
                else :

                    # Get existing dataframe
                    old_df = st.session_state['eml_top_accounts']

                    # Append new dataframe to the old dataframe
                    st.session_state['eml_top_accounts'] = old_df.append(result_df, ignore_index = True)
                
                # When there is no data for output table
                if len(st.session_state['eml_output_table']) == 0 :

                    # Assign the first dataframe
                    st.session_state['eml_output_table'] = output_df

                # When there is data for output table
                else :

                    # Get existing dataframe
                    old_df = st.session_state['eml_output_table']

                    # Append new dataframe to the old dataframe
                    st.session_state['eml_output_table'] = old_df.append(output_df, ignore_index = True)


        # When email is incomplete
        else :

            # Create dictionary of list for output table
            output_dict = {
                'File Name': [file_name],
                'Segment Name': ['Not Found'],
                'Total Top Accounts': [0]
            }

            # Create dataframe for top accounts
            output_df = pd.DataFrame(output_dict)

            # When there is no data for output table
            if len(st.session_state['eml_output_table']) == 0 :

                # Assign the first dataframe
                st.session_state['eml_output_table'] = output_df

            # When there is data for output table
            else :

                # Get existing dataframe
                old_df = st.session_state['eml_output_table']

                # Append new dataframe to the old dataframe
                st.session_state['eml_output_table'] = old_df.append(output_df, ignore_index = True)


    # When main content is not found
    else :

        # Create dictionary of list for output table
        output_dict = {
            'File Name': [file_name],
            'Segment Name': ['Unknown'],
            'Total Top Accounts': ['Unknown']
        }

        # Create dataframe for top accounts
        output_df = pd.DataFrame(output_dict)

        # When there is no data for output table
        if len(st.session_state['eml_output_table']) == 0 :

            # Assign the first dataframe
            st.session_state['eml_output_table'] = output_df

        # When there is data for output table
        else :

            # Get existing dataframe
            old_df = st.session_state['eml_output_table']

            # Append new dataframe to the old dataframe
            st.session_state['eml_output_table'] = old_df.append(output_df, ignore_index = True)


# Function to get main content html block
def getMainContent(soup) :

    # Anticipate error
    try :

        # Route: root -> table -> table -> thead + tbody (clean newline rows)
        content_table_html = [x for x in soup.find("table").find("table").contents if x != '\n']

    # When there is error
    except :

        # Set empty string
        content_table_html = ''

    # Return value
    return content_table_html


# Function to get intro page content
def getIntroPageContent(content_table_html) :

    # Anticipate error
    try :

        # Get intro page content
        # Route: content table -> thead -> all tr (clean newline rows)
        intro_page_html = [x for x in content_table_html[0].contents if x != '\n']

    # When there is error
    except:

        # Stop the code here
        return False

    # ================================
    # GET INTRO PAGE BLOCK & FIELDS
    # ================================

    # Anticipate error
    try :

        # Get title content
        # Route: intro page -> 1st tr -> table -> tbody (skipped) -> all tr (clean newline rows)
        title_info_html = [x for x in intro_page_html[0].find("table").find_all("tr") if x != '\n']

        # Get segment name
        # Route: title info -> 3rd tr
        segment = title_info_html[2].text.split(':')[1].strip()

        # Append to segment list
        st.session_state['segment'] = segment
    
    # When there is error
    except :

        # Set empty string
        st.session_state['segment'] = ''
    
    
    # Anticipate error
    try :

        # Get non title content
        # Route: intro page -> 2nd tr -> table -> table -> tbody (skipped) -> tr -> all td (clean newline rows)
        non_title_info_html = [x for x in intro_page_html[1].find("table").find("table").find("tr").contents if x != '\n']

        # Get timeframe of data
        # Route: non title info -> 1st td
        timeframe = non_title_info_html[0].text.split(':')[1].strip()

        # Append to timeframe list
        st.session_state['timeframe'] = timeframe
    
    # When there is error
    except :

        # Set empty string
        st.session_state['timeframe'] = ''
    
    # Return at the end
    return True


# Function to get profile page content
def getProfilePageContent(content_table_html) :

    # Anticipate error
    try:

        # Get account profile pages content
        # content table -> tbody -> tr (skipped) -> td -> all table
        profile_page_html_blocks = [x for x in content_table_html[1].find("td").contents if x.name == 'table']

    # When there is error
    except :

        # Stop the code here
        return False


    # Loop through each block to get each account data
    for block in profile_page_html_blocks:
        
        # Anticipate error
        try :
            
            # Check if the tr's exist in the next nested level
            if 'tr' not in [x.name for x in block.contents] :
                
                # While tr is not found
                while block.find_next().name != 'tr' :
                    
                    # Descend to the next lvl
                    block = block.find_next()
            
            # Route: block -> tbody (if present) -> all tr (clean newline rows and any non tr elements)
            clean_block = [x for x in block.contents if (x != '\n') and (x.name == 'tr')]
            

        # When there is error
        except :

            # Stop the code here
            return False


        # ================================
        # GET COMPANY INFO BLOCK
        # ================================

        # Anticipate error
        try :

            # Get the company info part
            # Route: clean block -> 1st tr -> table -> tbody (clean newline rows)
            company_info_html = [x for x in clean_block[0].find("table").find_all("tr") if x != '\n']

        # When there is error
        except :

            # Stop the code here
            return False
            

        # ================================
        # GET COMPANY INFO FIELDS
        # ================================

        # Anticipate error
        try :

            # Get account
            # Route: company info -> 1st tr -> span
            account = company_info_html[0].find("span").text.strip()

            # Append to account list
            st.session_state['account_list'].append(account)

        # When there is error
        except :

            # Set empty string
            st.session_state['account_list'].append('')


        # Anticipate error
        try :

            # Check for 6QA
            if '6QA' in company_info_html[0].text:

                # Append to 6QA list
                st.session_state['6QA_list'].append(True)
            
            # When no 6QA label
            else :

                # Append to 6QA list
                st.session_state['6QA_list'].append(False)

        # When there is error
        except :

            # Set empty string
            st.session_state['6QA_list'].append('')


        # Anticipate error
        try :

            # Get domain
            # Route: company info -> 2nd tr
            domain = company_info_html[1].text.split(',')[0].strip()

            # Append to domain list
            st.session_state['domain_list'].append(domain)

        # When there is error
        except :

            # Set empty string
            st.session_state['domain_list'].append('')


        # Anticipate error
        try :

            # Get country
            # Route: company info -> 2nd tr
            country = company_info_html[1].text.split(',')[1].strip().replace('\n', '')

            # Append to country list
            st.session_state['country_list'].append(country)

        # When there is error
        except :

            # Set empty string
            st.session_state['country_list'].append('')
        

        # Anticipate error
        try :

            # Get category
            # Route: company info -> 3rd tr -> span
            category = company_info_html[2].find("span").text.title().strip()

            # Append to category list
            st.session_state['category_list'].append(category)

        # When there is error
        except :

            # Set empty string
            st.session_state['category_list'].append('')


        # ================================
        # GET STAT INFO BLOCK
        # ================================

        # Anticipate error
        try :

            # Get the stat info part
            # Route: clean block -> 2nd tr and beyond
            stat_info_html = clean_block[1:]

            # Boolean variables
            has_6sense = False
            has_active = False
            has_webvisit = False
            has_keyword = False
            has_bombora = False

        # When there is error
        except :

            # Set empty string
            st.session_state['buying_stage_list'].append('')
            st.session_state['profile_fit_list'].append('')
            st.session_state['account_reach_list'].append('')
            st.session_state['active_contact_list'].append('')
            st.session_state['web_visit_count_list'].append('')
            st.session_state['known_contact_count_list'].append('')
            st.session_state['anonymous_count_list'].append('')
            st.session_state['web_url_list'].append('')
            st.session_state['keyword_list'].append('')
            st.session_state['bombora_topic_list'].append('')

            # Skip current account
            continue

        
        # ================================
        # GET STAT INFO FIELDS
        # ================================

        # Loop through each possible stat row
        for stat in stat_info_html:

            # Boolean checks 
            buying_stage_present = stat.text.find("Buying Stage") >= 0
            profile_fit_present = stat.text.find("Profile Fit") >= 0
            account_reach_present = stat.text.find("Account Reach") >= 0

            # Check for 6sense info row
            if (not has_6sense) and (buying_stage_present or profile_fit_present or account_reach_present) :

                # Get target line
                # Route: 2nd tr and beyond -> all tr
                target_line = [x for x in stat.contents if x != '\n']

                # Anticipate error
                try :

                    # Get buying stage
                    buying_stage = target_line[0].text.split(':')[-1].strip()

                    # Append to category list
                    st.session_state['buying_stage_list'].append(buying_stage)

                # When there is error
                except :

                    # Set empty string
                    st.session_state['buying_stage_list'].append('')

                
                # Anticipate error
                try :

                    # Get profile fit
                    profile_fit = target_line[1].text.split(':')[-1].strip()

                    # Append to category list
                    st.session_state['profile_fit_list'].append(profile_fit)

                # When there is error
                except :

                    # Set empty string
                    st.session_state['profile_fit_list'].append('')


                # Anticipate error
                try :

                    # Get account reach
                    account_reach = target_line[2].text.split(':')[-1].strip()

                    # Append to category list
                    st.session_state['account_reach_list'].append(account_reach)

                # When there is error
                except :

                    # Set empty string
                    st.session_state['account_reach_list'].append('')
                
                # Set boolean variable
                has_6sense = True 


            # Boolean checks 
            active_contact_present = stat.text.find("Active") >= 0

            # Check for active contact row
            if (not has_active) and (active_contact_present) :
                
                # Get target line
                # Route: 2nd tr and beyond -> table -> tbody -> all tr except 1st tr
                target_line = [x for x in stat.find("table").find_all("tr") if x != '\n'][1:]

                # Anticipate error
                try :

                    # Initialize loop variable
                    i = 0

                    # Initialize contact list
                    contact_list = []

                    # Loop over the contact rows with an interval of 2 (1 is contact info, 1 is contact action)
                    # Stops at the last item since it doesnt have a next item
                    while i < (len(target_line) - 1) :

                        # Get contact name
                        contact_name = target_line[i].find("span").text.strip()

                        # Get contact social
                        contact_social = [x.text.strip() for x in target_line[i].find_all("a")]

                        # Create a to-be-removed list - to remove contact name and contact social from full contact info line
                        contact_social.append(contact_name)
                        removed_stuff_list = list(contact_social)
                        
                        # Get full contact info list
                        full_contact_info_line = target_line[i].text.replace('\n', ' ').strip(',').replace(contact_name, '')
                        full_contact_info_list = full_contact_info_line.split(' ')

                        # Get contact job
                        contact_job = ' '.join([x.strip() for x in full_contact_info_list if x not in removed_stuff_list and len(x) > 0]).strip(',').strip()

                        # Get contact email
                        contact_email = target_line[i].find("a")['href'].split(':')[-1].strip()
                        
                        # Clean action string
                        action_str = [[y.strip() for y in x.text.split(' ') if y != '\n' and len(y) > 0] for x in target_line[i + 1].find_all("li")]

                        # Get contact action
                        # Replace '|' with '-' prior to joining
                        contact_action = ' | '.join([' '.join(x).replace('|', '-') for x in action_str])

                        # Put all contact stuffs together, separated by semi colon
                        # Replace ';' and '//' with '-' prior to joining
                        contact = ( 
                            contact_name.replace(';', '-').replace('//', '-') + '; ' \
                            + contact_email.replace(';', '-').replace('//', '-') + '; ' \
                            + contact_job.replace(';', '-').replace('//', '-') + '; ' \
                            + contact_action.replace(';', '-').replace('//', '-')
                        )

                        # Append to contact list
                        contact_list.append(contact)

                        # Set interval of 2
                        i += 2

                    # Append to active contact list
                    st.session_state['active_contact_list'].append(' // '.join(contact_list))

                # When there is error
                except :

                    # Set empty string
                    st.session_state['active_contact_list'].append('')

                # Set boolean variable
                has_active = True 


            # Boolean checks 
            web_visit_present = stat.text.find("Web Visit") >= 0

            # Check for web visit row
            if (not has_webvisit) and (web_visit_present) :
                
                # Get target line
                # Route: 2nd tr and beyond -> table -> tbody -> all tr except 1st tr
                target_line = stat.find("table").find("tr").text.strip()

                # Replace unique separators to a common separator
                replaced_text = target_line \
                                .replace('\n', '') \
                                .replace('- ', '/') \
                                .replace(', ', '/')
      
                # Split string into its components
                component_list = [x.strip() for x in replaced_text.split('/')]

                # Anticipate error
                try:

                    # Get web visit count
                    web_visit = cleanNumber(component_list[0].split(' ')[0].strip())

                    # Append to web visit count list
                    st.session_state['web_visit_count_list'].append(web_visit)

                # When there is error
                except :
                    
                    # Set empty string
                    st.session_state['web_visit_count_list'].append('')


                # Anticipate error
                try:

                    # Get known contact count
                    known_contact = cleanNumber(component_list[1].split(' ')[0].strip())

                    # Append to known contact count list
                    st.session_state['known_contact_count_list'].append(known_contact)

                # When there is error
                except :
                    
                    # Set empty string
                    st.session_state['known_contact_count_list'].append('')


                # Anticipate error
                try:

                    # Get anonymous count
                    anonymous = cleanNumber(component_list[2].split(' ')[0].strip())

                    # Append to anonymous count list
                    st.session_state['anonymous_count_list'].append(anonymous)

                # When there is error
                except :
                    
                    # Set empty string
                    st.session_state['anonymous_count_list'].append('')


                # Anticipate error
                try:

                    # Get all URLs                    
                    # Route: 2nd tr and beyond -> table -> tbody (skipped) -> all tr
                    raw_url_list = [x.find("a")["href"] for x in stat.find("table").find_all("tr") if x != '\n' and 'href' in str(x)]

                    # Clean raw url list
                    clean_url_list = cleanURL(raw_url_list)

                    # Append to web url list
                    st.session_state['web_url_list'].append(', '.join(clean_url_list))

                # When there is error
                except :
                    
                    # Set empty string
                    st.session_state['web_url_list'].append('')

                # Set boolean variable
                has_webvisit = True 

            
            # Boolean checks 
            keyword_present = stat.text.find("Keyword") >= 0

            # Check for keyword row
            if (not has_keyword) and (keyword_present) :

                # Get target line
                # Route: 2nd tr and beyond -> table -> tbody (skipped) -> last tr -> all span
                target_line = [x for x in stat.find("table").find_all("tr") if x != '\n'][-1].find_all("span")

                # Anticipate error
                try :

                    # Combine the list elements together and remove empty elements
                    keywords_array = [x.text.strip().replace(',', '-') for x in target_line if len(x.text.strip()) > 0]

                    # Append to profile fit list
                    st.session_state['keyword_list'].append(', '.join(keywords_array))

                # When there is error
                except :
                    
                    # Set empty string
                    st.session_state['keyword_list'].append('')

                # Set boolean variable
                has_keyword = True 


            # Boolean checks 
            intent_present = stat.text.find("Intent") >= 0

            # Check for bombora row
            if (not has_bombora) and (intent_present) :

                # Get target line
                # Route: 2nd tr and beyond -> table -> tbody (skipped) -> last tr -> all span
                target_line = stat.find("table").find_all("tr")[-1].text

                # Anticipate error
                try :

                    # Get bombora topic
                    bombora_topic = target_line.split(':')[-1].strip()

                    # Append to bombora topic list
                    st.session_state['bombora_topic_list'].append(bombora_topic)

                # When there is error
                except :
                    
                    # Set empty string
                    st.session_state['bombora_topic_list'].append('')

                # Set boolean variable
                has_bombora = True 


        # Insert empty strings when no occasional data
        
        # Case when no 6sense info row
        if has_6sense == False :

            # Set empty strings
            st.session_state['buying_stage_list'].append('')
            st.session_state['profile_fit_list'].append('')
            st.session_state['account_reach_list'].append('')

        # Case when no active contact row
        if has_active == False :

            # Set empty string
            st.session_state['active_contact_list'].append('')

        # Case when no web visit row
        if has_webvisit == False  :

            # Set empty strings
            st.session_state['web_visit_count_list'].append('')
            st.session_state['known_contact_count_list'].append('')
            st.session_state['anonymous_count_list'].append('')
            st.session_state['web_url_list'].append('')

        # Case when no keyword row
        if has_keyword == False :

            # Set empty string
            st.session_state['keyword_list'].append('')

        # Case when no bombora row
        if has_bombora == False :

            # Set empty string
            st.session_state['bombora_topic_list'].append('')


    # Return at the end
    return True


# Function to clean web urls
def cleanURL(raw_url_list) :

    # Initialize variable
    clean_url_list = []

    # Loop through each raw url
    for url in raw_url_list :

        # Replace special characters in url
        replaced_url = url \
                        .replace('%3D', '=') \
                        .replace('%3A', ':') \
                        .replace('%2F', '/') \
                        .replace('%25', '%') \
                        .replace('%20', ' ') \
                        .replace('%26', '&') \
        
        # Split raw url to obtain the real url
        split_url = replaced_url.split('redirect=')[-1].split('&event=')[0]

        # Append to clean url list
        clean_url_list.append(split_url)

    # Return list
    return clean_url_list


# Function for cleaning numbers
def cleanNumber(number) :

    # When number is a currency
    if '%' not in number :

        # Remove dollar sign and comma
        return number.strip().replace(',', '').replace('$', '')
    
    # When number is a percentage
    else :

        # Remove percentage and convert to decimal
        return str(round(float(number.strip().replace('%', '')) / 100, 5))


# Function to compile report
def compileReports(extract_date) :

    # Display download button
    st.download_button(
        label = 'Download Top Accounts Data',
        data = st.session_state['eml_top_accounts'].to_csv(encoding = 'utf-8-sig', index = False),
        file_name = '[' + str(extract_date) + ']' + ' Compiled Top Accounts Data.csv',
        mime = 'text/csv'
    )

