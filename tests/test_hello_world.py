import json, os, sys, threading, unittest, urllib.error, urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import hello_world


class HelloWorldTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = hello_world.make_server(0)          
        cls.port = cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=2) as r:
            return r.status, r.headers, json.loads(r.read())

    def test_root_reports_version(self):
        status, headers, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertEqual(body["version"], hello_world.VERSION)
        self.assertEqual(headers["X-App-Version"], hello_world.VERSION)

    def test_version(self):
        self.assertEqual(set(self.get("/version")[2]), {"app", "version", "git_sha"})

    def test_health(self):
        self.assertEqual(self.get("/health")[2], {"status": "ok"})

    def test_404(self):
        with self.assertRaises(urllib.error.HTTPError) as e:
            self.get("/nope")
        self.assertEqual(e.exception.code, 404)