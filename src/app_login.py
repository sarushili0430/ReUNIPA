from unipa import check_id
import flet as ft


def main(page: ft.Page):
    
    def check_login(e):
        check_id(id=username.value,pwd=pwd.value,url=unipa_url.value)
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