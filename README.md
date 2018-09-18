pc2018
====
## Description
This is a system which to win Encampment game of 'Programming Contest 2018' (Competitive Part).  
This system is 'Reinforcement Learning'.  
This learns by following the steps below.  
### Q - Learning

1.read q table which is 'Action Value Function'.  
2.initialize learning environment.  
3.learning (loop)  
  * calculate the best move  
  * get enemy's move  ★  
  * decide friend's and enemy's move  
  * get reward  
  * update q table  
4.save q table(result)

### Monte Calro Method
1.read q table which is 'Action Value Function'.  
2.initialize learning environment.  
3.learning (loop)  
  * calculate the best move  
  * get enemy's move ★  
  * decide friend's and enemy's move  
  * get reward  
  * save move and position  
  * "if tern ended" , update q table  
4.save q table(result)


the difference of both Q-Learning and Monte Calro Method is timing of updating q table .  
in Q-Learning, q table is updated every terns.  
on the other hand,in Monte Carlo Method, q table is updated at the end of game.

## Requirement
Python 3.6.5, go 1.10.3

## Usage
change directory that is 'pc2018-master'　and execute following commands in advance
> cd purocon/

> go run api.go

if you use Q-Learning system for learning 
> python3 QLprocon2018.py

if you use Monte Carlo Method system for learning
> python3 mcl0917.py

## Favor
i want Kota to make Enemy system.  
1. calculate the best move  
2. return direction(including stay) or remove panel   

引数を，ターン数/フィールド情報(サイズ，得点)/初期位置/として，最善手を計算し，  
1．”移動するなら方向を番号で（以下に示す）”，  
2．”移動するなら方向を番号で（以下に示す）”，  
3．”移動orパネル除去予定位置を[[x3,y3],[x4,y4]](フィールドの横(row)をx,フィールドの縦(column)をyとして，敵（3と4）の座標を収納)”，  
4．”パネルを除去するなら文字列で'remove'”  
を返して欲しい．  
今ある機能として，  
1．エージェントの位置を[[x,y],[x,y]]で返す．  
2．ターン数，フィールド情報（サイズ，得点）を返す．  
3．移動先がどんな状況なのか（フィールド範囲外なのか，相手のパネルがあるのか，パネルがないのか）を返す．  
4．実際に計算した最善手から行動させる．  
5．得点計算と勝敗判定  
6．API叩くときは，方向などを文字列で送るが，計算では方向に番号を振って数字で計算させる．だから，文字列↔︎数字の変換．  
がある．

詳しくはまたLINEして！  
それと，今回追加した'purocon'にあるフィールドサーバを使って欲しい．　　
