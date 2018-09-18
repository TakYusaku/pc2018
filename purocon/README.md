# how to use

## u can running this program and build local server

> go run api.go

## start the game

> curl localhost:8000/start

## move agent (example,usr1 moves right)

> curl -X POST localhost:8000/move -d "usr=1&d=r"


## remove the panel (example,usr1 removes right-up)

> curl -X POST localhost:8000/remove -d "usr=1&d=ru"


## u can show the field

> curl -X POST localhost:8000/show
