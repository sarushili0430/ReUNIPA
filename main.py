#import login
from unipa import UNIPA_Login
from dotenv import load_dotenv

import os

load_dotenv()

UNIPA_ID = os.environ["UNIPA_ID"]
UNIPA_PWD = os.environ["UNIPA_PWD"]
TEAMS_ID = os.environ["TEAMS_ID"]
TEAMS_PWD = os.environ["TEAMS_PWD"]

a = UNIPA_Login(UNIPA_ID, UNIPA_PWD)
a.login()
assignments = a.get_assignment()
print(assignments)

#b = login.Teams_Login(TEAMS_ID, TEAMS_PWD)
#b.login()
#print(assignments)
