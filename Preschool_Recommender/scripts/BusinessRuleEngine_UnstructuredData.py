import os
import pandas as pd

# Define file paths and directories
INPUT_FEES_EXCEL = 'filled_combined_preschool_list_with_fees.csv'
USER_INPUT_FILE = 'UserInput.csv'
OUTPUT_FILE_WITH_CONSTRAINT = 'WithConstraintPreschoolsUnstructedData.csv'
OUTPUT_FILE = 'FilteredPreschoolsUnstructedData.csv'
INPUT_DIRECTORY = ".//resources//BusinessRulesEngine//BusinessRulesEngine_Input_Files"
OUTPUT_DIRECTORY = ".//resources//BusinessRulesEngine//BusinessRulesEngine_Output_Files"

# Create directories if they don't exist
if not os.path.exists(INPUT_DIRECTORY):
    os.mkdir(INPUT_DIRECTORY)
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

# Define full file paths
input_file = os.path.join(INPUT_DIRECTORY, INPUT_FEES_EXCEL)
# user_input_file = os.path.join(INPUT_DIRECTORY, USER_INPUT_FILE)
output_file_with_constraint = os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILE_WITH_CONSTRAINT)
output_file = os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILE)

# Read input files
preschool_details = pd.read_csv(input_file)

# insert user input as dummy data first until able to fetch from front end in csv file
# user_input = pd.read_csv(user_input_file)

user_fees_sc_infant_care = 0 #user_fees_sc_infant_care = user_input['User_Preferred_Fees_SC_Infant_Care']
user_fees_sc_playgroup = 0
user_fees_sc_nursery = 1000
user_fees_sc_kindergarten = 0
user_fees_pr_infant_care = 0
user_fees_pr_playgroup = 0
user_fees_pr_nursery = 0 
user_fees_pr_kindergarten = 0
user_level = 3 #user_level = user_input['User_Preferred_Levels'] # 1 - Infant Care, 2 - Playgroup, 3 - Nursery, 4 - Kindergarten

#setting Within_Fees_Constraint and Within_Levels_Constraint and save to a csv
# List of all user_fees variables and corresponding column names
user_fees_list = [('user_fees_sc_infant_care', 'fees_sc_infant_care'),
                  ('user_fees_sc_playgroup', 'fees_sc_playgroup'),
                  ('user_fees_sc_nursery', 'fees_sc_nursery'),
                  ('user_fees_sc_kindergarten', 'fees_sc_kindergarten'),
                  ('user_fees_pr_infant_care', 'fees_pr_infant_care'),
                  ('user_fees_pr_playgroup', 'fees_pr_playgroup'),
                  ('user_fees_pr_nursery', 'fees_pr_nursery'),
                  ('user_fees_pr_kindergarten', 'fees_pr_kindergarten')]

# Initialize the column
preschool_details['Within_Fees_Constraint'] = 0

# Iterate over the user_fees variables
for user_fee, column in user_fees_list:
    if globals()[user_fee] != 0:  # Check if the user_fee is not 0
        # Update 'Within_Fees_Constraint' based on the condition
        preschool_details.loc[preschool_details[column] <= globals()[user_fee], 'Within_Fees_Constraint'] = 1
        preschool_details.loc[pd.isna(preschool_details[column]), 'Within_Fees_Constraint'] = 0
        
# User level mapping to DataFrame columns
user_level_mapping = {1: 'levels_infant_care', 2: 'levels_playgroup', 3: 'levels_nursery', 4: 'levels_kindergarten'}


# Corresponding column in the DataFrame
level_column = user_level_mapping[user_level]

# Update 'Within_Levels_Constraint' based on the condition
preschool_details['Within_Levels_Constraint'] = (preschool_details[level_column] == 1).astype(int)



# save to csv
# Get a list of all the column names
cols = list(preschool_details.columns)

# Rearrange the columns by inserting 'Within_Fees_Constraint' after 'fees_pr_kindergarten'
cols.insert(cols.index('fees_pr_kindergarten') + 1, cols.pop(cols.index('Within_Fees_Constraint')))

# Reindex the DataFrame with the new column order
preschool_details = preschool_details.reindex(columns=cols)

# add Within_Levels_Constraint after levels_kindergarten  
cols = list(preschool_details.columns)

# Rearrange the columns by inserting 'Within_Levels_Constraint' after 'levels_kindergarten'
cols.insert(cols.index('levels_kindergarten') + 1, cols.pop(cols.index('Within_Levels_Constraint')))

# Reindex the DataFrame with the new column order
preschool_details = preschool_details.reindex(columns=cols)

try:
    # Save output file
    # preschool_details.to_csv(output_file, index=False)
    preschool_details.to_csv(output_file_with_constraint, index=False)
    # print(f"Output saved to: {output_file}")
except Exception as e:
    print(f"An error occurred while saving the file: {e}")
    
# Filter and save only those preschools that meet all of the constraints
filtered_preschools = preschool_details[
    (preschool_details['Within_Fees_Constraint'] == 1) &
    (preschool_details['Within_Levels_Constraint'] == 1) 
]
filtered_preschools.to_csv(output_file, index=False)