import json
import cache
import urllib
import json
from os import remove as _os_remove_file

### --- SETTING POSTS ---

# Download a file from remote host and place it in /uploads
def upload_file(*args):
    if '..' in args[0]['filename']:
        return 'Nope'
    with open('../Frontend/uploads/'+args[0]['filename'],'wb') as f:
        f.write(args[1])
    return 'OK'


# Deletes a file from /uploads
def delete_file(*args):
    filename = args[0]['filename']
    if '..' in filename:  # no directory traversal
        return "Nope"
    try:  # Delet the fiile, bu don't tell the user abput errors, tht would enable destructive enumeration
        _os_remove_file("../Frontend/uploads/"+filename)
        db['force_update'] = True
        return 'OK'
    except FileNotFoundError:
        pass
        return 'File not found'


# Adds a new node to the database
def add_node(*args):
    node_id = int(args[0]['node_id'])
    db = cache.get_raw()
    db['node_html'].insert(node_id,[])
    db['html_index'].insert(node_id,0)
    db['update_timer'].insert(node_id,0)
    db['update_delay'].insert(node_id,2)
    db['force_update'] = True
    return 'OK'

# Removes a node
def delete_node(*args):
    node_id = int(args[0]['node_id'])
    db = cache.get_raw()
    del db['node_html'][node_id]
    del db['html_index'][node_id]
    del db['update_timer'][node_id]
    del db['update_delay'][node_id]
    db['force_update'] = True
    return 'OK'


# Add or remove a state from a node
def manage_node(*args):
    node_id = int(args[0]['node_id'])
    action = args[0]['action']
    db = cache.get_raw()

    # add new state
    if action in ['add','insert','a','i','+']:
        index = int(args[0]['index'])  # state index
        html = urllib.parse.unquote(args[0]['html'])
        db['node_html'][node_id].insert(index,html)
        db['force_update'] = True

    # remove state
    elif action in ['remove','delete','del','r','d','-']:
        index = int(args[0]['index'])  # state index
        del db['node_html'][node_id][index]
        db['force_update'] = True
        db['html_index'][node_id] = 0

    # change update delay [reset timer to prevent overflow]
    elif action in ["speed","delay"]:
        db['update_delay'][node_id] = abs(int(args[0]['delay']))
        db['update_timer'][node_id] = 0

    elif action in ["update","change","replace"]:
        index = int(args[0]['index'])  # state index
        html = urllib.parse.unquote(args[0]['html'])
        db['node_html'][node_id][index] = html
        db['force_update'] = True
    else:
        return "Invalid action"
    return "OK"


def update_grid(*args):
    cache.write(['grid','rows'],int(args[0]['rows']))
    cache.write(['grid','columns'],int(args[0]['columns']))
    return "OK"


# Set force update property
def force_update(*args):
    cache.write(['force_update'],True)
    return "OK"


def test(*args):
    return "You haz found the super secret mega epic POST endpoint... have a flag{wait_this_is_not_a_ctf}\n\n"+str(args[0])


def set_uuid(*args):
    cache.write(['auth_uuid'],args[0]['auth'])


# returns a dump of the Database
def db(*args):
    c = cache.get_raw().copy()
    c['config'] = ['No passwords for you, you don\'t need them anyways, right?']
    return json.dumps(c)


# Change the Board title
def update_title(*args):
    cache.write(['title'],urllib.parse.unquote(args[0]['title']))
    return 'OK'


# Danger zone Endpoints
def update_password(*args):
    temp = cache.read(['config'])
    temp['password'] = args[0]['password']
    cache.write(['config'],temp)
    return 'OK'


def windowtitle(*args):
    return cache.read(['title'])


def get_delay(*args):
    return cache.get_raw()['update_delay'][int(args[0]['node_id'])]
