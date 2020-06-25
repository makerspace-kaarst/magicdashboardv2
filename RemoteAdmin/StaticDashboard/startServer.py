import os,sys
port = 9001
try:
    os.system('python -m http.server '+str(port))
    sys.exit(0)
except:
    os.system('python -m SimpleHTTPServer '+str(port))
    sys.exit(0)
