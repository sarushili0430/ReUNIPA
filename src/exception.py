class KigenariBtnIntractError(Exception):
    def __str__(self) -> str:
        return "「期限あり」Element was not interacted successfully."


class MottoBtnIntractError(Exception):
    def __str__(self) -> str:
        return "「もっと見る」Element was not interacted successfully."


class HomeBtnIntractError(Exception):
    def __str__(self) -> str:
        return "UNIPAロゴ Element was not interacted successfully"
