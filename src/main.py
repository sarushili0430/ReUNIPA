from concurrent.futures import ThreadPoolExecutor
from view import views_handler
from dotenv import load_dotenv
from unipa import check_id
from unipa import UNIPA_Login
import flet as ft
import os

load_dotenv()

UNIPA_URL = os.environ["UNIPA_URL"]
UNIPA_ID = os.environ["UNIPA_ID"]   
UNIPA_PWD = os.environ["UNIPA_PWD"]

def main(page: ft.Page):

    def route_change(route):
        global UNIPA_ID, UNIPA_PWD
        UNIPA_ID = os.environ["UNIPA_ID"]   
        UNIPA_PWD = os.environ["UNIPA_PWD"]
        assignments = []
        print(page.route)
        if page.route == "/":
            with UNIPA_Login(ID=UNIPA_ID,PWD=UNIPA_PWD) as client:
                assignments = client.get_assignment()
        page.views.clear()
        page.views.append(
            views_handler(page,assignments=assignments)[page.route]
        )
    
    page.title = "ReUNIPA"
    page.scroll = "ADAPTIVE"
    page.window_width = 896
    page.window_height = 504
    page.window_visible = True
    #View handling
    page.on_route_change = route_change
    #On initial state    
    page.go("/home")

    #Login process handling
    if UNIPA_ID == "" or UNIPA_PWD=="" or UNIPA_URL == "":
        page.go("/login")
    elif check_id(id=UNIPA_ID,pwd=UNIPA_PWD,url=UNIPA_URL) == "ERROR":
        page.go("/login")
        page.snack_bar = ft.SnackBar(content=ft.Text("Login Failed"),duration=2000,bgcolor="#F94C10")
        page.snack_bar.open = True
        page.update()
    else:
        page.go("/")
        page.snack_bar = ft.SnackBar(content=ft.Text("Login Successful"),duration=2000,bgcolor="#03C988")
        page.snack_bar.open = True
        page.update()

ft.app(target=main, view=ft.AppView.FLET_APP_HIDDEN)