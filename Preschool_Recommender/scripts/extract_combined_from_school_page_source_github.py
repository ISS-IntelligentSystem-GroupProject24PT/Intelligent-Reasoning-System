import pandas as pd
import os
import glob
import re
import ast

# def search_txt_file(folder, preschool_name):
#     list_of_shortened_names = ['7oaks']

#     if(preschool_name[:5]in list_of_shortened_names):
#         #match by first five characters only for short preschool names or will not match
#         first_five_chars = preschool_name[:5].replace('_', '')
#     else:
#         first_five_chars = preschool_name[:7].replace('_', '')
    
#     contents = []
#     filenames = []
#     for filename in os.listdir(folder):
#         if filename.endswith(".txt") and filename.replace('_', '').startswith(first_five_chars):
#             with open(os.path.join(folder, filename), 'r', encoding='utf-8') as file:
#                 contents.append(file.read())
#                 filenames.append(filename)
#     return contents, filenames

def search_txt_file(folder, preschool_name):
    # when sent from outside preschool_name replaced all blanks with dash and lowered
    # special_names = {
    #     '7oaks': '7oaks',
    #     'pcf_s': 'pcfor',
    #     'ace_@': 'aceat'
    # }

    special_names = {
    '7oaks': '7oaks', 
    'ace_@': 'aceat', # manualy search cose preschool name and txt name do not match
                    # run full list to manual check which one else to intput 
    'agape': 'agape', #
    'carpe': 'carpe', 
    'child': 'child', 
    'child': 'child', # think how to differentiate this one with seven letters
    'cleme': 'cwked',
    'elfa_': 'elfap', 
    'e-bri': 'ebrid', 
    'glory': 'glory', 
    'haven': 'havensch', 
    'hope_': 'hopec', 
    'iman_': 'imane', # stop
    'iyad_': 'iyadp', 
    'jamiy': 'jcccj', 
    'just_': 'juste', 
    'kidz_': 'kidzm', 
    'my_fi': 'myfir', 
    'my_ki': 'mykid', 
    'my_le': 'mylea', 
    'my_li': 'mylit', 
    'my_wo': 'mywor', 
    'new_l': 'newli', 
    'pcf_s': 'pcfor',
    'posso': 'posso', 
    # 'sdm_c': 'sdmch', 
    'shaws': 'shaws', 
    'small': 'small', 
    'star_': 'starl', 
    'the_l': 'theli', 
    # 'the_o': 'theod', 
    'the_s': 'thesc', 
    'tung_': 'tungl', 
    'ymca_': 'ymcae',
    'zee_j': 'zeeco', 
    }
    
    # need to be longer 10 char or 13 char cos too similar
    long_special_names = {
    'little_bee': 'nonsense00', #should map to nothin cos no txt file
    'little_big': 'littlebig_', 
    'little_dol': 'littledolp', 
    'little_foo': 'littlefoot', 
    'little_gre': 'littlegree', 
    'little_mig': 'littlemigh', 
    'little_oli': 'nonsense00', 
    'little_pad': 'serangoonl', #serangoonlittlepadding txt file
    'little_see': 'littleseed', 
    'little_she': 'littleshep', 
    'raffles_ki': 'raffleskid', 
    'sdm_-_ichi': 'sdmchatswo', 
    'sdm_childc': 'sdmchatswo', 
    'sdm-moriah': 'sdmchatswo', 
    'serangoon_': 'nonsense00',
    # 'super_tale': 'supertalen', #replace to below - to delete
    # 'superland_': 'superlandc', #replace to below - to delete
    'the_orange': 'orangeacad',
    }
    long_13_names = {
    
    'etonhouse_bil': 'infoetonhouse',
    'etonhouse_pre': 'infoetonhouse',
    'just_kids_@_c': 'nonsense00000',#should map to nothin cos no txt file
    'sunflower_chi': 'nonsense00000',
    'sunflower_kid': 'sunflowerkidd',
    'sunflower_kin': 'sunflowerkind',
    'sunflower_pre': 'sunflowerkidc',
    'sunflower_tin': 'nonsense00000',
    'sunshine_kids': 'sunshinekidsc',
    'super_talent_': 'supertalentco',
    'superland_pre': 'superlandcoms',
    'the_little_sk': 'nonsense00000',
    }

    first_five_chars = preschool_name[:5]
    first_ten_chars =preschool_name[:10]
    first_thirteen_chars =preschool_name[:13]
    
    if first_five_chars in special_names:
        first_five_chars = special_names[first_five_chars]
        # print(first_five_chars)
    elif first_ten_chars in long_special_names:
        first_five_chars = long_special_names[first_ten_chars]
        print(first_five_chars)
    elif first_thirteen_chars in long_13_names:
        first_five_chars = long_13_names[first_thirteen_chars]
        print(first_five_chars)
    else:
        first_five_chars = preschool_name[:7].replace('_', '')

    contents = []
    filenames = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt") and filename.replace('_', '').startswith(first_five_chars):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as file:
                contents.append(file.read())
                filenames.append(filename)
    return contents, filenames

