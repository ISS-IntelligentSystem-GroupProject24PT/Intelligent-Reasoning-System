import os
from datetime import datetime
import pandas as pd
import spacy
from spacy.matcher import Matcher
import gensim.downloader as api
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob


class GoogleMapsReviews:

    # Define a function to replace abbreviations with their most similar words or their definitions
    def replace_abbreviations(self, text, w2v_model):
        # Load a spaCy model and create a Matcher object
        matcher = Matcher(self.nlp.vocab)
        # Define a pattern to match abbreviations
        pattern = [{"IS_UPPER": True}, {"IS_PUNCT": True, "OP": "*"}]
        matcher.add("ABBREVIATION", [pattern])
        # Parse the text with spaCy
        doc = self.nlp(text)
        # Create a list of tokens to store the modified text
        altered_tokens = [token.text for token in doc]
        # Loop through the matches found by the Matcher
        for match_id, start, end in matcher(doc):
            # Get the matched span
            span = doc[start:end]
            # Get the text of the span
            abbr = span.text
            # Get the most similar word or the definition from the word2vec model or the API
            try:
                similar_word = w2v_model.most_similar(positive=abbr, topn=1)[0][0]
                # Replace the abbreviation with the similar word in the token list
                altered_tokens[start] = similar_word
            except (KeyError, IndexError):
                # If the abbreviation is not found, skip it
                pass
        # Join the tokens back into a string
        return " ".join(altered_tokens)

    def my_preprocessing(self, raw_sentence, w2v_model):
        sentence = self.nlp(raw_sentence)
        preprocessed_sentence = [self.replace_abbreviations(token.lemma_.lower(), w2v_model) for token in sentence if
                                 not token.is_punct and not token.is_stop and token.is_alpha
                                 # and token.pos_ == 'NOUN'
                                 ]
        return preprocessed_sentence

    @staticmethod
    def get_sentiment(review_comment):
        blob = TextBlob(review_comment)
        return blob.sentiment.polarity

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

        df_topics = pd.DataFrame()
        for n_topics in range(2, num_topics + 1):
            try:
                OUTPUT_FILE = f"{n_topics}_Topics_ProcessedGoogleMaps_Output_Topic_Model.txt"
                output_file = os.path.join(output_directory_name, OUTPUT_FILE)
                topic_model_results = pd.read_csv(output_file)
                topic_model_results = topic_model_results[['Topic_Number', 'Word']]
                topic_model_results['File'] = OUTPUT_FILE
                topic_model_results['n_topics'] = n_topics
                topic_model_results.reset_index(drop=True, inplace=True)
                topic_model_results = topic_model_results.drop_duplicates(subset='Word')
                topic_model_results = topic_model_results.pivot(index=['File', 'n_topics'],
                                                                columns='Topic_Number',
                                                                values='Word')
                topic_model_results.reset_index(inplace=True)
                df_topics = df_topics._append(topic_model_results, ignore_index=True)
            except Exception as e:
                print(f"{e}")
        # Combine
        all_topics = (pd.merge(df_density, df_topics, on='n_topics', how='left', indicator=True).drop(columns=['_merge']))
        # Store results
        TOPIC_OUTPUT_FILE = f"Topics.csv"
        topic_output_file = os.path.join(output_directory_name, TOPIC_OUTPUT_FILE)
        all_topics.to_csv(path_or_buf=topic_output_file, index=False)

    INPUT_FILE_TXT = 'Google_Reviews_Output.txt'
    INPUT_WORD_CATEGORISATION = 'Topic_Modelling.csv'
    INPUT_FILE_TXT_WITH_DATE = f"Google_Reviews_Output_{datetime.now().date()}.txt"
    INPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Input_Files"
    OUTPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Output_Files"
    ARCHIVES_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Archives"

    def __init__(self):
        print('Processor_GoogleMapsReviews Start!')
        # Load NLP
        self.nlp = spacy.load('en_core_web_sm')
        w2v_model = api.load("word2vec-google-news-300")

        # Set up directory
        if not os.path.exists(self.OUTPUT_DIRECTORY_NAME):
            os.mkdir(self.OUTPUT_DIRECTORY_NAME)

        if not os.path.exists(self.ARCHIVES_DIRECTORY_NAME):
            os.mkdir(self.ARCHIVES_DIRECTORY_NAME)

        input_file_txt = os.path.join(self.INPUT_DIRECTORY_NAME, self.INPUT_FILE_TXT)
        input_file_txt_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.INPUT_FILE_TXT_WITH_DATE)

        # Set the display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        # Read input files
        df_unstructured_input_file = pd.read_csv(input_file_txt)
        df_comments = pd.DataFrame(columns=['Comment', 'Sentiment', 'Topic_Number', 'Word', 'Preschool_Name'])
        review_comments = df_unstructured_input_file.get('Review_Comments')
        review_comments = review_comments.fillna('')
        review_comment_splits = review_comments.str.split('", "')

        n_top_words = 20

        for n_topics in range(2, 7):
            print(f"n_topics: {n_topics}")
            # Preprocess and vectorize all comments
            all_comments = [' '.join(self.my_preprocessing(comment[0], w2v_model)) for comment in review_comment_splits]
            sparse_vectorizer = CountVectorizer(strip_accents='unicode')
            sparse_vectors = sparse_vectorizer.fit_transform(all_comments)
            feature_names = sparse_vectorizer.get_feature_names_out()
            # Train LDA model
            lda = LatentDirichletAllocation(n_components=n_topics, max_iter=1000, learning_method='online', random_state=0)
            lda.fit(sparse_vectors)
            # Get top words for each topic
            topic_top_words = {}
            for topic_idx, topic in enumerate(lda.components_):
                top_words_idx = topic.argsort()[:-n_top_words - 1:-1]
                top_words = [feature_names[i] for i in top_words_idx]
                topic_top_words[topic_idx] = top_words

            # Assign topics to comments
            for idx, review_comment_split in enumerate(review_comment_splits):
                for split_comment in review_comment_split:
                    preprocessed_comment = ' '.join(self.my_preprocessing(split_comment, w2v_model))
                    sentiment = self.get_sentiment(split_comment)
                    try:
                        if preprocessed_comment:
                            sparse_vector = sparse_vectorizer.transform([preprocessed_comment])
                            doc_topic_distribution = lda.transform(sparse_vector)
                            dominant_topic = doc_topic_distribution.argmax(axis=1)[0]
                            top_words = topic_top_words[dominant_topic]
                            pre_school_name = df_unstructured_input_file.loc[idx, 'Preschool_Name']
                            comment_row = pd.DataFrame({
                                'Comment': [split_comment],
                                'Sentiment': [sentiment],
                                'Topic_Number': [f"Topic {dominant_topic}"],
                                'Word': [top_words],
                                'Preschool_Name': [pre_school_name]
                            })
                            df_comments = pd.concat([df_comments, comment_row], ignore_index=True)
                        # Store results
                        FREQUENCY_OUTPUT_FILE = f"{n_topics}_Topics_ProcessedGoogleMaps_Output_Topic_Model.txt"
                        frequency_output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, FREQUENCY_OUTPUT_FILE)
                        df_comments.to_csv(path_or_buf=frequency_output_file, index=False)
                        # Store results in archives
                        FREQUENCY_OUTPUT_FILE_WITH_DATE = f"{n_topics}_Topics_ProcessedGoogleMaps_Output_Topic_Model{datetime.now().date()}.csv"
                        frequency_output_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, FREQUENCY_OUTPUT_FILE_WITH_DATE)
                        df_comments.to_csv(path_or_buf=frequency_output_file_with_date, index=False)

                    except Exception as e:
                        print(f"{preprocessed_comment}, {e}")

            compiled_output_file = df_comments.pivot_table(
                values='Sentiment',
                index=['Preschool_Name'],
                columns='Topic_Number'
            )
            compiled_output_file.reset_index(inplace=True)

            # Save output files
            OUTPUT_FILE = f"{n_topics}_Topics_ProcessedGoogleMaps_Output_Reviews.csv"
            output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, OUTPUT_FILE)
            compiled_output_file.to_csv(path_or_buf=output_file, index=False)

            # Store result in archives
            OUTPUT_FILE_WITH_DATE = f"{n_topics}_Topics_ProcessedGoogleMaps_Output_Reviews_{datetime.now().date()}.csv"
            output_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, OUTPUT_FILE_WITH_DATE)
            compiled_output_file.to_csv(path_or_buf=output_file_with_date, index=False)
        df_unstructured_input_file.to_csv(path_or_buf=input_file_txt_with_date, index=False)

        # Extract Topics
        self.extract_topics(self.OUTPUT_DIRECTORY_NAME, num_topics=6)


google_maps_reviews_processing = GoogleMapsReviews()
