from concurrent.futures import ThreadPoolExecutor
from view import views_handler
from dotenv import load_dotenv
from unipa import check_id
import flet as ft
import os

load_dotenv()

UNIPA_URL = os.environ["UNIPA_URL"]
UNIPA_ID = os.environ["UNIPA_ID"]   
UNIPA_PWD = os.environ["UNIPA_PWD"]

def main(page: ft.Page):

    def route_change(route):
        assignments = []
        print(page.route)
        page.views.clear()
        page.views.append(
            views_handler(page,assignments=assignments)[page.route]
        )
    
    page.title = "ReUNIPA"
    page.scroll = "ADAPTIVE"
    page.window_width = 896
    page.window_height = 504
    #View handling
    page.on_route_change = route_change
    #On initial state    
    page.go("/home")


    if check_id(id=UNIPA_ID,pwd=UNIPA_PWD,url=UNIPA_URL) == "ERROR":
        page.go("/login")
    else:
        page.go("/")
        page.snack_bar = ft.SnackBar(content=ft.Text("Login Successful"),duration=2000)
        page.snack_bar.open = True
        page.update()

ft.app(target=main)