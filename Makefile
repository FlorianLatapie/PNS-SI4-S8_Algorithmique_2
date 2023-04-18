OUR_AI_PORT=3001
OUR_AI=localhost:$(OUR_AI_PORT)

ENEMY_AI_PORT=3003
ENEMY_AI=localhost:$(ENEMY_AI_PORT)

ourMinmax:
	python3.11 api.py -p $(OUR_AI_PORT) -l minmax

ourMinmaxD2:
	python3.11 api.py -p $(OUR_AI_PORT) -l minmax -d 2

ourMinmaxD4:
	python3.11 api.py -p $(OUR_AI_PORT) -l minmax -d 4

ourMinmaxD6:
	python3.11 api.py -p $(OUR_AI_PORT) -l minmax -d 6

ourMinmaxD8:
	python3.11 api.py -p $(OUR_AI_PORT) -l minmax -d 8

ourMinmax2:
	python3.11 api.py -p $(ENEMY_AI_PORT) -l minmax

ourRandom:
	python3.11 api.py -p $(ENEMY_AI_PORT) -l random

enemyMedium:
	cd ./cp4-ai/cp4_ai/ && python3.11 main.py -p $(ENEMY_AI_PORT) -l medium

enemyAdvanced:
	cd ./cp4-ai/cp4_ai/ && python3.11 main.py -p $(ENEMY_AI_PORT) -l advanced

enemyExpert:
	cd ./cp4-ai/cp4_ai/ && python3 main.py -p $(ENEMY_AI_PORT) -l expert


arena:
	python3.11 arena.py --our=$(OUR_AI) --enemy=$(ENEMY_AI)

arenastats:
	python3.11 arena.py --our=$(OUR_AI) --enemy=$(ENEMY_AI) --enemylevel=Medium

arenasolver:
	python3.11 arena.py --our=$(OUR_AI) --enemy=solver --enemylevel=Solver

arenalogs:
	python3.11 arena.py --our=$(OUR_AI) --enemy=$(ENEMY_AI) --loglevel=debug

run:
	make arena

