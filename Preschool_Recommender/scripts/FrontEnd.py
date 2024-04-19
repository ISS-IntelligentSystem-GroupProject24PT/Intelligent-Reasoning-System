# Import the tkinter module
import os
import pandas
import tkinter
import tkinter.ttk
from typing import Tuple
import customtkinter

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

    # File Directory
    USER_OUTPUT_DIR = "..//resources//FrontEnd//FrontEnd_UserInputs"

    # Set up directory
    if not os.path.exists(USER_OUTPUT_DIR):
        os.makedirs(USER_OUTPUT_DIR)

    # Define DEFAULTS
    APP_NAME = "SG-Preschool Recommender"
    MIN_WIDTH = 1200
    MIN_HEIGHT = 800
    HEADING_FONT = None
    dataframe = pandas.DataFrame(columns=[
            'Latitude & Longitude', # Location
            'Distance Constraint', # Location Distance Constraint
            'Nursery_Singaporean', # Citizenship Status & Age
            'Playgroup_Singaporean', 
            'Kindergarten_Singaporean',
            'Nursery_PR',
            'Playgroup_PR', 
            'Kindergarten_PR', 
            'Budget', # Budget
            'Aesthetics & Creative Expression', # Programmes
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Redefine DEFAULTS
        WINDOWS.HEADING_FONT = tkinter.font.Font(family='Helvetica', size=30, weight='bold')
        # Define individual screen dimensions
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        if ((screenWidth*0.7 > WINDOWS.MIN_WIDTH) and (screenHeight*0.7 > WINDOWS.MIN_HEIGHT)):
            WINDOWS.MIN_WIDTH = screenWidth*0.7
            WINDOWS.MIN_HEIGHT = screenHeight*0.7

        # Find screen center point
        center_x = int(screenWidth/2 - WINDOWS.MIN_WIDTH / 2)
        center_y = int(screenHeight/2 - WINDOWS.MIN_HEIGHT / 2)

        # Main root window
        self.title(WINDOWS.APP_NAME)
        # self.geometry(f'{WINDOWS.MIN_WIDTH}x{WINDOWS.MIN_HEIGHT}+{center_x}+{center_y}')
        self.geometry(f'{WINDOWS.MIN_WIDTH}x{WINDOWS.MIN_HEIGHT}')

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

    def getHeadFont(self):
        return self.HEADING_FONT

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

class QuestionsPage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        # Set class defaults from DEFAULTS
        headFont = controller.getHeadFont()

        # Header Text
        qnsHeadText = "Find your child's ideal Preschool"
        qnsHeadText2 = "Answer the questionaire based on your preschool criterias."
        
        # Questionaire
        qnsQn1a = "Indicate your preferred Pre-school location."
        qnsQn1b = "Select a preferred distance range from the indicated location?"
        qnsQn2a = "What is your citizenship status?"
        qnsQn2b = "What is your available budget?"
        qnsQn2c = "How old is your child?"
        qnsQn3 = "Select the programmes you are interested to enroll your child in."
        qnsQn4 = "Select the Pre-school Curriculum style you prefer."
        qnsQn5 = "Select the days you would like to send your child to a Pre-school."
        qnsQn6a = "Select your preferred drop-off timings. (Monday to Friday)"
        qnsQn6b = "Select your preferred drop-off timings. (Saturday & Sunday)"
        qnsQn7a = "Select your preferred pick-up timings."
        qnsQn7b = "Select your preferred pick-up timings."
        qnsQn8 = "Overall rating of Pre-school"

        qns_Head1_Label = customtkinter.CTkLabel(
            self, 
            text=qnsHeadText
            )
        qns_Head2_Label = customtkinter.CTkLabel(
            self,
            text=qnsHeadText2
        )
        qns_Head1_Label.pack(padx=10, pady=10)
        qns_Head2_Label.pack()

        # Main Frame container
        mainFrameWidth = int(WINDOWS.MIN_WIDTH)
        mainFrameHeight = int(WINDOWS.MIN_HEIGHT)
        mainFrame = customtkinter.CTkFrame(
            self, 
            width=mainFrameWidth, height=mainFrameHeight)
        mainFrame.pack()

    # Question Frame containers
      # Question 1a: Location
        qns1Frame = customtkinter.CTkFrame(mainFrame)
        qns1Frame.pack()

        qns1Label = customtkinter.CTkLabel(qns1Frame, text=qnsQn1a)
        qns1Label2 = customtkinter.CTkLabel(qns1Frame, text="placeholder_address")
        qns1Button = customtkinter.CTkButton(qns1Frame,
                                    text="Open Maps View",
                                    command=lambda: MapWindow(controller))
        # qns1Button.bind("<Button>", 
        #          lambda e: MapWindow(controller))
        qns1Label.pack()
        qns1Label2.pack()
        qns1Button.pack()

      # Question 1b: Distance range
        qn1bChoices1 = ('1KM', '5KM', '10KM', '15KM')

        qn1bFrame = customtkinter.CTkFrame(mainFrame)
        qn1bFrame.pack()
        qn1bLabel  = customtkinter.CTkLabel(qn1bFrame, text=qnsQn1b)
        qn1bLabel.pack()
        distRangeAns = customtkinter.CTkComboBox(qn1bFrame, values=qn1bChoices1)
        distRangeAns.pack()

      # Question 2a: Citizenship
        qn2aChoices = ('Singaporean', 'Permanent Resident')
        qn2aFrame = customtkinter.CTkFrame(mainFrame)
        qn2aFrame.pack()

        qn2aLabel = customtkinter.CTkLabel(qn2aFrame, text=qnsQn2a)
        citizenStaAns = customtkinter.CTkComboBox(qn2aFrame, values=qn2aChoices) 

        qn2aLabel.pack()
        citizenStaAns.pack()

      # Question 2b: Budget
        qns2bFrame = customtkinter.CTkFrame(mainFrame)
        qns2bFrame.pack()

        qns2bLabel = customtkinter.CTkLabel(qns2bFrame, text=qnsQn2b)
        qns2bAnsLabel = customtkinter.CTkLabel(qns2bFrame, text="$")
        budgetAns = customtkinter.CTkEntry(qns2bFrame, height = 1, width = 100, placeholder_text="0")
        # TODO: add numbers constraint

        qns2bLabel.pack()
        qns2bAnsLabel.pack(side="left")
        budgetAns.pack(side="right")

      # Question 2c: Child Age
        curDatetime = datetime.datetime.now() # get current datetime
        qns2cFrame = customtkinter.CTkFrame(mainFrame)
        qns2cFrame.pack()

        qn2cLabel = customtkinter.CTkLabel(qns2cFrame, text=qnsQn2c)
        calAgeAns = DateEntry(qns2cFrame, width=12, 
                        year=curDatetime.year, month=curDatetime.month, day=curDatetime.day, 
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
        qn3Frame = customtkinter.CTkFrame(mainFrame)
        qn3Frame.pack()

        qn3Label = customtkinter.CTkLabel(qn3Frame, text=qnsQn3)
        progAns = checklistcombobox.ChecklistCombobox(qn3Frame, values=qn3Choices)

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
        qn4Frame = customtkinter.CTkFrame(mainFrame)
        qn4Frame.pack()

        qn4Label = customtkinter.CTkLabel(qn4Frame, text=qnsQn4)
        currAns = checklistcombobox.ChecklistCombobox(qn4Frame, values=qn4Choices)

        qn4Label.pack()
        currAns.pack()

      # Question 5: Days to send child (Mon to Sun)
        qn5Choices = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        qn5Frame = customtkinter.CTkFrame(mainFrame)
        qn5Frame.pack()

        qn5Label = customtkinter.CTkLabel(qn5Frame, text=qnsQn5)
        daysSentAns = checklistcombobox.ChecklistCombobox(qn5Frame, values=qn5Choices)
        daysSentAns.bind("<<ComboboxSelected>>", lambda e: QuestionsPage.refreshQuestion(daysSentAns, pickupWkEnd, dropoffWkEnd))

        qn5Label.pack()
        daysSentAns.pack()

      # Question 6 & 7: Pick Up and Drop off timing
        qn6Choices1 = ('7AM', '8AM', '9AM', '10AM', '11AM', '12PM')
        qn6Choices2 = ('7AM', '8AM', '9AM', '10AM')

        qn6FrameText = customtkinter.CTkFrame(mainFrame)
        qn6FrameText.pack()
        qn6LabelA  = customtkinter.CTkLabel(qn6FrameText, text=qnsQn6a)
        qn6LabelB  = customtkinter.CTkLabel(qn6FrameText, text=qnsQn6b)
        qn6LabelA.pack(side='left')
        qn6LabelB.pack(side='right')

        qn6FrameCombobox = customtkinter.CTkFrame(mainFrame)
        qn6FrameCombobox.pack()
        dropoffReg = customtkinter.CTkComboBox(qn6FrameCombobox, values=qn6Choices1)
        dropoffWkEnd = customtkinter.CTkComboBox(qn6FrameCombobox, values=qn6Choices2)
        dropoffReg.pack(side='left')
        dropoffWkEnd.pack_forget()

        qn7Choices1 = ('3PM', '4PM', '5PM', '6PM', '7PM')
        qn7Choices2 = ('12PM', '1PM', '2PM')

        qn7FrameText = customtkinter.CTkFrame(mainFrame)
        qn7FrameText.pack()
        qn7LabelA  = customtkinter.CTkLabel(qn7FrameText, text=qnsQn7a)
        qn7LabelB  = customtkinter.CTkLabel(qn7FrameText, text=qnsQn7b)
        qn7LabelA.pack(side='left')
        qn7LabelB.pack(side='right')

        qn7FrameCombobox = customtkinter.CTkFrame(mainFrame)
        qn7FrameCombobox.pack()
        pickupReg = customtkinter.CTkComboBox(qn7FrameCombobox, values=qn7Choices1)
        pickupWkEnd = customtkinter.CTkComboBox(qn7FrameCombobox, values=qn7Choices2)
        pickupReg.pack(side='left')
        pickupWkEnd.pack_forget()

        # Buttons
        qns_End_Frame = customtkinter.CTkFrame(self)
        qns_End_Frame.pack()
        switch_window = customtkinter.CTkButton(
            qns_End_Frame,
            text="Generate Results",
            command=lambda: QuestionsPage.outputQuestionaire(
                controller, distRangeAns, 
                citizenStaAns, budgetAns, calAgeAns, 
                progAns, currAns,
                daysSentAns, dropoffReg, dropoffWkEnd, pickupReg, pickupWkEnd
                )
        )
        quit_button = customtkinter.CTkButton(
            qns_End_Frame,
            text="Quit",
            command=lambda: controller.on_closing(),
        )
        switch_window.pack()
        quit_button.pack()

    def refreshQuestion(qn6Ans, qn7ComboB, qn8ComboB):
        selected = qn6Ans.selection_get()
        # print(selected)
        if "Saturday" in selected or "Sunday" in selected:
            qn7ComboB.pack(side='right')
            qn8ComboB.pack(side='right')
        else:
            qn7ComboB.pack_forget()
            qn8ComboB.pack_forget()

    def outputQuestionaire(controller, distRangeAns, 
                citizenStaAns, budgetAns, calAgeAns, 
                progAns, currAns,
                daysSentAns, dropoffReg, dropoffWkEnd, pickupReg, pickupWkEnd):
        userInput = []
        # userInput.append(MapWindow.get_position(MapWindow))
        userInput.extend(QuestionsPage.getMarkerPos())
        userInput.append(distRangeAns.get().strip("KM"))
        userInput.extend(QuestionsPage.getEduLvlWithCitizenship(citizenStaAns.get(), calAgeAns))
        userInput.append(budgetAns.get())
        userInput.extend(QuestionsPage.getSelectedProgrammes(progAns.get()))
        userInput.extend(QuestionsPage.getSelectedCurriculum(currAns.get()))
        userInput.extend(QuestionsPage.getSelectedDayswithTiming(daysSentAns.get(), dropoffReg.get(), dropoffWkEnd.get(), pickupReg.get(), pickupWkEnd.get()))
        # print(userInput)
        QuestionsPage.generateFile(userInput)

        controller.show_frame(Resultspage)

    def generateFile(userInput):
        # WINDOWS.dataframe = pandas.DataFrame(userInput)
        WINDOWS.dataframe.loc[len(WINDOWS.dataframe)] = userInput

        # print(len(userInput))
        # print(WINDOWS.dataframe)
        output_file = os.path.join(WINDOWS.USER_OUTPUT_DIR, WINDOWS.USER_OUTPUT_FILE)
        WINDOWS.dataframe.to_csv(path_or_buf=output_file, index=False)

    def getMarkerPos():
        if (len(WINDOWS.MARKER_LIST) <= 0):
            return ['1.290270, 103.851959']
        else:
            return [str(WINDOWS.MARKER_LIST[0].position)]

    def getEduLvlWithCitizenship(Status, calDate):
        eduLvlwithStatus = ['0', '0', '0', '0', '0', '0']
        # print(datetime.datetime.now().date())
        # print(calDate.get_date())
        date1 = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d')
        date2 = datetime.datetime.strptime(str(calDate.get_date()), '%Y-%m-%d')
        r = relativedelta.relativedelta(date1, date2)
        months = r.months +  12 * r.years
        if r.days > 0:
            months += 1
        # print(months)

        if Status == "Singaporean":
            if months <= 36:
                eduLvlwithStatus = ['1', '0', '0', '0', '0', '0']
            elif months > 36 and months <= 60:
                eduLvlwithStatus = ['0', '1', '0', '0', '0', '0']
            else:
                eduLvlwithStatus = ['0', '0', '1', '0', '0', '0']
        else:
            if months <= 36:
                eduLvlwithStatus = ['0', '0', '0', '1', '0', '0']
            elif months > 36 and months <= 60:
                eduLvlwithStatus = ['0', '0', '0', '0', '1', '0']
            else:
                eduLvlwithStatus = ['0', '0', '0', '0', '0', '1']

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
        daysSelectedwithTiming = ['100', '100', '100', '100', '100', '100', '100', '100', '100', '100', '100', '100', '100', '100']

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
        # print(daysSelectedwithTiming)
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

class Resultspage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        headingFont = tkinter.font.Font(family='Helvetica', size=15, weight='bold')

        qns_Head1_Label = customtkinter.CTkLabel(
            self, 
            text="This is the results page!",
            )
        qns_Head1_Label.pack()

        # Buttons
        result_End_Frame = customtkinter.CTkFrame(self)
        result_End_Frame.pack()
        result_Quit_Frame = customtkinter.CTkFrame(self)
        result_Quit_Frame.pack()
        restart_window = customtkinter.CTkButton(
            result_End_Frame, 
            text="Restart Application", 
            command=lambda: controller.show_frame(QuestionsPage)
        )
        quit_button = customtkinter.CTkButton(
            result_Quit_Frame,
            text="Quit",
            command=lambda: controller.on_closing(),
        )
        restart_window.pack(side="left")
        quit_button.pack()

class MapWindow(tkinter.Toplevel):

    MARKER_LIST = []

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

        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        # self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
        #                                                                command=self.change_map)
        # self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

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
        self.map_widget.set_address("Singapore")
        self.map_widget.set_zoom(12)
        # self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")

        # Define right click events before using event commands
        def add_marker_event(coords):
            # print("Add marker:", coords)
            coordsText = str(coords[0]) + "," + str(coords[1])
            if len(WINDOWS.MARKER_LIST) >= 1:
                for marker in WINDOWS.MARKER_LIST:
                    marker.delete()
            WINDOWS.MARKER_LIST.clear()
            WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(
                coords[0], coords[1], 
                text=coordsText
            ))

        self.map_widget.add_right_click_menu_command(
            label="Add Marker",  
            command=add_marker_event, 
            pass_coords=True
        )

    def search_event(self, event=None):
        self.map_widget.set_address(self.entry.get())
        current_position = self.map_widget.get_position()
        if len(WINDOWS.MARKER_LIST) >= 1:
            for marker in WINDOWS.MARKER_LIST:
                marker.delete()
            WINDOWS.MARKER_LIST.clear()
        WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(current_position[0], current_position[1]))

    def set_marker_event(self):
        current_position = self.map_widget.get_position()
        if len(WINDOWS.MARKER_LIST) >= 1:
            for marker in WINDOWS.MARKER_LIST:
                marker.delete()
            WINDOWS.MARKER_LIST.clear()
        WINDOWS.MARKER_LIST.append(self.map_widget.set_marker(current_position[0], current_position[1]))
        # print(WINDOWS.MARKER_LIST[0].position)

    def clear_marker_event(self):
        for marker in WINDOWS.MARKER_LIST:
            marker.delete()
        WINDOWS.MARKER_LIST.clear()

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # def change_map(self, new_map: str):
    #     if new_map == "OpenStreetMap":
    #         self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = WINDOWS()
    app.start()
