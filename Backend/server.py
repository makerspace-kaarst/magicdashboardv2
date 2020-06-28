from http.server import HTTPServer, BaseHTTPRequestHandler
import http.server
import get_routes
import post_routes
import traceback
import cache
import urllib
import json
import cache

def dictify(raw_unsave):
    raw = []
    if type(raw_unsave) == list:
        # flatten the list if needed
        for shard in raw_unsave:
            raw.append(shard)
        raw = '&'.join(raw)
    else:
        raw = raw_unsave
    out = {}
    for item in raw.split('&'):
        item = item.split('=')
        if len(item) == 2:
            out[item[0]] = item[1]
    return out


def multidecode(raw):
    try:
        out = json.loads(raw)
    except:
        out = dictify(urllib.parse.unquote(raw))
    return out


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        #self.send_header("Access-Control-Allow-Origin", "*")
        out = bytes('Generic Error/ Not authenticated','utf-16')
        # auto register first UUID
        if not cache.read(['config','secure-gets']):
            pass
        elif not cache.read(['auth_uuid']):
            args = dictify(self.path.split('?')[1:])
            if 'auth' in args.keys():
                cache.write(['auth_uuid'],args['auth'])

        status = 200
        try:  # try to execute a function from get_routes.py that has the same name as the first sub-directory
            if not self.path[1:].split('?')[0].startswith('_'):
                function = getattr(get_routes, self.path[1:].split('?')[0])  # gets function from module
                data = {}
                if len(self.path.split('?')) > 1:  # if there are GET parameters:
                    data = dictify(self.path.split('?')[1:])  # convert GETs to dict
                if not cache.read(['config','secure-gets']) or cache.read(['auth_uuid']) == data['auth']:
                    out = function(data)
                    out = bytes(str(out),'utf-16')  # convert string to returnable format
            else:
                raise AttributeError('cannot call function starting with _')
        except AttributeError:  # No dynamic route found, try loading a static file
            try:
                with open('../Frontend/'+self.path[1:],'rb') as f:  # open the file
                    out = f.read()  # and read the content
            except:  # there is no file?
                status = 404  # set the correct status code
                out = bytes("No dynamic or static route is linked to this path",'utf-16')  # Notify the user
        except Exception as e:  # the loaded function fails:
            status = 500  # set the correct status code
            out = bytes(traceback.format_exc(),'utf-16')  # return the traceback

        self.send_response(status)
        self.end_headers()
        self.wfile.write(out)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
        # Check password and auth Header
        if not (
                (not cache.read(['config'])['secure-api'])
                or self.path == '/http_upload'
                or (self.headers['X-API-Auth'] in
                    [cache.read(['config'])['password'],cache.read(['config'])['master_key']]
                if 'X-API-Auth' in self.headers.keys() else False)):
            self.send_response(500)
            self.end_headers()
            self.wfile.write(bytes('Not Authenticated.','utf-8'))
            return
        status = 200
        body = self.rfile.read(int(self.headers['Content-Length']))
        out = b'OK'
        try:  # try to execute a function from post_routes.py that has the same name as the first sub-directory
            function = getattr(post_routes, self.path[1:])
            try:
                out = function(multidecode(body.decode()))
            except:
                out = function(self.headers,body)

        except Exception as e:  # the loaded function fails:
            status = 500  # set the correct status code
            out = traceback.format_exc()  # return the traceback
            print(out)
        self.send_response(status)
        self.end_headers()
        self.wfile.write(bytes(str(out),'utf-8'))

    def log_message(self, format, *args):
        return


def server():
    httpd = HTTPServer(('', 1337), SimpleHTTPRequestHandler)
    httpd.serve_forever()


# Setup cache structure
cache.hard_set(
    {'node_html': [],  # Node html, can have multiple per node, cycles
     'html_index':[],  # currently displayed node HTML index
     'update_timer': [],  # internal timer, if value hits zero: reset to update_delay
     'update_delay': [],
     'force_update':False,  # If there is only one item, do not update unless this flag is set
     'auth_uuid':'',
     'title':'NodeBoard v0.25',
     'grid':{
         "rows":2,
         "columns":3
     }
     }
)

import os
if os.getcwd() == "/home/pi":
    os.chdir("/home/pi/Schreibtisch/magicdashboard/Backend/")

# Load data from config.json
with open('config.json','r') as f:
    cache.write(['config'],json.loads(f.read()))
# Start server
server()
