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

# Used for styling the GUI
import tkinter.font

class WINDOWS(customtkinter.CTk):
    # Define DEFAULTS
    APP_NAME = "SG-Preschool Recommender"
    MIN_WIDTH = 1200
    MIN_HEIGHT = 600
    HEADING_FONT = None
    dataframe = pandas.DataFrame(columns=[
        'Latitude',
        'Longitude',
        'user_distance_constraint',
        'Age(Months)',
        'English',
        'Chinese', 
        'Other Languages and Literacy', 
        'Mathematics', 
        'Science', 
        'Music', 
        'Sports', 
        'Digital Skills', 
        'Problem-Solving Skills', 
        'Project Work', 
        'Motor Skill Development', 
        'Social and Emotional Development', 
        'Morals Education',
        'Bilingual Curriculum Model', 
        'Reggio Emilia approach', 
        'English Curriculum', 
        'Early Years Foundation Stage curriculum', 
        'Montessori', 
        'SPARK certified Curriculum',
        'user_monday_drop_off',
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
        qnsQn1b = "Select a preferred travelling time."
        qnsQn2 = "What is your available budget?"
        qnsQn3 = "How old is your child?"
        qnsQn4 = "Select the programmes you are interested to enroll your child in."
        qnsQn5 = "Select the Pre-school Curriculum style you prefer."
        qnsQn6 = "Select the days you would like to send your child to a Pre-school."
        qnsQn7a = "Select your preferred drop-off timings. (Monday to Friday)"
        qnsQn7b = "Select your preferred drop-off timings. (Saturday & Sunday)"
        qnsQn8a = "Select your preferred pick-up timings."
        qnsQn8b = "Select your preferred pick-up timings."
        qnsQn9 = "Overall rating of Pre-school"

        qns_Head1_Label = tkinter.ttk.Label(
            self, 
            text=qnsHeadText,
            font=headFont
            )
        qns_Head2_Label = tkinter.ttk.Label(
            self,
            text=qnsHeadText2,
            font=headFont
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

        qns1Label = tkinter.ttk.Label(qns1Frame, text=qnsQn1a)
        qns1Label2 = tkinter.ttk.Label(qns1Frame, text="placeholder_address")
        qns1Button = customtkinter.CTkButton(qns1Frame,
                                    text="Open Maps View")
        qns1Button.bind("<Button>", 
                 lambda e: MapWindow(controller))
        qns1Label.pack()
        qns1Label2.pack()
        qns1Button.pack()

      # Question 1b: Travelling time
        qn1bChoices1 = ('5 Min', '10 Min', '15 Min')

        qn1bFrame = customtkinter.CTkFrame(mainFrame)
        qn1bFrame.pack()
        qn1bLabel  = tkinter.ttk.Label(qn1bFrame, text=qnsQn1b)
        qn1bLabel.pack()
        qn1bCombo = customtkinter.CTkComboBox(qn1bFrame, values=qn1bChoices1)
        qn1bCombo.pack()

      # Question 2: Budget
        qns2Frame = customtkinter.CTkFrame(mainFrame)
        qns2Frame.pack()

        qns2Label = tkinter.ttk.Label(qns2Frame, text=qnsQn2)
        qns2AnsLabel = tkinter.ttk.Label(qns2Frame, text="$")
        qns2Ans = tkinter.Text(qns2Frame, height = 1, width = 16)
        # TODO: add numbers constraint

        qns2Label.pack()
        qns2AnsLabel.pack(side="left")
        qns2Ans.pack(side="right")

      # Question 3: Child Age
        curDatetime = datetime.datetime.now() # get current datetime
        qns3Frame = customtkinter.CTkFrame(mainFrame)
        qns3Frame.pack()

        qn3Label = tkinter.ttk.Label(qns3Frame, text=qnsQn3)
        # TODO: add tkcalendar to question4Frame
        # Open Calendar default to current datetime
        # cal = Calendar(qns3Frame, selectmode = 'day',
        #        year = curDatetime.year, month = curDatetime.month,
        #        day = curDatetime.day)
        qn3Cal = DateEntry(qns3Frame, width=12, 
                        year=curDatetime.year, month=curDatetime.month, day=curDatetime.day, 
                        background='darkblue', 
                        foreground='white', 
                        orderwidth=2)
        qn3Label.pack()
        qn3Cal.pack(padx=10, pady=10)

      # Question 4: School Programmes
        qn4Choices = ('English', 'Chinese', 'Other Languages and Literacy', 
                      'Mathematics', 'Science', 'Music', 'Sports', 
                      'Digital Skills', 'Problem-Solving Skills', 'Project Work',
                      'Motor Skill Development', 'Social and Emotional Development', 'Morals Education')
        qn4Frame = customtkinter.CTkFrame(mainFrame)
        qn4Frame.pack()

        qn4Label = tkinter.ttk.Label(qn4Frame, text=qnsQn4)
        qn4Ans = checklistcombobox.ChecklistCombobox(qn4Frame, values=qn4Choices)

        qn4Label.pack()
        qn4Ans.pack()

      # Question 5: Curriculum
        qn5Choices = ('Bilingual Curriculum Model', 'Reggio Emilia approach', 'English Curriculum', 'Early Years Foundation Stage curriculum', 'Montessori', 'SPARK certified Curriculum')
        qn5Frame = customtkinter.CTkFrame(mainFrame)
        qn5Frame.pack()

        qn5Label = tkinter.ttk.Label(qn5Frame, text=qnsQn5)
        qn5Ans = checklistcombobox.ChecklistCombobox(qn5Frame, values=qn5Choices)

        qn5Label.pack()
        qn5Ans.pack()

      # Question 6: Days to send child (Mon to Sun)
        qn6Choices = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        qn6Frame = customtkinter.CTkFrame(mainFrame)
        qn6Frame.pack()

        qn6Label = tkinter.ttk.Label(qn6Frame, text=qnsQn6)
        qn6Ans = checklistcombobox.ChecklistCombobox(qn6Frame, values=qn6Choices)
        qn6Ans.bind("<<ComboboxSelected>>", lambda e: QuestionsPage.refreshQuestion(qn6Ans, qn7ComboB, qn8ComboB))

        qn6Label.pack()
        qn6Ans.pack()

      # Question 7 & 8: Pick Up and Drop off timing
        qn7Choices1 = ('7AM', '8AM', '9AM', '10AM', '11AM', '12PM')
        qn7Choices2 = ('7AM', '8AM', '9AM', '10AM')

        qn7FrameText = customtkinter.CTkFrame(mainFrame)
        qn7FrameText.pack()
        qn7LabelA  = tkinter.ttk.Label(qn7FrameText, text=qnsQn7a)
        qn7LabelB  = tkinter.ttk.Label(qn7FrameText, text=qnsQn7b)
        qn7LabelA.pack(side='left')
        qn7LabelB.pack(side='right')

        qn7FrameCombobox = customtkinter.CTkFrame(mainFrame)
        qn7FrameCombobox.pack()
        qn7ComboA = customtkinter.CTkComboBox(qn7FrameCombobox, values=qn7Choices1)
        qn7ComboB = customtkinter.CTkComboBox(qn7FrameCombobox, values=qn7Choices2)
        qn7ComboA.pack(side='left')
        qn7ComboB.pack_forget()

        qn8Choices1 = ('3PM', '4PM', '5PM', '6PM', '7PM')
        qn8Choices2 = ('12PM', '1PM', '2PM')

        qn8FrameText = customtkinter.CTkFrame(mainFrame)
        qn8FrameText.pack()
        qn8LabelA  = tkinter.ttk.Label(qn8FrameText, text=qnsQn8a)
        qn8LabelB  = tkinter.ttk.Label(qn8FrameText, text=qnsQn8b)
        qn8LabelA.pack(side='left')
        qn8LabelB.pack(side='right')

        qn8FrameCombobox = customtkinter.CTkFrame(mainFrame)
        qn8FrameCombobox.pack()
        qn8ComboA = customtkinter.CTkComboBox(qn8FrameCombobox, values=qn8Choices1)
        qn8ComboB = customtkinter.CTkComboBox(qn8FrameCombobox, values=qn8Choices2)
        qn8ComboA.pack(side='left')
        qn8ComboB.pack_forget()

        # Buttons
        qns_End_Frame = customtkinter.CTkFrame(self)
        qns_End_Frame.pack()
        switch_window = customtkinter.CTkButton(
            qns_End_Frame,
            text="Generate Results",
            command=lambda: QuestionsPage.outputQuestionaire(
                controller, qn1bCombo, qns2Ans, qn3Cal, qn4Ans, qn5Ans, qn6Ans, qn7ComboA, qn7ComboB, qn8ComboA, qn8ComboB),
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

    def outputQuestionaire(controller, qn1bCombo, qns2Ans, qn3Cal, qn4Ans, qn5Ans, qn6Ans, qn7ComboA, qn7ComboB, qn8ComboA, qn8ComboB):
        userInput = []
        userInput.append(qn1bCombo.get())
        userInput.append(qns2Ans.get("1.0", 'end'))
        userInput.append(qn3Cal.get_date())
        userInput.append(qn4Ans.get())
        userInput.append(qn5Ans.get())
        userInput.append(qn6Ans.get())
        userInput.append(qn7ComboA.get())
        userInput.append(qn7ComboB.get())
        userInput.append(qn8ComboA.get())
        userInput.append(qn8ComboB.get())
        print(userInput)
        # print(qns2Ans.get("1.0", 'end'))
        # print(qn3Cal.get_date())
        # print(qn4Ans.get())
        # print(qn5Ans.get())
        # print(qn6Ans.get())
        # print(qn7ComboA.get())
        # print(qn7ComboB.get())
        # print(qn8ComboA.get())
        # print(qn8ComboB.get())

        controller.show_frame(Resultspage)

class Resultspage(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        headingFont = tkinter.font.Font(family='Helvetica', size=15, weight='bold')

        qns_Head1_Label = tkinter.ttk.Label(
            self, 
            text="This is the results page!",
            font=headingFont
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

    def __init__(self, master = None):
         
        tkinter.Toplevel.__init__(self)
        self.title("Map")
        self.geometry("800x600")
        # create map widget
        map_widget = tkintermapview.TkinterMapView(self, width=800, height=600, corner_radius=0)
        map_widget.place(relx=0.5, rely=0.5, anchor="center")

        # set default widget position and zoom level
        map_widget.set_position(1.290270, 103.851959)  # Singapore
        map_widget.set_zoom(14)
        # # set current widget position by address
        # map_widget.set_address("colosseo, rome, italy")

        # set current widget position by address
        marker_1 = map_widget.set_position(1.290270, 103.851959, marker=True)

        print(marker_1.position, marker_1.text)  # get position and text

        marker_1.set_text("Singapore")  # set new text
        # marker_1.set_position(48.860381, 2.338594)  # change position
        # marker_1.delete()

        # Define right click events before using event commands
        def add_marker_event(coords):
            print("Add marker:", coords)
            new_marker = map_widget.set_marker(
                coords[0], coords[1], 
                text="new marker"
            )

        map_widget.add_right_click_menu_command(
            label="Add Marker",  
            command=add_marker_event, 
            pass_coords=True
        )

        def left_click_event(coordinates_tuple):
            print("Left click event with coordinates:", coordinates_tuple)

        map_widget.add_left_click_map_command(left_click_event)


if __name__ == "__main__":
    app = WINDOWS()
    app.start()
