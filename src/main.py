from time import sleep
import flet as ft
import pickle
import warnings
from g4f.client import Client

warnings.filterwarnings('ignore')
client = Client()

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


class IntroText(ft.Text):
    def __init__(self, value='Study Buddy', weight=ft.FontWeight.BOLD,
                 theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM, duration=500, wait=0.5):
        super().__init__()
        self.wait = wait
        self.animate_opacity = ft.Animation(duration=duration, curve=ft.AnimationCurve.EASE_IN)
        self.animate_offset = ft.Animation(duration=duration, curve=ft.AnimationCurve.EASE_OUT)
        self.opacity = 0
        self.value = value
        self.offset = ft.Offset(0, 0.25)
        self.weight = weight
        self.theme_style = theme_style

    def did_mount(self):
        sleep(self.wait)
        self.opacity = 1
        self.offset = ft.Offset(0, 0)
        self.update()


class StepsColumn(ft.Column):
    def __init__(self, controls=None, spacing=None):
        super().__init__()
        self.controls = controls
        self.spacing = spacing
        self.animate_opacity = ft.Animation(duration=400, curve=ft.AnimationCurve.EASE_IN)
        self.opacity = 0

    def next(self):
        for i in range(len(self.controls) - 1):
            if self.controls[i].value:
                self.controls[i].value = False
                self.controls[i].bgcolor = ft.Colors.ON_PRIMARY_CONTAINER
                self.controls[i].content.color = ft.Colors.ON_PRIMARY
                self.controls[i].update()

                self.controls[i + 1].value = True
                self.controls[i + 1].bgcolor = ft.Colors.ON_PRIMARY
                self.controls[i + 1].content.color = ft.Colors.WHITE
                self.controls[i + 1].update()

                break

    def did_mount(self):
        sleep(0.2)
        self.opacity = 1
        self.update()


class Step(ft.Container):
    def __init__(self, value=False, text='Step text'):
        super().__init__()
        self.bgcolor = ft.Colors.ON_PRIMARY if value else ft.Colors.ON_PRIMARY_CONTAINER
        self.padding = 15
        self.value = value
        self.border_radius = 30
        self.alignment = ft.alignment.center
        self.content = ft.Text(value=text, theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                               color=ft.Colors.WHITE if value else ft.Colors.ON_PRIMARY
                               )


