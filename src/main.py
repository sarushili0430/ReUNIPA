#import login
from unipa import UNIPA_Login
from unipa import UNIPA_Submit
from dotenv import load_dotenv
import flet as ft
import app

import os

load_dotenv()

UNIPA_ID = os.environ["UNIPA_ID"]   
UNIPA_PWD = os.environ["UNIPA_PWD"]
TEAMS_ID = os.environ["TEAMS_ID"]
TEAMS_PWD = os.environ["TEAMS_PWD"]

a = UNIPA_Login(UNIPA_ID, UNIPA_PWD)
assignments = a.get_assignment()
ReUNIPA_App = app.AppMain(assignments=assignments)
print(assignments)
ft.app(target=ReUNIPA_App.app_main)
#b = UNIPA_Submit(UNIPA_ID,UNIPA_PWD)
#b.submit_assignment(id=assignments[0][0],file_path="")

#b = login.Teams_Login(TEAMS_ID, TEAMS_PWD)
#b.login()
#print(assignments)
