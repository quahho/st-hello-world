
# Import libraries
import streamlit as st
import pandas as pd
import copy
from random import randint


# =====================================================================================================================


# Function to ensure uploaded campaign list is perfect
def checkCampaignList(campaign_list) :

    # Anticipate errors in the code below
    try :

        # Read file content into a dataframe
        df = pd.read_csv(campaign_list)

        # When file's columns doesnt match expected columns
        if list(df.columns) != ['Campaign ID', 'Campaign Name'] :

            # Disable other widgets in the page
            st.session_state['env_bs_disable_step_2_and_3_and_4'] = True

            # Display error message
            st.error('Invalid file content. Please ensure file contains *Campaign ID* and *Campaign Name* fields.')

        # When file does not contain any campaign data but the field names are present
        elif df.empty :

            # Disable other widgets in the page
            st.session_state['env_bs_disable_step_2_and_3_and_4'] = True

            # Display error message
            st.error('Missing file content. Please ensure file contains records of *Campaign ID* and *Campaign Name*.')
            
        # When file contains duplicate combinations of campaign id and campaign name
        elif len(df[df.duplicated()]) > 0 :

            # Disable other widgets in the page
            st.session_state['env_bs_disable_step_2_and_3_and_4'] = True

            # Display error message
            st.error('There are duplicate combinations of *Campaign ID* and *Campaign Name* found.')
            
        # When file's columns matches expected columns
        else :
            
            # Enable other widgets in the page
            st.session_state['env_bs_disable_step_2_and_3_and_4'] = False

            # Hide uploaded campaign list
            with st.expander('*View uploaded campaign list*'):

                # Set index to start from 1
                df.index += 1
                
                # Display dataframe
                st.dataframe(df)

            # Return dataframe
            return df

    # When the file is completely empty
    except pd.errors.EmptyDataError :

        # Disable other widgets in the page
        st.session_state['env_bs_disable_step_2_and_3_and_4'] = True

        # Display error message
        st.error('There is nothing in this file, please ensure there is content in file.')
    
    # When the file is not a perfect table
    except pd.errors.ParserError :

        # Disable other widgets in the page
        st.session_state['env_bs_disable_step_2_and_3_and_4'] = True

        # Display error message
        st.error('Invalid file content. Please ensure file contains *Campaign ID* and *Campaign Name* fields.')


# Function to obtain campaign id
def getCampaignInfo(campaign_df, campaign_choice) :

    # Get selected campaign info
    campaign_info = campaign_df[campaign_df['Campaign Name'] == campaign_choice]

    # Store campaign info in a dictionary 
    campaign_info_dict = campaign_info.to_dict('records')[0]

    # Return campaign info dictionary
    return campaign_info_dict


# Function to ensure uploaded CSV file is a perfect table
def checkCSVFiles(uploaded_files) :

    # Reset problematic file trigger when redo 
    st.session_state['env_bs_any_problematic_files'] = False

    # Initialize lists
    file_names_list = []
    dataframe_list = []

    # Go through each file
    for file in uploaded_files :

        # Create copies of the file for handling imperfect table
        file_copy_1 = copy.deepcopy(file)
        file_copy_2 = copy.deepcopy(file)
        
        # Anticipate errors in the code below
        try :

            # Read file content into a dataframe
            df = pd.read_csv(file)

            # When the file has headers but no rows
            if df.empty :

                # Display error message
                st.error('There are no rows of data in *{x}*.'.format(x = file.name))

                # Set problematic file trigger
                st.session_state['env_bs_any_problematic_files'] = True

                # End iteration
                continue
            
            # When there are nulls appearing in the dataframe
            if (df.isnull().values.any()) and ('Unnamed' in ' '.join(df.columns)) :

                # Drop rows with null values
                df = df.dropna()

                # Set first row of data as columns
                df.columns = df.iloc[0]
                
                # Remove first row of data
                df = df[1:]
            
            # Add dataframe to list
            dataframe_list.append(df)

            # Add file name to list
            file_names_list.append(file.name)
        
        # When the file is completely empty
        except pd.errors.EmptyDataError :

            # Display error message
            st.error('There is nothing at all in *{x}*.'.format(x = file.name))

            # Set problematic file trigger
            st.session_state['env_bs_any_problematic_files'] = True
        
        # When the file is not a perfect table
        except pd.errors.ParserError :

            # Get all rows of the file in a list
            all_rows = file_copy_1.readlines()

            # Initialize max content count
            max_content_count = 0

            # Initialize row number
            row_number = 0

            # Loop through each row
            for row in all_rows :

                # Split row based on comma and only count items that exist
                row_content = [x for x in row.decode().split(',') if len(x) > 0]
                
                # Get number of items in the row
                row_content_count = len(row_content)

                # On the first run
                if max_content_count == 0 :
                    
                    # Accept the first content count
                    max_content_count = row_content_count

                    # Increase row number
                    row_number = row_number + 1
                
                # On the next few rows where content count is the same as the first
                elif max_content_count == row_content_count :
                    
                    # Increase row number
                    row_number = row_number + 1
                
                # Once a different content count is encountered
                elif max_content_count != row_content_count :

                    # Stop counting row number
                    break
            
            # Place file reading code in try block
            try :

                # Read file content into a dataframe while skipping first few rows
                df = pd.read_csv(file_copy_2, skiprows = row_number)

                # Add dataframe to list
                dataframe_list.append(df)

                # Add file name to list
                file_names_list.append(file.name)

            # For handling any possible errors
            except :

                # Display error message
                st.error('There is something very unusual in *{x}*.'.format(x = file.name))

                # Set problematic file trigger
                st.session_state['env_bs_any_problematic_files'] = True

    # Return dataframe list
    return (file_names_list, dataframe_list)


