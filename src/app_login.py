from unipa import check_id
from dotenv import load_dotenv
import flet as ft
import dotenv

load_dotenv()
print("dotenv loaded")

def main(page: ft.Page):
    
    def check_login(e):
        if check_id(id=username.value,pwd=pwd.value,url=unipa_url.value) == "SUCCESS":
            print("SUCCESS")
            dotenv_file = dotenv.find_dotenv()
            dotenv.set_key(dotenv_path=dotenv_file,key_to_set="UNIPA_URL",value_to_set=unipa_url.value)
            dotenv.set_key(dotenv_path=dotenv_file,key_to_set="UNIPA_ID",value_to_set=username.value)
            dotenv.set_key(dotenv_path=dotenv_file,key_to_set="UNIPA_PWD",value_to_set=pwd.value)
        
    
    page.title = "Login"
    unipa_url = ft.TextField(label="UNIPA URL")
    username = ft.TextField(label="UNIPA Username")
    pwd = ft.TextField(label="UNIPA Password",password=True,can_reveal_password=True)
    submit = ft.ElevatedButton(text="Submit",on_click=check_login)
    page.add(
        unipa_url,
        username,
        pwd,
        submit,
    )
    
    


ft.app(target=main)