def search_txt_file_exact_match(folder, filename):
    # Initialize empty lists to store contents and filenames
    contents = []
    filenames = []

    filename_txt = filename + '.txt'
    print(f"Searching for file: {filename_txt}")
    
    # Check if the file exists in the folder
    if filename_txt in os.listdir(folder):
        # Open the file and read its contents
        with open(os.path.join(folder, filename_txt), 'r', encoding='utf-8') as file:
            print("matched and read")
            contents.append(file.read())
            filenames.append(filename)

    return contents, filenames

# List can be updated to screen for these programme names
# list_of_programmes = ['programme enquiries','childcare','food']

curriculum  = {
"active_learning": ["active learning", "active exploratory learning","active exploratory learning" ],
"bilingual_curriculum": ["bilingual curriculum", "bloom curriculum", "bilingual"],
"child_directed": ["child directed", "child-centered approach","child-directed"],
"chinese_curriculum": ["chinese curriculum", "chinese integrated curriculum", "chinese"],
"early_years_development_framework": ["early years development framework",
                                       "singapore early years development framework",
                                         "aesthetics & creative expressions", "discovery of the world", 
                                         "language and literacy", "motor skills development", "numeracy", 
                                         "social and emotional development", "playgroup activities", 
                                         "sensory exploration","early years foundation stage curriculum", 
                                         "early years development", "early years"],
"english_curriculum": ["english curriculum", "english"],
"ib_pyp": ["ib pyp", "primary year programme framework",
            "primary year", "international baccalaureate primary years programme",
            "primary year programme framework"],
"inquiry_based": ["inquiry based","inquiry"],
"integrated_curriculum": ["integrated curriculum", "integrated thematic approach", "integrated",
                          "integrated theme based learning", "holistic development","holistic",
                          ],
"montessori": ["montessori"],
"moe": ["moe", "moe kindergarten curriculum framework"],
"nurturing_early_learners_curriculum": ["nurturing early learners curriculum", 
                                        "aesthetics & creative expressions", "discovery of the world", 
                                        "language and literacy", "motor skills development", "numeracy",
                                          "social and emotional development", "playgroup activities",
                                            "sensory exploration","nurturing early learners", 
                                            ],
"play_based_curriculum": ["play based", "play based curriculum", "play-based"],
"project_based": ["project based", "practical life", "project-based"],
"reggio_emilia_approach": ["reggio emilia"],
"thematic": ["thematic","theme"],
"isteam": ["isteam", "s.t.r.e.a.m."]
}


