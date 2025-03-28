from time import sleep
from flet import (Text, Animation, Column, Row, TextField, TextThemeStyle, FontWeight,
                  AnimationCurve, AnimatedSwitcher, AnimatedSwitcherTransition, Offset, MainAxisAlignment,
                  CrossAxisAlignment,
                  Dropdown, DropdownOption, DecorationImage, Colors, Container, alignment, InputBorder,
                  NumbersOnlyInputFilter,
                  Slider, FilledButton, FilledTonalButton, Icons, Theme, Page, Margin, ScrollMode,
                  DataColumn, DataRow, DataCell, DataTable, ImageFit, ProgressRing, Tabs, Tab, Markdown,
                  Divider, Stack, Chip, Tooltip, Icon, app)
import pickle
from g4f.client import Client

client = Client()

models = {
    "reg": pickle.load(open('student_performance_reg.pkl', 'rb')),
    "clf": pickle.load(open('student_stress_clf.pkl', 'rb'))
}

global_features = {
    'reg': {
        "Sleep_Hours": None,
        "Physical_Activity": None,
        "Parental_Involvement_Low": None,
        "Parental_Involvement_Medium": None,
        "Access_to_Resources_Low": 0,
        "Access_to_Resources_Medium": 1,
        "Extracurricular_Activities_Yes": None,
        "Internet_Access_Yes": 1,
        "Family_Income_Low": None,
        "Family_Income_Medium": None,
        'Teacher_Quality_Low': 0,
        'Teacher_Quality_Medium': 1,
        "School_Type_Public": 1,
        "Peer_Influence_Neutral": 0,
        "Peer_Influence_Positive": 1,
        "Learning_Disabilities_Yes": 0,
        "Parental_Education_Level_High_School": 1,
        "Parental_Education_Level_Postgraduate": 0,
        "Distance_from_Home_Moderate": None,
        "Distance_from_Home_Near": None,
        "Gender_Male": None,
    },
    'clf': {
        # "Study_Hours_Per_Day": None,
        "Extracurricular_Hours": None,
        "Sleep_Hours": None,
        "Social_Hours_Per_Day": None,
        "Physical_Activity": None,
        # "GPA": None,
    }
}

features = []


class IntroText(Text):
    def __init__(self, value='Study Buddy', weight=FontWeight.BOLD,
                 theme_style=TextThemeStyle.DISPLAY_MEDIUM, duration=500, wait=0.5):
        super().__init__()
        self.wait = wait
        self.animate_opacity = Animation(duration=duration, curve=AnimationCurve.EASE_IN)
        self.animate_offset = Animation(duration=duration, curve=AnimationCurve.EASE_OUT)
        self.opacity = 0
        self.value = value
        self.offset = Offset(0, 0.25)
        self.weight = weight
        self.theme_style = theme_style

    def did_mount(self):
        sleep(self.wait)
        self.opacity = 1
        self.offset = Offset(0, 0)
        self.update()


class StepsColumn(Column):
    def __init__(self, controls=None, spacing=None):
        super().__init__()
        self.controls = controls
        self.spacing = spacing
        self.animate_opacity = Animation(duration=400, curve=AnimationCurve.EASE_IN)
        self.opacity = 0

    def next(self):
        for i in range(len(self.controls) - 1):
            if self.controls[i].value:
                self.controls[i].value = False
                self.controls[i].bgcolor = Colors.ON_PRIMARY_CONTAINER
                self.controls[i].content.color = Colors.ON_PRIMARY
                self.controls[i].update()

                self.controls[i + 1].value = True
                self.controls[i + 1].bgcolor = Colors.ON_PRIMARY
                self.controls[i + 1].content.color = Colors.WHITE
                self.controls[i + 1].update()

                break

    def did_mount(self):
        sleep(0.2)
        self.opacity = 1
        self.update()


