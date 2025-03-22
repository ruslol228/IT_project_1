import time

import flet as ft



class IntroText(ft.Text):
    def __init__(self, value='Study Buddy', weight=ft.FontWeight.BOLD,
                 theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM, duration=500, wait=0.5):
        super().__init__()
        self.wait = wait
        self.animate_opacity = ft.Animation(duration=duration, curve=ft.AnimationCurve.EASE_IN)
        self.opacity = 0
        self.value = value
        self.weight = weight
        self.theme_style = theme_style

    def did_mount(self):
        time.sleep(self.wait)
        self.opacity = 1
        self.update()



class IntroButton(ft.FilledButton):
    def __init__(self, text='Get Started', icon="ARROW_FORWARD", on_click=None):
        super().__init__()
        self.on_click = on_click
        self.text = text
        self.icon = icon
        self.animate_opacity = ft.Animation(duration=500, curve=ft.AnimationCurve.EASE_IN)
        self.opacity = 0

    def did_mount(self):
        time.sleep(0.6)
        self.opacity = 1
        self.update()



def main(page: ft.Page):
    page.title = 'Study Buddy'
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.padding = 0


    def change_screen(e):
        screenManager.content = app_screen
        page.update()

    app_screen = ft.Container(bgcolor=ft.Colors.WHITE)

    intro_screen = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=IntroText(), alignment=ft.alignment.center),
                ft.Container(content=IntroText(
                    value="Study Buddy - an AI-powered study assistant.",
                    weight=ft.FontWeight.W_200,
                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                    wait=0.55
                ),
                    alignment=ft.alignment.center),
                ft.Container(content=IntroButton(on_click=change_screen),
                             alignment=ft.alignment.center
                             )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )


    screenManager = ft.AnimatedSwitcher(
        intro_screen,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=500,
        reverse_duration=500,
        switch_in_curve=ft.AnimationCurve.EASE_IN,
        switch_out_curve=ft.AnimationCurve.EASE_OUT
    )

    main_screen = ft.Container(
            content=screenManager,
            alignment=ft.alignment.center,
            expand=1,
            padding=0,
            margin=0,
            image=ft.DecorationImage(src='images/bg_main.jpg', fit=ft.ImageFit.FILL)
        )

    page.add(
        main_screen
    )


ft.app(main)
