
# Import libraries
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup


# =====================================================================================================================


# Function to clear stored data whenever file upload changes
def clearStoredData() :
    
    # Set process to end
    st.session_state['html_disable_start'] = False
    
    # Disable buttons
    st.session_state['html_disable_export'] = True
    st.session_state['html_show_export'] = False

    # Clear out stored data
    st.session_state['html_output_table'] = []
    st.session_state['html_device_type'] = []
    st.session_state['html_summary_data'] = []


# Function to disable start button at the end of process
def showOutput() :

    # Disable start button
    st.session_state['html_disable_start'] = True


# Function to extract data from html files
def extractData(uploaded_files, extract_date) :

    # Loop through each file
    for file in uploaded_files :

        # Pass file to parser 
        soup = BeautifulSoup(file, "lxml")

        # Get campaign involved for summary data and device type
        found_summary_and_device = getSummaryAndDevice(soup, extract_date)

        # When there is summary data and device type
        if found_summary_and_device :
            
            # Create dictionary
            row_dict = {
                'File Name': file.name,
                'Summary Data': True,
                'Device Type': True,
                'Unknown': False
            }

        # When there is no data found
        else :

            # Create dictionary
            row_dict = {
                'File Name': file.name,
                'Summary Data': False,
                'Device Type': False,
                'Unknown': True
            }
        
        # Create dataframe
        output_df = pd.DataFrame([row_dict])

        # When there is no data for output table
        if len(st.session_state['html_output_table']) == 0 :

            # Assign the first dataframe
            st.session_state['html_output_table'] = output_df

        # When there is data for output table
        else :

            # Get existing dataframe
            old_df = st.session_state['html_output_table']

            # Append new dataframe to the old dataframe
            st.session_state['html_output_table'] = pd.concat([old_df, output_df], ignore_index = True)


# Function to get summary data and device type data
def getSummaryAndDevice(soup, extract_date) :

    # Get campaign id
    campaign_id = getCampaignID(soup)

    # When campaign id is found
    if campaign_id != '' :

        # Get highlights fields
        highlights = getHighlights(soup)
        total_spent = highlights[0]
        budget = highlights[1]
        accounts_reached = highlights[2]
        
        # Get account analytics fields
        account_analytics = getAccountAnalytics(soup)
        avg_inc_act_eng = account_analytics[0]
        act_newly_eng = account_analytics[1]
        act_with_inc_eng = account_analytics[2]
        
        # Get campaign analytics fields
        campaign_analytics = getCampaignAnalytics(soup)
        ctr = campaign_analytics[0]
        vtr = campaign_analytics[1]
        impressions = campaign_analytics[2]
        clicks = campaign_analytics[3]
        ecpm = campaign_analytics[4]
        views = campaign_analytics[5]
        inf_form_fills = campaign_analytics[6]

        # Get campaign trend fields
        campaign_trend = getCampaignTrend(soup)
        ecpc = campaign_trend[0]
        actr = campaign_trend[1]
        avtr = campaign_trend[2]

        # Create dictionary
        row_dict = {
            'Campaign ID': campaign_id,
            'Extract Date': extract_date,
            'Total Spent': total_spent, 
            'Budget': budget,
            'Accounts Reached': accounts_reached,
            'Avg. Increase in Account Engagement': avg_inc_act_eng, 
            'Accounts Newly Engaged': act_newly_eng, 
            'Accounts With Increased Engagement': act_with_inc_eng,
            'Account CTR': actr, 
            'Account VTR': avtr,
            'CTR': ctr, 
            'VTR': vtr, 
            'Impressions': impressions, 
            'Clicks': clicks, 
            'eCPM': ecpm, 
            'eCPC': ecpc,
            'Views': views, 
            'Influenced Form Fills': inf_form_fills
        }

        # Create dataframe
        summary_df = pd.DataFrame([row_dict])

        # Modify columns of dataframe
        del summary_df['Budget']
        del summary_df['Accounts Reached']

        # When there is no data for summary data
        if len(st.session_state['html_summary_data']) == 0 :

            # Assign the first dataframe
            st.session_state['html_summary_data'] = summary_df

        # When there is data for summary data
        else :

            # Get existing dataframe
            old_df = st.session_state['html_summary_data']

            # Append new dataframe to the old dataframe
            st.session_state['html_summary_data'] = pd.concat([old_df, summary_df], ignore_index = True)
        

        # ==================================================================================================

        # Get device type list of dictionaries
        device_types = getDeviceTypes(soup)

        # Create dataframe
        device_df = pd.DataFrame(device_types)

        # Modify columns of dataframe
        device_df['Campaign ID'] = campaign_id
        device_df['Extract Date'] = extract_date

        # When there is no data for device type
        if len(st.session_state['html_device_type']) == 0 :

            # Assign the first dataframe
            st.session_state['html_device_type'] = device_df

        # When there is data for device type
        else :

            # Get existing dataframe
            old_df = st.session_state['html_device_type']

            # Append new dataframe to the old dataframe
            st.session_state['html_device_type'] = pd.concat([old_df, device_df], ignore_index = True)


        # Return true at the end
        return True


    # When no campaign id is found
    else :

        # Return false
        return False

  