class Step(Container):
    def __init__(self, value=False, text='Step text'):
        super().__init__()
        self.bgcolor = Colors.ON_PRIMARY if value else Colors.ON_PRIMARY_CONTAINER
        self.padding = 15
        self.value = value
        self.border_radius = 30
        self.alignment = alignment.center
        self.content = Text(value=text, theme_style=TextThemeStyle.TITLE_MEDIUM,
                            color=Colors.WHITE if value else Colors.ON_PRIMARY
                            )


class Subject(Container):
    def __init__(self, deletable=True, index=0, on_remove=None, check=None):
        super().__init__()
        self.check = check
        features.append({
            'Subject_Name': None,
            'Hours_Studied': None,
            'Tutoring_Sessions': 2,
            'Attendance_Rate': None,
            'Previous_Scores': None,
            'Motivation_Level_Low': 0,
            'Motivation_Level_Medium': 1
        })

        self.bgcolor = Colors.SURFACE
        self.index = index
        self.attendance_rate = TextField(
            border=InputBorder.UNDERLINE,
            input_filter=NumbersOnlyInputFilter(),
            on_change=self.attendance_changed,
            data='Attendance_Rate',
            width=32,
            hint_text='%',
        )

        self.slider = Slider(max=100, divisions=20, expand=1, label='{value}%', on_change=self.slider_changed)
        self.remove_btn = []
        if deletable: self.remove_btn.append(FilledTonalButton(
            text='Remove subject', icon=Icons.REMOVE_OUTLINED, bgcolor=Colors.ERROR,
            icon_color=Colors.ERROR_CONTAINER, color=Colors.ERROR_CONTAINER,
            on_click=on_remove, data=self.index
        ))
        self.subject_name = TextField(label=f'Subject {self.index + 1}', border=InputBorder.UNDERLINE,
                                      expand=1, on_change=self.on_change, data='Subject_Name',
                                      autofocus=bool(self.index)
                                      )
        self.hours_studied = TextField(label='Hours studied a day',
                                       border=InputBorder.UNDERLINE,
                                       filled=True,
                                       input_filter=NumbersOnlyInputFilter(), on_change=self.on_change,
                                       data='Hours_Studied'
                                       )
        self.previous_score = TextField(label='Previous score',
                                        border=InputBorder.UNDERLINE,
                                        filled=True,
                                        input_filter=NumbersOnlyInputFilter(), on_change=self.on_change,
                                        data='Previous_Scores'
                                        )

        self.content = Column(
            controls=[
                Row(controls=[
                                 self.subject_name
                             ] + self.remove_btn),
                self.hours_studied,
                self.previous_score,
                Row(controls=[
                    Text('Attendance rate',
                         theme_style=TextThemeStyle.TITLE_MEDIUM),

                    self.attendance_rate
                ]),

                self.slider
            ]
        )

        self.border_radius = 25
        self.padding = 25

    def on_change(self, e):
        if e.control.data == 'Subject_Name':
            features[self.index]['Subject_Name'] = e.control.value if e.control.value else None
        else:
            if e.control.data == 'Hours_Studied':
                features[self.index][e.control.data] = int(e.control.value) * 7 if e.control.value else None
            else:
                features[self.index][e.control.data] = int(e.control.value) if e.control.value else None
        self.check()

    def __repr__(self):
        return f'Subject(index={self.index})'

    def slider_changed(self, e):
        self.attendance_rate.value = str(round(e.control.value))
        features[self.index]["Attendance_Rate"] = round(e.control.value)
        self.check()
        self.update()

    def attendance_changed(self, e):
        self.slider.value = min(100, int(e.control.value)) if e.control.value else 0
        self.on_change(e)
        self.update()


