import flet as ft
from unipa import *
import dotenv
import os

#For testing
ASSIGNMENTS = [['funcForm:j_idt162:j_idt211:0:j_idt232', 'Lecture 12 EX', '2023/11/02', 'See the attached file and submit your file by the end of next Thursday.\n        '], ['funcForm:j_idt162:j_idt211:1:j_idt232', 'Quiz 12 first submission', '2023/11/03', 'Hello students!This is for the first submission for Quiz 12.Before giving marks for your answers, take a photo of the Quiz paper, and then submit the photo to here. That is the confirmation that you solved the Quiz by yourself. The submission deadline is 8am on 3rd November.Give the filename of the photo as follows:2021m000_Quiz12_1.jpgFilename consists of "student ID number" + "Quiz number" + "submission number". Your cooperation will be appreciated.Enjoy everything!Kind regards,Takahiro Namazu\n        '], ['funcForm:j_idt162:j_idt211:2:j_idt232', '遠隔課題\u3000スポーツと国際社会人基礎力  Online assignment: Sport and Basic Skills for International Working Adult', '2023/11/08', 'SLSⅣ\u3000種目共通課題②\u3000スポーツと国際社会人基礎力今回のテーマは「スポーツと国際社会人基礎力」です。下記のURLから動画を視聴し、動画内で指示された課題を提出してください。231024_秋学期SLSⅣ種目共通課題②_梶田担当.mp4\xa0【レポート提出について】文字数：①②の合計で全角400字（半角800字）程度期\u3000限：11月8日\u30009:29まで方\u3000法：先端なびからWeb提出遠隔授業における映像視聴と課題提出により、今週の授業は出席になります。それでは今週も課題提出期限に間に合うように、計画的に取り組みましょう。早川The theme of this week\'s on-demand assignment is " Sport and Basic Skills for International working Adult ".Please watch the video at the URL below and submit the assignment indicated in the video.231024_秋学期SLSⅣ種目共通課題②_梶田担当_英語版.mp4\xa0【Report Submission】Number of words：about 200 wordsThe deadline of submission：November 8th 9:29.Submission method：web submission from “sentan navi”.For remote classes, attendance is considered as both viewing the video and submitting assignments.Hayakawa\n        ']]

load_dotenv()

UNIPA_ID = os.environ["UNIPA_ID"]   
UNIPA_PWD = os.environ["UNIPA_PWD"]


class AppHeader(ft.UserControl):
    def __init__(self,page: ft.Page):
        super().__init__(self)
        self.page = page
        self.name = ft.Text(
            value="2022MXXX\nTaro Yamada",
            width=120,
            height=60,
            size=20,
            font_family="Inter",
            text_align="Center",
        )
        self.assignment_name = ft.Text(
            value = "Assignment Name",
            width = 560,
            height = 60,
            text_align="Center",
            font_family = "Inter",
            size = 40
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
    
    def change_assignment_name(self,name):
        self.assignment_name.value = name
        print(self.assignment_name.value)
        self.update()
        print(self.assignment_name.value)

    def build(self):
        return self.header
    
class AppBody(ft.UserControl):
    def __init__(self, page:ft.Page,assignments:list,header:AppHeader):
        super().__init__(self)
        self.page = page
        self.header = header
        self.assignment_path = None
        self.assignments = self.list_to_dict(assignments)
        self.lv = ft.ListView(expand=1.0,spacing=20,padding=20)
        for _ in range(len(self.assignments)): self.lv.controls.append(ft.TextButton(text=assignments[_][1],on_click=self.assignment_clicked,data=[assignments[_][1],assignments[_][3]]))
        self.assignment_list = ft.Container(
            self.lv,
            width=160,
            height=304,
        )
        self.pickfile = ft.FilePicker(on_result=self.assignment_file_selected)
        self.page.controls.append(self.pickfile)
        self.assignment_details = ft.Text(
            value="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris non iaculis arcu.",
            width=560,
            height=260,
            text_align="Left",
            font_family="Inter",
            size=15,
            max_lines=100,
        )

        self.assignment_submition = ft.Row(
            [
                ft.ElevatedButton(text="Pick Files",
                                  icon=ft.icons.UPLOAD_FILE,
                                  on_click=lambda x: self.pickfile.pick_files(allow_multiple=False)
                ),
                ft.TextButton(text="Submit",on_click=self.assignment_submit_clicked)
            ]
        )
        self.body = ft.Container(
            ft.Row(
                [
                    self.assignment_list,
                    ft.Column(
                        [
                            self.assignment_details,
                            self.assignment_submition,
                        ]
                    )
                ]
            )
        )

    def list_to_dict(self,ls:list):
        assign_dict = {}
        for _ in ls:
            assign_dict[_[1]] = _[0]
        return assign_dict

    def assignment_file_selected(self, e:ft.FilePickerResultEvent):
        self.assignment_path = e.files[0].path
        print(self.assignment_path)

    def assignment_submit_clicked(self,e):
        SUBMISSION = UNIPA_Submit(UNIPA_ID,UNIPA_PWD)
        result = SUBMISSION.submit_assignment(id=self.assignments[self.header.assignment_name.value],file_path=self.assignment_path)
        print("Submission result: "+str(result))
    
    def assignment_clicked(self, e):
        self.header.change_assignment_name(name=e.control.data[0])
        self.assignment_details.value = e.control.data[1]
        self.update()
        print(self.header.assignment_name)
        
    def build(self):
        return self.body

class AppMain():
    def __init__(self,assignments:list):
        self.assignments = assignments
    
    def app_main(self,page: ft.Page):
        page.title = "ReUNIPA"
        page.scroll = "ADAPTIVE"
        page.window_width = 896
        page.window_height = 504
        pickfile = ft.FilePicker(on_result=lambda x: print("completed"))
        page.overlay.append(pickfile)  
        #lv.controls.append(ft.TextButton(text="assignment1"))

        header = AppHeader(page)
        body = AppBody(page,assignments=self.assignments,header=header)

        page.add(ft.Column([header,body]))


def main(page: ft.Page):

    header = AppHeader(page)
    body = AppBody(page,header=header,assignments=ASSIGNMENTS)

    page.add(
        #header
        ft.Column(
            [
                header,
                body
            ]
        )
    )

if __name__ == "__main__":
    ReUNIPA = AppMain(assignments=ASSIGNMENTS)
    ft.app(target=ReUNIPA.app_main)
