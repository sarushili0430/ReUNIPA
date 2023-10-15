import login

ID = "XXXXXXX"
PWD = "XXXXXXX"

a = login.Login(ID,PWD)
a.login()
assignments = a.get_assignment()

print(assignments)
