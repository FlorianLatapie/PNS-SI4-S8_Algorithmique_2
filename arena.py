from time import time
import requests
import utils
import argparse
import math
import statistics
import logging
FORMAT = "%(message)s"

__ENEMY_AI_URL = ""
__OUR_AI_URL = ""
__POS_PLAYED = ""

__GAMES_TO_PLAY = 2
__GAMES_PLAYED = 0
__OUR_AI_WINS = 0
__ENEMY_AI_WINS = 0
__DRAWS = 0
__OUR_LOST_DEPTH = 0
__OUR_WIN_DEPTH = 0

__ENEMY_AI_LEVEL="none"

__OUR_EXEC_TIME=[]
__ENEMY_EXEC_TIME=[]

__DATA=[]

def toggle_grid(grid: str):
    return grid.replace("1", "a").replace("2", "1").replace("a", "2")

def add_stat(winner: str, turn: str, starting: str):
    global __OUR_AI_WINS
    global __ENEMY_AI_WINS
    global __OUR_LOST_DEPTH
    global __OUR_WIN_DEPTH
    global __GAMES_PLAYED
    global __DRAWS
    global __ENEMY_AI_LEVEL
    __GAMES_PLAYED += 1
    our_exec_mean = statistics.mean(__OUR_EXEC_TIME) * 1000
    our_exec_max = max(__OUR_EXEC_TIME) * 1000
    enemy_exec_mean = statistics.mean(__ENEMY_EXEC_TIME) * 1000
    __DATA.append({
        "winner": winner + " AI",
        "turn": turn,
        "starting_player": starting + " AI",
        "enemy_ai_level": __ENEMY_AI_LEVEL,
        "our_mean_exec_time": our_exec_mean,
        "our_max_exec_time": our_exec_max,
        "enemy_mean_exec_time": enemy_exec_mean
    })
    logging.debug("winner " + winner)
    if winner == "our":
        __OUR_AI_WINS += 1
        __OUR_WIN_DEPTH = turn
    if winner == "enemy":
        __ENEMY_AI_WINS += 1
        __OUR_LOST_DEPTH = turn
    if winner == "draw":
        __DRAWS +=1

def player_plays(player_name: str, grid: str) -> str:
    global __POS_PLAYED
    url = __ENEMY_AI_URL
    if player_name == "our": url = __OUR_AI_URL
    logging.debug(player_name + " " + url)
    url += "/move?b=" + grid
    res = requests.get(url)
    if res.status_code == 200:
        move = res.json()
        __POS_PLAYED += str(move)
        move_to_0_index = move - 1
        logging.debug("Player "+ str(player_name) + "AI played " + str(move_to_0_index))
        updated_grid = utils.add_move_to_grid(grid, move_to_0_index, "2")
        return updated_grid
    else:
        raise Exception("Error: ",
                        "player ",
                        player_name,
                        "AI responded with: ",
                        res.status_code,
                        " ",
                        res.json()
                        )

def solver_plays(grid:str):
    global __POS_PLAYED
    url = "https://connect4.gamesolver.org/solve?pos=" + __POS_PLAYED;
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    best_move = -1
    best_move_score = -math.inf
    if res.status_code == 200:
        data = res.json()
        scores = data["score"]
        nb_scores = len(scores)
        for i in range(nb_scores):
            if scores[i] > best_move_score and scores[i] != 100:
                best_move_score = scores[i]
                best_move = i +1
    __POS_PLAYED += str(best_move)
    move_to_0_index = best_move - 1
    logging.debug("Solver played " + str(move_to_0_index))
    updated_grid = utils.add_move_to_grid(grid, move_to_0_index, "2")
    return updated_grid

def add_time(time: float, player: str):
    global __OUR_EXEC_TIME
    global __ENEMY_EXEC_TIME
    if player == "our": __OUR_EXEC_TIME.append(time)
    elif player == "enemy": __ENEMY_EXEC_TIME.append(time)



