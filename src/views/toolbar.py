import flet as ft


class AppToolbar:
    def __init__(self):
        self.toolbar = ft.Container(
            ft.Row(
                [
                    ft.NavigationRail(
                        selected_index=0,
                        label_type=ft.NavigationRailLabelType.ALL,
                        group_alignment=-1.0,
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.icons.HOME_OUTLINED,
                                selected_icon=ft.icons.HOME,
                                label="Home",
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.SETTINGS_OUTLINED,
                                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                                label_content=ft.Text("Settings"),
                            ),
                        ],
                        on_change=lambda e: print(
                            "Selected destination:", e.control.selected_index
                        ),
                    ),
                ]
            ),
            width=90,
            height=504,
            padding=ft.padding.only(12, 0, 0, 0),
            alignment=ft.alignment.center,
        )
