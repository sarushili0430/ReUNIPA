import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import flet as ft
from unipa import UNIPA_Submit
from unipa import UNIPA_Login
from dotenv import load_dotenv
from tools import list_to_dict

# For testing
ASSIGNMENTS = [
    [
        "funcForm:j_idt162:j_idt211:0:j_idt232",
        "Lecture 12 EX",
        "See the attached file and submit your file by the end of next Thursday.\n        ",
        "2023/11/02",
        "FILE",
    ],
    [
        "funcForm:j_idt162:j_idt211:1:j_idt232",
        "Quiz 12 first submission",
        'Hello students!This is for the first submission for Quiz 12.Before giving marks for your answers, take a photo of the Quiz paper, and then submit the photo to here. That is the confirmation that you solved the Quiz by yourself. The submission deadline is 8am on 3rd November.Give the filename of the photo as follows:2021m000_Quiz12_1.jpgFilename consists of "student ID number" + "Quiz number" + "submission number". Your cooperation will be appreciated.Enjoy everything!Kind regards,Takahiro Namazu\n        ',
        "2023/11/03",
        "FILE",
    ],
    [
        "funcForm:j_idt162:j_idt211:2:j_idt232",
        "遠隔課題\u3000スポーツと国際社会人基礎力  Online assignment: Sport and Basic Skills for International Working Adult",
        'SLSⅣ\u3000種目共通課題②\u3000スポーツと国際社会人基礎力今回のテーマは「スポーツと国際社会人基礎力」です。下記のURLから動画を視聴し、動画内で指示された課題を提出してください。231024_秋学期SLSⅣ種目共通課題②_梶田担当.mp4\xa0【レポート提出について】文字数：①②の合計で全角400字（半角800字）程度期\u3000限：11月8日\u30009:29まで方\u3000法：先端なびからWeb提出遠隔授業における映像視聴と課題提出により、今週の授業は出席になります。それでは今週も課題提出期限に間に合うように、計画的に取り組みましょう。早川The theme of this week\'s on-demand assignment is " Sport and Basic Skills for International working Adult ".Please watch the video at the URL below and submit the assignment indicated in the video.231024_秋学期SLSⅣ種目共通課題②_梶田担当_英語版.mp4\xa0【Report Submission】Number of words：about 200 wordsThe deadline of submission：November 8th 9:29.Submission method：web submission from “sentan navi”.For remote classes, attendance is considered as both viewing the video and submitting assignments.Hayakawa\n        ',
        "2023/11/08",
        "TEXT",
    ],
]

load_dotenv()

UNIPA_ID = os.environ["UNIPA_ID"]
UNIPA_PWD = os.environ["UNIPA_PWD"]