# Function to match columns with template columns
def matchColumns(df_columns, template_columns) :

    # Return boolean response
    return all(field in df_columns for field in template_columns)


# Function to remove columns not found in template columns
def removeColumns(df, template_columns) :

    # Loop over template columns and remove non-template columns
    for column in df.columns :
        if column not in template_columns :
            del df[column]
    
    # Return modified dataframe
    return df


# Function to add the necessary columns
def addColumns(df, campaign_id, extract_date, product) :
    
    # Add the necessary columns
    df['Campaign ID'] = campaign_id
    df['Extract Date'] = extract_date
    df['Product Name'] = product

    # Return modified dataframe
    return df
    

# Function to get file category based on file's columns
def checkCategory(df, campaign_id, extract_date, product) :

    # Check if file was already enriched
    if ('Extract Date' in df.columns) and ('Campaign ID' in df.columns) :

        # Return value
        return 'Already Enriched'

    # ================================================================================================

    # Buying stage accounts fields
    BUYING_STAGE_ACCOUNTS_FIELDS = [
        '6sense Company Name',
        '6sense Domain',
        '6sense Country',
        'Buying Stage: Start',
        'Buying Stage: End',
        'Max Engagement State: Start',
        'Max Engagement State: End',
        'New Pipeline (USD)',
        'Total Won (USD)'
    ]

    # Check fields for match
    if matchColumns(df.columns, BUYING_STAGE_ACCOUNTS_FIELDS) :

        # Remove extra fields
        df = removeColumns(df, BUYING_STAGE_ACCOUNTS_FIELDS)

        # Add necessary fields
        df = addColumns(df, campaign_id, extract_date, product)

        # Clean numerical fields
        for column in df[['New Pipeline (USD)', 'Total Won (USD)']]:
            
            # Replace dollar sign and commas
            df[column].replace("[$,]", "", inplace = True, regex = True)
        

        # When there is no data for this category
        if len(st.session_state['env_bs_buying_stage_accounts']) == 0 :

            # Assign the first dataframe
            st.session_state['env_bs_buying_stage_accounts'] = df

        # When there is data for this category
        else :

            # Get existing dataframe
            old_df = st.session_state['env_bs_buying_stage_accounts']

            # Append new dataframe to the old dataframe
            st.session_state['env_bs_buying_stage_accounts'] = pd.concat([old_df, df], ignore_index=True)

        # Return category
        return 'Buying Stage Accounts'

    # ================================================================================================

    # Buying stage fields
    BUYING_STAGE_FIELDS = [
        'Timeframe',
        'Buying Stage',
        'Number of Accounts',
        'New Pipeline (USD)',
        'Total Won (USD)'
    ]

    # Check fields for match
    if matchColumns(df.columns, BUYING_STAGE_FIELDS) :

        # Remove extra fields
        df = removeColumns(df, BUYING_STAGE_FIELDS)

        # Add necessary fields
        df = addColumns(df, campaign_id, extract_date, product)

        # Remove the older timeframe
        df = df[:-5]

        # Clean numerical fields
        for column in df[['Number of Accounts', 'New Pipeline (USD)', 'Total Won (USD)']]:
            
            # Replace dollar sign and commas
            df[column].replace("[$,]", "", inplace = True, regex = True)


        # When there is no data for this category
        if len(st.session_state['env_bs_buying_stage']) == 0 :

            # Assign the first dataframe
            st.session_state['env_bs_buying_stage'] = df

        # When there is data for this category
        else :

            # Get existing dataframe
            old_df = st.session_state['env_bs_buying_stage']

            # Append new dataframe to the old dataframe
            st.session_state['env_bs_buying_stage'] = pd.concat([old_df, df], ignore_index = True)

        # Return category
        return 'Buying Stage'

    # ================================================================================================
    
    # If reach the end, return not found category
    return 'Unrecognised Content'


