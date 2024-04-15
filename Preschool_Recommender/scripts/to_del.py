import os
import pandas as pd

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

class GiveUp:
    @staticmethod
    def extract_topics(output_directory_name, num_topics):
        df_density = pd.DataFrame()
        for n_topics in range(2, num_topics + 1):
            try:
                OUTPUT_FILE = f"{n_topics}_Topics_ProcessedGoogleMaps_Output_Reviews.csv"
                output_file = os.path.join(output_directory_name, OUTPUT_FILE)
                topic_model_results = pd.read_csv(output_file)
                topic_model_results['File'] = OUTPUT_FILE
                topic_model_results['n_topics'] = n_topics
                topic_model_results['Total'] = len(topic_model_results)
                for n in range(0, n_topics):
                    topic_model_results[f"Topic_{n}_Blank"] = topic_model_results[f"Topic {n}"].isnull().astype(int)
                    topic_model_results[f"Topic_{n}_Filled"] = topic_model_results[f"Topic {n}"].notnull().astype(int)
                    topic_model_results = topic_model_results.drop(columns=f"Topic {n}")
                topic_model_results = topic_model_results.drop(columns='Preschool_Name')
                topic_model_results = pd.pivot_table(
                    topic_model_results,
                    index=['File', 'n_topics', 'Total'],
                    values=[(f"Topic_{n}_Blank") for n in range(0, n_topics)],
                    aggfunc='sum'
                )
                topic_model_results.reset_index(inplace=True)
                for n in range(0, n_topics):
                    topic_model_results[f"Topic_{n}_Blank"] = topic_model_results[f"Topic_{n}_Blank"] / topic_model_results['Total']
                df_density = df_density._append(topic_model_results, ignore_index=True)
            except Exception as e:
                print(f"{e}")
        print(df_density)

        df_topics = pd.DataFrame()
        for n_topics in range(2, num_topics + 1):
            try:
                OUTPUT_FILE = f"{n_topics}_Topics_ProcessedGoogleMaps_Output_Topic_Model.txt"
                output_file = os.path.join(output_directory_name, OUTPUT_FILE)
                topic_model_results = pd.read_csv(output_file)
                topic_model_results = topic_model_results[['Topic_Number', 'Word']]
                # topic_model_results = topic_model_results.drop_duplicates()
                topic_model_results['File'] = OUTPUT_FILE
                topic_model_results['n_topics'] = n_topics
                topic_model_results.reset_index(drop=True, inplace=True)
                topic_model_results = topic_model_results.drop_duplicates(subset='Word')
                # print(topic_model_results)
                # topic_model_results = topic_model_results.drop_duplicates(subset='Topic_Number')
                topic_model_results = topic_model_results.pivot(index=['File', 'n_topics'],
                                                                columns='Topic_Number',
                                                                values='Word')
                topic_model_results.reset_index(inplace=True)
                df_topics = df_topics._append(topic_model_results, ignore_index=True)
            except Exception as e:
                print(f"{e}")
        print(df_topics)

        # Combine
        all_topics = (
            pd.merge(df_density, df_topics, on='n_topics', how='left', indicator=True)
            .drop(columns=['_merge']))
        print(all_topics)

        # Store results
        TOPIC_OUTPUT_FILE = f"Topics.csv"
        topic_output_file = os.path.join(output_directory_name, TOPIC_OUTPUT_FILE)
        all_topics.to_csv(path_or_buf=topic_output_file, index=False)

    OUTPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Output_Files"

    def __init__(self):
        self.extract_topics(self.OUTPUT_DIRECTORY_NAME, num_topics=6)

GiveUp = GiveUp()