from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import json
import get
import post
import traceback

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


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        out = bytes('Generic Error/ Not authenticated','utf-16')

        status = 200
        try:  # try to execute a function from get_routes.py that has the same name as the first sub-directory
            if not self.path[1:].split('?')[0].startswith('_'):
                function = getattr(get, self.path[1:].split('?')[0])  # gets function from module
                data = {}
                if len(self.path.split('?')) > 1:  # if there are GET parameters:
                    data = dictify(self.path.split('?')[1:])  # convert GETs to dict
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

    def do_POST(self):
        # Check password and auth Header
        if not (
                (not config['secure-api'])
                or (self.headers['X-API-Auth'] in
                    [config['password'],config['master_key']]
        if 'X-API-Auth' in self.headers.keys() else False)):
            self.send_response(500)
            self.end_headers()
            self.wfile.write(bytes('Not Authenticated.','utf-8'))
            return
        status = 200
        body = self.rfile.read(int(self.headers['Content-Length']))
        out = b'OK'
        try:  # try to execute a function from post_routes.py that has the same name as the first sub-directory
            function = getattr(post, self.path[1:])
            try:
                out = function(dictify(urllib.parse.unquote(body.decode())))
            except:
                out = function(self.headers,body)

        except Exception as e:  # the loaded function fails:
            status = 500  # set the correct status code
            out = traceback.format_exc()  # return the traceback
        self.send_response(status)
        self.end_headers()
        self.wfile.write(bytes(out,'utf-8'))

    def log_message(self, format, *args):
        return


def server():
    httpd = HTTPServer(('', 9001), SimpleHTTPRequestHandler)
    httpd.serve_forever()


config = json.loads("""{
  "secure-api":true,
  "password":"ChangeMe",
  "secure-gets":true,
  "master_key":"HardcodedPasswordsAreVeryCashMoneyForAnyAttacker"
}""")
# Start server
server()
