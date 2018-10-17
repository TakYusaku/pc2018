# LINE通知機能
# coding:UTF-8
import requests

def main_m(message):
    url = "https://notify-api.line.me/api/notify"
    token = "token"
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


if __name__ == '__main__':
    m = "https://item.rakuten.co.jp/denpcy/11838002/?scid=af_pc_etc&sc2id=af_102_1_10000903#10002463"
    main_m(m)
