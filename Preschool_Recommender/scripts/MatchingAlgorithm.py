import os
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
from scipy.stats import pearsonr


class MatchingAlgorithm:
    INPUT_FILE = 'BusinessRuleEngine_Distance_OpeningHours_Budget_Filtered.csv'
    OUTPUT_FILE = 'MatchingAlgorithm_Output.csv'
    INPUT_FILE_WITH_DATE = f"BusinessRuleEngine_Distance_OpeningHours_Budget_Filtered_{datetime.now().date()}.csv"
    OUTPUT_FILE_WITH_DATE = f"MatchingAlgorithm_Output_{datetime.now().date()}.csv"
    BUSIENSS_RULES_OUPUT_FILE = 'BusinessRuleEngine_Distance_OpeningHours_Budget.csv'

    INPUT_DIRECTORY_NAME = "..//resources//MatchingAlgorithm//MatchingAlgorithm_Input_Files"
    OUTPUT_DIRECTORY_NAME = "..//resources//MatchingAlgorithm//MatchingAlgorithm_Output_Files"
    ARCHIVES_DIRECTORY_NAME = "..//resources//MatchingAlgorithm//MatchingAlgorithm_Archives"
    BUSINESS_RULES_NON_FILTERED_FILE_DIRECTORY_NAME = "..//resources//BusinessRulesEngine//BusinessRulesEngine_Output_Files"

    def __init__(self):

        # Set the display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        # Set up directory
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
        business_rules_non_filtered_file = os.path.join(self.BUSINESS_RULES_NON_FILTERED_FILE_DIRECTORY_NAME, self.BUSIENSS_RULES_OUPUT_FILE)

        # Read input files
        business_rules_engine_output_raw = pd.read_csv(input_file)
        business_rules_engine_output_raw.columns = business_rules_engine_output_raw.columns.str.replace(' ', '_')
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
                "user_level"    # 1 - Infant Care, 2 - Playgroup, 3 - Nursery, 4 - Kindergarten
            ]]

        if business_rules_engine_output["user_level"].iloc[0] == 1:
            business_rules_engine_output = business_rules_engine_output.drop(columns=[
                'fees_sc_playgroup',
                'fees_sc_nursery',
                'fees_sc_kindergarten',
                'fees_pr_playgroup',
                'fees_pr_nursery',
                'fees_pr_kindergarten',
                'user_level'
            ])
        elif business_rules_engine_output["user_level"].iloc[0] == 2:
            business_rules_engine_output = business_rules_engine_output.drop(columns=[
                'fees_sc_infant_care',
                'fees_sc_nursery',
                'fees_sc_kindergarten',
                'fees_pr_infant_care',
                'fees_pr_nursery',
                'fees_pr_kindergarten',
                'user_level'
            ])
        elif business_rules_engine_output["user_level"].iloc[0] == 3:
            business_rules_engine_output = business_rules_engine_output.drop(columns=[
                'fees_sc_infant_care',
                'fees_sc_playgroup',
                'fees_sc_kindergarten',
                'fees_pr_infant_care',
                'fees_pr_playgroup',
                'fees_pr_kindergarten',
                'user_level'
            ])
        elif business_rules_engine_output["user_level"].iloc[0] == 4:
            business_rules_engine_output = business_rules_engine_output.drop(columns=[
                'fees_sc_infant_care',
                'fees_sc_playgroup',
                'fees_sc_nursery',
                'fees_pr_infant_care',
                'fees_pr_playgroup',
                'fees_pr_nursery',
                'user_level'
            ])

        # Normalise the data
        columns_to_normalise = [
                'Distance_To_User_km',
                'Average_Stars',
                'fees_sc_nursery',
                'fees_pr_nursery'
        ]
        scaler = MinMaxScaler()
        business_rules_engine_output[columns_to_normalise] = scaler.fit_transform(
            business_rules_engine_output[columns_to_normalise])

        # Drop reference column
        business_rules_engine_output_numeric = business_rules_engine_output.drop(columns=['Preschool_Name'])
        # Handle null values
        business_rules_engine_output_numeric = business_rules_engine_output_numeric.fillna(0)

        # Calculate cosine similarity
        similarity_result = cosine_similarity(
            business_rules_engine_output_numeric.values,
            business_rules_engine_output_numeric.iloc[[0]] # To replace with user input
        )
        similarity_result = similarity_result.flatten()
        business_rules_engine_output['Cosine_Similarity'] = similarity_result

        # Calculate Euclidean Distance
        euclidean_dist = distance.cdist(
            business_rules_engine_output_numeric.values,
            business_rules_engine_output_numeric.iloc[[0]],  # To replace with user input
            'euclidean'
        )
        euclidean_dist = euclidean_dist.flatten()
        business_rules_engine_output['Euclidean_Distance'] = euclidean_dist

        # Calculate Manhattan Distance
        cityblock_dist = distance.cdist(
            business_rules_engine_output_numeric.values,
            business_rules_engine_output_numeric.iloc[[0]],  # To replace with user input
            'cityblock'
        )
        cityblock_dist = cityblock_dist.flatten()
        business_rules_engine_output['Manhattan_Distance'] = cityblock_dist
        print(business_rules_engine_output.head())

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


MatchingAlgorithm = MatchingAlgorithm()



