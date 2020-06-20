import requests
import urllib

IP = 'http://127.0.0.1'
PORT = 1337
PASSWORD='ChangeMe'


# Upload a file to the NodeBoard Server
def upload_file(filename):
    return requests.post(IP+':'+str(PORT)+'/upload_file',data=open(filename, 'rb'), headers={'filename': filename, 'X-API-Auth': PASSWORD}).text


# Delete a file from the NodeBoard Server
def delete_file(filename):
    return requests.post(IP+':'+str(PORT)+'/delete_file', headers={'filename': filename, 'X-API-Auth': PASSWORD}).text


# Add a node
def add_node(node_id):
    return requests.post(IP+':'+str(PORT)+'/add_node', headers={'X-API-Auth': PASSWORD}, data={
        'node_id': node_id
    }).text


# Delete a node
def delete_node(node_id):
    return requests.post(IP+':'+str(PORT)+'/delete_node', headers={'X-API-Auth': PASSWORD}, data={
        'node_id': node_id
    }).text


# Delete a node
def update_grid(rows,columns):
    return requests.post(IP+':'+str(PORT)+'/update_grid', headers={'X-API-Auth': PASSWORD}, data={
        'rows': rows,
        'columns': columns
    }).text

# --- All things that can be done with /manage_node ---


# Add a new state/slide to a node
def add_html(node_id, html, index=99999):
    html = urllib.parse.quote(html)
    return requests.post(IP+':'+str(PORT)+'/manage_node', headers={'X-API-Auth': PASSWORD}, data={
        'node_id': node_id,
        'action': 'add',
        'index': index,
        'html': html
    }).text


# Removes a slide/stae from a node
def remove_html(node_id, index):
    return requests.post(IP+':'+str(PORT)+'/manage_node', headers={'X-API-Auth': PASSWORD}, data={
        'node_id': node_id,
        'action': 'remove',
        'index': index
    }).text


# Change state display time/ refresh-delay
def set_delay(node_id, delay):
    return requests.post(IP+':'+str(PORT)+'/manage_node', headers={'X-API-Auth': PASSWORD}, data={
        'node_id': node_id,
        'action': 'delay',
        'delay': delay
    }).text


# Change state display time/ refresh-delay
def update_html(node_id, index, html):
    html = urllib.parse.quote(html)
    return requests.post(IP+':'+str(PORT)+'/manage_node', headers={'X-API-Auth': PASSWORD}, data={
        'node_id': node_id,
        'action': 'update',
        'index': index,
        'html': html
    }).text

# Change state display time/ refresh-delay
def dump_db():
    return requests.post(IP+':'+str(PORT)+'/db', headers={'X-API-Auth': PASSWORD}).text


# Set the current authentication UUID, blank allows the first connection to authenticate
def overwrite_uuid(uuid):
    return requests.post(IP+':'+str(PORT)+'/set_uuid', headers={'X-API-Auth': PASSWORD}, data={
        'auth':uuid
    }).text


# Change the Board title
def update_title(title):
    return requests.post(IP+':'+str(PORT)+'/update_title', headers={'X-API-Auth': PASSWORD}, data={
        'title':urllib.parse.quote(title)
    }).text


def update_password(password):
    global PASSWORD
    PASSWORD = password
    return requests.post(IP+':'+str(PORT)+'/update_password', headers={'X-API-Auth': PASSWORD}, data={
        'password':password
    }).text


def master_key_password_reset(master_key,password):
    global PASSWORD
    PASSWORD = password
    return requests.post(IP+':'+str(PORT)+'/update_password', headers={'X-API-Auth': master_key}, data={
        'password':password
    }).text


def unsave_console():
    print('API functions can be used without module name, you are authenticated with the data enered by whatever dropped you here.\n\n')
    while True:
        cmd = input('>>> ')
        try:
            print(eval(cmd,globals()))
        except SyntaxError:
            exec(cmd,globals())

# --- IF MAIN: Shows all features of the API in order, animated and commented
if __name__ == '__main__':
    import time
    print("changing the title")
    update_title('NodeBoard API features')
    time.sleep(2)
    # Add node
    print("adding a new blank node")
    add_node(0)
    time.sleep(3)

    print('updating the display grid to 2x2')
    # Update the grid to [X*Y]
    update_grid(2,2)

    # Add new node
    print("Adding a second node")
    add_node(0)

    time.sleep(3)

    # Add nw state to a node
    print("Adding some content")
    add_html(0,'<h1>API first</h1><p>Thats how we roll</p>')

    time.sleep(5)  # else you would not see a thing

    # Remove state
    print("removing the content again")
    remove_html(0,0)

    time.sleep(5)  # else you would not see a thing

    # Add 3 states for later
    print("You can have multiple conten slides cyceling")
    add_html(0,'<h1>1</h1><p>Slide 1</p>')
    add_html(0,'<h1>2</h1><p>Slide 2</p>')
    add_html(0,'<h1>3</h1><p>Slide 3</p>')

    time.sleep(7)  # else you would not see a thing

    print("you can change the update delay")
    set_delay(0,3)

    time.sleep(12)  # else you would not see a thing

    print("you can edit any content state")
    update_html(0,1,'<h1>UPDATE:</h1><p>This slide has been replaced</p>')

    time.sleep(12)
    print("you can delete nodes")
    # Remove Node
    delete_node(0)
    time.sleep(1)
    print("you can also upload files, change the password, deregister the current UUID and more.")
    print("\n\nhave a nice shell:\n")
    unsave_console()
