import json, logging, os, signal, sys, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

APP_NAME = "hello-world"
VERSION = os.environ.get("APP_VERSION", "0.0.0")   
GIT_SHA = os.environ.get("GIT_SHA", "unknown")

logging.basicConfig(level="INFO", stream=sys.stdout)
log = logging.getLogger(APP_NAME)


def version_info():
    return {"app": APP_NAME, "version": VERSION, "git_sha": GIT_SHA}


class Handler(BaseHTTPRequestHandler):
    server_version = APP_NAME
    sys_version = ""                       

    def _send(self, status, body):
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-App-Version", VERSION)
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            self._send(200, {"message": "Hello, World!", **version_info()})
        elif path == "/version":
            self._send(200, version_info())
        elif path == "/health":
            self._send(200, {"status": "ok"})
        else:
            self._send(404, {"error": "not found"})


def make_server(port):
    return ThreadingHTTPServer(("0.0.0.0", port), Handler)


def main():
    if "--version" in sys.argv:
        print(VERSION)
        return
    server = make_server(int(os.environ.get("PORT", "8080")))

    def stop(signum, _):
        log.info("signal %s, shutting down", signum)
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    log.info("%s %s listening on :%s", APP_NAME, VERSION, server.server_address[1])
    server.serve_forever()


if __name__ == "__main__":
    main()