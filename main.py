import login

ID = "2022m089"
PWD = "Saru0430"

a = login.Login(ID,PWD)
a.login()
assignments = a.get_assignment()

print(assignments)