def play_game(starting_player="our"):
    if starting_player == "our": second_player = "enemy"
    else: second_player = "our"
    grid = "000000000000000000000000000000000000000000"
    i = 1
    while True:
        grid = toggle_grid(grid)
        start_time = time()
        grid = player_plays(starting_player, grid)
        end_time = time()
        exec_duration = end_time - start_time
        i += 1
        add_time(exec_duration, starting_player)
        grid = toggle_grid(grid)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "1")
        logging.debug(has_won)
        if has_won:
            add_stat(starting_player, str(i), starting_player)
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i), starting_player)
            return

        start_time = time()
        grid = player_plays(second_player, grid)
        end_time = time()
        exec_duration = end_time - start_time
        i += 1
        add_time(exec_duration, second_player)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "2")
        logging.debug(has_won)
        if has_won:
            add_stat(second_player, str(i), starting_player)
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i), starting_player)
            return


def main():
    parser = argparse.ArgumentParser(description="CONNECT 4 Arena")
    parser.add_argument('--our')
    parser.add_argument('--enemy')
    parser.add_argument('--loglevel')
    parser.add_argument('--enemylevel')
    args = parser.parse_args()
    global __ENEMY_AI_URL
    global __OUR_AI_URL
    global __ENEMY_AI_LEVEL
    __ENEMY_AI_URL = "http://" + args.enemy
    __OUR_AI_URL = "http://" + args.our
    __ENEMY_AI_LEVEL = args.enemylevel
    logging.disable = False
    loglevel = logging.INFO
    if args.loglevel == "debug":
        loglevel = logging.DEBUG

    if __ENEMY_AI_URL == "" or __OUR_AI_URL == "":
        logging.error("Enter our and enemy args (the url of the connect 4 servers)")
        return

    logging.basicConfig(level = loglevel, format=FORMAT)
    global __GAMES_PLAYED
    global __GAMES_TO_PLAY
    global __OUR_AI_WINS
    global __ENEMY_AI_WINS
    global __DEPTHS
    global __DRAWS
    global __DATA
    
    starting_player = "our"
    while(__GAMES_PLAYED < __GAMES_TO_PLAY):

        if args.enemy == "solver" :
            play_against_solver(starting_player)
        else: play_game(starting_player)
        
        if starting_player == "our": starting_player = "enemy"
        else: starting_player = "our"

        logging.debug("games played " + str(__GAMES_PLAYED))

    print_stats(__DATA)
    # logging.info("Games played: " + str(__GAMES_PLAYED))
    # logging.info("Our AI wins: " + str(__OUR_AI_WINS))
    # logging.info("Enemy AI wins: " + str(__ENEMY_AI_WINS))
    # logging.info("Draws: "+ str(__DRAWS))

def print_stats(data):
    game_nb = 1
    for data_point in data:
        logging.info("Game n°" + str(game_nb))
        logging.info("Winner: " + str(data_point["winner"]))
        logging.info("Turns played: " + str(data_point["depth"]))
        logging.info("Starting Player: " + str(data_point["starting_player"]))
        logging.info("Enemy AI Level: " + str(data_point["enemy_ai_level"]))
        logging.info("Our mean exec time (ms): " + str(data_point["our_mean_exec_time"]))
        logging.info("Our max exec time (ms): " + str(data_point["our_max_exec_time"]))
        logging.info("Enemy mean exec time (ms): " + str(data_point["enemy_mean_exec_time"]))
        logging.info("")
        game_nb += 1

def play_against_solver(starting_player="our"):
    global __POS_PLAYED
    __POS_PLAYED = ""
    if starting_player == "our": second_player = "enemy"
    else: second_player = "our"
    grid = "000000000000000000000000000000000000000000"
    i = 1
    while True:
        grid = toggle_grid(grid)
        start_time = time()
        if starting_player == "our": grid = player_plays(starting_player, grid)
        else : grid = solver_plays(grid)
        end_time = time()
        exec_duration = end_time - start_time
        i += 1
        add_time(exec_duration, starting_player)
        grid = toggle_grid(grid)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "1")
        logging.debug(has_won)
        if has_won:
            add_stat(starting_player, str(i), starting_player)
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i), starting_player)
            return

        start_time = time()
        if second_player == "our": grid = player_plays(second_player, grid)
        else : grid = solver_plays(grid)
        end_time = time()
        exec_duration = end_time - start_time
        i += 1
        add_time(exec_duration, second_player)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "2")
        logging.debug(has_won)
        if has_won:
            add_stat(second_player, str(i), starting_player)
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i), starting_player)
            return



if __name__ == '__main__':
    main()
