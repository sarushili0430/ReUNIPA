from flet import *
from views.app import HomeView
from views.login import LoginView
from views.start import StartView

ASSIGNMENTS = [
    [
        "funcForm:j_idt162:j_idt211:0:j_idt232",
        "Lecture 12 EX",
        "2023/11/02",
        "See the attached file and submit your file by the end of next Thursday.\n        ",
    ],
    [
        "funcForm:j_idt162:j_idt211:1:j_idt232",
        "Quiz 12 first submission",
        "2023/11/03",
        'Hello students!This is for the first submission for Quiz 12.Before giving marks for your answers, take a photo of the Quiz paper, and then submit the photo to here. That is the confirmation that you solved the Quiz by yourself. The submission deadline is 8am on 3rd November.Give the filename of the photo as follows:2021m000_Quiz12_1.jpgFilename consists of "student ID number" + "Quiz number" + "submission number". Your cooperation will be appreciated.Enjoy everything!Kind regards,Takahiro Namazu\n        ',
    ],
    [
        "funcForm:j_idt162:j_idt211:2:j_idt232",
        "遠隔課題\u3000スポーツと国際社会人基礎力  Online assignment: Sport and Basic Skills for International Working Adult",
        "2023/11/08",
        'SLSⅣ\u3000種目共通課題②\u3000スポーツと国際社会人基礎力今回のテーマは「スポーツと国際社会人基礎力」です。下記のURLから動画を視聴し、動画内で指示された課題を提出してください。231024_秋学期SLSⅣ種目共通課題②_梶田担当.mp4\xa0【レポート提出について】文字数：①②の合計で全角400字（半角800字）程度期\u3000限：11月8日\u30009:29まで方\u3000法：先端なびからWeb提出遠隔授業における映像視聴と課題提出により、今週の授業は出席になります。それでは今週も課題提出期限に間に合うように、計画的に取り組みましょう。早川The theme of this week\'s on-demand assignment is " Sport and Basic Skills for International working Adult ".Please watch the video at the URL below and submit the assignment indicated in the video.231024_秋学期SLSⅣ種目共通課題②_梶田担当_英語版.mp4\xa0【Report Submission】Number of words：about 200 wordsThe deadline of submission：November 8th 9:29.Submission method：web submission from “sentan navi”.For remote classes, attendance is considered as both viewing the video and submitting assignments.Hayakawa\n        ',
    ],
]


def views_handler(page, assignments):
    return {
        "/": View(
            route="/",
            controls=[HomeView(page=page, assignments=assignments)],
        ),
        "/home": View(
            route="/home",
            controls=[StartView(page=page)],
        ),
        "/login": View(
            route="/login",
            controls=[LoginView(page=page)],
        ),
    }
