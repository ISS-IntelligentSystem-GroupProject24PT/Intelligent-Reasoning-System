import os
from datetime import datetime
import pandas as pd
import re
from collections import Counter
import spacy
from spacy.matcher import Matcher
import gensim.downloader as api
from spacytextblob.spacytextblob import SpacyTextBlob


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
                                 not token.is_punct and not token.is_stop and token.is_alpha and token.pos_ == 'NOUN']
        return preprocessed_sentence

    INPUT_FILE_TXT = 'Google_Reviews_Output.txt'
    INPUT_WORD_CATEGORISATION = 'Word_Categorisation.csv'
    OUTPUT_FILE = 'ProcessedGoogleMaps_Output_Reviews.csv'
    TEMP_OUTPUT_FILE = 'ProcessedGoogleMaps_Output_Reviews_Temp.csv'
    FREQUENCY_OUTPUT_FILE = 'ProcessedGoogleMaps_Output_Noun_Frequency.csv'
    INPUT_FILE_TXT_WITH_DATE = f"Google_Reviews_Output_{datetime.now().date()}.txt"
    OUTPUT_FILE_WITH_DATE = f"ProcessedGoogleMaps_Output_Reviews_{datetime.now().date()}.csv"
    FREQUENCY_OUTPUT_FILE_WITH_DATE = f"ProcessedGoogleMaps_Output_Noun_Frequency_{datetime.now().date()}.csv"

    INPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Input_Files"
    OUTPUT_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Output_Files"
    ARCHIVES_DIRECTORY_NAME = "..//resources//ProcessedGoogleMaps//ProcessedGoogleMaps_Archives"

    def __init__(self):
        # Load NLP
        self.nlp = spacy.load('en_core_web_sm')
        self.nlp.add_pipe('spacytextblob')
        w2v_model = api.load("word2vec-google-news-300")

        # Set up directory
        if not os.path.exists(self.OUTPUT_DIRECTORY_NAME):
            os.mkdir(self.OUTPUT_DIRECTORY_NAME)

        if not os.path.exists(self.ARCHIVES_DIRECTORY_NAME):
            os.mkdir(self.ARCHIVES_DIRECTORY_NAME)

        input_file_txt = os.path.join(self.INPUT_DIRECTORY_NAME, self.INPUT_FILE_TXT)
        input_word_categorisation = os.path.join(self.INPUT_DIRECTORY_NAME, self.INPUT_WORD_CATEGORISATION)
        output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, self.OUTPUT_FILE)
        temp_output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, self.TEMP_OUTPUT_FILE)
        input_file_txt_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.INPUT_FILE_TXT_WITH_DATE)
        output_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME, self.OUTPUT_FILE_WITH_DATE)
        frequency_output_file = os.path.join(self.OUTPUT_DIRECTORY_NAME, self.FREQUENCY_OUTPUT_FILE)
        frequency_output_file_with_date = os.path.join(self.ARCHIVES_DIRECTORY_NAME,
                                                       self.FREQUENCY_OUTPUT_FILE_WITH_DATE)

        # Set the display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        # Read input files
        df_unstructured_input_file = pd.read_csv(input_file_txt)
        df_word_categorisation = pd.read_csv(input_word_categorisation)

        df_comments = pd.DataFrame(columns=['Preschool_Name', 'Comment', 'Sentiment', 'Word'])
        all_preprocessed_sentences = []

        for index, row in df_unstructured_input_file.iterrows():
            preschool_name = row['Preschool_Name']
            review_comments = str(row['Review_Comments'])
            # review_comments = review_comments.replace('.,', '.    ')
            # review_comments = review_comments.replace('!,', '!    ')
            # review_comments = review_comments.replace('),', ')    ')
            # review_comments = re.sub(r", ([A-Z])", r",  \1", review_comments)
            review_comment = review_comments.split('", "')
            print(review_comments)
            for i in range(0, len(review_comment)):
                print(review_comment[i])

            for comment in review_comment:
                token_sentence = self.nlp(comment.strip())
                if comment == 'nan':
                    print(preschool_name)
                else:
                    preprocessed_sentences = self.my_preprocessing(token_sentence, w2v_model)
                    sorted_word_counts = sorted(Counter(preprocessed_sentences).items(), key=lambda item: item[1],
                                                reverse=True)  # Sort the word counts by their occurrences
                    if not sorted_word_counts:
                        sorted_word_counts = [('-', 0)]
                    all_preprocessed_sentences.extend(preprocessed_sentences)
                    comment_row = pd.DataFrame({
                        'Preschool_Name': [preschool_name],
                        'Comment': [comment],
                        'Sentiment': [token_sentence._.polarity],
                        'Word': [sorted_word_counts[0][0]]
                    })
                    df_comments = pd.concat([df_comments, comment_row], ignore_index=True)

        # Noun Frequency Table
        total_sorted_word_counts = sorted(Counter(all_preprocessed_sentences).items(), key=lambda item: item[1],
                                          reverse=True)  # Sort the word counts by their occurrences
        df_word_counts_by_noun = pd.DataFrame(total_sorted_word_counts, columns=['Word', 'Frequency'])
        df_word_counts_by_noun = (
            pd.merge(df_word_counts_by_noun, df_word_categorisation, on='Word', how='left', indicator=True)
            .drop(columns=['_merge'])).drop_duplicates(subset='Word')
        # Sentiment by Category / Preschool
        df_sentiment_by_category = (pd.merge(df_comments, df_word_categorisation, on='Word', how='left', indicator=True)
                                    .drop(columns=['_merge'])).drop_duplicates(subset='Word')
        df_sentiment_by_category_cleaned = df_sentiment_by_category.drop(columns=['Comment', 'Word'])
        df_average_sentiment_by_category = df_sentiment_by_category_cleaned.pivot_table(values='Sentiment',
                                                                                        index=['Preschool_Name'],
                                                                                        columns='Category')
        df_average_sentiment_by_category.reset_index(inplace=True)
        df_average_sentiment_by_preschool = df_sentiment_by_category_cleaned.pivot_table(values='Sentiment',
                                                                                         index=['Preschool_Name'])
        df_average_sentiment_by_preschool.reset_index(inplace=True)
        compiled_output_file = (
            pd.merge(df_average_sentiment_by_preschool, df_average_sentiment_by_category, on='Preschool_Name',
                     how='left',
                     indicator=True)
            .drop(columns=['_merge']))
        compiled_output_file.rename(columns={'Sentiment': 'Overall_Sentiment'}, inplace=True)

        # Save output files
        df_unstructured_input_file.to_csv(path_or_buf=input_file_txt_with_date, index=False)
        df_word_counts_by_noun.to_csv(path_or_buf=frequency_output_file, index=False)
        df_word_counts_by_noun.to_csv(path_or_buf=frequency_output_file_with_date, index=False)
        df_sentiment_by_category.to_csv(path_or_buf=temp_output_file, index=False)
        compiled_output_file.to_csv(path_or_buf=output_file, index=False)
        compiled_output_file.to_csv(path_or_buf=output_file_with_date, index=False)


google_maps_reviews_processing = GoogleMapsReviews()