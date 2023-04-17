import requests
import utils
import argparse
import math

__PLAYER1_URL = ""
__PLAYER2_URL = ""
__POS_PLAYED = ""

__GAMES_TO_PLAY = 1
__GAMES_PLAYED = 0
__PLAYER1_WINS = 0
__PLAYER2_WINS = 0
__DRAWS = 0
__DEPTHS = [] 


def toggle_grid(grid: str):
    return grid.replace("1", "a").replace("2", "1").replace("a", "2")

def add_stat(winner: str, depth: str):
    global __PLAYER1_WINS
    global __PLAYER2_WINS
    global __DEPTHS
    global __GAMES_PLAYED
    global __DRAWS
    __GAMES_PLAYED += 1
    print("winner", winner)
    if winner == "1":
        __PLAYER1_WINS += 1
    if winner == "2":
        __PLAYER2_WINS += 1
    if winner == "draw":
        __DRAWS +=1
    __DEPTHS.append(depth)

def player_plays(player_num: int, grid: str) -> str:
    global __POS_PLAYED
    url = __PLAYER1_URL
    if player_num == 2: url = __PLAYER2_URL
    url += "/move?b=" + grid
    res = requests.get(url)
    if res.status_code == 200:
        move = res.json()
        __POS_PLAYED += str(move)
        move_to_0_index = move - 1
        print("Player ", player_num, " played", move_to_0_index)
        updated_grid = utils.add_move_to_grid(grid, move_to_0_index, str(2))
        return updated_grid
    else:
        raise Exception("Error: ",
                        "player ",
                        player_num,
                        "responded with: ",
                        res.status_code,
                        " ",
                        res.json()
                        )
def solver_plays(player_num: int, grid:str):
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
            if scores[i] > best_move_score:
                best_move_score = scores[i]
                best_move = i +1
    __POS_PLAYED += str(best_move)
    move_to_0_index = best_move - 1
    print("Solver played", move_to_0_index)
    updated_grid = utils.add_move_to_grid(grid, move_to_0_index, str(2))
    return updated_grid


def play_game():
    grid = "000000000000000000000000000000000000000000"
    i = 1
    while True:
        grid = toggle_grid(grid)
        grid = player_plays(1, grid)
        grid = toggle_grid(grid)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "1")
        print(has_won)
        if has_won:
            add_stat("1", str(i))
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i))
            return

        i += 1
        grid = player_plays(2, grid)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "2")
        print(has_won)
        if has_won:
            add_stat("2", str(i))
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i))
            return


def main():
    parser = argparse.ArgumentParser(description="CONNECT 4 Arena")
    parser.add_argument('--player1')
    parser.add_argument('--player2')
    args = parser.parse_args()
    global __PLAYER1_URL
    global __PLAYER2_URL
    __PLAYER1_URL = "http://" + args.player1
    __PLAYER2_URL = "http://" + args.player2
    if __PLAYER1_URL == "" or __PLAYER2_URL == "":
        print("enter player1 and player2 args (the url of the connect 4 servers)")
        return
    global __GAMES_PLAYED
    global __GAMES_TO_PLAY
    global __PLAYER1_WINS
    global __PLAYER2_WINS
    global __DEPTHS
    global __DRAWS
    
    while(__GAMES_PLAYED < __GAMES_TO_PLAY):
        play_game()
        # play_against_solver()

        print(__GAMES_PLAYED)

    print("Games played: ", __GAMES_PLAYED)
    print("Player 1 wins: ", __PLAYER1_WINS)
    print("Player 2 wins: ", __PLAYER2_WINS)
    print("Draws: ", __DRAWS)


def play_against_solver():
    grid = "000000000000000000000000000000000000000000"
    i = 1
    while True:
        grid = toggle_grid(grid)
        grid = player_plays(1, grid)
        grid = toggle_grid(grid)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "1")
        print(has_won)
        if has_won:
            add_stat("1", str(i))
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i))
            return

        i += 1
        grid = solver_plays(2, grid)
        utils.print_grid(grid)
        has_won = utils.has_player_won(grid, "2")
        print(has_won)
        if has_won:
            add_stat("2", str(i))
            return
        is_over = utils.is_game_over(grid)
        if is_over: 
            add_stat("draw", str(i))
            return



if __name__ == '__main__':
    main()
