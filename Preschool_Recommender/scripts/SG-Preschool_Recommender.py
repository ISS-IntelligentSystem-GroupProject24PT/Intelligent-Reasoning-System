# Import the tkinter module
import os
from tkinter import messagebox

import pandas
import tkinter
import tkinter.ttk
import customtkinter
import webbrowser

# Import tkinter extension modules
import tkintermapview
# import checklistcombobox
from ChecklistCombobox import checklistcombobox
from tkcalendar import DateEntry
import datetime
from dateutil import relativedelta

# Used for styling the GUI
import tkinter.font


class WINDOWS(customtkinter.CTk):
    # File name
    USER_OUTPUT_FILE = 'FrontEnd_UserInput.csv'
    USER_RESULT_FILE = 'Results.csv'

    # File Directory
    USER_OUTPUT_DIR = "C://Preschool_Recommender//resources//FrontEnd//FrontEnd_UserInputs"
    USER_RESULT_DIR = "C://Preschool_Recommender//resources//FrontEnd//FrontEnd_RuleAlgo_Output"

    # Set up directory
    working_dir = os.path.dirname(os.path.abspath(__file__))
    if not (os.getcwd() == working_dir):
        os.chdir(working_dir)
    if not os.path.exists(USER_OUTPUT_DIR):
        os.makedirs(USER_OUTPUT_DIR)

    # Define DEFAULTS
    APP_NAME = "SG-Preschool Recommender"
    MIN_WIDTH = 1150
    MIN_HEIGHT = 850
    HEAD1_FONT = None
    HEAD2_FONT = None
    CUSTOM_FONT = None
    CUSTOM_BOLDFONT = None
    dataframe = pandas.DataFrame(columns=[
        'Primary_key',
        'Latitude_Longitude',  # Location
        'Distance_Constraint',  # Location Distance Constraint
        'Infant_Care_Singaporean',  # Citizenship Status & Age
        'Playgroup_Singaporean',
        'Nursery_Singaporean',
        'Kindergarten_Singaporean',
        'Infant_Care_PR',
        'Playgroup_PR',
        'Nursery_PR',
        'Kindergarten_PR',
        'Education_Level',  # Education Level
        'Aesthetics_Creative_Expression',  # Programmes
        'Chinese',
        'Digital_Skills',
        'Discovery_of_the_World',
        'English',
        'Language_and_Literacy',
        'Math',
        'Moral_Education',
        'Motor_Skill_Development',
        'Music',
        'Nature',
        'Numeracy',
        'Problem-solving_Skills',
        'Project Work',
        'Science',
        'Sensory Play',
        'Social & Emotional Development',
        'Speech and Drama',
        'Sports',
        'Active Learning Curriculum',  # Curriculum
        'Bilingual Curriculum',
        'Child Directed',
        'Chinese Curriculum',
        'Early Years Development Framework',
        'English Curriculum',
        'IB PYP',
        'Inquiry Based',
        'Integrated Curriculum',
        'Montessori',
        'MOE',
        'Nurturning Early Learners Curriculum',
        'Play-based Curriculum',
        'Project-based Curriculum',
        'Reggio Emilia approach',
        'SPARK certified Curriculum',
        'Thematic',
        'ISteam',
        'user_monday_drop_off',  # Drop off & Pick up Timings
        'user_monday_pick_up',
        'user_tuesday_drop_off',
        'user_tuesday_pick_up',
        'user_wednesday_drop_off',
        'user_wednesday_pick_up',
        'user_thursday_drop_off',
        'user_thursday_pick_up',
        'user_friday_drop_off',
        'user_friday_pick_up',
        'user_saturday_drop_off',
        'user_saturday_pick_up',
        'user_sunday_drop_off',
        'user_sunday_pick_up'])

    MARKER_LIST = []
    MAP_LOCATION = None
    BRAND_LIST = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Redefine DEFAULTS
        WINDOWS.HEAD1_FONT = customtkinter.CTkFont(family='Helvetica', size=30, weight='bold')
        WINDOWS.HEAD2_FONT = customtkinter.CTkFont(family='Helvetica', size=20, weight='bold')
        WINDOWS.CUSTOM_FONT = customtkinter.CTkFont(family='Roboto', size=24)
        WINDOWS.CUSTOM_BOLDFONT = customtkinter.CTkFont(family='Roboto', size=14, weight='bold')
        # Define individual screen dimensions
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        # if (screenWidth * 0.8 > WINDOWS.MIN_WIDTH):
        #     WINDOWS.MIN_WIDTH = int(screenWidth * 0.8)
        # if (screenHeight * 0.9 > WINDOWS.MIN_HEIGHT):
        #     WINDOWS.MIN_HEIGHT = int(screenHeight)

        # Find screen center point
        center_x = int(screenWidth / 2 - WINDOWS.MIN_WIDTH / 2)
        center_y = int(screenHeight / 2 - WINDOWS.MIN_HEIGHT / 2)

        # Main root window
        self.title(WINDOWS.APP_NAME)
        self.geometry(f'{WINDOWS.MIN_WIDTH}x{WINDOWS.MIN_HEIGHT}+{center_x}+{center_y}')

        # Change listbox size
        self.option_add("*Listbox*Font", "Helvetica 16")

        # Create a frame and assign to 'container' in WINDOWS(root)
        container = customtkinter.CTkFrame(self, height=WINDOWS.MIN_HEIGHT, width=WINDOWS.MIN_WIDTH)
        container.pack(side="top", fill="both", expand=True, padx=50)
        # Configure the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create a dictionary of frames
        self.frames = {}
        # Add the page Frame(s) to the dictionary.
        for F in (QuestionsPage, Resultspage):
            frame = F(container, self)

            # the WINDOWS class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Method to switch frames
        self.show_frame(QuestionsPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # Raise the current frame to the top

    def show_question_frame(self, cont):
        frame = self.frames[cont]
        for i in range(len(WINDOWS.BRAND_LIST)):
            brand = str(WINDOWS.BRAND_LIST[i])
            if i == 0:
                Resultspage.tab_view._segmented_button._buttons_dict["Preschool 1"].configure(text="Preschool 1")
                Resultspage.tab1_sch_name.set("-")
                Resultspage.tab1_address.set("-")
                Resultspage.tab1_weblink.set("-")
                Resultspage.tab1_button.configure(state='disable')
                Resultspage.tab1_map.set_position(1.417300, 103.833000, marker=False)
            else:
                Resultspage.tab_view.delete(brand)

        WINDOWS.BRAND_LIST.clear()
        frame.tkraise()  # Raise the current frame to the top

    def show_result_frame(self, cont):
        frame = self.frames[cont]

        result_dir = os.path.join(WINDOWS.USER_RESULT_DIR, WINDOWS.USER_RESULT_FILE)
        result_df = pandas.read_csv(result_dir)

        if len(result_df.index) == 0:
            Resultspage.no_result.pack(pady=15)
            frame.tkraise()
            return

        result_df = result_df.drop_duplicates(subset='preschool_brand', keep='first')
        result_df = result_df.sort_values(by="Cosine_Similarity", ascending=False)

        preschool_names_list = result_df['Preschool_Name'].tolist()
        preschool_brand_list = result_df['preschool_brand'].tolist()
        address_list = result_df['Address'].tolist()
        weblink_list = result_df['Preschool_Website'].tolist()
        location_list = result_df['Latitude_Longitude'].tolist()
        
        for top3 in range(3):
            try:
                preschool_name = str(preschool_names_list[top3])
            except:
                break
            preschool_name = str(preschool_names_list[top3])
            preschool_brand = str(preschool_brand_list[top3])
            WINDOWS.BRAND_LIST.append(preschool_brand)
            address = str(address_list[top3])
            weblink = str(weblink_list[top3])
            location = str(location_list[top3])
            if top3 == 0:
                Resultspage.tab_view._segmented_button._buttons_dict["Preschool 1"].configure(text=preschool_brand)
                Resultspage.tab1_sch_name.set(preschool_name)
                Resultspage.tab1_address.set(address)
                Resultspage.tab1_weblink.set(weblink)
                Resultspage.tab1_button.configure(state='normal')
                Resultspage.tab1_map.set_address(location, marker=True)
                Resultspage.tab1_map.set_zoom(13)
            else:
                Resultspage.tab_view.add(preschool_brand)
                tab_Frame = customtkinter.CTkFrame(Resultspage.tab_view.tab(preschool_brand))
                tab_Frame.pack()
                for i in range(2):
                    for j in range(3):
                        # Create Label.grids in all tabs
                        if (i == 1 and j == 2):
                            tab_button = customtkinter.CTkButton(
                                tab_Frame, 
                                width=250,
                                command=lambda: Resultspage.openlink())
                            tab_button._text_label.configure(wraplength=300, justify='left')
                            tab_button.grid(row=i, column=j, padx=15, pady=10)
                        elif i == 0:
                            tab_labels = customtkinter.CTkLabel(
                                tab_Frame, 
                                width=300, 
                                bg_color='light blue',
                                text_color='black',
                                wraplength=250, 
                                justify='center')
                            tab_labels.grid(row=i, column=j, padx=1, pady=10)
                        else:
                            tab_labels = customtkinter.CTkLabel(tab_Frame, wraplength=250, justify='center')
                            tab_labels.grid(row=i, column=j, padx=15, pady=10)

                        # Insert Headings
                        if (i == 0):
                            match j:
                                case 0:
                                    tab_labels.configure(text="Preschool Name", font=WINDOWS.CUSTOM_BOLDFONT)
                                case 1:
                                    tab_labels.configure(text="Address", font=WINDOWS.CUSTOM_BOLDFONT)
                                case 2:
                                    tab_labels.configure(text="Website Link", font=WINDOWS.CUSTOM_BOLDFONT)

                        # Insert Default Values
                        if (i == 1):
                            match j:
                                case 0:
                                    tab_labels.configure(text=preschool_name)
                                case 1:
                                    tab_labels.configure(text=address)
                                case 2:
                                    tab_button.configure(text=weblink)
                                    tab_button.configure(state='normal')

                tab_map = tkintermapview.TkinterMapView(
                    Resultspage.tab_view.tab(preschool_brand), 
                    width=1400, height=700,
                    corner_radius=0)
                tab_map.pack(pady=10)
        
                tab_map.set_address(location, marker=True)
                tab_map.set_zoom(13)

        frame.tkraise() # Raise the current frame to the top

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


class QuestionsPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent, width=1000, fg_color="light yellow", )

        WINDOWS.MAP_LOCATION = tkinter.StringVar()
        # adr = tkintermapview.convert_coordinates_to_address(1.417300, 103.833000)
        # question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
        WINDOWS.MAP_LOCATION.set("Current address: Yishun Ave 2, Singapore 769092")

        # Header Text
        qnsHeadText = "Find your child's ideal preschool"
        qnsHeadText2 = "Answer the questionaire based on your preschool criteria."

        # Questionaire
        qnsQn1a = "Question 1: Indicate your preferred preschool location. *"
        qnsQn1b = "Question 2: Select a preferred distance range from the indicated location? *"
        qnsQn2a = "Question 3: What is your citizenship status? *"
        qnsQn2b = "Question 4: What is your monthly budget? (SGD $) *"
        qnsQn2c = "Question 5: What is your child's date of birth? *"
        qnsQn3 = "Question 6: Select the programmes you are interested to enroll your child in."
        qnsQn4 = "Question 7: Select the preschool Curriculum style you prefer."
        qnsQn5 = "Question 8: Select the days you would like to send your child to a preschool."
        qnsQn6a = "Select your preferred drop-off timings. (Monday to Friday)"
        qnsQn6b = "Select your preferred drop-off timings. (Saturday & Sunday)"
        qnsQn7a = "Select your preferred pick-up timings."
        qnsQn7b = "Select your preferred pick-up timings."

        # ============ create 3 CTkFrames for QuestionPage() ============

        self.frame_head = customtkinter.CTkFrame(master=self, corner_radius=1, fg_color="#393e41")
        self.frame_head.pack(fill='x', padx=0, pady=0)

        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color="light yellow")
        self.frame_left.pack(side='left', padx=10, pady=25)

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color="light yellow")
        self.frame_right.pack(side='left', padx=0, pady=25)

        # ============ frame_head ============

        qns_Head1_Label = customtkinter.CTkLabel(
            self.frame_head,
            text=qnsHeadText,
            font=WINDOWS.HEAD1_FONT,
            text_color='white'
        )
        qns_Head2_Label = customtkinter.CTkLabel(
            self.frame_head,
            text=qnsHeadText2,
            font=WINDOWS.HEAD2_FONT,
            text_color='white'
        )
        qns_Head1_Label.pack(padx=10, pady=20)
        qns_Head2_Label.pack(padx=10, pady=10)

        # ============ frame_left ============

        # Question Frame containers
        # Question 1a: Location
        qns1Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qns1Frame.pack(fill='x', anchor='w')

        qns1Label = customtkinter.CTkLabel(qns1Frame, text=qnsQn1a, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        qns1Label2 = customtkinter.CTkLabel(qns1Frame, textvariable=WINDOWS.MAP_LOCATION, text_color="black")
        qns1Button = customtkinter.CTkButton(qns1Frame,
                                             text="Open Maps View",
                                             command=lambda: MapWindow(controller), height=40, width=770,
                                             fg_color="#393e41")
        qns1Label.pack(anchor='w')
        qns1Label2.pack(anchor='w')
        qns1Button.pack(anchor='w')

        # Question 1b: Distance range
        qn1bChoices1 = ('1KM', '2KM', '3KM', '4KM', '5KM', '10KM', '15KM', '20KM', '25KM')

        qn1bFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qn1bFrame.pack(fill='x', anchor='w')
        qn1bLabel = customtkinter.CTkLabel(qn1bFrame, text=qnsQn1b, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        qn1bLabel.pack(anchor='w')
        distRangeAns = customtkinter.CTkComboBox(qn1bFrame, values=qn1bChoices1, height=40, width=770,
                                                 font=(WINDOWS.CUSTOM_BOLDFONT, 16),
                                                 dropdown_font=(WINDOWS.CUSTOM_BOLDFONT, 16),
                                                 fg_color="white",
                                                 text_color="black"
                                                 )
        distRangeAns.pack(anchor='w')

        # Question 2a: Citizenship
        qn2aChoices = ('Singaporean', 'Permanent Resident')
        qn2aFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qn2aFrame.pack(fill='x', anchor='w')

        qn2aLabel = customtkinter.CTkLabel(qn2aFrame, text=qnsQn2a, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        citizenStaAns = customtkinter.CTkComboBox(qn2aFrame, values=qn2aChoices,
                                                  height=40, width=770,
                                                  font=(WINDOWS.CUSTOM_BOLDFONT, 16),
                                                  dropdown_font=(WINDOWS.CUSTOM_BOLDFONT, 16),
                                                  fg_color="white",
                                                  text_color="black"
                                                  )

        qn2aLabel.pack(anchor='w')
        citizenStaAns.pack(anchor='w')

        # Question 2b: Budget
        qns2bFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qns2bFrame.pack(fill='x', anchor='w')

        qns2bLabel = customtkinter.CTkLabel(qns2bFrame, text=qnsQn2b,
                                            font=WINDOWS.CUSTOM_BOLDFONT,
                                            text_color="black"
                                            )

        def only_numbers(char):
            return char.isdigit()

        validation = self.register(only_numbers)
        budgetAns = customtkinter.CTkEntry(
            qns2bFrame,
            height=40,
            width=770,
            placeholder_text="e.g. 1000",
            font=(WINDOWS.CUSTOM_BOLDFONT, 16),
            validate="key",
            validatecommand=(validation, '%S'),
            fg_color="white",
            text_color="black"
        )
        qns2bLabel.pack(anchor='w')
        budgetAns.pack(anchor='w')

        # Question 2c: Child Age
        curDatetime = datetime.datetime.now()  # get current datetime
        eigthteen_month_earlier = curDatetime + relativedelta.relativedelta(months=-18)
        qns2cFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qns2cFrame.pack(fill='x', anchor='w')

        qn2cLabel = customtkinter.CTkLabel(qns2cFrame, text=qnsQn2c, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        calAgeAns = DateEntry(
            qns2cFrame,
            width=71,
            font=WINDOWS.CUSTOM_FONT,
            year=eigthteen_month_earlier.year, month=eigthteen_month_earlier.month, day=eigthteen_month_earlier.day,
            background='darkblue',
            foreground='light yellow',
            orderwidth=2,
            bg_color="#393e41"
        )
        qn2cLabel.pack(anchor='w')
        calAgeAns.pack(anchor='w')

        # Question 3: School Programmes
        qn3Choices = ('Aesthetics & Creative Expression',
                      'Chinese',
                      'Digital Skills',
                      'Discovery of the World',
                      'English',
                      'Language and Literacy',
                      'Math',
                      'Moral Education',
                      'Motor Skill Development',
                      'Music',
                      'Nature',
                      'Numeracy',
                      'Problem-solving Skills',
                      'Project Work',
                      'Science',
                      'Sensory Play',
                      'Social & Emotional Development',
                      'Speech and Drama',
                      'Sports')
        qn3Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qn3Frame.pack(fill='x', anchor='w')

        qn3Label = customtkinter.CTkLabel(qn3Frame, text=qnsQn3, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        progAns = checklistcombobox.ChecklistCombobox(
            qn3Frame,
            width=71,
            font=WINDOWS.CUSTOM_FONT,
            values=qn3Choices,
        )

        qn3Label.pack(anchor='w')
        progAns.pack(anchor='w')

        # Question 4: Curriculum
        qn4Choices = ('Active Learning Curriculum',
                      'Bilingual Curriculum',
                      'Child Directed',
                      'Chinese Curriculum',
                      'Early Years Development Framework',
                      'English Curriculum',
                      'IB PYP',
                      'Inquiry Based',
                      'Integrated Curriculum',
                      'Montessori',
                      'MOE',
                      'Nurturning Early Learners Curriculum',
                      'Play-based Curriculum',
                      'Project-based Curriculum',
                      'Reggio Emilia approach',
                      'SPARK certified Curriculum',
                      'Thematic',
                      'ISteam')
        qn4Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qn4Frame.pack(fill='x', anchor='w')

        qn4Label = customtkinter.CTkLabel(qn4Frame, text=qnsQn4, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        currAns = checklistcombobox.ChecklistCombobox(
            qn4Frame,
            width=71,
            font=WINDOWS.CUSTOM_FONT,
            values=qn4Choices,
        )

        qn4Label.pack(anchor='w')
        currAns.pack(anchor='w')

        # Question 5: Days to send child (Mon to Sun)
        qn5Choices = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        qn5Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qn5Frame.pack(fill='x', anchor='w')

        qn5Label = customtkinter.CTkLabel(qn5Frame, text=qnsQn5, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        daysSentAns = checklistcombobox.ChecklistCombobox(
            qn5Frame,
            width=71,
            font=WINDOWS.CUSTOM_FONT,
            values=qn5Choices,
        )

        daysSentAns.bind("<<ComboboxSelected>>",
                         lambda e: QuestionsPage.refreshQuestion(
                             daysSentAns, dropoffWkEnd, pickupWkEnd, qn7FrameRight, qn6FrameLeft, qn6QnLabel
                         ))

        qn5Label.pack(anchor='w')
        daysSentAns.pack(anchor='w')

        # Question 9 Left & Right: Pick Up and Drop off timing
        qn9Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0, fg_color="light yellow")
        qn9Frame.pack(fill="x", anchor='w')
        qn6QnLabel = customtkinter.CTkLabel(qn9Frame, text="Question 9:", font=WINDOWS.CUSTOM_BOLDFONT,
                                            text_color="black")
        # qn6QnLabel.pack(anchor='w')

        qn6Choices1 = ('', '7AM', '8AM', '9AM', '10AM', '11AM', '12PM')
        qn6Choices2 = ('', '7AM', '8AM', '9AM', '10AM')

        qn6FrameLeft = customtkinter.CTkFrame(qn9Frame, corner_radius=0, fg_color="light yellow")
        # qn6FrameLeft.pack(side="left", anchor='w')
        qn7FrameRight = customtkinter.CTkFrame(qn9Frame, corner_radius=0, fg_color="light yellow")
        # qn7FrameRight.pack(side="left", anchor='w')

        qn6LabelA = customtkinter.CTkLabel(qn6FrameLeft, text=qnsQn6a, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        qn6LabelB = customtkinter.CTkLabel(qn7FrameRight, text=qnsQn6b, font=WINDOWS.CUSTOM_BOLDFONT,
                                           text_color="black")

        qn6LabelA.pack(padx=(0, 30), pady=0, anchor='w')
        qn6LabelB.pack(padx=(0, 30), pady=0, anchor='w')

        dropoffReg = customtkinter.CTkComboBox(qn6FrameLeft, values=qn6Choices1, height=40, width=325,
                                               fg_color="white",
                                               text_color="black"
                                               )
        dropoffWkEnd = customtkinter.CTkComboBox(qn7FrameRight, values=qn6Choices2, height=40, width=325,
                                                 fg_color="white",
                                                 text_color="black"
                                                 )
        dropoffReg.pack(anchor='w')
        dropoffWkEnd.pack(anchor='w')

        qn7Choices1 = ('', '1PM', '2PM', '3PM', '4PM', '5PM', '6PM', '7PM')
        qn7Choices2 = ('', '12PM', '1PM', '2PM')

        qn7LabelA = customtkinter.CTkLabel(qn6FrameLeft, text=qnsQn7a, font=WINDOWS.CUSTOM_BOLDFONT, text_color="black")
        qn7LabelB = customtkinter.CTkLabel(qn7FrameRight, text=qnsQn7b, font=WINDOWS.CUSTOM_BOLDFONT,
                                           text_color="black")
        qn7LabelA.pack(pady=0, anchor='w')
        qn7LabelB.pack(pady=0, anchor='w')

        pickupReg = customtkinter.CTkComboBox(qn6FrameLeft, values=qn7Choices1, height=40, width=325,
                                              fg_color="white",
                                              text_color="black"
                                              )
        pickupWkEnd = customtkinter.CTkComboBox(qn7FrameRight, values=qn7Choices2, height=40, width=325,
                                                fg_color="white",
                                                text_color="black"
                                                )
        pickupReg.pack(anchor='w')
        pickupWkEnd.pack(anchor='w')

        dropoffWkEnd.configure(state='disable')
        pickupWkEnd.configure(state='disable')

        # Buttons
        switch_window = customtkinter.CTkButton(
            self.frame_right,
            text="Generate Results",
            command=lambda: QuestionsPage.outputQuestionaire(
                controller, distRangeAns,
                citizenStaAns, budgetAns, calAgeAns,
                progAns, currAns,
                daysSentAns, dropoffReg, dropoffWkEnd, pickupReg, pickupWkEnd
            ), height=40, width=150, fg_color='#e94f37',
            font=WINDOWS.CUSTOM_BOLDFONT
        )
        quit_button = customtkinter.CTkButton(
            self.frame_right,
            text="Quit",
            command=lambda: controller.on_closing(),
            height=40, width=150, fg_color="#393e41",
            font=WINDOWS.CUSTOM_BOLDFONT
        )
        switch_window.pack(padx=5, pady=5, anchor='w')
        quit_button.pack(padx=5, pady=5, anchor='w')


    def refreshQuestion(qn6Ans, dropoffWkEnd, pickupWkEnd, qn7FrameRight, qn6FrameLeft, qn6QnLabel):
        selected = qn6Ans.selection_get()
        if "Saturday" in selected or "Sunday" in selected:
            dropoffWkEnd.configure(state='normal')
            pickupWkEnd.configure(state='normal')
            qn6QnLabel.pack(anchor='w')
            qn7FrameRight.pack(side="left", anchor='w')
        elif "Saturday" not in selected and "Sunday" not in selected:
            dropoffWkEnd.configure(state='disable')
            pickupWkEnd.configure(state='disable')
            qn7FrameRight.pack_forget()
        else:
            qn6QnLabel.pack(anchor='w')
            qn7FrameRight.pack(side="left", anchor='w')

        if "Monday" in selected or "Tuesday" in selected or "Wednesday" in selected or "Thursday" in selected or "Friday" in selected:
            qn6QnLabel.pack(anchor='w')
            qn6FrameLeft.pack(side="left", anchor='w')
        elif "Monday" not in selected and "Tuesday" not in selected and "Wednesday" not in selected and "Thursday" not in selected and "Friday" not in selected:
            qn6FrameLeft.pack_forget()
        else:
            qn6QnLabel.pack(anchor='w')
            qn6FrameLeft.pack(side="left", anchor='w')

    def outputQuestionaire(controller, distRangeAns,
                           citizenStaAns, budgetAns, calAgeAns,
                           progAns, currAns,
                           daysSentAns, dropoffReg, dropoffWkEnd, pickupReg, pickupWkEnd):
        if budgetAns.get() == "":
            messagebox.showerror("Error", "Please input a monthly budget.")
            return
        else:
            userInput = []
            userInput.append(str(datetime.datetime.now()))
            userInput.extend(QuestionsPage.getMarkerPos())
            userInput.append(distRangeAns.get().strip("KM"))
            userInput.extend(QuestionsPage.getEduLvlWithCitizenship(citizenStaAns.get(), calAgeAns, budgetAns.get()))
            userInput.extend(QuestionsPage.getSelectedProgrammes(progAns.get()))
            userInput.extend(QuestionsPage.getSelectedCurriculum(currAns.get()))
            userInput.extend(
                QuestionsPage.getSelectedDayswithTiming(daysSentAns.get(), dropoffReg.get(), dropoffWkEnd.get(),
                                                        pickupReg.get(), pickupWkEnd.get()))
            QuestionsPage.generateFile(userInput)

        import BusinessRuleEngine
        BusinessRuleEngine.BusinessRulesEngine().trigger_business_rule()

        controller.show_result_frame(Resultspage)

    def generateFile(userInput):
        WINDOWS.dataframe.drop(WINDOWS.dataframe.index, inplace=True)
        WINDOWS.dataframe.loc[len(WINDOWS.dataframe)] = userInput

        output_file = os.path.join(WINDOWS.USER_OUTPUT_DIR, WINDOWS.USER_OUTPUT_FILE)
        WINDOWS.dataframe.to_csv(path_or_buf=output_file, index=False)

    def getMarkerPos():
        if (len(WINDOWS.MARKER_LIST) <= 0):
            return ['1.417300, 103.833000']
        else:
            temp = str(WINDOWS.MARKER_LIST[0].position).strip("()")
            return [temp]

    def getEduLvlWithCitizenship(Status, calDate, budget):
        eduLvlwithStatus = ['0', '0', '0', '0', '0', '0', '0', '0', '1']
        date1 = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        date2 = datetime.datetime.strptime(str(calDate.get_date()), '%Y-%m-%d')
        r = relativedelta.relativedelta(date1, date2)
        months = r.months + 12 * r.years
        if r.days > 0:
            months += 1

        years = r.years

        if Status == "Singaporean":
            if years >= 5:  # Kindergarten_Singaporean
                eduLvlwithStatus = ['0', '0', '0', budget, '0', '0', '0', '0', '4']
            elif years >= 3 and years <= 4:  # Nursery_Singaporean
                eduLvlwithStatus = ['0', '0', budget, '0', '0', '0', '0', '0', '3']
            elif months >= 18 and months <= 24:
                eduLvlwithStatus = ['0', budget, '0', '0', '0', '0', '0', '0', '2']
            elif months >= 2 and months <= 17:
                eduLvlwithStatus = [budget, '0', '0', '0', '0', '0', '0', '0', '1']
        else:
            if years >= 5:  # Kindergarten_Singaporean
                eduLvlwithStatus = ['0', '0', '0', '0', '0', '0', '0', budget, '4']
            elif years >= 3 and years <= 4:  # Nursery_Singaporean
                eduLvlwithStatus = ['0', '0', '0', '0', '0', '0', budget, '0', '3']
            elif months >= 18 and months <= 24:
                eduLvlwithStatus = ['0', '0', '0', '0', '0', budget, '0', '0', '2']
            elif months >= 2 and months <= 17:
                eduLvlwithStatus = ['0', '0', '0', '0', budget, '0', '0', '0', '1']

        return eduLvlwithStatus

    def getSelectedProgrammes(programmes):
        programmesSelected = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                              '0']
        qn3Choices = ['Aesthetics & Creative Expression',
                      'Chinese',
                      'Digital Skills',
                      'Discovery of the World',
                      'English',
                      'Language and Literacy',
                      'Math',
                      'Moral Education',
                      'Motor Skill Development',
                      'Music',
                      'Nature',
                      'Numeracy',
                      'Problem-solving Skills',
                      'Project Work',
                      'Science',
                      'Sensory Play',
                      'Social & Emotional Development',
                      'Speech and Drama',
                      'Sports']
        for programme in programmes:
            prog_index = qn3Choices.index(programme) if programme in qn3Choices else -1
            if (prog_index != -1):
                programmesSelected[prog_index] = '1'

        return programmesSelected

    def getSelectedCurriculum(curriculums):
        curriculumSelected = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
        qn4Choices = ['Active Learning Curriculum',
                      'Bilingual Curriculum',
                      'Child Directed',
                      'Chinese Curriculum',
                      'Early Years Development Framework',
                      'English Curriculum',
                      'IB PYP',
                      'Inquiry Based',
                      'Integrated Curriculum',
                      'Montessori',
                      'MOE',
                      'Nurturning Early Learners Curriculum',
                      'Play-based Curriculum',
                      'Project-based Curriculum',
                      'Reggio Emilia approach',
                      'SPARK certified Curriculum',
                      'Thematic',
                      'ISteam']
        for curriculum in curriculums:
            curr_index = qn4Choices.index(curriculum) if curriculum in qn4Choices else -1
            if (curr_index != -1):
                curriculumSelected[curr_index] = '1'

        return curriculumSelected

    def getSelectedDayswithTiming(daysSelected, dropoffReg, dropoffWkEnd, pickupReg, pickupWkEnd):
        daysSelectedwithTiming = ['', '', '', '', '', '', '', '', '', '', '', '', '', '']

        dropoffReg = QuestionsPage.stripTiming(dropoffReg)
        pickupReg = QuestionsPage.stripTiming(pickupReg)
        dropoffWkEnd = QuestionsPage.stripTiming(dropoffWkEnd)
        pickupWkEnd = QuestionsPage.stripTiming(pickupWkEnd)

        for days in daysSelected:
            match days:
                case 'Monday':
                    daysSelectedwithTiming[0] = dropoffReg
                    daysSelectedwithTiming[1] = pickupReg
                case 'Tuesday':
                    daysSelectedwithTiming[2] = dropoffReg
                    daysSelectedwithTiming[3] = pickupReg
                case 'Wednesday':
                    daysSelectedwithTiming[4] = dropoffReg
                    daysSelectedwithTiming[5] = pickupReg
                case 'Thursday':
                    daysSelectedwithTiming[6] = dropoffReg
                    daysSelectedwithTiming[7] = pickupReg
                case 'Friday':
                    daysSelectedwithTiming[8] = dropoffReg
                    daysSelectedwithTiming[9] = pickupReg
                case 'Saturday':
                    daysSelectedwithTiming[10] = dropoffWkEnd
                    daysSelectedwithTiming[11] = pickupWkEnd
                case 'Sunday':
                    daysSelectedwithTiming[12] = dropoffWkEnd
                    daysSelectedwithTiming[13] = pickupWkEnd
        return daysSelectedwithTiming

    def stripTiming(timing):
        if "AM" in timing:
            return timing.strip("AM")
        elif "PM" in timing:
            timing = timing.strip("PM")
            if (timing == '12'):
                return timing
            else:
                timing = str(int(timing) + 12)
                return timing


class MapWindow(tkinter.Toplevel):
    def __init__(self, master=None):

        tkinter.Toplevel.__init__(self)
        self.title("Map")
        self.geometry("1400x900")

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Change listbox size
        self.option_add("*Listbox*Font", "Helvetica 16")

        # self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        # self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============
        #
        # self.frame_left.grid_rowconfigure(2, weight=1)
        #
        # self.button_1 = customtkinter.CTkButton(master=self.frame_left,
        #                                         text="Pick Location",
        #                                         command=self.set_marker_event)
        # self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = tkintermapview.TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=4, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Clear",
                                                command=self.clear_marker_event)
        self.button_2.grid(row=0, column=2, sticky="w", padx=(5, 0), pady=12)

        self.button_6 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Confirm",
                                                command=self.on_closing)
        self.button_6.grid(row=0, column=3, sticky="w", padx=(5, 0), pady=12)

        # Set default values
        if len(WINDOWS.MARKER_LIST) >= 1:
            address = str(WINDOWS.MARKER_LIST[0].position).strip("()")
            WINDOWS.MARKER_LIST.clear()
            self.map_widget.set_position(float(address.split(',')[0]), float(address.split(',')[1]))
            WINDOWS.MARKER_LIST.append(
                self.map_widget.set_marker(float(address.split(',')[0]), float(address.split(',')[1])))
        else:
            # self.map_widget.set_address(1.4173, 103.8330)
            self.map_widget.set_position(1.417300, 103.833000)
            WINDOWS.MARKER_LIST.append(
                self.map_widget.set_marker(1.417300, 103.833000))
        self.map_widget.set_zoom(12)

        # Define right click events before using event commands
        def add_marker_event(coords):
            coordsText = str(coords[0]) + "," + str(coords[1])
            self.map_widget.delete_all_marker()
            WINDOWS.MARKER_LIST.clear()
            WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(
                coords[0], coords[1],
                text=coordsText
            ))

            try:
                adr = tkintermapview.convert_coordinates_to_address(coords[0], coords[1])
                question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
                WINDOWS.MAP_LOCATION.set(question_location)
            except:
                print("API call error. Current address is updated in the database. Please proceed with the Questionaire.")

        # self.map_widget.add_right_click_menu_command(
        #     label="Pick Location",
        #     command=add_marker_event,
        #     pass_coords=True
        # )

        self.map_widget.add_left_click_map_command(
            callback_function=add_marker_event
        )

    def search_event(self, event=None):
        self.map_widget.set_address(f"{self.entry.get()}, Singapore")
        current_position = self.map_widget.get_position()
        self.map_widget.delete_all_marker()
        WINDOWS.MARKER_LIST.clear()
        WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(current_position[0], current_position[1]))
        try:
            adr = tkintermapview.convert_coordinates_to_address(current_position[0], current_position[1])
            question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
            WINDOWS.MAP_LOCATION.set(question_location)
        except:
            print("API call error. Current address is updated in the database. Please proceed with the Questionaire.")

    # def set_marker_event(self):
    #     current_position = self.map_widget.get_position()
    #     self.map_widget.delete_all_marker()
    #     WINDOWS.MARKER_LIST.clear()
    #     WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(current_position[0], current_position[1]))
    #     adr = tkintermapview.convert_coordinates_to_address(current_position[0], current_position[1])
    #     question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
    #     WINDOWS.MAP_LOCATION.set(question_location)

    def clear_marker_event(self):
        self.map_widget.delete_all_marker()
        WINDOWS.MARKER_LIST.clear()

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


class Resultspage(customtkinter.CTkFrame):
    # Instantiate Result variables
    tab_view = None
    tab1_button= None

    tab1_sch_name = None
    tab1_address = None
    tab1_weblink = None
    tab1_map = None

    no_result = None

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent, fg_color="light yellow")

        # ResultPage textvariables
        Resultspage.tab1_sch_name = tkinter.StringVar()
        Resultspage.tab1_address = tkinter.StringVar()
        Resultspage.tab1_weblink = tkinter.StringVar()

        # Set default value for empty results
        Resultspage.tab1_sch_name.set("-")
        Resultspage.tab1_address.set("-")
        Resultspage.tab1_weblink.set("-")

        resultHeading = customtkinter.CTkLabel(
            self, 
            text="Find your child's ideal Preschool",
            font=WINDOWS.HEAD1_FONT,
            text_color='black')
        resultHeading.pack(pady=15)

        resultHeading2 = customtkinter.CTkLabel(
            self, 
            text="The Top 3 School Brands with the closest match will be shown below.",
            font=WINDOWS.HEAD2_FONT,
            text_color='black')
        resultHeading2.pack()

        Resultspage.no_result = customtkinter.CTkLabel(
            self, 
            text="No results found! Please click \"Redo\".",
            font=WINDOWS.HEAD2_FONT,
            text_color='black')
        Resultspage.no_result.pack_forget()

        Resultspage.tab_view = customtkinter.CTkTabview(self)
        Resultspage.tab_view.pack(padx=20, pady=20)

        # Add result tabs
        Resultspage.tab_view.add("Preschool 1")

        tab1_Frame = customtkinter.CTkFrame(Resultspage.tab_view.tab("Preschool 1"))
        tab1_Frame.pack()

        for i in range(2):
            for j in range(3):
                # Create Label.grids in all tabs
                
                if (i == 1 and j == 2):
                    Resultspage.tab1_button = customtkinter.CTkButton(
                        tab1_Frame, 
                        width=250,
                        command=lambda: Resultspage.openlink())
                    Resultspage.tab1_button._text_label.configure(wraplength=250, justify='left')
                    Resultspage.tab1_button.configure(state='disabled')
                    Resultspage.tab1_button.grid(row=i, column=j, padx=1, pady=10)
                elif i == 0:
                    tab1_labels = customtkinter.CTkLabel(
                        tab1_Frame, 
                        width=300, 
                        bg_color='light blue',
                        text_color='black',
                        wraplength=250, 
                        justify='center')
                    tab1_labels.grid(row=i, column=j, padx=1, pady=10)
                else:
                    tab1_labels = customtkinter.CTkLabel(tab1_Frame, wraplength=250, justify='center')
                    tab1_labels.grid(row=i, column=j, padx=1, pady=10)

                # Insert Headings
                if (i == 0):
                    match j:
                        case 0:
                            tab1_labels.configure(text="Preschool Name", font=WINDOWS.CUSTOM_BOLDFONT)
                        case 1:
                            tab1_labels.configure(text="Address", font=WINDOWS.CUSTOM_BOLDFONT)
                        case 2:
                            tab1_labels.configure(text="Website Link", font=WINDOWS.CUSTOM_BOLDFONT)

                # Insert Default Values
                if (i == 1):
                    match j:
                        case 0:
                            tab1_labels.configure(textvariable=Resultspage.tab1_sch_name)
                        case 1:
                            tab1_labels.configure(textvariable=Resultspage.tab1_address)
                        case 2:
                            Resultspage.tab1_button.configure(textvariable=Resultspage.tab1_weblink)

        Resultspage.tab1_map = tkintermapview.TkinterMapView(
            Resultspage.tab_view.tab("Preschool 1"), 
            width=1200, height=600,
            corner_radius=0)
        Resultspage.tab1_map.pack(pady=10)
        
        Resultspage.tab1_map.set_position(1.417300, 103.833000)
        Resultspage.tab1_map.set_zoom(13)

        # Buttons
        result_End_Frame = customtkinter.CTkFrame(self, fg_color='light yellow')
        result_End_Frame.pack()
        restart_window = customtkinter.CTkButton(
            result_End_Frame, 
            text="Redo", 
            bg_color='transparent',
            command=lambda: controller.show_question_frame(QuestionsPage)
        )
        quit_button = customtkinter.CTkButton(
            result_End_Frame,
            text="Quit",
            bg_color='transparent',
            command=lambda: controller.on_closing()
        )
        restart_window.pack(pady=10)
        quit_button.pack(pady=10)

    def openlink():
        webbrowser.open_new_tab(Resultspage.tab1_weblink.get())


if __name__ == "__main__":
    app = WINDOWS()
    app.start()