programme = {
    "aesthetics & creative expression": [
        "art", "creative arts", "creative chinese class (k1)", "creative expression",
        "creative writing", "creativity", "music", "speech and drama", "drama", "visual arts",
        "sensory play"
    ],
    "chinese": [
        "chinese as a 2nd language", "chinese culture", "chinese integrated curriculum",
        "chinese language", "chinese preschool programme", "chinese skillworks",
        "chinese speech and drama", "mandarin", "mandarin immersion programme",
        "chinese reading scheme"
    ],
    "digital skills": [
        "computer & it appreciation", "coding", "digital citizenship/ keeping safe curriculum",
        "digital literacy", "computer science", "information technology", "it", "robotics",
        "technology"
    ],
    "discovery of the word": [
        "bible as a teaching tool", "better understanding of the world through mother tongue",
        "big art", "budding literacy programme", "camps", "care & support", "character & values",
        "character building", "character development", "chatterbox", "child as a communicator",
        "child care", "childcare", "children's music programme", "exploration",
        "inquiry-based learning", "investigative learning", "project work", "phonics", "reading",
        "writing"
    ],
    "english": [
        "english", "language and literacy", "english language", "english reading scheme",
        "english speech and drama", "speech and drama", "language", "literacy",
        "reading scheme", "speech", "writing", "phonics", "reading"
    ],
    "language and literacy": [
        "english", "language", "literacy", "reading scheme", "speech", "writing", "reading", "words", "word"
    ],
    "math": [
        "math", "numeracy", "problem-solving skills", "mathematics", "reasoning", "counting",
        "numbers"
    ],
    "moral education": [
        "moral education"
    ],
    "motor skill development": [
        "motor skill"
    ],
    "music": [
        "music"
    ],
    "nature": [
        "nature", "outdoor", 
    ],
    "numeracy": [
        "numeracy"
    ],
    "problem-solving skills": [
        "problem-solving skills",
    ],
    "project work": [
        "project work", "inquiry-based learning", 
        "project-based learning", "inquiry", "research", "exploration"
    ],
    "science": [
        "science", "scientific inquiry", "scientific method", "experiments", "sciences",
        "discovery"
    ],
    "sensory play": [
        "sensory play"
    ],
    "social & emotional development": [
        "social & emotional development", "emotional intelligence", "empathy", "friendship",
        "social skills", "social", "emotional", "awareness"
    ],
    "speech and drama": [
        "speech and drama"
    ],
    "sports": [
        "sports"
    ]
}

levels =  {
    "infant_care":[
        'baby', 'baby and child care',
        'caregiving', 'infant', 'infant and toddler care', 'infant class', 
        'infant development', 'infant education', 'infant growth', 'infant learning', 
        'infant nurturing', 'infant school', 'infant teaching', 'infant_education', 
        'maternal care', 'maternal and child health Care', 'maternal health', 
        ]
    ,
    "playgroup" :[
        'INquiry Programme', 'ME Time', 'PlayGROUNDS', 'baby', 'baby class', 'care-giving', 
        'creative', "creative t's", 'curriculum framework', 'daycare', 'development', 
        'early childhood education', 'early education', 'early learner', 'early learning', 
        'early learning centre', 'early years', 'early years education', 'early years programme', 
        'infant', 'infant care', 'infant programme', 'infant school', 'kids school', 
        'play and learn', 'play based learning', 'play-based', 
        'play-based learning', 'playcenter', 'playgroup', 'playhouse', 
        'playplace', 'playschool', 'playspace', 'playtime', 'playyard', 'pre-nursery',
        'pre-school', 'preschool'],
    "nursery":[
        'care-giving', 'child care', 'childcare', 'creative', 'creche', 'crèche', 
        'daycare', 'early childhood', 'early childhood education', 'early learning', 'early years', 
        'pre-kindergarten', 'nursery education', 'nursery', 'nursery one', 'nursery school',
        'nursery two', 'n1', 'n2', 
        'nursery school', 'play-based',  'pre-school', 'preschool', 'toddler', 'toddler group'],
    "kindergarten" :[
        'child development center', 'child care', 'childcare', 'daycare',
        'early childhood care', 'early childhood education', 'early education', 'early learning', 
        'early learning centre', 'early years',  'junior school', "kid's school", 'kiddie school', 
        'kids school', "kids' learning center",  "kids' school",
        'kindergarten', 'kindergarten one', 'kindergarten programme', 
        'kindergarten two','kindergarten program', 'kindergarten school','k1', 'k2',  'learning center', 
        'play school', 'pre-primary', 'pre-primary school', 'pre-school', 'preschool', 
        "young children's center", "young children's learning"]
}

