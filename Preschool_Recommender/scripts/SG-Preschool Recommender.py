# Import the tkinter module
import os
import pandas
import tkinter
import tkinter.ttk
import customtkinter
import webbrowser

# Import tkinter extension modules
import tkintermapview
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
    MIN_WIDTH = 1050
    MIN_HEIGHT = 750
    HEAD1_FONT = None
    HEAD2_FONT = None
    CUSTOM_FONT = None
    CUSTOM_BOLDFONT = None
    dataframe = pandas.DataFrame(columns=[
            'Primary_key',
            'Latitude_Longitude', # Location
            'Distance_Constraint', # Location Distance Constraint
            'Infant_Care_Singaporean',  # Citizenship Status & Age
            'Playgroup_Singaporean', 
            'Nursery_Singaporean', 
            'Kindergarten_Singaporean',
            'Infant_Care_PR',
            'Playgroup_PR', 
            'Nursery_PR',
            'Kindergarten_PR', 
            'Education_Level', # Education Level
            'Aesthetics_Creative_Expression', # Programmes
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
            'Active Learning Curriculum', #Curriculum
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
            'user_monday_drop_off', # Drop off & Pick up Timings
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
        if (screenWidth*0.7 > WINDOWS.MIN_WIDTH):
            WINDOWS.MIN_WIDTH = int(screenWidth*0.65)
        if (screenHeight*0.8 > WINDOWS.MIN_HEIGHT):
            WINDOWS.MIN_HEIGHT = int(screenHeight*0.8)

        # Find screen center point
        center_x = int(screenWidth/2 - WINDOWS.MIN_WIDTH / 2)
        center_y = int(screenHeight/2 - WINDOWS.MIN_HEIGHT / 2)

        # Main root window
        self.title(WINDOWS.APP_NAME)
        self.geometry(f'{WINDOWS.MIN_WIDTH}x{WINDOWS.MIN_HEIGHT}+{center_x}+{center_y}')

        # Create a frame and assign to 'container' in WINDOWS(root)
        container = customtkinter.CTkFrame(self, height=WINDOWS.MIN_HEIGHT, width=WINDOWS.MIN_WIDTH)
        container.pack(side="top", fill="both", expand=True)
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
        frame.tkraise() # Raise the current frame to the top

    def show_question_frame(self, cont):
        frame = self.frames[cont]

        for i in range(len(WINDOWS.BRAND_LIST)):
            brand = str(WINDOWS.BRAND_LIST[i]).rstrip()
            if i == 0:
                Resultspage.tab_view._segmented_button._buttons_dict["Preschool 1"].configure(text="Preschool 1")
                Resultspage.tab1_sch_name.set("-")
                Resultspage.tab1_address.set("-")
                Resultspage.tab1_weblink.set("-")
                Resultspage.tab1_button.configure(state='disable')
                Resultspage.tab1_map.set_address("Singapore", marker=False)
            else:
                Resultspage.tab_view.delete(brand)

        WINDOWS.BRAND_LIST.clear()
        frame.tkraise() # Raise the current frame to the top

    def show_result_frame(self, cont):
        frame = self.frames[cont]

        result_dir = os.path.join(WINDOWS.USER_RESULT_DIR, WINDOWS.USER_RESULT_FILE)
        result_df = pandas.read_csv(result_dir)

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
                                command=lambda: Resultspage.openlink())
                            tab_button._text_label.configure(wraplength=300, justify='left')
                            tab_button.grid(row=i, column=j, padx=15, pady=10)
                        else:
                            tab_labels = customtkinter.CTkLabel(tab_Frame, wraplength=300, justify='center')
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
                    width=1100, height=500,
                    corner_radius=0)
                tab_map.pack()
        
                tab_map.set_address(location, marker=True)
                tab_map.set_zoom(13)

        frame.tkraise() # Raise the current frame to the top  

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

class QuestionsPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent, width=1000)

        WINDOWS.MAP_LOCATION = tkinter.StringVar()
        adr = tkintermapview.convert_coordinates_to_address(1.290270, 103.851959)
        question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
        WINDOWS.MAP_LOCATION.set(question_location)

        # Header Text
        qnsHeadText = "Find your child's ideal Preschool"
        qnsHeadText2 = "Answer the questionaire based on your preschool criterias."
        
        # Questionaire
        qnsQn1a = "Question 1: Indicate your preferred Preschool location."
        qnsQn1b = "Question 2: Select a preferred distance range from the indicated location?"
        qnsQn2a = "Question 3: What is your citizenship status?"
        qnsQn2b = "Question 4: What is your available budget? ($)"
        qnsQn2c = "Question 5: How old is your child?"
        qnsQn3 = "Question 6: Select the programmes you are interested to enroll your child in."
        qnsQn4 = "Question 7: Select the Pre-school Curriculum style you prefer."
        qnsQn5 = "Question 8: Select the days you would like to send your child to a Pre-school."
        qnsQn6a = "Select your preferred drop-off timings. (Monday to Friday)"
        qnsQn6b = "Select your preferred drop-off timings. (Saturday & Sunday)"
        qnsQn7a = "Select your preferred pick-up timings."
        qnsQn7b = "Select your preferred pick-up timings."
        qnsQn8 = "Question 11: Overall rating of Pre-school"

        # ============ create 3 CTkFrames for QuestionPage() ============

        self.frame_head = customtkinter.CTkFrame(master=self, corner_radius=1, fg_color="#B1F1FF",)
        self.frame_head.pack(fill='x', padx=0, pady=0)

        self.frame_left = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color=None)
        self.frame_left.pack(side='left', padx=10, pady=25)

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        self.frame_right.pack(side='left', padx=0, pady=25)

        # ============ frame_head ============

        qns_Head1_Label = customtkinter.CTkLabel(
            self.frame_head, 
            text=qnsHeadText,
            font=WINDOWS.HEAD1_FONT
            )
        qns_Head2_Label = customtkinter.CTkLabel(
            self.frame_head,
            text=qnsHeadText2,
            font=WINDOWS.HEAD2_FONT
        )
        qns_Head1_Label.pack(padx=10, pady=20)
        qns_Head2_Label.pack(padx=10, pady=10)

        # ============ frame_left ============

    # Question Frame containers
      # Question 1a: Location
        qns1Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qns1Frame.pack(fill='x')

        qns1Label = customtkinter.CTkLabel(qns1Frame, text=qnsQn1a, font=WINDOWS.CUSTOM_BOLDFONT)
        qns1Label2 = customtkinter.CTkLabel(qns1Frame, textvariable=WINDOWS.MAP_LOCATION)
        qns1Button = customtkinter.CTkButton(qns1Frame,
                                    text="Open Maps View",
                                    command=lambda: MapWindow(controller))
        qns1Label.pack()
        qns1Label2.pack()
        qns1Button.pack()

      # Question 1b: Distance range
        qn1bChoices1 = ('1KM', '5KM', '10KM', '15KM')

        qn1bFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qn1bFrame.pack(fill='x')
        qn1bLabel  = customtkinter.CTkLabel(qn1bFrame, text=qnsQn1b, font=WINDOWS.CUSTOM_BOLDFONT)
        qn1bLabel.pack()
        distRangeAns = customtkinter.CTkComboBox(qn1bFrame, values=qn1bChoices1)
        distRangeAns.pack()

      # Question 2a: Citizenship
        qn2aChoices = ('Singaporean', 'Permanent Resident')
        qn2aFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qn2aFrame.pack(fill='x')

        qn2aLabel = customtkinter.CTkLabel(qn2aFrame, text=qnsQn2a, font=WINDOWS.CUSTOM_BOLDFONT)
        citizenStaAns = customtkinter.CTkComboBox(qn2aFrame, values=qn2aChoices) 

        qn2aLabel.pack()
        citizenStaAns.pack()

      # Question 2b: Budget
        qns2bFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qns2bFrame.pack(fill='x')

        qns2bLabel = customtkinter.CTkLabel(qns2bFrame, text=qnsQn2b, font=WINDOWS.CUSTOM_BOLDFONT)
        budgetAns = customtkinter.CTkEntry(qns2bFrame, height = 1, width = 120, placeholder_text="e.g. 1000")
        # TODO: add numbers constraint

        qns2bLabel.pack()
        budgetAns.pack()

      # Question 2c: Child Age
        curDatetime = datetime.datetime.now() # get current datetime
        eigthteen_month_earlier = curDatetime + relativedelta.relativedelta(months=-18)
        qns2cFrame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qns2cFrame.pack(fill='x')

        qn2cLabel = customtkinter.CTkLabel(qns2cFrame, text=qnsQn2c, font=WINDOWS.CUSTOM_BOLDFONT)
        calAgeAns = DateEntry(
            qns2cFrame, 
            width=24, 
            font=WINDOWS.CUSTOM_FONT,
            year=eigthteen_month_earlier.year, month=eigthteen_month_earlier.month, day=eigthteen_month_earlier.day, 
            background='darkblue', 
            foreground='white', 
            orderwidth=2)
        qn2cLabel.pack()
        calAgeAns.pack(padx=10, pady=10)

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
        qn3Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qn3Frame.pack(fill='x')

        qn3Label = customtkinter.CTkLabel(qn3Frame, text=qnsQn3, font=WINDOWS.CUSTOM_BOLDFONT)
        progAns = checklistcombobox.ChecklistCombobox(
            qn3Frame, 
            width=60,
            font=WINDOWS.CUSTOM_FONT,
            values=qn3Choices)

        qn3Label.pack()
        progAns.pack()

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
        qn4Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qn4Frame.pack(fill='x')

        qn4Label = customtkinter.CTkLabel(qn4Frame, text=qnsQn4, font=WINDOWS.CUSTOM_BOLDFONT)
        currAns = checklistcombobox.ChecklistCombobox(
            qn4Frame, 
            width=60,
            font=WINDOWS.CUSTOM_FONT, 
            values=qn4Choices)

        qn4Label.pack()
        currAns.pack()

      # Question 5: Days to send child (Mon to Sun)
        qn5Choices = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        qn5Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qn5Frame.pack(fill='x')

        qn5Label = customtkinter.CTkLabel(qn5Frame, text=qnsQn5, font=WINDOWS.CUSTOM_BOLDFONT)
        daysSentAns = checklistcombobox.ChecklistCombobox(
            qn5Frame, 
            width=48,
            font=WINDOWS.CUSTOM_FONT, 
            values=qn5Choices)
        daysSentAns.bind("<<ComboboxSelected>>", lambda e: QuestionsPage.refreshQuestion(daysSentAns, dropoffWkEnd, pickupWkEnd))

        qn5Label.pack()
        daysSentAns.pack()

      # Question 9 Left & Right: Pick Up and Drop off timing
        qn9Frame = customtkinter.CTkFrame(self.frame_left, corner_radius=0)
        qn9Frame.pack(fill="x")
        qn6QnLabel = customtkinter.CTkLabel(qn9Frame, text="Question 9:", font=WINDOWS.CUSTOM_BOLDFONT)
        qn6QnLabel.pack()

        qn6Choices1 = ('7AM', '8AM', '9AM', '10AM', '11AM', '12PM')
        qn6Choices2 = ('7AM', '8AM', '9AM', '10AM')

        qn6FrameLeft = customtkinter.CTkFrame(qn9Frame, corner_radius=0, fg_color="transparent")
        qn6FrameLeft.pack(side="left")
        qn7FrameRight = customtkinter.CTkFrame(qn9Frame, corner_radius=0, fg_color="transparent")
        qn7FrameRight.pack(side="left")
        
        qn6LabelA  = customtkinter.CTkLabel(qn6FrameLeft, text=qnsQn6a, font=WINDOWS.CUSTOM_BOLDFONT)
        qn6LabelB  = customtkinter.CTkLabel(qn7FrameRight, text=qnsQn6b, font=WINDOWS.CUSTOM_BOLDFONT)
        
        qn6LabelA.pack(padx=15, pady=0)
        qn6LabelB.pack(padx=15, pady=0)

        dropoffReg = customtkinter.CTkComboBox(qn6FrameLeft, values=qn6Choices1)
        dropoffWkEnd = customtkinter.CTkComboBox(qn7FrameRight, values=qn6Choices2)
        dropoffReg.pack()
        dropoffWkEnd.pack()

        qn7Choices1 = ('3PM', '4PM', '5PM', '6PM', '7PM')
        qn7Choices2 = ('12PM', '1PM', '2PM')

        qn7LabelA  = customtkinter.CTkLabel(qn6FrameLeft, text=qnsQn7a, font=WINDOWS.CUSTOM_BOLDFONT)
        qn7LabelB  = customtkinter.CTkLabel(qn7FrameRight, text=qnsQn7b, font=WINDOWS.CUSTOM_BOLDFONT)
        qn7LabelA.pack(padx=15, pady=0)
        qn7LabelB.pack(padx=15, pady=0)

        pickupReg = customtkinter.CTkComboBox(qn6FrameLeft, values=qn7Choices1)
        pickupWkEnd = customtkinter.CTkComboBox(qn7FrameRight, values=qn7Choices2)
        pickupReg.pack()
        pickupWkEnd.pack()

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
                )
        )
        quit_button = customtkinter.CTkButton(
            self.frame_right,
            text="Quit",
            command=lambda: controller.on_closing(),
        )
        switch_window.pack(padx=5, pady=5)
        quit_button.pack(padx=5, pady=5)

    def refreshQuestion(qn6Ans, dropoffWkEnd, pickupWkEnd):
        selected = qn6Ans.selection_get()
        # print(selected)
        if "Saturday" in selected or "Sunday" in selected:
            dropoffWkEnd.configure(state='normal')
            pickupWkEnd.configure(state='normal')
        else:
            dropoffWkEnd.configure(state='disable')
            pickupWkEnd.configure(state='disable')

    def outputQuestionaire(controller, distRangeAns, 
                citizenStaAns, budgetAns, calAgeAns, 
                progAns, currAns,
                daysSentAns, dropoffReg, dropoffWkEnd, pickupReg, pickupWkEnd):
        userInput = []
        userInput.append(str(datetime.datetime.now()))
        userInput.extend(QuestionsPage.getMarkerPos())
        userInput.append(distRangeAns.get().strip("KM"))
        userInput.extend(QuestionsPage.getEduLvlWithCitizenship(citizenStaAns.get(), calAgeAns, budgetAns.get()))
        userInput.extend(QuestionsPage.getSelectedProgrammes(progAns.get()))
        userInput.extend(QuestionsPage.getSelectedCurriculum(currAns.get()))
        userInput.extend(QuestionsPage.getSelectedDayswithTiming(daysSentAns.get(), dropoffReg.get(), dropoffWkEnd.get(), pickupReg.get(), pickupWkEnd.get()))
        QuestionsPage.generateFile(userInput)

        import BusinessRuleEngine
        BusinessRuleEngine.BusinessRulesEngine().trigger_business_rule()

        controller.show_result_frame(Resultspage)

    def generateFile(userInput):
        WINDOWS.dataframe.drop(WINDOWS.dataframe.index,inplace=True)                                                              
        WINDOWS.dataframe.loc[len(WINDOWS.dataframe)] = userInput

        output_file = os.path.join(WINDOWS.USER_OUTPUT_DIR, WINDOWS.USER_OUTPUT_FILE)
        WINDOWS.dataframe.to_csv(path_or_buf=output_file, index=False)

    def getMarkerPos():
        if (len(WINDOWS.MARKER_LIST) <= 0):
            return ['1.290270, 103.851959']
        else:
            temp = str(WINDOWS.MARKER_LIST[0].position).strip("()")
            return [temp]

    def getEduLvlWithCitizenship(Status, calDate, budget):
        eduLvlwithStatus = ['0', '0', '0', '0', '0', '0', '0', '0', '1']
        date1 = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        date2 = datetime.datetime.strptime(str(calDate.get_date()), '%Y-%m-%d')
        r = relativedelta.relativedelta(date1, date2)
        months = r.months +  12 * r.years
        if r.days > 0:
            months += 1

        years = r.years

        if Status == "Singaporean":
            if years >= 5: # Kindergarten_Singaporean
                eduLvlwithStatus = ['0', '0', '0', budget, '0', '0', '0', '0', '4']
            elif years >= 3 and years <= 4: # Nursery_Singaporean
                eduLvlwithStatus = ['0', '0', budget, '0', '0', '0', '0', '0', '3']
            elif months >= 18 and months <= 24:
                eduLvlwithStatus = ['0', budget, '0', '0', '0', '0', '0', '0', '2']
            elif months >= 2 and months <= 17:
                eduLvlwithStatus = [budget, '0', '0', '0', '0', '0', '0', '0', '1']
        else:
            if years >= 5: # Kindergarten_Singaporean
                eduLvlwithStatus = ['0', '0', '0', '0', '0', '0', '0', budget, '4']
            elif years >= 3 and years <= 4: # Nursery_Singaporean
                eduLvlwithStatus = ['0', '0', '0', '0', '0', '0', budget, '0', '3']
            elif months >= 18 and months <= 24:
                eduLvlwithStatus = ['0', '0', '0', '0', '0', budget, '0', '0', '2']
            elif months >= 2 and months <= 17:
                eduLvlwithStatus = ['0', '0', '0', '0', budget, '0', '0', '0', '1']

        return eduLvlwithStatus
    
    def getSelectedProgrammes(programmes):
        programmesSelected = ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
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
    def __init__(self, master = None):
         
        tkinter.Toplevel.__init__(self)
        self.title("Map")
        self.geometry("1400x900")

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Set Marker",
                                                command=self.set_marker_event)
        self.button_1.grid(pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Clear Markers",
                                                command=self.clear_marker_event)
        self.button_2.grid(pady=(20, 0), padx=(20, 20), row=1, column=0)

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = tkintermapview.TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text="type address")
        self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        self.entry.bind("<Return>", self.search_event)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search_event)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values
        if len(WINDOWS.MARKER_LIST) >= 1:
            address = str(WINDOWS.MARKER_LIST[0].position).strip("()")
            WINDOWS.MARKER_LIST.clear()
            self.map_widget.set_address(address)
            WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(float(address.split(',')[0]), float(address.split(',')[1])))
        else:
            self.map_widget.set_address("Singapore")
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
            adr = tkintermapview.convert_coordinates_to_address(coords[0], coords[1])
            question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
            WINDOWS.MAP_LOCATION.set(question_location)

        self.map_widget.add_right_click_menu_command(
            label="Add Marker",  
            command=add_marker_event, 
            pass_coords=True
        )

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())
        current_position = self.map_widget.get_position()
        self.map_widget.delete_all_marker()
        WINDOWS.MARKER_LIST.clear()
        WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(current_position[0], current_position[1]))
        adr = tkintermapview.convert_coordinates_to_address(current_position[0], current_position[1])
        question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
        WINDOWS.MAP_LOCATION.set(question_location)

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        self.map_widget.delete_all_marker()
        WINDOWS.MARKER_LIST.clear()
        WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(current_position[0], current_position[1]))
        adr = tkintermapview.convert_coordinates_to_address(current_position[0], current_position[1])
        question_location = "Current address: " + adr.street + ", Singapore " + adr.postal
        WINDOWS.MAP_LOCATION.set(question_location)

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
    tab2_sch_name = None
    tab3_sch_name = None
    tab1_address = None
    tab2_address = None
    tab3_address = None
    tab1_weblink = None
    tab2_weblink = None
    tab3_weblink = None

    tab1_map = None
    tab2_map = None
    tab3_map = None

    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)

        # ResultPage textvariables
        Resultspage.tab1_sch_name = tkinter.StringVar()
        Resultspage.tab2_sch_name = tkinter.StringVar()
        Resultspage.tab3_sch_name = tkinter.StringVar()
        Resultspage.tab1_address = tkinter.StringVar()
        Resultspage.tab2_address = tkinter.StringVar()
        Resultspage.tab3_address = tkinter.StringVar()
        Resultspage.tab1_weblink = tkinter.StringVar()
        Resultspage.tab2_weblink = tkinter.StringVar()
        Resultspage.tab3_weblink = tkinter.StringVar()

        # Set default value for empty results
        Resultspage.tab1_sch_name.set("-")
        Resultspage.tab2_sch_name.set("-")
        Resultspage.tab3_sch_name.set("-")
        Resultspage.tab1_address.set("-")
        Resultspage.tab2_address.set("-")
        Resultspage.tab3_address.set("-")
        Resultspage.tab1_weblink.set("-")
        Resultspage.tab2_weblink.set("-")
        Resultspage.tab3_weblink.set("-")

        resultHeading = customtkinter.CTkLabel(
            self, 
            text="Find your child's ideal Preschool",
            font=WINDOWS.HEAD1_FONT)
        resultHeading.pack()

        resultHeading2 = customtkinter.CTkLabel(
            self, 
            text="The Top 3 School Brands with the closest match will be shown below.",
            font=WINDOWS.HEAD2_FONT)
        resultHeading2.pack()

        Resultspage.tab_view = customtkinter.CTkTabview(self)
        Resultspage.tab_view.pack(padx=20, pady=20)

        # Add result tabs
        Resultspage.tab_view.add("Preschool 1")

        # Create Frames in all tabs
        tab1_Frame = customtkinter.CTkFrame(Resultspage.tab_view.tab("Preschool 1"))
        tab1_Frame.pack()

        for i in range(2):
            for j in range(3):
                # Create Label.grids in all tabs
                
                if (i == 1 and j == 2):
                    Resultspage.tab1_button = customtkinter.CTkButton(
                        tab1_Frame, 
                        command=lambda: Resultspage.openlink())
                    Resultspage.tab1_button._text_label.configure(wraplength=300, justify='left')
                    Resultspage.tab1_button.configure(state='disabled')
                    Resultspage.tab1_button.grid(row=i, column=j, padx=15, pady=10)
                else:
                    tab1_labels = customtkinter.CTkLabel(tab1_Frame, wraplength=300, justify='center')
                    tab1_labels.grid(row=i, column=j, padx=15, pady=10)

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
            width=1100, height=500,
            corner_radius=0)
        Resultspage.tab1_map.pack()
        
        Resultspage.tab1_map.set_address("Singapore")
        Resultspage.tab1_map.set_zoom(13)

        # Buttons
        result_End_Frame = customtkinter.CTkFrame(self)
        result_End_Frame.pack()
        result_Quit_Frame = customtkinter.CTkFrame(self)
        result_Quit_Frame.pack()
        restart_window = customtkinter.CTkButton(
            result_End_Frame, 
            text="Restart Application", 
            command=lambda: controller.show_question_frame(QuestionsPage)
        )
        quit_button = customtkinter.CTkButton(
            result_Quit_Frame,
            text="Quit",
            command=lambda: controller.on_closing(),
        )
        restart_window.pack(pady=10)
        quit_button.pack(pady=10)

    def openlink():
        webbrowser.open_new_tab(Resultspage.tab1_weblink.get())

if __name__ == "__main__":
    app = WINDOWS()
    app.start()