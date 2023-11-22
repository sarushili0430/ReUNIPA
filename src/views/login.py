from unipa import check_id
from dotenv import load_dotenv
import flet as ft
import dotenv

load_dotenv()

class LoginView(ft.UserControl):

    def __init__(self,page:ft.Page):
        super().__init__()
        #Login components
        self.page = page
        self.unipa_url = ft.TextField(label="UNIPA URL")
        self.username = ft.TextField(label="UNIPA Username")
        self.pwd = ft.TextField(label="UNIPA Password",password=True,can_reveal_password=True)
        self.submit = ft.ElevatedButton(text="Submit",on_click=self.check_login)
        self.prog_ring = ft.ProgressRing(visible=False)
        #Login condition banner
        self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Login Successful")
            )
        self.submit_container = ft.Row(
            [
                self.submit,
                self.prog_ring,
            ]
        )
        self.login_instance = ft.Column(
            [
                self.unipa_url,
                self.username,
                self.pwd,
                self.submit_container
            ]
        )

    def check_login(self,e):

        #Disable submit button
        #Enable progress ring
        self.submit.disabled = True
        self.prog_ring.visible = True
        self.update()

        check_result = check_id(id=self.username.value,pwd=self.pwd.value,url=self.unipa_url.value)

        #Check whether id is available or not
        if check_result:
            #Enable submit button
            print("SUCCESS")
            self.page.go("/")
        else:
            self.submit.disabled = False
            self.prog_ring.visible = False
            self.update()

    def build(self):
        return self.login_instance
