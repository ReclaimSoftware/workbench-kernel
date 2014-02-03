import argparse
import BaseHTTPServer, json
from context import Context

context = Context()

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):

        if self.path == '/api/reset':
            context.reset()
            self.respond_json(200, {})

        elif self.path == '/api/execute':
            inputs = json.loads(self.read_request_body())['inputs']
            self.respond_json(200, {
                'execution_results': [context.run_code(code) for code in inputs]
            })

    def read_request_body(self):
        length_header = self.headers.getheader('content-length')
        if length_header is None:
            self.respond_error("Content-Length header required")
            return
        length = int(length_header)
        return self.rfile.read(length)

    def respond_json(self, code, info):
        data = json.dumps(info, sort_keys=True, indent=2, separators=(',', ': '))
        self.respond(code, data, 'application/json')

    def respond_error(self, message):
        self.respond(500, str(message), 'text/plain')

    def respond(self, code, data, mime):
        self.send_response(code)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    listen_on = ('127.0.0.1', args.port)
    server = BaseHTTPServer.HTTPServer(listen_on, Handler)
    print "Listening on %d..." % args.port
    while True:
        server.handle_request()


if __name__ == '__main__':
  main()
