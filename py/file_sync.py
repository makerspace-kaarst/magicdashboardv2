import requests,json

def get_string(path,remote_target):
    return requests.get(remote_target+path).text

def download_file(remote,local,remote_target):
    url = remote_target+remote
    response = requests.get(url)
    if response.status_code == 200:
        with open("../"+local,'wb') as f:
            f.write(response.content)

def sync(provider="127.0.0.1:9001"):
    provider = "http://"+provider+'/'
    for file in json.loads(get_string('_internal/index',provider).replace("'","\"")):
        download_file(file,file,provider)
