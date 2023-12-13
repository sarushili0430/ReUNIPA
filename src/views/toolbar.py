import flet as ft


class AppToolbar:
    def __init__(self, app):
        self.app = app
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
                                icon=ft.icons.CHECK_BOX_OUTLINED,
                                selected_icon=ft.icons.CHECK_BOX,
                                label="Attendance",
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.CALENDAR_MONTH_OUTLINED,
                                selected_icon=ft.icons.CALENDAR_MONTH,
                                label="Schedule",
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.SETTINGS_OUTLINED,
                                selected_icon=ft.icons.SETTINGS,
                                label="Settings",
                            ),
                        ],
                        on_change=lambda e: self.app.change_container_view(
                            target=views_routing(e.control.selected_index)
                        ),
                    ),
                ]
            ),
            width=90,
            height=504,
            padding=ft.padding.only(12, 0, 0, 0),
            alignment=ft.alignment.center,
        )


def views_routing(index: int):
    print(index)
    if index == 0:
        return "home"
    elif index == 1:
        return "attendance"
    elif index == 2:
        return "schedule"
    elif index == 3:
        return "settings"
