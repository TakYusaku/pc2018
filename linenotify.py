# LINE通知機能
# coding:UTF-8
import requests

def main_m(message):
    url = "https://notify-api.line.me/api/notify"
<<<<<<< HEAD
    token = "送信先のtoken"
=======
    token = "token"
>>>>>>> origin/master
    headers = {"Authorization" : "Bearer "+ token}

    #message =  'ここにメッセージを入れます'
    payload = {"message" :  message}

    r = requests.post(url ,headers = headers ,params=payload)


def main_f(message,figname):
    url = "https://notify-api.line.me/api/notify"
    token = "GHJQgEc3BZ0dXYYirYi9DG0v6KYw7wD9hFUPCLlmkON"
    headers = {"Authorization" : "Bearer "+ token}

    #message =  'ここにメッセージを入れます'
    payload = {"message" :  message}
    files = {"imageFile": open(figname, "rb")}

    r = requests.post(url ,headers = headers ,params=payload,files=files)
<<<<<<< HEAD
=======


>>>>>>> origin/master
