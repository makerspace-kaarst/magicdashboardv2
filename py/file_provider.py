from http.server import HTTPServer, BaseHTTPRequestHandler
from os import listdir
import os.path as path


def get_filenames():
    data = []
    for subfolder in ["img","nodes"]:
        target = '../'+subfolder+'/'
        data.append([subfolder+'/'+f for f in listdir(target) if path.isfile(target+ f)])

    # Flatten list of files
    flat_list = []
    for sublist in data:
        for item in sublist:
            flat_list.append(item)
    return flat_list

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global debug_display_timer
        self.path = self.path[1:]
        status = 200
        if self.path == "_internal/index":
            print("Sync system requested file list")
            out = bytes(str(get_filenames()),'utf-8')
        else:
            print("Sync system requested",self.path)
            if self.path == '':
                self.path = 'index.html'
            # Serve file
            try:
                with open("../"+self.path,'rb') as f:
                    out = f.read()
            except FileNotFoundError:
                status = 404
                out = bytes('','utf-8')
        self.send_response(status)
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, format, *args):
        return

def server():
    httpd = HTTPServer(('localhost', 9001), SimpleHTTPRequestHandler)
    httpd.serve_forever()

server()