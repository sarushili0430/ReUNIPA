import login

ID = "XXXXXXXX"
PWD = "XXXXXXXX"


a = login.UNIPA_Login(ID,PWD)
a.login()
assignments = a.get_assignment()

b = login.Teams_Login("2022m089@kuas.ac.jp","Saru0430")
b.login()
print(assignments)
