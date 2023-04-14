PLAYER1_PORT=3001
PLAYER1=localhost:$(PLAYER1_PORT)

PLAYER2_PORT=3003
PLAYER2=localhost:$(PLAYER2_PORT)

ourRandom:
	python3 api.py -p $(PLAYER1_PORT) -l random

ourMinMax:
	python3 api.py -p $(PLAYER2_PORT) -l minmax

arena:
	python3 arena.py --player1=$(PLAYER1) --player2 $(PLAYER2)

# run:
# 	make start_servers & make arena

run:
	make arena