class HomeView(ft.UserControl):
    def __init__(self, page: ft.Page, assignments):
        super().__init__(self)
        self.page = page
        # Header Components
        self.name = ft.Text(
            value="2022MXXX\nTaro Yamada",
            width=120,
            height=60,
            size=20,
            font_family="Inter",
            text_align="Center",
        )
        self.assignment_name = ft.Text(
            value="",
            width=560,
            height=60,
            text_align="Center",
            font_family="Inter",
            size=40,
        )
        self.header = ft.Container(
            ft.Row(
                [
                    self.name,
                    self.assignment_name,
                ],
            ),
            padding=20,
        )
        # Body Components
        self.retry_get_assignment_btn = ft.IconButton(
            icon=ft.icons.REFRESH, on_click=self.refresh_assignment_list
        )
        self.lv = ft.ListView(expand=1.0, spacing=20, padding=20)
        # Controlling the assignments list according to assignments.
        if assignments == []:
            pass
        elif assignments == None:
            self.lv.controls.append(self.retry_get_assignment_btn)
        else:
            self.assignments = list_to_dict(assignments)
            print(self.assignments)
            for _ in range(len(self.assignments)):
                self.lv.controls.append(
                    ft.TextButton(
                        text=assignments[_][1],
                        on_click=self.assignment_clicked,
                        data=[assignments[_][1], assignments[_][2], assignments[_][4]],
                    )
                )
        self.assignment_list = ft.Container(
            self.lv,
            width=160,
            height=304,
        )
        self.pickfile = ft.FilePicker(on_result=self.assignment_file_selected)
        self.page.controls.append(self.pickfile)
        self.page.overlay.append(self.pickfile)
        self.assignment_details = ft.Text(
            value="",
            text_align="Left",
            font_family="Inter",
            size=15,
            max_lines=100,
        )
        self.pickfile_btn = ft.ElevatedButton(
            text="Pick Files",
            icon=ft.icons.UPLOAD_FILE,
            on_click=lambda x: self.pickfile.pick_files(allow_multiple=False),
            visible=False,
        )
        self.text_submit_box = ft.TextField(
            width=500,
            min_lines=1,
            max_lines=20,
            multiline=True,
            on_change=self.assignment_text_entered,
            visible=False,
        )
        self.text_submit_box_container = ft.Column(
            [self.text_submit_box],
            scroll=ft.ScrollMode.HIDDEN,
            width=500,
            height=60,
            visible=False,
        )
        self.file_submit_btn = ft.TextButton(
            text="Submit",
            on_click=self.assignment_submit_clicked,
            visible=False,
            disabled=True,
        )
        self.assignment_submition = ft.Container(
            ft.Row(
                [
                    self.text_submit_box_container,
                    self.pickfile_btn,
                    self.file_submit_btn,
                ]
            ),
            padding=ft.padding.symmetric(horizontal=20),
        )
        self.body = ft.Container(
            ft.Row(
                [
                    self.assignment_list,
                    ft.Column(
                        [
                            ft.Container(
                                ft.Column(
                                    [self.assignment_details],
                                    expand=1,
                                    scroll=ft.ScrollMode.HIDDEN,
                                ),
                                width=560,
                                height=260,
                                margin=ft.margin.only(left=20),
                            ),
                            self.assignment_submition,
                        ],
                    ),
                ]
            ),
        )
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Submit Successful"))

    def assignment_clicked(self, e):
        print(e.control.data)
        self.change_assignment_name(name=e.control.data[0])
        self.assignment_details.value = e.control.data[1]
        self.file_submit_btn.visible = True
        if e.control.data[2] == "FILE":
            self.pickfile_btn.visible = True
            self.text_submit_box.visible = False
            self.text_submit_box_container.visible = False
        elif e.control.data[2] == "TEXT":
            self.pickfile_btn.visible = False
            self.text_submit_box.visible = True
            self.text_submit_box_container.visible = True
        self.update()
        print(self.assignment_name)

    def change_assignment_name(self, name):
        self.assignment_name.value = name
        print(self.assignment_name.value)
        self.update()
        print(self.assignment_name.value)

    def assignment_text_entered(self, e):
        if e.control.value != "":
            self.file_submit_btn.disabled = False
        else:
            self.file_submit_btn.disabled = True
        self.update()

    def assignment_file_selected(self, e: ft.FilePickerResultEvent):
        try:
            self.assignment_path = e.files[0].path
            self.file_submit_btn.disabled = False
            self.update()
            print(self.assignment_path)
        except Exception as e:
            print(e)

    def assignment_submit_clicked(self, e):
        with UNIPA_Submit(UNIPA_ID, UNIPA_PWD) as client:
            if self.assignments[self.assignment_name.value][1] == "FILE":
                result = client.submit_assignment(
                    id=self.assignments[self.assignment_name.value][0],
                    file_path=self.assignment_path,
                )
            elif self.assignments[self.assignment_name.value][1] == "TEXT":
                result = client.submit_assignment(
                    id=self.assignments[self.assignment_name.value][0],
                    text=self.text_submit_box.value,
                )
        if result == True:
            self.page.snack_bar.content = ft.Text("Submit Success")
            self.page.snack_bar.open = True
            self.page.update()
            self.refresh_assignment_list()
            self.clear_assignment_detail()
        else:
            self.page.snack_bar.content = ft.Text("Submit failed")
            self.page.snack_bar.bgcolor = "#F94C10"
            self.page.snack_bar.open = True
            self.page.update()
        print("Submission result: " + str(result))

    def refresh_assignment_list(self, e=None):
        new_assignment_list = []
        try:
            with UNIPA_Login(UNIPA_ID, UNIPA_PWD) as client:
                new_assignment_list = client.get_assignment()
            self.lv.clean()
            self.assignments = list_to_dict(new_assignment_list)
            for _ in range(len(self.assignments)):
                self.lv.controls.append(
                    ft.TextButton(
                        text=new_assignment_list[_][1],
                        on_click=self.assignment_clicked,
                        data=[
                            new_assignment_list[_][1],
                            new_assignment_list[_][2],
                            new_assignment_list[_][4],
                        ],
                    )
                )
            print(new_assignment_list)
        except Exception as e:
            print(e)
            self.lv.clean()
            self.lv.controls.append(self.retry_get_assignment_btn)
        self.update()

    def clear_assignment_detail(self):
        self.assignment_details.value = ""
        self.assignment_name.value = ""
        self.pickfile_btn.visible = False
        self.text_submit_box.visible = False
        self.file_submit_btn.visible = False
        self.update()

    def build(self):
        return ft.Column([self.header, self.body])


def main(page: ft.Page):
    page.window_width = 896
    page.window_height = 504
    page.window_visible = True
    page.add(HomeView(page, assignments=ASSIGNMENTS))


if __name__ == "__main__":
    ft.app(target=main)
