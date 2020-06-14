from http.server import HTTPServer, BaseHTTPRequestHandler
DEBUG = False
if DEBUG:
    # Get the current IP for connection
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    print(ip_addr)
    s.close()
    ip_addr = "192.168.0.72"  # DEBUG ONLY

page_title = "Magic Mirror"

node_html = [[],[],[],[],[],[]]
nodes_states = [0,0,0,0,0,0]


def fetch_node_states():
    global node_html,nodes_states
    nodes_states = [0,0,0,0,0,0]
    for i in range(6):
        with open('nodes_html/'+str(i)+'.txt','r') as f:
            node_html[i] = [x.strip() for x in f.read().split("END_OF_HTML_NODE_SECTION") if x.strip()]


def node_data(node_id):
    global nodes_states
    if len(node_html[node_id]) != 0:
        state = nodes_states[node_id]
        state += 1
        state %= len(node_html[node_id])
        nodes_states[node_id] = state
        return bytes(node_html[node_id][state],'utf-8')
    else:
        return bytes('reset','utf-8')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.path = self.path[1:]
        status = 200
        # Node status
        if self.path.startswith('nodes/'):
            out = node_data(int(self.path[-1]))

        elif self.path == 'reload':
            fetch_node_states()
            out = bytes('OK','utf-8')
        elif self.path == 'topbar':
            out = bytes(page_title+'\n'+(ip_addr if DEBUG else 'clock'),'utf-8')
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

fetch_node_states()
server()
