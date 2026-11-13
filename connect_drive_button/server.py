from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
ThreadingHTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler).serve_forever()
