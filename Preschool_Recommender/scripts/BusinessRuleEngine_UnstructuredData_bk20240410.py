import os
import pandas as pd

# Define file paths and directories
INPUT_FILE = 'PreschoolDetails.csv'
USER_INPUT_FILE = 'UserInput.csv'
OUTPUT_FILE = 'FilteredPreschools.csv'
INPUT_DIRECTORY = "..//resources//BusinessRulesEngine//Input_Files"
OUTPUT_DIRECTORY = "..//resources//BusinessRulesEngine//Output_Files"

# Create directories if they don't exist
if not os.path.exists(INPUT_DIRECTORY):
    os.mkdir(INPUT_DIRECTORY)
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

# Define full file paths
input_file = os.path.join(INPUT_DIRECTORY, INPUT_FILE)
user_input_file = os.path.join(INPUT_DIRECTORY, USER_INPUT_FILE)
output_file = os.path.join(OUTPUT_DIRECTORY, OUTPUT_FILE)

# Read input files
preschool_details = pd.read_csv(input_file)
user_input = pd.read_csv(user_input_file)

#check how to read and also for multiple programme and curriculum 
# as long as match one for whole row keep the row 
# Get user input
user_fees = 1500 #user_fees = user_input['User_Preferred_Fees'][0]
user_level = 3 #user_level = user_input['User_Preferred_Levels'][0]
user_programmes =  10, 11, 12  #user_programmes = user_input['User_Preferred_Programmes'][0]
user_curriculum = 7,8,9 #user_curriculum = user_input['User_Preferred_Curriculum'][0]

# Apply business rules
preschool_details['Within_Fees_Constraint'] = (preschool_details['Fees'] <= user_fees).astype(int)
preschool_details['Within_Levels_Constraint'] = (preschool_details['Levels'] == user_level).astype(int)
preschool_details['Within_Programmes_Constraint'] = (preschool_details['Programmes'] == user_programmes).astype(int)
preschool_details['Within_Curriculum_Constraint'] = (preschool_details['Curriculum'] == user_curriculum).astype(int)

# Save output file
preschool_details.to_csv(output_file, index=False)

# Filter and save only those preschools that meet any of the constraints
filtered_preschools = preschool_details[
    (preschool_details['Within_Fees_Constraint'] == 1) |
    (preschool_details['Within_Levels_Constraint'] == 1) |
    (preschool_details['Within_Programmes_Constraint'] == 1) |
    (preschool_details['Within_Curriculum_Constraint'] == 1)
]
filtered_preschools.to_csv(output_file, index=False)