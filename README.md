pc2018
====
## Description
This is a system which to win Encampment game of 'Programming Contest 2018' (Competitive Part).

This system is 'Reinforcement Learning'.

This learns by following the steps below
# Q- Learning

1.read q table which is 'Action Value Function'.

2.initialize learning environment.

3.learning (loop 3.1 ~ 3.5)

  3.1 calculate the best move
  
  3.2 get enemy's move
  
  3.3 decide friend's and enemy's move 
  
  3.4 get reward
  
  3.5 update q table
  
4.save q table(result)

## Requirement
Python 3.6.5, go 1.10.3

## Usage
change directory that is 'pc2018-master'　and execute following commands in advance
> cd purocon/

> go run api.go

if you use Q-Learning system by learning 
> python3 QLprocon2018.py

if you use Monte Carlo Method system by learning
> python3 mcl0917.py

## Favor
i want Kota to make Enemy system.

