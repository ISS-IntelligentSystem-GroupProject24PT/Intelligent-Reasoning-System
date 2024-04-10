import pandas as pd
import os

def save_to_csv(df):
    df.to_csv('./resources/SchoolPages/SchoolPage_Website_Links/filled_combined_preschool_list_with_fees.csv', index=False)
    
    
# read excel file from here 
# Load the Excel file with search terms
excel_file = './resources/SchoolPages/SchoolPage_Website_Links/filled_combined_preschool_list_with_fees_bk20240410_02.csv'
# df = pd.read_csv(excel_file)
df = pd.read_csv(excel_file, encoding='cp1252')
#print(df.columns)
import pandas as pd

# Assuming df is your DataFrame
columns = ['fees_sc_infant_care','fees_sc_playgroup',
           'fees_sc_nursery','fees_sc_kindergarten',
           'fees_pr_infant_care','fees_pr_playgroup',
           'fees_pr_nursery','fees_pr_kindergarten']

# Initialize the columns
df['found_levels'] = pd.Series([[] for _ in range(len(df))])
df['levels_infant_care'] = 0
df['levels_playgroup'] = 0
df['levels_nursery'] = 0
df['levels_kindergarten'] = 0
# Iterate over the rows
for index, row in df.iterrows():
    try:    
        for col in columns:
            if pd.notna(row[col]):  # Check if the fee is not blank
               
                if col == 'fees_sc_infant_care' or col == 'fees_pr_infant_care':
                    if col == 'fees_sc_infant_care':
                        df.at[index, 'found_levels'].append(col.replace('fees_sc_', ''))  # Append the column name to 'found_levels'
                    # if col == 'fees_pr_infant_care':
                    #     df.at[index, 'found_levels'].append(col.replace('fees_pr', ''))
                    df.at[index, 'levels_infant_care'] = 1  # Update the 'levels_infant_care' column
                
                if col == 'fees_sc_playgroup' or col == 'fees_pr_playgroup':
                    if col == 'fees_sc_playgroup':
                        df.at[index, 'found_levels'].append(col.replace('fees_sc_', ''))  # Append the column name to 'found_levels'
                    # if col == 'fees_pr_playgroup':
                    #     df.at[index, 'found_levels'].append(col.replace('fees_pr', ''))
                    df.at[index, 'levels_playgroup'] = 1  # Update the 'levels_playgroup' column
                if col == 'fees_sc_nursery' or col == 'fees_pr_nursery':
                    if col == 'fees_sc_nursery':
                        df.at[index, 'found_levels'].append(col.replace('fees_sc_', ''))  # Append the column name to 'found_levels'
                    # if col == 'fees_pr_nursery':
                    #     df.at[index, 'found_levels'].append(col.replace('fees_pr', ''))
                    df.at[index, 'levels_nursery'] = 1 # Update the 'levels_nursery' column
                if col == 'fees_sc_kindergarten' or col == 'fees_pr_kindergarten':
                    if col == 'fees_sc_kindergarten':
                        df.at[index, 'found_levels'].append(col.replace('fees_sc_', ''))  # Append the column name to 'found_levels'
                    # if col == 'fees_pr_kindergarten':
                    #     df.at[index, 'found_levels'].append(col.replace('fees_pr', ''))
                    df.at[index, 'levels_kindergarten'] = 1 # Update the 'levels_kindergarten' column
                    
            
    except Exception as e:
        print(f"An error occurred for loop: {e}")
        
save_to_csv(df)