# Function to get campaign id
def getCampaignID(soup) :

    # Anticipate error
    try :
        
        # Get all html block in this section
        html_list = soup.find_all("div", class_="campaignInfoKeyPoints--V-BeF")

        # Get all text from the html blocks
        text_list = [x.text for x in html_list]

        # Initialize variable
        campaign_id = ''

        # Search for campaign id
        for text in text_list :
            
            # When campaign id exists
            if 'Campaign ID' in text :

                # Obtain campaign id
                campaign_id = text.replace('Campaign ID', '')
    
    # When there is an error
    except :

        # Set empty string
        campaign_id = ''

    # Return value
    return campaign_id


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


# Function to get highlights related info
def getHighlights(soup) :

    # Anticipate error
    try :

        # Get all html block in this section
        html_list = soup.find("div", class_="highlights--QIliH")

        # Get all text from the html blocks
        text_list = [x.text for x in html_list]

        # Initialize variable
        total_spent = ''
        budget = ''
        accounts_reached = ''

        # Search for highlights related info
        for text in text_list :
            
            # When total spent exists
            if 'Total Spent' in text :

                # Obtain total spent
                total_spent = cleanNumber(text.replace('Total Spent', '').split('/')[0])

                # Obtain budget
                budget = cleanNumber(text.replace('Total Spent', '').split('/')[1])

            # When accounts reached exists
            elif 'Accounts Reached' in text :

                # Obtain accounts reached
                accounts_reached = cleanNumber(text.replace('Accounts Reached', '').replace('View All', ''))

        # Create list
        highlight_list = [total_spent, budget, accounts_reached]

    # When there is an error
    except :

        # Set empty list
        highlight_list = ['', '', '']

    # Return list
    return highlight_list


# Function to get account analytics related info
def getAccountAnalytics(soup) :

    # Anticipate error
    try :

        # Get all html block in account analytics section
        html_list = soup.find("div", class_="accountAnalytics--2KzuA")

        # Get all text from the html blocks
        text_list = [x.text for x in html_list]

        # Initialize variable
        avg_inc_act_eng = ''
        act_newly_eng = ''
        act_with_inc_eng = ''

        # Search for account analytics related info
        for text in text_list :
            
            # When average increase in account engagement exists
            if 'Avg. Increase in Account Engagement' in text :

                # Obtain average increase in account engagement
                avg_inc_act_eng = cleanNumber(text.replace('Avg. Increase in Account Engagement', ''))

            # When accounts newly engaged exists
            elif 'Accounts Newly Engaged' in text :

                # Obtain accounts reached
                act_newly_eng = cleanNumber(text.replace('Accounts Newly Engaged', ''))

            # When accounts with increased engagement exists
            elif 'Accounts With Increased Engagement' in text :

                # Obtain accounts reached
                act_with_inc_eng = cleanNumber(text.replace('Accounts With Increased Engagement', ''))

        # Create list
        account_analytics_list = [avg_inc_act_eng, act_newly_eng, act_with_inc_eng]

    # When there is an error
    except :

        # Set empty list
        account_analytics_list = ['', '', '']

    # Return list
    return account_analytics_list


# Function to get campaign analytics related info
def getCampaignAnalytics(soup) :

    # Anticipate error
    try :

        # Get all html block in campaign analytics section
        html_list = soup.find("div", class_="campaignAnalytics--1XqIl")

        # Get all text from the html blocks
        text_list = [x.text for x in html_list]

        # Initialize variable
        ctr = ''
        vtr = ''
        impressions = ''
        clicks = ''
        ecpm = ''
        views = ''
        inf_form_fills = ''

        # Search for campaign analytics related info
        for text in text_list :
            
            # When CTR exists
            if 'CTR' in text :

                # Obtain CTR
                ctr = cleanNumber(text.replace('CTR', ''))

            # When VTR exists
            elif 'VTR' in text :

                # Obtain VTR
                vtr = cleanNumber(text.replace('VTR', ''))

            # When impressions exists
            elif 'Impressions' in text :

                # Obtain impressions
                impressions = cleanNumber(text.replace('Impressions', ''))
            
            # When clicks exists
            elif 'Clicks' in text :

                # Obtain clicks
                clicks = cleanNumber(text.replace('Clicks', ''))
            
            # When eCPM exists
            elif 'eCPM' in text :

                # Obtain eCPM
                ecpm = cleanNumber(text.replace('eCPM', ''))
            
            # When view throughs exists
            elif 'View-throughs' in text :

                # view throughs
                views = cleanNumber(text.replace('View-throughs', ''))

            # When influenced form fills exists
            elif 'Influenced Form Fills' in text :

                # Obtain influenced form fills
                inf_form_fills = cleanNumber(text.replace('Influenced Form Fills', ''))

        # Create list
        campaign_analytics_list = [ctr, vtr, impressions, clicks, ecpm, views, inf_form_fills]

    # When there is an error
    except :

        # Set empty list
        campaign_analytics_list = ['', '', '', '', '', '', '']

    # Return list
    return campaign_analytics_list


