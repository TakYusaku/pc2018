pc2018
====
## Description and Usage
チーム名:シンタローズ  作品名:AIけーじくん  
initCSV.py -> Qテーブルの初期化  
> python3 initCSV.py 'filename'  

linenotify.py -> 学習の進行具合・結果をLINEで通知  
mcl0917.py -> モンテカルロ法で学習させる  
> python3 mcl0917.py  

QLprocon2018.py -> Q学習で学習させる  
> python3 QLprocon2018.py  

q_table_MCM.csv , q_table_QL.csv -> モンテカルロ法，Q学習で学習させた結果を保存するファイル  

/result -> 学習結果の保存(現在入っているのは一例)  
/qr -> QRコードを読み込むスクリプト  
/purocon/api.go , field.py -> 両方ともゲームを行うフィールド(goは学習用，pythonはアプリ用)  
/app -> 学習済みモデルを動かすアプリケーション(未)  
　
## Development environment
使用OS:macOS HighSierra 10.13.6, Ubuntu 18.04  
使用言語:Python3 , Go lang, JavaScript, html, CSS, Node.js  
使用ライブラリ:OpenAI gym, OpenCV, pyzbar  
使用フレームワーク: Flask, Electron  