class Subject(ft.Container):
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

        self.bgcolor = ft.Colors.SURFACE
        self.index = index
        self.attendance_rate = ft.TextField(
            border=ft.InputBorder.UNDERLINE,
            input_filter=ft.NumbersOnlyInputFilter(),
            on_change=self.attendance_changed,
            data='Attendance_Rate',
            width=32,
            hint_text='%',
        )

        self.slider = ft.Slider(max=100, divisions=20, expand=1, label='{value}%', on_change=self.slider_changed)
        self.remove_btn = []
        if deletable: self.remove_btn.append(ft.FilledTonalButton(
            text='Remove subject', icon=ft.Icons.REMOVE_OUTLINED, bgcolor=ft.Colors.ERROR,
            icon_color=ft.Colors.ERROR_CONTAINER, color=ft.Colors.ERROR_CONTAINER,
            on_click=on_remove, data=self.index
        ))
        self.subject_name = ft.TextField(label=f'Subject {self.index + 1}', border=ft.InputBorder.UNDERLINE,
                                         expand=1, on_change=self.on_change, data='Subject_Name',
                                         autofocus=bool(self.index)
                                         )
        self.hours_studied = ft.TextField(label='Hours studied a day',
                                          border=ft.InputBorder.UNDERLINE,
                                          filled=True,
                                          input_filter=ft.NumbersOnlyInputFilter(), on_change=self.on_change,
                                          data='Hours_Studied'
                                          )
        self.previous_score = ft.TextField(label='Previous score',
                                           border=ft.InputBorder.UNDERLINE,
                                           filled=True,
                                           input_filter=ft.NumbersOnlyInputFilter(), on_change=self.on_change,
                                           data='Previous_Scores'
                                           )

        self.content = ft.Column(
            controls=[
                ft.Row(controls=[
                                    self.subject_name
                                ] + self.remove_btn),
                self.hours_studied,
                self.previous_score,
                ft.Row(controls=[
                    ft.Text('Attendance rate',
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM),

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


def main(page: ft.Page):
    page.title = 'Study Buddy'
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_PURPLE)
    page.padding = 0
    page.window.min_width, page.window.min_height = 1280, 720
    page.window.center()

    global global_features
    models = {}

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

    def load_models():
        models["reg"] = pickle.load(open('assets/models/student_performance_reg.pkl', 'rb'))
        models["clf"] = pickle.load(open('assets/models/student_stress_clf.pkl', 'rb'))

    page.run_thread(load_models)

    steps = StepsColumn(
        controls=[
            Step(value=True, text="Enter your academic factors"),
            Step(text="Receive performance predictions"),
            Step(text="Get feedback and advises")
        ],
        spacing=25
    )

    left_screen = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=IntroText(), alignment=ft.alignment.center),
                ft.Container(content=IntroText(
                    value="Study Buddy - an AI-powered study assistant.",
                    weight=ft.FontWeight.W_300,
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,

                    wait=0.15
                ),
                    alignment=ft.alignment.center),
                ft.Container(content=steps,
                             alignment=ft.alignment.center,
                             padding=25
                             )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        margin=ft.Margin(0, 100, 0, 0),
        expand=21
    )

    general_questions = ft.Column(controls=[
        ft.Text('General questions:', weight=ft.FontWeight.BOLD,
                theme_style=ft.TextThemeStyle.TITLE_LARGE),

        ft.Row(controls=[
            ft.TextField(label='Hours of sleep', filled=True, expand=1, suffix_text='per day',
                         input_filter=ft.NumbersOnlyInputFilter(), on_change=change_feature_global,
                         data=['Sleep_Hours', int], border=ft.InputBorder.UNDERLINE),
            ft.TextField(label='Extracurricular hours', filled=True, expand=1, suffix_text='per day',
                         input_filter=ft.NumbersOnlyInputFilter(), on_change=change_feature_global,
                         data='extr', border=ft.InputBorder.UNDERLINE),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

        ft.Row(controls=[
            ft.TextField(label='Physical activities hours', filled=True, expand=1, suffix_text='per day',
                         input_filter=ft.NumbersOnlyInputFilter(), on_change=change_feature_global,
                         data=['Physical_Activity', int], border=ft.InputBorder.UNDERLINE),
            ft.TextField(label='Social hours', filled=True, expand=1, suffix_text='per day',
                         input_filter=ft.NumbersOnlyInputFilter(), on_change=change_feature_global,
                         data=['Social_Hours_Per_Day', int], border=ft.InputBorder.UNDERLINE)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

        ft.Row(controls=[
            ft.Dropdown(label='Gender', width=250, filled=True,
                        on_change=change_feature_global, data=['Gender_Male', lambda g: 1 if g == 'Male' else 0],
                        options=[
                            ft.DropdownOption(key='Male'),
                            ft.DropdownOption(key='Female')
                        ]),
            ft.Dropdown(label='Distance from home', width=250, filled=True,
                        on_change=change_feature_global, data='dist',
                        options=[
                            ft.DropdownOption(key='Near'),
                            ft.DropdownOption(key='Moderate'),
                            ft.DropdownOption(key='Far')
                        ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

        ft.Row(controls=[
            ft.Dropdown(label='Parental Involvement', width=250, filled=True,
                        on_change=change_feature_global, data='pinv',
                        options=[
                            ft.DropdownOption(key='Low'),
                            ft.DropdownOption(key='Medium'),
                            ft.DropdownOption(key='High')
                        ]),
            ft.Dropdown(label='Family income', width=250, filled=True,
                        on_change=change_feature_global, data='finc',
                        options=[
                            ft.DropdownOption(key='Low'),
                            ft.DropdownOption(key='Medium'),
                            ft.DropdownOption(key='High')
                        ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, expand=1)

    subjects_col = ft.Column(controls=[
        Subject(deletable=False, check=check_subjects)
    ], spacing=20, scroll=ft.ScrollMode.ALWAYS, expand=1)

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

            reg_dt.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(pred)) for pred in [subject["Subject_Name"],
                                                            subject['Result'],
                                                            category(subject["Result"])]
                ]
            ))

        global_features['clf']['Study_Hours_Per_Day'] //= len(features)
        global_features["clf"]['GPA'] = round(global_features["clf"]['GPA'] / len(features) / 25.00, 2)

        reg_column.content.controls = [
            ft.Text(value='Final exam performance predictions:', theme_style=ft.TextThemeStyle.TITLE_LARGE,
                    weight=ft.FontWeight.BOLD
                    ),
            reg_dt,
            ft.Text(value=f'Your GPA score: {global_features['clf']['GPA']}',
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                    weight=ft.FontWeight.BOLD)
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

        clf_column.content = ft.Container(content=ft.Column(controls=[
            ft.Column(controls=[
                ft.Text(value='Your predicted stress level is:', theme_style=ft.TextThemeStyle.TITLE_LARGE,
                        weight=ft.FontWeight.BOLD
                        ),
                ft.Container(
                    image=ft.DecorationImage(src=f'images/{global_features['clf']['Stress_Level'].lower()}.png',
                                             fit=ft.ImageFit.FILL),
                    width=154, height=79
                ),

                ft.Text(value=global_features['clf']['Stress_Level'], theme_style=ft.TextThemeStyle.TITLE_LARGE,
                        weight=ft.FontWeight.BOLD
                        )

            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
                spacing=25, expand=1
            ),

            ft.Row(alignment=ft.MainAxisAlignment.END, controls=[
                ft.FilledButton(text='Continue', icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                                on_click=feedback_event
                                )
            ])

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER,
            spacing=25, expand=1
        ), alignment=ft.alignment.center, expand=1)

        clf_column.update()

    def feedback_event(e):
        steps.next()
        screenManager.content = feedback_screen
        for subject in features:
            feedback_tabs.tabs.append(ft.Tab(text=subject['Subject_Name'], content=ft.Container(
                padding=20,
                content=ft.Column(controls=[
                    ft.Text(value='Generating feedback...',
                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                    ft.ProgressRing()
                ], scroll=ft.ScrollMode.AUTO, spacing=25)
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
        feedback_tabs.tabs[index].content = ft.Container(content=ft.Column(controls=[
            ft.Markdown(value=response.choices[0].message.content)
        ], scroll=ft.ScrollMode.AUTO), padding=15)
        feedback_tabs.update()


    def feedback():
        for i, subject in enumerate(features):
            page.run_thread(gpt, i, f'''You're a part of a program called "Study Buddy", which is a simple AI assistant for tracking student performance. It predicts exam score for each subject user provides, as well as predicting overall stress level. You're given a subject's name, a predicted exam score and stress level.
        Give some tactics and ideas of how to improve user's result and to reduce stress level.
        SUBJECT: {subject['Subject_Name']}
        SCORE: {subject['Result']}
        STRESS_LEVEL: {global_features['clf']['Stress_Level']}
        ''')



    reg_dt = ft.DataTable(columns=[
        ft.DataColumn(ft.Text("Subject")),
        ft.DataColumn(ft.Text("Result"), numeric=True),
        ft.DataColumn(ft.Text('Category'))
    ], sort_column_index=1
    )

    reg_column = ft.Container(alignment=ft.alignment.center, expand=1,
                              content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text(value='Loading regression report...',
                                                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                                                    ft.ProgressRing()
                                                ]))

    clf_column = ft.Container(alignment=ft.alignment.center, expand=1,
                              content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text(value='Loading classification report...',
                                                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                                                    ft.ProgressRing()
                                                ]))

    reports_screen = ft.Column(controls=[
        reg_column,
        ft.Divider(),
        clf_column
    ])

    feedback_tabs = ft.Tabs(animation_duration=400, tabs=[])

    feedback_screen = ft.Container(content=feedback_tabs, alignment=ft.alignment.center, expand=1, padding=25)

    def continue_event(e):
        steps.next()
        screenManager.content = reports_screen
        page.update()

        page.run_thread(predictions)

    continue_btn = ft.FilledButton(text='Continue', disabled=True, icon=ft.Icons.ARROW_FORWARD_ROUNDED,
                                   on_click=continue_event,
                                   tooltip=ft.Tooltip(message='Fill all blanks before continuing...',
                                                      enable_tap_to_dismiss=False,
                                                      )
                                   )

    subjects = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.START, expand=1,
                         spacing=20,
                         controls=[
                             subjects_col,
                             ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[ft.FilledButton(text='Add new',
                                                              icon=ft.Icons.ADD_OUTLINED,
                                                              on_click=new_subject
                                                              ),
                                              continue_btn
                                              ])
                         ])

    intro_screen = ft.Column(controls=[
        general_questions,
        ft.Column(expand=1, controls=[
            ft.Container(alignment=ft.alignment.center,
                         content=ft.Text('Subjects:', weight=ft.FontWeight.BOLD,
                                         theme_style=ft.TextThemeStyle.TITLE_LARGE)),

            subjects,

        ]),
    ],
        alignment=ft.MainAxisAlignment.START,
    )

    screenManager = ft.AnimatedSwitcher(
        intro_screen,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=500,
        reverse_duration=500,
        switch_in_curve=ft.AnimationCurve.EASE_IN,
        switch_out_curve=ft.AnimationCurve.EASE_OUT
    )

    right_screen = ft.Container(
        expand=20, padding=25, animate_opacity=ft.Animation(duration=400, curve=ft.AnimationCurve.EASE_IN),
        opacity=0,
        content=screenManager
    )

    main_screen = ft.Container(
        content=ft.Row(
            controls=[left_screen, right_screen]
        ),
        padding=0,
        margin=0,
        image=ft.DecorationImage(src='images/bg_main.png', fit=ft.ImageFit.FILL),
        expand=1
    )

    def open_git(e):
        page.launch_url('https://github.com/ruslol228/IT_project_1')
        page.update()

    page.add(
        ft.Stack(controls=[main_screen,
                           ft.Chip(label=ft.Text('Github'),
                                   leading=ft.Icon(name='link'),
                                   on_click=open_git,
                                   left=32, bottom=32)
                           ], expand=1)
    )

    sleep(0.1)
    right_screen.opacity = 1
    page.update()


ft.app(main, assets_dir='assets/')
