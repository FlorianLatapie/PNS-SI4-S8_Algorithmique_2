import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from min_max_tree_search import play_move
import json

from random_ai import random_ai_play
from utils import convert_string_to_grid

IA_TO_LAUNCH = ''

class RequestProcessingError(Exception):
    def __init__(self, status, detail):
        self.status = status
        self.detail = detail

class AIHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_request = urlparse(self.path)

        path = parsed_request.path
        print(path)
        query = parsed_request.query
        print(query)

        try:
            if path == '/move':
                column = self.do_get_move(query)

                if column is not None:
                    self.send_response(200)
                    self.send_header('Content-Type', "application/json")
                    self.end_headers()

                    self.wfile.write(json.dumps(column).encode())

                else:
                    raise RequestProcessingError(422, 'board is full')

            else:
                # path not found
                self.send_error(404)

        except RequestProcessingError as e:
            self.send_response(e.status)
            self.send_header('Content-Type', "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"detail": e.detail}).encode())

    def do_get_move(self, query):
        try:
            # row oriented board content, starting with the bottom-left corner
            board_string = parse_qs(query)['b'][0]

        except KeyError:
            raise RequestProcessingError(400, 'missing arg: b')

        else:
            global IA_TO_LAUNCH
            board = convert_string_to_grid(board_string)

            if IA_TO_LAUNCH == "random":
                return random_ai_play(board)
            else:
                play_move(board)

def main():
    parser = argparse.ArgumentParser(description="Connect 4 AI API")
    parser.add_argument('--port', '-p', type=int, default=3150)
    parser.add_argument('--level', '-l',
                        choices=['random', 'minmax'],
                         default='minmax'
                         )

    args = parser.parse_args()

    print(args.level)
    global IA_TO_LAUNCH
    IA_TO_LAUNCH = args.level

    # app_logger = LogMgr.setup(args.verbose)

    listening_port = args.port

    # level = args.level
    # app_logger.info("using strategy %s (%s)", strategy.name, strategy.description)

    server = HTTPServer(
        ('', listening_port),
        AIHTTPRequestHandler,
    )

    #app_logger.info('API server listening on port %d...', listening_port)
    try:
        server.serve_forever()

    except KeyboardInterrupt:
        # app_logger.info('interrupted')
        pass


if __name__ == '__main__':
    main()
