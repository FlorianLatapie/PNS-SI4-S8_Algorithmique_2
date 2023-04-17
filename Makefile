PLAYER1_PORT=3001
PLAYER1=localhost:$(PLAYER1_PORT)

PLAYER2_PORT=3003
PLAYER2=localhost:$(PLAYER2_PORT)

ourMinMax:
	python3 api.py -p $(PLAYER1_PORT) -l minmax

ourMinMax2:
	python3 api.py -p $(PLAYER2_PORT) -l minmax

ourRandom:
	python3 api.py -p $(PLAYER2_PORT) -l random

enemyMedium:
	cd ./cp4-ai/cp4_ai/ && python3 main.py -p $(PLAYER2_PORT) -l medium

enemyAdvanced:
	cd ./cp4-ai/cp4_ai/ && python3 main.py -p $(PLAYER2_PORT) -l advanced





arena:
	python3 arena.py --player1=$(PLAYER1) --player2 $(PLAYER2)

arena-reversed:
	python3 arena.py --player1=$(PLAYER2) --player2 $(PLAYER1)

# run:
# 	make start_servers & make arena

run:
	make arena


run2:
	make arena-reversed
