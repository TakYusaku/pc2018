# LINE通知機能
# coding:UTF-8
import requests

def main():
    url = "https://notify-api.line.me/api/notify"
    token = "GHJQgEc3BZ0dXYYirYi9DG0v6KYw7wD9hFUPCLlmkON" 
    headers = {"Authorization" : "Bearer "+ token}

    message =  'ここにメッセージを入れます'
    payload = {"message" :  message}
    #files = {"imageFile": open("1008_ri_2.png", "rb")} #バイナリで画像ファイルを開きます。対応している形式はPNG/JPEGです。

    r = requests.post(url ,headers = headers ,params=payload, files=files)

if __name__ == '__main__':
    main()
