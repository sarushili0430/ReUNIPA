import flet as ft
from view import views_handler
from dotenv import load_dotenv
from unipa import UNIPA_Login
import os

load_dotenv()

UNIPA_URL = os.environ["UNIPA_URL"]
UNIPA_ID = os.environ["UNIPA_ID"]   
UNIPA_PWD = os.environ["UNIPA_PWD"]

def main(page: ft.Page):

    def route_change(route):
        assignments = []
        print(page.route)
        if page.route == "/":
            assignments = UNIPA_Login(UNIPA_ID,UNIPA_PWD)
            assignments = assignments.get_assignment()
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
    if UNIPA_URL == "" or UNIPA_ID == "" or UNIPA_PWD == "":
        page.go("/login")
    else:
        page.go("/")

ft.app(target=main)