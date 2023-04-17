import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

from cp4_ai.log import LogMgr
from cp4_ai.strategy import AbstractStrategy, DumbStrategy, BasicStrategy, MediumStrategy, AdvancedStrategy
from cp4_ai.models import Board

COLUMNS_COUNT = 7
ROWS_COUNT = 6


class RequestProcessingError(Exception):
    def __init__(self, status, detail):
        self.status = status
        self.detail = detail


class AIHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_request = urlparse(self.path)

        path = parsed_request.path
        query = parsed_request.query

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
            board = Board.from_string(board_string)
            server: 'AIHTTPServer' = self.server
            return server.strategy.get_move(board)


class AIHTTPServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        self.strategy: AbstractStrategy = kwargs.pop('strategy')
        super().__init__(*args, **kwargs)


STRATEGIES = {
    'dumb': (DumbStrategy, None),
    'basic': BasicStrategy,
    'medium': MediumStrategy,
    'advanced': AdvancedStrategy
}
# add shortened version of strategy names
_strategy_keys = list(STRATEGIES.keys())[:]
for k in _strategy_keys:
    STRATEGIES[k[0]] = STRATEGIES[k]


def main():
    parser = argparse.ArgumentParser(description="CyberP4 MinMax based AI")
    parser.add_argument('--port', '-p', type=int, default=3150)
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--level', '-l',
                        choices=['dumb', 'd', 'basic', 'b', 'medium', 'm', 'advanced', 'a'],
                        default='advanced'
                        )

    args = parser.parse_args()

    app_logger = LogMgr.setup(args.verbose)

    listening_port = args.port

    level = args.level
    strategy = STRATEGIES[level]()
    app_logger.info("using strategy %s (%s)", strategy.name, strategy.description)

    server = AIHTTPServer(
        ('', listening_port),
        AIHTTPRequestHandler,
        strategy=strategy
    )

    app_logger.info('API server listening on port %d...', listening_port)
    try:
        server.serve_forever()

    except KeyboardInterrupt:
        app_logger.info('interrupted')


if __name__ == '__main__':
    main()