# Function to get campaign trend related info
def getCampaignTrend(soup) :

    # Anticipate error
    try :

        # Get all html block in campaign trend section - for eCPC
        html_list = soup.find_all("div", class_="flexEnd--_-3M9")

        # Get all text from the html blocks
        text_list = [x.text for x in html_list]

        # Initialize variable
        ecpc = ''

        # Search for campaign trend related info
        for text in text_list :
            
            # When eCPC exists
            if 'eCPC' in text :

                # Obtain eCPC
                ecpc = cleanNumber(text.replace('eCPC:', ''))

    # When there is an error
    except :

        # Set empty string
        ecpc = ''


    # Anticipate error
    try :

        # Get all html block in campaign trend section - for ACTR & AVTR
        html_list = soup.find_all("div", class_="allSidePadding--1DLo7")

        # Get all text from the html blocks
        text_list = [x.text for x in html_list]

        # Initialize variable
        actr = ''
        avtr = ''
    
        # Search for campaign trend related info
        for text in text_list :
            
            # When ACTR exists
            if 'ACTR' in text :

                # Obtain ACTR
                actr = cleanNumber(text.replace('ACTR', ''))

            # When AVTR exists
            elif 'AVTR' in text :

                # Obtain AVTR
                avtr = cleanNumber(text.replace('AVTR', ''))

    # When there is an error
    except :

        # Set empty string
        actr = ''
        avtr = ''


    # Create list
    campaign_trend_list = [ecpc, actr, avtr]

    # Return list
    return campaign_trend_list


# Function to get device types related info
def getDeviceTypes(soup) :

    # Anticipate error
    try :

        # Get all html block in device type section
        html_list = soup.find("div", class_="highcharts-legend highcharts-no-tooltip").select("div.highcharts-legend-item.highcharts-pie-series")

        # Initialize variable
        row_list = []

        # Loop through each html block
        for item in html_list :

            # Get all text from the html blocks
            text_list = [x.text for x in item.find_all("div")]

            # Initialize variable
            device = ''
            accounts_reached = ''
            impressions = ''
            clicks = ''

            # Search for device info
            for text in text_list :
                
                # Get device
                if ('Mobile' in text) or ('Desktop' in text) or ('Tablet' in text) : 

                    # Remove whitespace from text
                    device = text.strip()

                # Get accounts reached
                elif 'Accounts Reached' in text :

                    # Obtain accounts reached
                    accounts_reached = cleanNumber(text.replace('Accounts Reached', ''))

                # Get impressions
                elif 'Impressions' in text :

                    # Obtain impressions
                    impressions = cleanNumber(text.replace('Impressions', ''))

                # Get clicks
                elif 'Clicks' in text :

                    # Obtain clicks
                    clicks = cleanNumber(text.replace('Clicks', ''))

            # Create dictionary
            row_dict = {
                'Device Type': device, 
                'Accounts Reached': accounts_reached, 
                'Impressions': impressions, 
                'Clicks': clicks
            }

            # Append dictionary to list
            row_list.append(row_dict)


    # When there is an error
    except :

        # Set empty list
        row_list = []

    # Return list
    return row_list


# Function to compile reports by category
def compileReports(extract_date) :

    # When there is data for summary data
    if len(st.session_state['html_summary_data']) > 0 :

        # Display download button
        st.download_button(
            label = 'Download Summary Data',
            data = st.session_state['html_summary_data'].to_csv(encoding = 'utf-8-sig', index = False),
            file_name = '[' + str(extract_date) + ']' + ' Compiled Summary Data.csv',
            mime = 'text/csv'
        )

    # When there is data for device types
    if len(st.session_state['html_device_type']) > 0 :

        # Display download button
        st.download_button(
            label = 'Download Device Type Distribution Data',
            data = st.session_state['html_device_type'].to_csv(encoding = 'utf-8-sig', index = False),
            file_name = '[' + str(extract_date) + ']' + ' Compiled Device Type Distribution.csv',
            mime = 'text/csv'
        )