#  if really no match, can add to reference
# "nursery": ["Nursery", "nursery", "nursery"],
# "kindergarten": ["Kindergarten", "kindergarten", "kindergarten"],


# Function to search for programmes in the text
def search_programmes(text,reference_number):
    # Find programmes in the text
    offered_programmes = []
    for category, values in reference_number.items():
        for value in values:
            if re.search(value, text, re.IGNORECASE):
                offered_programmes.append(category)
                break
    return offered_programmes



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
excel_file = './resources/SchoolPages/SchoolPage_Website_Links/Preschool_List_Txt_File_Address_Full.csv'
# df = pd.read_csv(excel_file)
df = pd.read_csv(excel_file, encoding='cp1252')
#print(df.columns)

for index, row in df[['Preschool_Name','Page_Source']].iterrows():
# for index, row in df[['Preschool_Name']].head(50).iterrows():
    try:
        preschool_name = row['Preschool_Name']
        page_source = row['Page_Source']
        print(preschool_name)
        # preschool_name = "7oaks"
        data_to_extract = [curriculum, programme, levels]
        folder = "./resources/SchoolPages/SchoolPage_Page_Source"
        preschool_name_lower = preschool_name.lower().replace(" ", "_")
        
        # Check if Page_Source is not blank
        if pd.notna(page_source):
            # Check if page_source is a string representation of a list
            if isinstance(page_source, str) and page_source.startswith('[') and page_source.endswith(']'):
                # # Convert string representation of list to actual list
                # try:
                #     page_source_list = ast.literal_eval(page_source)
                # except (ValueError, SyntaxError):
                #     print(f"Error: Invalid string representation of list: {page_source}")
                #     continue
                page_source_list = page_source[1:-1].split(', ')

            # Initialize empty lists to store contents and filenames
            txt_contents = []
            filenames = []

            # Loop through each item in the list
            for source in page_source_list:
                try:
                    # Get the contents and filename
                    
                    #  see if can put the apostrophe around each value in the list of string
                    content, filename = search_txt_file_exact_match(folder, source)
                    
                    if isinstance(content, list):
                        content = ' '.join(content)
                    if isinstance(filename, list):
                        filename = ', '.join(filename)

                    if content:
                        txt_contents.append(content)
                    if filename:
                        filenames.append(filename)
                except Exception as e:
                    print(f"An error occurred in the loop over page_source_list: {e}")
                    continue
        else:
        
            txt_contents, filenames = search_txt_file(folder, preschool_name_lower)

            # join information from different files into a single string
        txt_content = ' '.join(txt_contents)
        filename = ', '.join(filenames)

        # If txt_content is None, continue to the next iteration
            
        if txt_content is None:
            filename = ''
            print("No text content found for", preschool_name)
            data = {'preschool_name': preschool_name, 'txt_file_opened': '', 'found_programmes': ''}
            for data_column in data_to_extract:
                if data_column is curriculum:
                    data_type = 'curriculum' 
                elif data_column is programme:
                    data_type = 'programme'
                else:
                    data_type = 'levels'
                     
                found_programmes = ""
               
                data['found_'+data_type]= found_programmes
                for category in data_column.keys():
                    data[data_type + '_' + category.lower().replace(" ", "_")] = 0
            df = pd.DataFrame([data])
            save_to_csv(df)
        else: 

            data = {'preschool_name': preschool_name, 'txt_file_opened': filename}
                
            for data_column in data_to_extract:
                if data_column is curriculum:
                    data_type = 'curriculum' 
                elif data_column is programme:
                    data_type = 'programme'
                else:
                    data_type = 'levels'
                     
                found_programmes = search_programmes(txt_content, data_column)
                print(found_programmes)
                
                data['found_'+data_type]= found_programmes
                # data = {'preschool_name': preschool_name, 'txt_file_opened': filename, 'found_programmes': found_programmes}
                for category in data_column.keys():
                    data[data_type + '_' + category.lower().replace(" ", "_")] = 1 if category in found_programmes else 0

            df = pd.DataFrame([data])
            save_to_csv(df)
            # save_to_csv(preschool_name, feature_info_url,query)

    except Exception as e:
        print(f"An error occurred for loop: {e}")