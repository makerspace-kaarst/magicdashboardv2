from http.server import HTTPServer, BaseHTTPRequestHandler
node_html = ["","","","","",""]
nodes_valid = [False,False,False,False,False,False]

def node_data(node_id):
    global nodes_valid
    out = ""
    if not nodes_valid[node_id]:
        out = node_html[node_id]
    nodes_valid[node_id] = True
    return bytes(out,'utf-8')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.path = self.path[1:]
        status = 200
        # Node status
        if self.path.startswith('nodes/'):
            out = node_data(int(self.path[-1]))
        else:
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
    httpd = HTTPServer(('localhost', 1337), SimpleHTTPRequestHandler)
    httpd.serve_forever()

server()