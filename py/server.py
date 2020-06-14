from http.server import HTTPServer, BaseHTTPRequestHandler
import html_generator
import file_sync
import requests

page_title = "Magic Mirror"

node_html = [[],[],[],[],[],[]]
nodes_states = [0,0,0,0,0,0]

# Debug/Connection data node generator and utils
current_ip = ""
debug_display_timer = 4
def get_ip():
    global current_ip
    if current_ip:
        return current_ip
    return "192.168.0.72"  #DEBUG!!
    # Get the current IP for connection
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    current_ip = s.getsockname()[0]
    s.close()
    return current_ip

def debug_node():
    return f"""5
            <h1 class="headline">Debug info:</h1>
            <h1 style="color:#fff;text-align:center">IP: <span style="color:#c54848">{get_ip()}</span></h1>
            <h1 style="color:#fff;text-align:center">Port: <span style="color:#c54848">1337</span></h1>"""

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
        return bytes('1\nreset','utf-8')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global debug_display_timer
        self.path = self.path[1:]
        status = 200
        # Node status
        if self.path.startswith('nodes/'):
            if debug_display_timer > 0 and int(self.path[-1]) == 5:
                out = bytes(debug_node(),'utf-8')
                debug_display_timer -= 1
            else:
                out = node_data(int(self.path[-1]))

        elif self.path == 'topbar':
            out = bytes(page_title+'\nclock','utf-8')

        elif self.path.startswith('sync/'):
            out = bytes('OK','utf-8')
            try:
                file_sync.sync(self.path.split('/')[-1])
                html_generator.reload_all()
                fetch_node_states()
            except requests.exceptions.InvalidURL:
                out =  bytes('Invalid hostname, you have to use a valid IP and PORT: /sync/127.0.0.1:9001 [Invalid Hostname]','utf-8')
            except requests.exceptions.ConnectionError:
                out =  bytes('Invalid hostname, you have to use a valid IP and PORT: /sync/127.0.0.1:9001 [Invalid PORT / Maximum retries]','utf-8')
        elif self.path == 'debug':
            out = bytes('OK','utf-8')
            debug_display_timer += 1

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

html_generator.reload_all()
fetch_node_states()
server()
