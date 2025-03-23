import time

import flet as ft


class IntroText(ft.Text):
    def __init__(self, value='Study Buddy', weight=ft.FontWeight.BOLD,
                 theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM, duration=500, wait=0.5):
        super().__init__()
        self.wait = wait
        self.animate_opacity = ft.Animation(duration=duration, curve=ft.AnimationCurve.EASE_IN)
        self.animate_offset = ft.Animation(duration=duration, curve=ft.AnimationCurve.EASE_IN_OUT)
        self.opacity = 0
        self.value = value
        self.offset = ft.Offset(0, 0.25)
        self.weight = weight
        self.theme_style = theme_style

    def did_mount(self):
        time.sleep(self.wait)
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

    def did_mount(self):
        time.sleep(0.6)
        self.opacity = 1
        self.update()


class Step(ft.Container):
    def __init__(self, value=False, text='Step text'):
        super().__init__()
        self.bgcolor =  ft.Colors.ON_PRIMARY if value else ft.Colors.ON_PRIMARY_CONTAINER
        self.padding = 15
        self.border_radius = 30
        self.alignment = ft.alignment.center
        self.content = ft.Text(value=text, theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                               color=ft.Colors.WHITE if value else ft.Colors.ON_PRIMARY
                               )



def main(page: ft.Page):
    page.title = 'Study Buddy'
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.DEEP_PURPLE)
    page.padding = 0

    left_screen = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=IntroText(), alignment=ft.alignment.center),
                ft.Container(content=IntroText(
                    value="Study Buddy - an AI-powered study assistant.",
                    weight=ft.FontWeight.W_300,
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,

                    wait=0.55
                ),
                    alignment=ft.alignment.center),
                ft.Container(content=StepsColumn(
                    controls=[
                        Step(value=True, text="Enter your academic factors."),
                        Step(text="Receive performance predictions."),
                        Step(text="Get feedback and advises.")
                    ],
                    spacing=25
                ),
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

    right_screen = ft.Container(expand=20)

    # screenManager = ft.AnimatedSwitcher(
    #     intro_screen,
    #     transition=ft.AnimatedSwitcherTransition.FADE,
    #     duration=500,
    #     reverse_duration=500,
    #     switch_in_curve=ft.AnimationCurve.EASE_IN,
    #     switch_out_curve=ft.AnimationCurve.EASE_OUT
    # )

    main_screen = ft.Container(
        content=ft.Row(
            controls=[left_screen, right_screen]
        ),
        padding=0,
        margin=0,
        image=ft.DecorationImage(src='images/bg_main.png', fit=ft.ImageFit.FILL),
        expand=1
    )

    page.add(
        main_screen
    )


ft.app(main)
