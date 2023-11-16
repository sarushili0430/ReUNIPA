import flet as ft

class StartView(ft.UserControl):

    def __init__(self,page:ft.Page):
        super().__init__()
        self.page = page
        self.logo = ft.Text(
            value="ReUnipa",
            text_align=ft.TextAlign.CENTER,
            size=100,
            width=670,
            height=120,
        )
        self.prog_ring = ft.ProgressRing(
            height=75,
            width=75,
        )
        self.start_screen = ft.Container(
                    ft.Column(
                        [
                            self.logo,
                            self.prog_ring,
                        ],
                        spacing=30,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    width=700,
                    height=300,
                    margin=90,
                )
    
    def build(self):
        return self.start_screen
