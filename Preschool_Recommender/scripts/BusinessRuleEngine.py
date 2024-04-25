import math
import os
from datetime import datetime
import pandas as pd
from MatchingAlgorithm import MatchingAlgorithm


class BusinessRulesEngine:
    INPUT_FILE_EXCEL = 'ProcessedGoogleMaps_Output.csv'
    USER_INPUT_FILE = 'FrontEnd_UserInput.csv'
    INPUT_FEES_EXCEL = 'filled_combined_preschool_list_with_fees.csv'
    OUTPUT_FILE = 'BusinessRuleEngine_Distance_OpeningHours_Budget.csv'
    INPUT_FILE_EXCEL_WITH_DATE = f"ProcessedGoogleMaps_Output_{datetime.now().date()}.csv"
    OUTPUT_FILE_WITH_DATE = f"BusinessRuleEngine_Distance_OpeningHours_Budget_{datetime.now().date()}.csv"
    FILTERED_OUTPUT_FILE = 'BusinessRuleEngine_Distance_OpeningHours_Budget_Filtered.csv'
    FILTERED_OUTPUT_FILE_WITH_DATE = f"BusinessRuleEngine_Distance_OpeningHours_Budget_Filtered_{datetime.now().date()}.csv"
    FRONTEND_RULE_ALGO_OUTPUT_FILE = 'Results.csv'
    COMPILED_RESULTS_HISTORY = 'Results_History.csv'

    INPUT_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Input_Files"
    OUTPUT_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Output_Files"
    ARCHIVES_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Archives"
    MATCHING_ALGORITHM_INPUT_DIRECTORY_NAME = "..//resources//MatchingAlgorithm//MatchingAlgorithm_Input_Files"
    MATCHING_ALGORITHM_OUTPUT_DIRECTORY_NAME = "..//resources//MatchingAlgorithm//MatchingAlgorithm_Output_Files"
    FRONTEND_RULE_ALGO_OUTPUT_DIRECTORY_NAME = "..//resources//FrontEnd//FrontEnd_RuleAlgo_Output"
    FRONTEND_USER_INPUTS_DIRECTORY_NAME = "..//resources//FrontEnd//FrontEnd_UserInputs"

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        # Radius of earth in kilometers is about 6371
        km = 6371 * c
        return km

    @staticmethod
    def if_empty_0(x):
        if x > 0:
            x = x
        else:
            x = 0
        return x

    @staticmethod
    def if_empty_100(x):
        if x > 0:
            x = x
        else:
            x = 100
        return x

    def directory_setup(self):
        # Set up directory
        if not os.path.exists(self.INPUT_DIRECTORY_NAME):
            os.mkdir(self.INPUT_DIRECTORY_NAME)

        if not os.path.exists(self.OUTPUT_DIRECTORY_NAME):
            os.mkdir(self.OUTPUT_DIRECTORY_NAME)

        if not os.path.exists(self.ARCHIVES_DIRECTORY_NAME):
            os.mkdir(self.ARCHIVES_DIRECTORY_NAME)

    def trigger_business_rule(self):
        # Set the display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        self.directory_setup()

        # Path Definition
        input_file_excel = os.path.join(self.INPUT_DIRECTORY_NAME, self.INPUT_FILE_EXCEL)
        input_fees_excel = os.path.join(self.INPUT_DIRECTORY_NAME, self.INPUT_FEES_EXCEL)
        input_file_excel_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.INPUT_FILE_EXCEL_WITH_DATE)
        user_input_file = os.path.join(self.FRONTEND_USER_INPUTS_DIRECTORY_NAME, self.USER_INPUT_FILE)
        output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, self.OUTPUT_FILE)
        output_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.OUTPUT_FILE_WITH_DATE)
        filtered_output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, self.FILTERED_OUTPUT_FILE)
        filtered_output_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.FILTERED_OUTPUT_FILE_WITH_DATE)
        output_file_for_matching_algorithm = os.path.join(self.MATCHING_ALGORITHM_INPUT_DIRECTORY_NAME,
                                                          self.FILTERED_OUTPUT_FILE)
        results_history_file = os.path.join(self.MATCHING_ALGORITHM_OUTPUT_DIRECTORY_NAME,
                                            self.COMPILED_RESULTS_HISTORY)
        results = os.path.join(self.FRONTEND_RULE_ALGO_OUTPUT_DIRECTORY_NAME, self.FRONTEND_RULE_ALGO_OUTPUT_FILE)

        # Read input files
        processed_googlemaps = pd.read_csv(input_file_excel)
        processed_schoolpages = pd.read_csv(input_fees_excel)
        processed_schoolpages.rename(columns={'preschool_name': 'Preschool_Name'}, inplace=True)
        user_input = pd.read_csv(user_input_file)
        results_history = pd.read_csv(results_history_file)

        # Get user input
        user_lat = float(user_input['Latitude_Longitude'].item().split(',')[0])
        user_long = float(user_input['Latitude_Longitude'].item().replace(' ', '').split(',')[1])
        user_distance_constraint = user_input['Distance_Constraint'].item()
        user_monday_drop_off = user_input['user_monday_drop_off'].item()
        user_monday_pick_up = user_input['user_monday_pick_up'].item()
        user_tuesday_drop_off = user_input['user_tuesday_drop_off'].item()
        user_tuesday_pick_up = user_input['user_tuesday_pick_up'].item()
        user_wednesday_drop_off = user_input['user_wednesday_drop_off'].item()
        user_wednesday_pick_up = user_input['user_wednesday_pick_up'].item()
        user_thursday_drop_off = user_input['user_thursday_drop_off'].item()
        user_thursday_pick_up = user_input['user_thursday_pick_up'].item()
        user_friday_drop_off = user_input['user_friday_drop_off'].item()
        user_friday_pick_up = user_input['user_friday_pick_up'].item()
        user_saturday_drop_off = user_input['user_saturday_drop_off'].item()
        user_saturday_pick_up = user_input['user_saturday_pick_up'].item()
        user_sunday_drop_off = user_input['user_sunday_drop_off'].item()
        user_sunday_pick_up = user_input['user_sunday_pick_up'].item()

        user_monday_drop_off = self.if_empty_100(user_monday_drop_off)
        user_monday_pick_up = self.if_empty_0(user_monday_pick_up)
        user_tuesday_drop_off = self.if_empty_100(user_tuesday_drop_off)
        user_tuesday_pick_up = self.if_empty_0(user_tuesday_pick_up)
        user_wednesday_drop_off = self.if_empty_100(user_wednesday_drop_off)
        user_wednesday_pick_up = self.if_empty_0(user_wednesday_pick_up)
        user_thursday_drop_off = self.if_empty_100(user_thursday_drop_off)
        user_thursday_pick_up = self.if_empty_0(user_thursday_pick_up)
        user_friday_drop_off = self.if_empty_100(user_friday_drop_off)
        user_friday_pick_up = self.if_empty_0(user_friday_pick_up)
        user_saturday_drop_off = self.if_empty_100(user_saturday_drop_off)
        user_saturday_pick_up = self.if_empty_0(user_saturday_pick_up)
        user_sunday_drop_off = self.if_empty_100(user_sunday_drop_off)
        user_sunday_pick_up = self.if_empty_0(user_sunday_pick_up)

        self.user_fees_sc_infant_care = user_input[
            'Infant_Care_Singaporean'].item()  # user_fees_sc_infant_care = user_input['User_Preferred_Fees_SC_Infant_Care']
        self.user_fees_sc_playgroup = user_input['Playgroup_Singaporean'].item()
        self.user_fees_sc_nursery = user_input['Nursery_Singaporean'].item()
        self.user_fees_sc_kindergarten = user_input['Kindergarten_Singaporean'].item()
        self.user_fees_pr_infant_care = user_input['Infant_Care_PR'].item()
        self.user_fees_pr_playgroup = user_input['Playgroup_PR'].item()
        self.user_fees_pr_nursery = user_input['Nursery_PR'].item()
        self.user_fees_pr_kindergarten = user_input['Kindergarten_PR'].item()

        # Determine level
        # Dictionary of user fees
        user_fees = {
            'infant_care': [self.user_fees_sc_infant_care, self.user_fees_pr_infant_care],
            'playgroup': [self.user_fees_sc_playgroup, self.user_fees_pr_playgroup],
            'nursery': [self.user_fees_sc_nursery, self.user_fees_pr_nursery],
            'kindergarten': [self.user_fees_sc_kindergarten, self.user_fees_pr_kindergarten]
        }
        # Levels dictionary
        levels = {'infant_care': 1, 'playgroup': 2, 'nursery': 3, 'kindergarten': 4}
        # Initialize user_level to None
        user_level = None
        # Check each fee
        for level, fees in user_fees.items():
            # If any fee for this level is non-zero, set user_level to the corresponding level
            if any(fee != 0 for fee in fees):
                user_level = levels[level]
                break

        # Checking if any match with history
        user_input_filled = user_input.drop(columns='Primary_key')
        results_history_filled = results_history.drop(columns='Primary_key').drop_duplicates()
        try:
            filtered_results_history = pd.merge(results_history_filled, user_input_filled, how='inner')
        except Exception as e:
            filtered_results_history = pd.DataFrame()
            print(f"{e}")
        if len(filtered_results_history) > 0:
            filtered_results_history.to_csv(path_or_buf=results, index=False)
        else:
            # Get preschool lat long
            df_lat_long = processed_googlemaps[['Preschool_Name', 'Preschool_Latitude', 'Preschool_Longitude']]
            df_opening_hours = processed_googlemaps[
                [
                    'Preschool_Name',
                    'Monday_Start_Number',
                    'Monday_End_Number',
                    'Tuesday_Start_Number',
                    'Tuesday_End_Number',
                    'Wednesday_Start_Number',
                    'Wednesday_End_Number',
                    'Thursday_Start_Number',
                    'Thursday_End_Number',
                    'Friday_Start_Number',
                    'Friday_End_Number',
                    'Saturday_Start_Number',
                    'Saturday_End_Number',
                    'Sunday_Start_Number',
                    'Sunday_End_Number'
                ]
            ]

            # Distance Calculation
            df_distance = pd.DataFrame(
                columns=['Preschool_Name', 'Preschool_Latitude', 'Preschool_Longitude', 'Distance_To_User_km',
                         'Within_Distance_Constraint'])
            for index, row in df_lat_long.iterrows():
                preschool_name = row['Preschool_Name']
                preschool_latitude = row['Preschool_Latitude']
                preschool_longitude = row['Preschool_Longitude']
                distance = self.haversine(user_lat, user_long, preschool_latitude, preschool_longitude)
                if distance <= user_distance_constraint:
                    within_distance_constraint = 1  # yes
                else:
                    within_distance_constraint = 0  # no
                distance_row = pd.DataFrame({
                    'Preschool_Name': [preschool_name],
                    'Preschool_Latitude': [preschool_latitude],
                    'Preschool_Longitude': [preschool_longitude],
                    'Distance_To_User_km': [distance],
                    'Within_Distance_Constraint': [within_distance_constraint]
                })
                df_distance = pd.concat([df_distance, distance_row], ignore_index=True).drop_duplicates(
                    subset='Preschool_Name')

            # Opening Hours Calculation
            df_open = pd.DataFrame(
                columns=[
                    'Preschool_Name',
                    'Monday_Start_Number',
                    'Monday_End_Number',
                    'Tuesday_Start_Number',
                    'Tuesday_End_Number',
                    'Wednesday_Start_Number',
                    'Wednesday_End_Number',
                    'Thursday_Start_Number',
                    'Thursday_End_Number',
                    'Friday_Start_Number',
                    'Friday_End_Number',
                    'Saturday_Start_Number',
                    'Saturday_End_Number',
                    'Sunday_Start_Number',
                    'Sunday_End_Number',
                    'Monday_Open',
                    'Monday_Close',
                    'Tuesday_Open',
                    'Tuesday_Close',
                    'Wednesday_Open',
                    'Wednesday_Close',
                    'Thursday_Open',
                    'Thursday_Close',
                    'Friday_Open',
                    'Friday_Close',
                    'Saturday_Open',
                    'Saturday_Close',
                    'Sunday_Open',
                    'Sunday_Close',
                    'Within_Opening_Hours_Constraint'
                ])
            for index, row in df_opening_hours.iterrows():
                preschool_name = row['Preschool_Name']
                if row['Monday_Start_Number'] == 'Closed':
                    monday_start_number = 100
                else:
                    monday_start_number = float(row['Monday_Start_Number'])
                if row['Monday_End_Number'] == 'Closed':
                    monday_end_number = 100
                else:
                    monday_end_number = float(row['Monday_End_Number'])
                if row['Tuesday_Start_Number'] == 'Closed':
                    tuesday_start_number = 100
                else:
                    tuesday_start_number = float(row['Tuesday_Start_Number'])
                if row['Tuesday_End_Number'] == 'Closed':
                    tuesday_end_number = 100
                else:
                    tuesday_end_number = float(row['Tuesday_End_Number'])
                if row['Wednesday_Start_Number'] == 'Closed':
                    wednesday_start_number = 100
                else:
                    wednesday_start_number = float(row['Wednesday_Start_Number'])
                if row['Wednesday_End_Number'] == 'Closed':
                    wednesday_end_number = 100
                else:
                    wednesday_end_number = float(row['Wednesday_End_Number'])
                if row['Thursday_Start_Number'] == 'Closed':
                    thursday_start_number = 100
                else:
                    thursday_start_number = float(row['Thursday_Start_Number'])
                if row['Thursday_End_Number'] == 'Closed':
                    thursday_end_number = 100
                else:
                    thursday_end_number = float(row['Thursday_End_Number'])
                if row['Friday_Start_Number'] == 'Closed':
                    friday_start_number = 100
                else:
                    friday_start_number = float(row['Friday_Start_Number'])
                if row['Friday_End_Number'] == 'Closed':
                    friday_end_number = 100
                else:
                    friday_end_number = float(row['Friday_End_Number'])
                if row['Saturday_Start_Number'] == 'Closed':
                    saturday_start_number = 100
                else:
                    saturday_start_number = float(row['Saturday_Start_Number'])
                if row['Saturday_End_Number'] == 'Closed':
                    saturday_end_number = 100
                else:
                    saturday_end_number = float(row['Saturday_End_Number'])
                if row['Sunday_Start_Number'] == 'Closed':
                    sunday_start_number = 100
                else:
                    sunday_start_number = float(row['Sunday_Start_Number'])
                if row['Sunday_End_Number'] == 'Closed':
                    sunday_end_number = 100
                else:
                    sunday_end_number = float(row['Sunday_End_Number'])

                if user_monday_drop_off >= monday_start_number:
                    monday_open = 1
                else:
                    monday_open = 0
                if user_monday_pick_up <= monday_end_number:
                    monday_close = 1
                else:
                    monday_close = 0

                if user_tuesday_drop_off >= tuesday_start_number:
                    tuesday_open = 1
                else:
                    tuesday_open = 0
                if user_tuesday_pick_up <= tuesday_end_number:
                    tuesday_close = 1
                else:
                    tuesday_close = 0

                if user_wednesday_drop_off >= wednesday_start_number:
                    wednesday_open = 1
                else:
                    wednesday_open = 0
                if user_wednesday_pick_up <= wednesday_end_number:
                    wednesday_close = 1
                else:
                    wednesday_close = 0

                if user_thursday_drop_off >= thursday_start_number:
                    thursday_open = 1
                else:
                    thursday_open = 0
                if user_thursday_pick_up <= thursday_end_number:
                    thursday_close = 1
                else:
                    thursday_close = 0

                if user_friday_drop_off >= friday_start_number:
                    friday_open = 1
                else:
                    friday_open = 0
                if user_friday_pick_up <= friday_end_number:
                    friday_close = 1
                else:
                    friday_close = 0

                if user_saturday_drop_off >= saturday_start_number:
                    saturday_open = 1
                else:
                    saturday_open = 0
                if user_saturday_pick_up <= saturday_end_number:
                    saturday_close = 1
                else:
                    saturday_close = 0

                if user_sunday_drop_off >= sunday_start_number:
                    sunday_open = 1
                else:
                    sunday_open = 0
                if user_sunday_pick_up <= sunday_end_number:
                    sunday_close = 1
                else:
                    sunday_close = 0

                within_opening_hours_constraint = int(math.floor(
                    (monday_open + monday_close + tuesday_open + tuesday_close + wednesday_open + wednesday_close +
                     thursday_open + thursday_close + friday_open + friday_close + saturday_open + saturday_close +
                     sunday_open + sunday_close) / 14))

                open_row = pd.DataFrame({
                    'Preschool_Name': [preschool_name],
                    'Monday_Start_Number': [monday_start_number],
                    'Monday_End_Number': [monday_end_number],
                    'Tuesday_Start_Number': [tuesday_start_number],
                    'Tuesday_End_Number': [tuesday_end_number],
                    'Wednesday_Start_Number': [wednesday_start_number],
                    'Wednesday_End_Number': [wednesday_end_number],
                    'Thursday_Start_Number': [thursday_start_number],
                    'Thursday_End_Number': [thursday_end_number],
                    'Friday_Start_Number': [friday_start_number],
                    'Friday_End_Number': [friday_end_number],
                    'Saturday_Start_Number': [saturday_start_number],
                    'Saturday_End_Number': [saturday_end_number],
                    'Sunday_Start_Number': [sunday_start_number],
                    'Sunday_End_Number': [sunday_end_number],
                    'Monday_Open': [monday_open],
                    'Monday_Close': [monday_close],
                    'Tuesday_Open': [tuesday_open],
                    'Tuesday_Close': [tuesday_close],
                    'Wednesday_Open': [wednesday_open],
                    'Wednesday_Close': [wednesday_close],
                    'Thursday_Open': [thursday_open],
                    'Thursday_Close': [thursday_close],
                    'Friday_Open': [friday_open],
                    'Friday_Close': [friday_close],
                    'Saturday_Open': [saturday_open],
                    'Saturday_Close': [saturday_close],
                    'Sunday_Open': [sunday_open],
                    'Sunday_Close': [sunday_close],
                    'Within_Opening_Hours_Constraint': [within_opening_hours_constraint]
                })
                df_open = pd.concat([df_open, open_row], ignore_index=True).drop_duplicates(subset='Preschool_Name')

            # Budget Calculation
            # setting Within_Fees_Constraint and Within_Levels_Constraint and save to a csv
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
            processed_schoolpages['Within_Fees_Constraint'] = 0
            # Iterate over the user_fees variables
            for user_fee, column in user_fees_list:
                user_fee_value = getattr(self, user_fee)
                if user_fee_value != 0:  # Check if the user_fee is not 0
                    processed_schoolpages.loc[
                        processed_schoolpages[column] <= float(user_fee_value), 'Within_Fees_Constraint'] = 1
                    processed_schoolpages.loc[pd.isna(processed_schoolpages[column]), 'Within_Fees_Constraint'] = 0
            # User level mapping to DataFrame columns
            user_level_mapping = {
                1: 'levels_infant_care',
                2: 'levels_playgroup',
                3: 'levels_nursery',
                4: 'levels_kindergarten'
            }
            # Corresponding column in the DataFrame
            level_column = user_level_mapping[user_level]
            # Update 'Within_Levels_Constraint' based on the condition
            processed_schoolpages['Within_Levels_Constraint'] = (processed_schoolpages[level_column] == 1).astype(int)
            # save to csv
            # Get a list of all the column names
            cols = list(processed_schoolpages.columns)
            # Rearrange the columns by inserting 'Within_Fees_Constraint' after 'fees_pr_kindergarten'
            cols.insert(cols.index('fees_pr_kindergarten') + 1, cols.pop(cols.index('Within_Fees_Constraint')))
            # Reindex the DataFrame with the new column order
            preschool_details = processed_schoolpages.reindex(columns=cols)
            # add Within_Levels_Constraint after levels_kindergarten
            cols = list(preschool_details.columns)
            # Rearrange the columns by inserting 'Within_Levels_Constraint' after 'levels_kindergarten'
            cols.insert(cols.index('levels_kindergarten') + 1, cols.pop(cols.index('Within_Levels_Constraint')))
            # Reindex the DataFrame with the new column order
            df_preschool_details = preschool_details.reindex(columns=cols)

            # Combine both files
            compiled_output_file = (pd.merge(df_distance, df_open, on='Preschool_Name', how='left', indicator=True)
                                    .drop(columns=['_merge'])).drop_duplicates(subset='Preschool_Name')
            no_dup_processed_googlemaps = processed_googlemaps.drop(columns=[
                'Preschool_Latitude',
                'Preschool_Longitude',
                'Monday_Start_Number',
                'Monday_End_Number',
                'Tuesday_Start_Number',
                'Tuesday_End_Number',
                'Wednesday_Start_Number',
                'Wednesday_End_Number',
                'Thursday_Start_Number',
                'Thursday_End_Number',
                'Friday_Start_Number',
                'Friday_End_Number',
                'Saturday_Start_Number',
                'Saturday_End_Number',
                'Sunday_Start_Number',
                'Sunday_End_Number'
            ])
            compiled_output_file = (
                pd.merge(compiled_output_file, no_dup_processed_googlemaps, on='Preschool_Name', how='left',
                         indicator=True)
                .drop(columns=['_merge'])).drop_duplicates(subset='Preschool_Name')
            compiled_output_file = (
                pd.merge(compiled_output_file, df_preschool_details, on='Preschool_Name', how='left', indicator=True)
                .drop(columns=['_merge'])).drop_duplicates(subset='Preschool_Name')
            compiled_output_file['user_level'] = user_level
            compiled_output_file = pd.concat([user_input] * len(compiled_output_file), ignore_index=True).join(
                compiled_output_file)

            # Filtered only those within
            filtered_compiled_output_file = compiled_output_file[
                (compiled_output_file['Within_Distance_Constraint'] == 1) &
                (compiled_output_file['Within_Opening_Hours_Constraint'] == 1) &
                (compiled_output_file['Within_Fees_Constraint'] == 1) &
                (compiled_output_file['Within_Levels_Constraint'] == 1)
                ]

            # Save output files
            processed_googlemaps.to_csv(path_or_buf=input_file_excel_with_date, index=False)
            compiled_output_file.to_csv(path_or_buf=output_file, index=False)
            compiled_output_file.to_csv(path_or_buf=output_file_with_date, index=False)
            filtered_compiled_output_file.to_csv(path_or_buf=filtered_output_file, index=False)
            filtered_compiled_output_file.to_csv(path_or_buf=filtered_output_file_with_date, index=False)
            filtered_compiled_output_file.to_csv(path_or_buf=output_file_for_matching_algorithm, index=False)

            MatchingAlgorithm().trigger_match()


BusinessRulesEngine().trigger_business_rule()
