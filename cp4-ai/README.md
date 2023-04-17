# Strategy computation service

## Overview

This service uses a MinMax algorithm to find the best play for next machine
turn. 

The search time is optimized by pruning subtrees using the alpha-beta method.

Sources : 
- https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f
- https://www.researchgate.net/publication/331552609_Research_on_Different_Heuristics_for_Minimax_Algorithm_Insight_from_Connect-4_Game

The service exposes a REST API made of a single request : `GET /move?b=<board-configuration>`

The board configuration is represented by a string which each character represent the content
of a board cell, encoded as :

- `0` : empty
- `1` : player
- `2` : machine

`p` and `h` can be used as aliases for 1. `a` and `m` can be uses as aliases for `2`. 
The board is scanned row by row, starting from the bottom-left corner.

The response contains the number of the column to be played, in the `[1, 7]` range.

## Development

Have a look at the Makefile targets for the project build and deployment tasks

## Dependencies

- Python 3.9.2
- packages : see `requirements.txt` file
