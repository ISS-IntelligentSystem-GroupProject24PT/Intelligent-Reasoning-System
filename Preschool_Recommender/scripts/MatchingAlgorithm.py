import os
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
import numpy as np


class MatchingAlgorithm:
    INPUT_FILE = 'BusinessRuleEngine_Distance_OpeningHours_Budget_Filtered.csv'
    OUTPUT_FILE = 'MatchingAlgorithm_Output.csv'
    INPUT_FILE_WITH_DATE = f"BusinessRuleEngine_Distance_OpeningHours_Budget_Filtered_{datetime.now().date()}.csv"
    OUTPUT_FILE_WITH_DATE = f"MatchingAlgorithm_Output_{datetime.now().date()}.csv"
    BUSINESS_RULES_OUTPUT_FILE = 'BusinessRuleEngine_Distance_OpeningHours_Budget.csv'
    FRONTEND_RULE_ALGO_OUTPUT_FILE = 'Results.csv'
    COMPILED_RESULTS_HISTORY = 'Results_History.csv'
    USER_INPUT_FILE = 'FrontEnd_UserInput.csv'

    INPUT_DIRECTORY_NAME = "C://Preschool_Recommender//resources//MatchingAlgorithm//MatchingAlgorithm_Input_Files"
    OUTPUT_DIRECTORY_NAME = "C://Preschool_Recommender//resources//MatchingAlgorithm//MatchingAlgorithm_Output_Files"
    ARCHIVES_DIRECTORY_NAME = "C://Preschool_Recommender//resources//MatchingAlgorithm//MatchingAlgorithm_Archives"
    BUSINESS_RULES_NON_FILTERED_FILE_DIRECTORY_NAME = "C://Preschool_Recommender//resources//BusinessRulesEngine//BusinessRulesEngine_Output_Files"
    FRONTEND_RULE_ALGO_OUTPUT_DIRECTORY_NAME = "C://Preschool_Recommender//resources//FrontEnd//FrontEnd_RuleAlgo_Output"
    FRONTEND_USER_INPUTS_DIRECTORY_NAME = "C://Preschool_Recommender//resources//FrontEnd//FrontEnd_UserInputs"

    def trigger_match(self):

        # Set the display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        # Set up directory
        working_dir = os.path.dirname(os.path.abspath(__file__))
        if not (os.getcwd() == working_dir):
            os.chdir(working_dir)
        if not os.path.exists(self.INPUT_DIRECTORY_NAME):
            os.mkdir(self.INPUT_DIRECTORY_NAME)

        if not os.path.exists(self.OUTPUT_DIRECTORY_NAME):
            os.mkdir(self.OUTPUT_DIRECTORY_NAME)

        if not os.path.exists(self.ARCHIVES_DIRECTORY_NAME):
            os.mkdir(self.ARCHIVES_DIRECTORY_NAME)

        input_file = os.path.join(self.INPUT_DIRECTORY_NAME, self.INPUT_FILE)
        input_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.INPUT_FILE_WITH_DATE)
        output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, self.OUTPUT_FILE)
        output_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.OUTPUT_FILE_WITH_DATE)
        business_rules_non_filtered_file = os.path.join(self.BUSINESS_RULES_NON_FILTERED_FILE_DIRECTORY_NAME,
                                                        self.BUSINESS_RULES_OUTPUT_FILE)
        frontEnd_rulealgo_output = os.path.join(self.FRONTEND_RULE_ALGO_OUTPUT_DIRECTORY_NAME,
                                                self.FRONTEND_RULE_ALGO_OUTPUT_FILE)
        results_history = os.path.join(self.OUTPUT_DIRECTORY_NAME, self.COMPILED_RESULTS_HISTORY)
        user_input_file = os.path.join(self.FRONTEND_USER_INPUTS_DIRECTORY_NAME, self.USER_INPUT_FILE)

        # Read input files
        user_input = pd.read_csv(user_input_file)
        business_rules_engine_output_raw = pd.read_csv(input_file)
        business_rules_engine_output_raw.columns = business_rules_engine_output_raw.columns.str.replace(' ', '_')

        user_fees_sc_infant_care = user_input['Infant_Care_Singaporean'].item()
        user_fees_sc_playgroup = user_input['Playgroup_Singaporean'].item()
        user_fees_sc_nursery = user_input['Nursery_Singaporean'].item()
        user_fees_sc_kindergarten = user_input['Kindergarten_Singaporean'].item()
        user_fees_pr_infant_care = user_input['Infant_Care_PR'].item()
        user_fees_pr_playgroup = user_input['Playgroup_PR'].item()
        user_fees_pr_nursery = user_input['Nursery_PR'].item()
        user_fees_pr_kindergarten = user_input['Kindergarten_PR'].item()

        user_input_fees = {
            'fees_sc_infant_care': [user_fees_sc_infant_care],
            'fees_sc_playgroup': [user_fees_sc_playgroup],
            'fees_sc_nursery': [user_fees_sc_nursery],
            'fees_sc_kindergarten': [user_fees_sc_kindergarten],
            'fees_pr_infant_care': [user_fees_pr_infant_care],
            'fees_pr_playgroup': [user_fees_pr_playgroup],
            'fees_pr_nursery': [user_fees_pr_nursery],
            'fees_pr_kindergarten': [user_fees_pr_kindergarten]
        }
        # Convert the dictionary to a numpy array
        user_fees = np.array(list(user_input_fees.values()))
        # Find the indices of non-zero elements
        non_zero_indices = np.nonzero(user_fees)
        # Print the keys corresponding to non-zero values
        for index in non_zero_indices[0]:
            fee_qualifier = list(user_input_fees.keys())[index]
        # Select relevant features
        business_rules_engine_output = business_rules_engine_output_raw[
            [
                "Preschool_Name",
                "Distance_To_User_km",
                "Average_Stars",
                "Topic_0",
                "Topic_1",
                "Topic_2",
                "Topic_3",
                "Topic_4",
                "Topic_5",
                "fees_sc_infant_care",
                "fees_sc_playgroup",
                "fees_sc_nursery",
                "fees_sc_kindergarten",
                "fees_pr_infant_care",
                "fees_pr_playgroup",
                "fees_pr_nursery",
                "fees_pr_kindergarten",
                "curriculum_active_learning",
                "curriculum_bilingual_curriculum",
                "curriculum_child_directed",
                "curriculum_chinese_curriculum",
                "curriculum_early_years_development_framework",
                "curriculum_english_curriculum",
                "curriculum_ib_pyp",
                "curriculum_inquiry_based",
                "curriculum_integrated_curriculum",
                "curriculum_montessori",
                "curriculum_moe",
                "curriculum_nurturing_early_learners_curriculum",
                "curriculum_play_based_curriculum",
                "curriculum_project_based",
                "curriculum_reggio_emilia_approach",
                "curriculum_spark_certified_curriculum",
                "curriculum_thematic",
                "curriculum_isteam",
                "programme_aesthetics_&_creative_expression",
                "programme_chinese",
                "programme_digital_skills",
                "programme_discovery_of_the_word",
                "programme_english",
                "programme_language_and_literacy",
                "programme_math",
                "programme_moral_education",
                "programme_motor_skill_development",
                "programme_music",
                "programme_nature",
                "programme_numeracy",
                "programme_problem-solving_skills",
                "programme_project_work",
                "programme_science",
                "programme_sensory_play",
                "programme_social_&_emotional_development",
                "programme_speech_and_drama",
                "programme_sports",
                "user_level"  # 1 - Infant Care, 2 - Playgroup, 3 - Nursery, 4 - Kindergarten
            ]]
        business_rules_engine_output.loc[:, 'fees_sc_infant_care'] = business_rules_engine_output['fees_sc_infant_care'].replace(',', '', regex=True).astype(float)
        business_rules_engine_output.loc[:, 'fees_sc_playgroup'] = business_rules_engine_output['fees_sc_playgroup'].replace(',', '', regex=True).astype(float)
        business_rules_engine_output.loc[:, 'fees_sc_nursery'] = business_rules_engine_output['fees_sc_nursery'].replace(',', '', regex=True).astype(float)
        business_rules_engine_output.loc[:, 'fees_sc_kindergarten'] = business_rules_engine_output['fees_sc_kindergarten'].replace(',', '', regex=True).astype(float)
        business_rules_engine_output.loc[:, 'fees_pr_infant_care'] = business_rules_engine_output['fees_pr_infant_care'].replace(',', '', regex=True).astype(float)
        business_rules_engine_output.loc[:, 'fees_pr_playgroup'] = business_rules_engine_output['fees_pr_playgroup'].replace(',', '', regex=True).astype(float)
        business_rules_engine_output.loc[:, 'fees_pr_nursery'] = business_rules_engine_output['fees_pr_nursery'].replace(',', '', regex=True).astype(float)
        business_rules_engine_output.loc[:, 'fees_pr_kindergarten'] = business_rules_engine_output['fees_pr_kindergarten'].replace(',', '', regex=True).astype(float)

        # Normalise the data
        columns_to_normalise = [
            'Distance_To_User_km',
            'Average_Stars',
            'fees_sc_infant_care',
            'fees_sc_playgroup',
            'fees_sc_nursery',
            'fees_sc_kindergarten',
            'fees_pr_infant_care',
            'fees_pr_playgroup',
            'fees_pr_nursery',
            'fees_pr_kindergarten'
        ]
        scaler = MinMaxScaler()
        business_rules_engine_output.loc[:, columns_to_normalise] = scaler.fit_transform(
            business_rules_engine_output[columns_to_normalise])

        try:
            if fee_qualifier == 'fees_sc_infant_care':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                    'user_level'
                ])
            elif fee_qualifier == 'fees_sc_playgroup':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                    'user_level'
                ])
            elif fee_qualifier == 'fees_sc_nursery':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                    'user_level'
                ])
            elif fee_qualifier == 'fees_sc_kindergarten':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                    'user_level'
                ])
            elif fee_qualifier == 'fees_pr_infant_care':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                    'user_level'
                ])
            elif fee_qualifier == 'fees_pr_playgroup':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                    'user_level'
                ])
            elif fee_qualifier == 'fees_pr_nursery':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_kindergarten',
                    'user_level'
                ])
            elif fee_qualifier == 'fees_pr_kindergarten':
                business_rules_engine_output = business_rules_engine_output.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'user_level'
                ])
            # Drop reference column
            business_rules_engine_output_numeric = business_rules_engine_output.drop(columns=['Preschool_Name'])
            # Handle null values
            business_rules_engine_output_numeric = business_rules_engine_output_numeric.fillna(0)
        except Exception as e:
            print(f"No business rules data: {e}")
        try:
            # User Input
            user_input_values = pd.DataFrame({
                'Distance_To_User_km': [0],
                'Average_Stars': [1],
                'Topic_0': [1],
                'Topic_1': [1],
                'Topic_2': [1],
                'Topic_3': [1],
                'Topic_4': [1],
                'Topic_5': [1],
                'fees_sc_infant_care': [0],
                'fees_sc_playgroup': [0],
                'fees_sc_nursery': [0],
                'fees_sc_kindergarten': [0],
                'fees_pr_infant_care': [0],
                'fees_pr_playgroup': [0],
                'fees_pr_nursery': [0],
                'fees_pr_kindergarten': [0],
                'curriculum_active_learning': [user_input['Active Learning Curriculum'].item()],
                'curriculum_bilingual_curriculum': [user_input['Bilingual Curriculum'].item()],
                'curriculum_child_directed': [user_input['Child Directed'].item()],
                'curriculum_chinese_curriculum': [user_input['Chinese Curriculum'].item()],
                'curriculum_early_years_development_framework': [
                    user_input['Early Years Development Framework'].item()],
                'curriculum_english_curriculum': [user_input['English Curriculum'].item()],
                'curriculum_ib_pyp': [user_input['IB PYP'].item()],
                'curriculum_inquiry_based': [user_input['Inquiry Based'].item()],
                'curriculum_integrated_curriculum': [user_input['Integrated Curriculum'].item()],
                'curriculum_montessori': [user_input['Montessori'].item()],
                'curriculum_moe': [user_input['MOE'].item()],
                'curriculum_nurturing_early_learners_curriculum': [
                    user_input['Nurturning Early Learners Curriculum'].item()],
                'curriculum_play_based_curriculum': [user_input['Play-based Curriculum'].item()],
                'curriculum_project_based': [user_input['Project-based Curriculum'].item()],
                'curriculum_reggio_emilia_approach': [user_input['Reggio Emilia approach'].item()],
                'curriculum_spark_certified_curriculum': [user_input['SPARK certified Curriculum'].item()],
                'curriculum_thematic': [user_input['Thematic'].item()],
                'curriculum_isteam': [user_input['ISteam'].item()],
                'programme_aesthetics_&_creative_expression': [user_input['Aesthetics_Creative_Expression'].item()],
                'programme_chinese': [user_input['Chinese'].item()],
                'programme_digital_skills': [user_input['Digital_Skills'].item()],
                'programme_discovery_of_the_word': [user_input['Discovery_of_the_World'].item()],
                'programme_english': [user_input['English'].item()],
                'programme_language_and_literacy': [user_input['Language_and_Literacy'].item()],
                'programme_math': [user_input['Math'].item()],
                'programme_moral_education': [user_input['Moral_Education'].item()],
                'programme_motor_skill_development': [user_input['Motor_Skill_Development'].item()],
                'programme_music': [user_input['Music'].item()],
                'programme_nature': [user_input['Nature'].item()],
                'programme_numeracy': [user_input['Numeracy'].item()],
                'programme_problem-solving_skills': [user_input['Problem-solving_Skills'].item()],
                'programme_project_work': [user_input['Project Work'].item()],
                'programme_science': [user_input['Science'].item()],
                'programme_sensory_play': [user_input['Sensory Play'].item()],
                'programme_social_&_emotional_development': [user_input['Social & Emotional Development'].item()],
                'programme_speech_and_drama': [user_input['Speech and Drama'].item()],
                'programme_sports': [user_input['Sports'].item()]
            })
            if fee_qualifier == 'fees_sc_infant_care':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                ])
            elif fee_qualifier == 'fees_sc_playgroup':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                ])
            elif fee_qualifier == 'fees_sc_nursery':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                ])
            elif fee_qualifier == 'fees_sc_kindergarten':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                ])
            elif fee_qualifier == 'fees_pr_infant_care':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                ])
            elif fee_qualifier == 'fees_pr_playgroup':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_nursery',
                    'fees_pr_kindergarten',
                ])
            elif fee_qualifier == 'fees_pr_nursery':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_kindergarten',
                ])
            elif fee_qualifier == 'fees_pr_kindergarten':
                user_input_values = user_input_values.drop(columns=[
                    'fees_sc_infant_care',
                    'fees_sc_playgroup',
                    'fees_sc_nursery',
                    'fees_sc_kindergarten',
                    'fees_pr_infant_care',
                    'fees_pr_playgroup',
                    'fees_pr_nursery',
                ])
        except Exception as e:
            print(f"No user input data: {e}")

        try:
            # Calculate cosine similarity
            similarity_result = cosine_similarity(
                business_rules_engine_output_numeric.values,
                user_input_values.iloc[[0]]  # To replace with user input
            )
            similarity_result = similarity_result.flatten()
            business_rules_engine_output['Cosine_Similarity'] = similarity_result

            # Calculate Euclidean Distance
            euclidean_dist = distance.cdist(
                business_rules_engine_output_numeric.values,
                user_input_values.iloc[[0]],  # To replace with user input
                'euclidean'
            )
            euclidean_dist = euclidean_dist.flatten()
            business_rules_engine_output['Euclidean_Distance'] = euclidean_dist

            # Calculate Manhattan Distance
            cityblock_dist = distance.cdist(
                business_rules_engine_output_numeric.values,
                user_input_values.iloc[[0]],  # To replace with user input
                'cityblock'
            )
            cityblock_dist = cityblock_dist.flatten()
            business_rules_engine_output['Manhattan_Distance'] = cityblock_dist
        except Exception as e:
            print(f"No similarity: {e}")

        # Combine business rules output file
        feature_data = pd.read_csv(business_rules_non_filtered_file)
        business_rules_engine_output = (
            pd.merge(
                business_rules_engine_output,
                feature_data,
                on='Preschool_Name', how='left', indicator=True
            ).drop(columns=['_merge']))

        # Save output files
        business_rules_engine_output_raw.to_csv(path_or_buf=input_file_with_date, index=False)
        business_rules_engine_output.to_csv(path_or_buf=output_file, index=False)
        business_rules_engine_output.to_csv(path_or_buf=output_file_with_date, index=False)
        business_rules_engine_output.drop(columns='Primary_key').to_csv(path_or_buf=frontEnd_rulealgo_output,
                                                                        index=False)

        # Add into results history
        try:
            current_results_history = pd.read_csv(results_history)
            current_results_history = pd.concat([current_results_history, business_rules_engine_output]).reset_index(
                drop=True)
            current_results_history.to_csv(path_or_buf=results_history, index=False)
        except Exception as e:
            business_rules_engine_output.to_csv(path_or_buf=results_history, index=False)
            print(f"{e}")


MatchingAlgorithm().trigger_match()