def main(page: Page):
    page.title = 'Study Buddy'
    page.theme = Theme(color_scheme_seed=Colors.DEEP_PURPLE)
    page.padding = 0
    page.window.min_width, page.window.min_height = 1280, 720
    page.window.center()

    global global_features

    def global_ready():
        for model in global_features:
            if None in global_features[model].values():
                return False
        return True

    def subjects_ready():
        for subject in subjects_col.controls:
            if None in features[subject.index].values():
                return False
        return True

    def check_subjects():
        if global_ready() and subjects_ready():
            continue_btn.disabled = False
            continue_btn.tooltip = None
            continue_btn.update()
        else:
            continue_btn.disabled = True
            continue_btn.update()

    def change_feature_global(e):

        if e.control.data == 'extr':
            if not e.control.value:
                global_features['reg']['Extracurricular_Activities_Yes'] = None
                global_features['clf']['Extracurricular_Hours'] = None
            else:
                global_features['reg']['Extracurricular_Activities_Yes'] = 1 if int(e.control.value) > 1 else 0
                global_features['clf']['Extracurricular_Hours'] = int(e.control.value) if e.control.value else None
        elif e.control.data == 'dist':
            if not e.control.value:
                global_features['reg']['Distance_from_Home_Near'] = None
                global_features['reg']['Distance_from_Home_Moderate'] = None
            else:
                global_features['reg']['Distance_from_Home_Near'] = 1 if e.control.value == 'Near' else 0
                global_features['reg']['Distance_from_Home_Moderate'] = 1 if e.control.value == 'Moderate' else 0
        elif e.control.data == 'pinv':
            if not e.control.value:
                global_features['reg']['Parental_Involvement_Low'] = None
                global_features['reg']['Parental_Involvement_Medium'] = None
            else:
                global_features['reg']['Parental_Involvement_Low'] = 1 if e.control.value == 'Low' else 0
                global_features['reg']['Parental_Involvement_Medium'] = 1 if e.control.value == 'Medium' else 0
        elif e.control.data == 'finc':
            if not e.control.value:
                global_features['reg']['Family_Income_Low'] = None
                global_features['reg']['Family_Income_Medium'] = None
            else:
                global_features['reg']['Family_Income_Low'] = 1 if e.control.value == 'Low' else 0
                global_features['reg']['Family_Income_Medium'] = 1 if e.control.value == 'Medium' else 0
        else:
            for model in global_features:
                if e.control.data[0] in global_features[model]:
                    if not e.control.value:
                        global_features[model][e.control.data[0]] = None
                    else:
                        global_features[model][e.control.data[0]] = e.control.data[1](e.control.value)

        if global_ready() and subjects_ready():
            continue_btn.disabled = False
            continue_btn.tooltip = None
            continue_btn.update()
        else:
            continue_btn.disabled = True
            continue_btn.update()

    steps = StepsColumn(
        controls=[
            Step(value=True, text="Enter your academic factors"),
            Step(text="Receive performance predictions"),
            Step(text="Get feedback and advises")
        ],
        spacing=25
    )

    left_screen = Container(
        content=Column(
            controls=[
                Container(content=IntroText(), alignment=alignment.center),
                Container(content=IntroText(
                    value="Study Buddy - an AI-powered study assistant.",
                    weight=FontWeight.W_300,
                    theme_style=TextThemeStyle.TITLE_LARGE,

                    wait=0.15
                ),
                    alignment=alignment.center),
                Container(content=steps,
                          alignment=alignment.center,
                          padding=25
                          )
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=20
        ),
        margin=Margin(0, 100, 0, 0),
        expand=21
    )

    general_questions = Column(controls=[
        Text('General questions:', weight=FontWeight.BOLD,
             theme_style=TextThemeStyle.TITLE_LARGE),

        Row(controls=[
            TextField(label='Hours of sleep', filled=True, expand=1, suffix_text='per day',
                      input_filter=NumbersOnlyInputFilter(), on_change=change_feature_global,
                      data=['Sleep_Hours', int], border=InputBorder.UNDERLINE),
            TextField(label='Extracurricular hours', filled=True, expand=1, suffix_text='per day',
                      input_filter=NumbersOnlyInputFilter(), on_change=change_feature_global,
                      data='extr', border=InputBorder.UNDERLINE),
        ], alignment=MainAxisAlignment.SPACE_BETWEEN),

        Row(controls=[
            TextField(label='Physical activities hours', filled=True, expand=1, suffix_text='per day',
                      input_filter=NumbersOnlyInputFilter(), on_change=change_feature_global,
                      data=['Physical_Activity', int], border=InputBorder.UNDERLINE),
            TextField(label='Social hours', filled=True, expand=1, suffix_text='per day',
                      input_filter=NumbersOnlyInputFilter(), on_change=change_feature_global,
                      data=['Social_Hours_Per_Day', int], border=InputBorder.UNDERLINE)
        ], alignment=MainAxisAlignment.SPACE_BETWEEN),

        Row(controls=[
            Dropdown(label='Gender', width=250, filled=True,
                     on_change=change_feature_global, data=['Gender_Male', lambda g: 1 if g == 'Male' else 0],
                     options=[
                         DropdownOption(key='Male'),
                         DropdownOption(key='Female')
                     ]),
            Dropdown(label='Distance from home', width=250, filled=True,
                     on_change=change_feature_global, data='dist',
                     options=[
                         DropdownOption(key='Near'),
                         DropdownOption(key='Moderate'),
                         DropdownOption(key='Far')
                     ])
        ], alignment=MainAxisAlignment.SPACE_BETWEEN),

        Row(controls=[
            Dropdown(label='Parental Involvement', width=250, filled=True,
                     on_change=change_feature_global, data='pinv',
                     options=[
                         DropdownOption(key='Low'),
                         DropdownOption(key='Medium'),
                         DropdownOption(key='High')
                     ]),
            Dropdown(label='Family income', width=250, filled=True,
                     on_change=change_feature_global, data='finc',
                     options=[
                         DropdownOption(key='Low'),
                         DropdownOption(key='Medium'),
                         DropdownOption(key='High')
                     ])
        ], alignment=MainAxisAlignment.SPACE_BETWEEN),

    ], horizontal_alignment=CrossAxisAlignment.CENTER, spacing=15, expand=1)

    subjects_col = Column(controls=[
        Subject(deletable=False, check=check_subjects)
    ], spacing=20, scroll=ScrollMode.ALWAYS, expand=1)

    def new_subject(e):
        subjects_col.controls.append(Subject(index=len(subjects_col.controls), on_remove=remove_subject,
                                             check=check_subjects
                                             ))
        check_subjects()
        subjects_col.update()

    def category(num: int) -> str:
        if num > 90: return "A"
        if num > 80: return "B"
        if num > 70: return "C"
        if num > 60: return "D"
        if num > 50:
            return "E"
        else:
            return "F"

    def remove_subject(e):
        index = e.control.data
        subjects_col.controls.pop(index)
        features.pop(index)
        for i in range(index, len(subjects_col.controls)):
            subject = subjects_col.controls[i]
            subject.index -= 1
            subject.subject_name.label = f'Subject {i + 1}'
            subject.remove_btn[0].data = i
            subjects_col.controls[i].update()
        check_subjects()
        subjects_col.update()

    def predictions():
        global_features['clf']['GPA'] = 0
        global_features['clf']['Study_Hours_Per_Day'] = 0

        # Regression
        for subject in features:
            subject["Result"] = round(models['reg'].predict(
                [[
                    subject['Hours_Studied'],
                    subject['Attendance_Rate'],
                    global_features['reg']['Sleep_Hours'],
                    subject['Previous_Scores'],
                    subject['Tutoring_Sessions'],
                    global_features['reg']['Physical_Activity'],
                    global_features['reg']['Parental_Involvement_Low'],
                    global_features['reg']['Parental_Involvement_Medium'],
                    global_features['reg']['Access_to_Resources_Low'],
                    global_features['reg']['Access_to_Resources_Medium'],
                    global_features['reg']['Extracurricular_Activities_Yes'],
                    subject['Motivation_Level_Low'],
                    subject['Motivation_Level_Medium'],
                    global_features['reg']['Internet_Access_Yes'],
                    global_features['reg']['Family_Income_Low'],
                    global_features['reg']['Family_Income_Medium'],
                    global_features['reg']['Teacher_Quality_Low'],
                    global_features['reg']['Teacher_Quality_Medium'],
                    global_features['reg']['School_Type_Public'],
                    global_features['reg']['Peer_Influence_Neutral'],
                    global_features['reg']['Peer_Influence_Positive'],
                    global_features['reg']['Learning_Disabilities_Yes'],
                    global_features['reg']['Parental_Education_Level_High_School'],
                    global_features['reg']['Parental_Education_Level_Postgraduate'],
                    global_features['reg']['Distance_from_Home_Moderate'],
                    global_features['reg']['Distance_from_Home_Near'],
                    global_features['reg']['Gender_Male'],
                ]]
            )[0], 2)

            global_features['clf']['Study_Hours_Per_Day'] += subject['Hours_Studied']
            global_features["clf"]['GPA'] += subject['Result']

            reg_dt.rows.append(DataRow(
                cells=[
                    DataCell(Text(pred)) for pred in [subject["Subject_Name"],
                                                      subject['Result'],
                                                      category(subject["Result"])]
                ]
            ))

        global_features['clf']['Study_Hours_Per_Day'] //= len(features)
        global_features["clf"]['GPA'] = round(global_features["clf"]['GPA'] / len(features) / 25.00, 2)

        reg_column.content.controls = [
            Text(value='Final exam performance predictions:', theme_style=TextThemeStyle.TITLE_LARGE,
                 weight=FontWeight.BOLD
                 ),
            reg_dt,
            Text(value=f'Your GPA score: {global_features['clf']['GPA']}',
                 theme_style=TextThemeStyle.TITLE_LARGE,
                 weight=FontWeight.BOLD)
        ]

        reg_column.update()

        global_features['clf']['Stress_Level'] = ['High', 'Low', 'Moderate'][models['clf'].predict([[
            global_features['clf']['Study_Hours_Per_Day'],
            global_features['clf']['Extracurricular_Hours'],
            global_features['clf']['Sleep_Hours'],
            global_features['clf']['Social_Hours_Per_Day'],
            global_features['clf']['Physical_Activity'],
            global_features['clf']['GPA']
        ]])[0]]

        clf_column.content = Container(content=Column(controls=[
            Column(controls=[
                Text(value='Your predicted stress level is:', theme_style=TextThemeStyle.TITLE_LARGE,
                     weight=FontWeight.BOLD
                     ),
                Container(
                    image=DecorationImage(src=f'images/{global_features['clf']['Stress_Level'].lower()}.png',
                                          fit=ImageFit.FILL),
                    width=154, height=79
                ),

                Text(value=global_features['clf']['Stress_Level'], theme_style=TextThemeStyle.TITLE_LARGE,
                     weight=FontWeight.BOLD
                     )

            ], horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER,
                spacing=25, expand=1
            ),

            Row(alignment=MainAxisAlignment.END, controls=[
                FilledButton(text='Continue', icon=Icons.ARROW_FORWARD_ROUNDED,
                             on_click=feedback_event
                             )
            ])

        ], horizontal_alignment=CrossAxisAlignment.CENTER, alignment=MainAxisAlignment.CENTER,
            spacing=25, expand=1
        ), alignment=alignment.center, expand=1)

        clf_column.update()

    def feedback_event(e):
        steps.next()
        screenManager.content = feedback_screen
        for subject in features:
            feedback_tabs.tabs.append(Tab(text=subject['Subject_Name'], content=Container(
                padding=20,
                content=Column(controls=[
                    Text(value='Generating feedback...',
                         theme_style=TextThemeStyle.TITLE_MEDIUM),
                    ProgressRing()
                ], scroll=ScrollMode.AUTO, spacing=25)
            )))

        page.update()

        page.run_thread(feedback)

    def gpt(index, prompt):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            web_search=False
        )
        feedback_tabs.tabs[index].content = Container(content=Column(controls=[
            Markdown(value=response.choices[0].message.content)
        ], scroll=ScrollMode.AUTO), padding=15)
        feedback_tabs.update()

    def feedback():
        for i, subject in enumerate(features):
            page.run_thread(gpt, i, f'''You're a part of a program called "Study Buddy", which is a simple AI assistant for tracking student performance. It predicts exam score for each subject user provides, as well as predicting overall stress level. You're given a subject's name, a predicted exam score and stress level.
        Give some tactics and ideas of how to improve user's result and to reduce stress level.
        SUBJECT: {subject['Subject_Name']}
        SCORE: {subject['Result']}
        STRESS_LEVEL: {global_features['clf']['Stress_Level']}
        ''')

    reg_dt = DataTable(columns=[
        DataColumn(Text("Subject")),
        DataColumn(Text("Result"), numeric=True),
        DataColumn(Text('Category'))
    ], sort_column_index=1
    )

    reg_column = Container(alignment=alignment.center, expand=1,
                           content=Column(horizontal_alignment=CrossAxisAlignment.CENTER,
                                          alignment=MainAxisAlignment.CENTER,
                                          controls=[
                                              Text(value='Loading regression report...',
                                                   theme_style=TextThemeStyle.TITLE_MEDIUM),
                                              ProgressRing()
                                          ]))

    clf_column = Container(alignment=alignment.center, expand=1,
                           content=Column(horizontal_alignment=CrossAxisAlignment.CENTER,
                                          alignment=MainAxisAlignment.CENTER,
                                          controls=[
                                              Text(value='Loading classification report...',
                                                   theme_style=TextThemeStyle.TITLE_MEDIUM),
                                              ProgressRing()
                                          ]))

    reports_screen = Column(controls=[
        reg_column,
        Divider(),
        clf_column
    ])

    feedback_tabs = Tabs(animation_duration=400, tabs=[])

    feedback_screen = Container(content=feedback_tabs, alignment=alignment.center, expand=1, padding=25)

    def continue_event(e):
        steps.next()
        screenManager.content = reports_screen
        page.update()

        page.run_thread(predictions)

    continue_btn = FilledButton(text='Continue', disabled=True, icon=Icons.ARROW_FORWARD_ROUNDED,
                                on_click=continue_event,
                                tooltip=Tooltip(message='Fill all blanks before continuing...',
                                                enable_tap_to_dismiss=False,
                                                )
                                )

    subjects = Column(horizontal_alignment=CrossAxisAlignment.START, expand=1,
                      spacing=20,
                      controls=[
                          subjects_col,
                          Row(alignment=MainAxisAlignment.SPACE_BETWEEN,
                              controls=[FilledButton(text='Add new',
                                                     icon=Icons.ADD_OUTLINED,
                                                     on_click=new_subject
                                                     ),
                                        continue_btn
                                        ])
                      ])

    intro_screen = Column(controls=[
        general_questions,
        Column(expand=1, controls=[
            Container(alignment=alignment.center,
                      content=Text('Subjects:', weight=FontWeight.BOLD,
                                   theme_style=TextThemeStyle.TITLE_LARGE)),

            subjects,

        ]),
    ],
        alignment=MainAxisAlignment.START,
    )

    screenManager = AnimatedSwitcher(
        intro_screen,
        transition=AnimatedSwitcherTransition.FADE,
        duration=500,
        reverse_duration=500,
        switch_in_curve=AnimationCurve.EASE_IN,
        switch_out_curve=AnimationCurve.EASE_OUT
    )

    right_screen = Container(
        expand=20, padding=25, animate_opacity=Animation(duration=400, curve=AnimationCurve.EASE_IN),
        opacity=0,
        content=screenManager
    )

    main_screen = Container(
        content=Row(
            controls=[left_screen, right_screen]
        ),
        padding=0,
        margin=0,
        image=DecorationImage(src='images/bg_main.png', fit=ImageFit.FILL),
        expand=1
    )

    def open_git(e):
        page.launch_url('https://github.com/ruslol228/IT_project_1')
        page.update()

    page.add(
        Stack(controls=[main_screen,
                        Chip(label=Text('Github'),
                             leading=Icon(name='link'),
                             on_click=open_git,
                             left=32, bottom=32)
                        ], expand=1)
    )

    sleep(0.1)
    right_screen.opacity = 1
    page.update()


app(main, assets_dir='assets/')
