import requests
import utils
import argparse

__PLAYER1_URL = ""
__PLAYER2_URL = ""


def toggle_grid(grid: str):
    return grid.replace("1", "a").replace("2", "1").replace("a", "2")

def player_plays(player_num: int, grid: str) -> str:
    url = __PLAYER1_URL
    if player_num == 2: url = __PLAYER2_URL
    url += "/move?b=" + grid
    res = requests.get(url)
    print("responded", res)
    if res.status_code == 200:
        move = res.json()  # TODO: check move field
        move_to_0_index = move - 1
        updated_grid = utils.add_move_to_grid(grid, move_to_0_index, str(player_num))
        print("Player ", player_num, " played", move)
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


def main():
    parser = argparse.ArgumentParser(description="CONNECT 4 Arena")
    parser.add_argument('--player1')
    parser.add_argument('--player2')
    args = parser.parse_args()
    global __PLAYER1_URL
    global __PLAYER2_URL
    __PLAYER1_URL = "http://" + args.player1
    __PLAYER2_URL = "http://" + args.player2
    grid = "000000000000000000000000000000000000000000"
    if __PLAYER1_URL == "" or __PLAYER2_URL == "":
        print("enter player1 and player2 args (the url of the connect 4 servers)")
        return
    i = 0
    while True:
        grid = toggle_grid(grid)
        grid = player_plays(2, grid)
        is_over = utils.is_game_over(grid)
        if is_over: return

        grid = toggle_grid(grid)
        grid = player_plays(2, grid)
        is_over = utils.is_game_over(grid)
        if is_over: return

        i += 1


if __name__ == '__main__':
    main()
