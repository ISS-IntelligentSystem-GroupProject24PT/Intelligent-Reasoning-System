import pandas as pd
import os
import glob
import re
import ast


def save_to_csv(df):
    # df = pd.DataFrame([{'preschool_name': preschool_name, 'txt_file_referenced': txt_file, 
    #                     'found_programmes': found_programmes,
    #                     'programme_enquiries': has_programme_enquiries, 'childcare': has_childcare}])
    if not os.path.isfile('./resources/SchoolPages/SchoolPage_Website_Links/filled_combined_preschool_list.csv'):
        df.to_csv('./resources/SchoolPages/SchoolPage_Website_Links/filled_combined_preschool_list.csv', index=False)
    else: # else it exists so append without writing the header
        df.to_csv('./resources/SchoolPages/SchoolPage_Website_Links/filled_combined_preschool_list.csv', mode='a', header=False, index=False)

    
# read excel file from here 
# Load the Excel file with search terms
excel_file = './resources/SchoolPages/SchoolPage_Website_Links/filled_combined_preschool_list_with_fees.csv'
# df = pd.read_csv(excel_file)
df = pd.read_csv(excel_file, encoding='cp1252')
#print(df.columns)

for index, row in df[['preschool_name','fees_sc_infant_care','fees_sc_playgroup',
                      'fees_sc_nursery','fees_sc_kindergarten',
                      'fees_pr_infant_care','fees_pr_playgroup',
                      'fees_pr_nursery','fees_pr_kindergarten',
                      'found_levels','levels_infant_care','levels_playgroup',
                      'levels_nursery','levels_kindergarten'
                      ]].iterrows():
# for index, row in df[['Preschool_Name']].head(50).iterrows():
    try:
        preschool_name = row['preschool_name']
        print(preschool_name)
        fees_sc_infant_care = row['fees_sc_infant_care']
        fees_sc_playgroup = row['fees_sc_playgroup']
        fees_sc_nursery = row['fees_sc_nursery']
        fees_sc_kindergarten = row['fees_sc_kindergarten']
        fees_pr_infant_care = row['fees_pr_infant_care']
        fees_pr_playgroup = row['fees_pr_playgroup']
        fees_pr_nursery = row['fees_pr_nursery']
        fees_pr_kindergarten = row['fees_pr_kindergarten']
       
        
        # If txt_content is None, continue to the next iteration
        found_levels = []
        if fees_sc_infant_care or fees_pr_infant_care:
            found_levels.append('infant_care')
        if fees_sc_playgroup or fees_pr_playgroup:
            found_levels.append('playgroup')
        if fees_sc_nursery or fees_pr_nursery:
            found_levels.append('nursery')
        if fees_sc_kindergarten or fees_pr_kindergarten:
            found_levels.append('kindergarten')
            
            
        if found_levels is None:
            data[levels + '_' + 'infant_care'] = 0
            data[levels + '_' + 'playgroup'] = 0
            data[levels + '_' + 'nursery'] = 0
            data[levels + '_' + 'kindergarten'] = 0
            df = pd.DataFrame([data])
            save_to_csv(df)
        else: 
            data[levels + '_' + 'infant_care'] = 1
            data[levels + '_' + 'playgroup'] = 1
            data[levels + '_' + 'nursery'] = 1
            data[levels + '_' + 'kindergarten'] = 1
            df = pd.DataFrame([data])
            save_to_csv(df)

    except Exception as e:
        print(f"An error occurred for loop: {e}")