# Function to enrich data and remove uploaded CSV file
def startProcess(file_names, dataframes, campaign_info, extract_date, separator) :

    # Enrich data
    enrichData(file_names, dataframes, campaign_info, extract_date, separator)

    # Clears the list of uploaded files
    st.session_state['env_bs_csv_files_randomizer'] = str(randint(1000, 100000000))


# Function to enrich csv files
def enrichData(file_names, dataframes, campaign_info, extract_date, separator) :

    # Go through each dataframes
    for name, df in zip(file_names, dataframes) :

        # Add file name to file history
        st.session_state['env_bs_file_history'].append(name)

        st.session_state['env_bs_product_history'].append(name.split(separator)[0])

        # Add campaign name to campaign history
        st.session_state['env_bs_campaign_history'].append(campaign_info['Campaign Name'])

        # Add batch number to batch history
        st.session_state['env_bs_batch_history'].append(st.session_state['env_bs_batch_number'])

        # Add category to category history
        st.session_state['env_bs_category_history'].append(checkCategory(df, campaign_info['Campaign ID'], extract_date, name.split(separator)[0]))

    # There should be categorized files to show any output
    has_output = len(st.session_state['env_bs_category_history']) > 0
    
    # When there are output data
    if has_output :

        # Increment batch number at the end
        st.session_state['env_bs_batch_number'] += 1
    

# Function to obtain dataframe for process history
def getProcessHistory() :

    # Create dictionary of list
    dict_of_list = {
        'Category': st.session_state['env_bs_category_history'],
        'Batch': st.session_state['env_bs_batch_history'],
        'Campaign Name': st.session_state['env_bs_campaign_history'],
        'Product Name': st.session_state['env_bs_product_history'],
        'File Name': st.session_state['env_bs_file_history']
    }

    # Create dataframe for processed logs 
    process_log_df = pd.DataFrame(dict_of_list)

    # Set index to start from 1
    process_log_df.index += 1

    # Return dataframe
    return process_log_df


# Function to obtain dataframe for category count
def getCategoryAggregate(df) :

    # Create dataframe for category counter
    category_log_df = df.groupby(['Category']).size().reset_index(name = 'File Count')

    # Set index to start from 1
    category_log_df.index += 1

    # Create dataframe containing only valid categories for export
    working_files_df = df[~df['Category'].isin(['Already Enriched', 'Unrecognised Content'])]

    # Pass working files dataframe to session variables
    st.session_state['env_bs_valid_category'] = working_files_df

    # Return dataframe
    return category_log_df


# Function to obtain dataframe for campaign count
def getCampaignAggregate(df) :

    # Create dataframe for campaign counter
    campaign_log_df = df.groupby(['Campaign Name']).size().reset_index(name = 'File Count')

    # Set index to start from 1
    campaign_log_df.index += 1

    # Return dataframe
    return campaign_log_df


# Function to compile reports by category
def compileReports(extract_date) :

    # When there is data for buying stage accounts
    if len(st.session_state['env_bs_buying_stage_accounts']) > 0 :

        # Display download button
        st.download_button(
            label = 'Download Buying Stage Accounts Data',
            data = st.session_state['env_bs_buying_stage_accounts'].to_csv(encoding = 'utf-8-sig', index = False),
            file_name = '[' + str(extract_date) + ']' + ' Compiled Buying Stage Accounts.csv',
            mime = 'text/csv'
        )

    # When there is data for buying stage
    if len(st.session_state['env_bs_buying_stage']) > 0 :

        # Display download button
        st.download_button(
            label = 'Download Buying Stage Data',
            data = st.session_state['env_bs_buying_stage'].to_csv(encoding = 'utf-8-sig', index = False),
            file_name = '[' + str(extract_date) + ']' + ' Compiled Buying Stage.csv',
            mime = 'text/csv'
        )









