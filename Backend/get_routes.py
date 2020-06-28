import json
import cache
import traceback

### --- SAVE GETS --- [The only ones you SHOULD have]

# returns amount of nodes and grid settings
# Rows|Columns|Node amount
def grid_settings(*args):
    try:
        node_template = """<div class="node"><div class="node-content"></div><div class="node-content hidden"></div></div>""".replace('"','\'')
        return "["+str(cache.read(['grid','rows']))+","+str(cache.read(['grid','columns']))+","+str(len(cache.read(['update_delay'])))+",\""+node_template+"\"]"
    except Exception as e:
        print(traceback.format_exc())

### --- UNSAVE GETS --- [The ones you SHOULD NOT have]

# Checks for update timers to hit 0  and returns booleans
# for every node, describing their need for an update
def newContentAvailable(*args):
    # for faster access, get the DB object
    db = cache.get_raw()
    out = []
    for nid,node in enumerate(db['update_timer']):
        out.append(node <= 0 and len(db['node_html'][nid]) > 1 or db['force_update'])
        if node <= 0:
            db['update_timer'][nid] = db['update_delay'][nid]-1
        else:
            db['update_timer'][nid] -= 1
    db['force_update'] = False
    return json.dumps(out)


# Reurns the current HTMl for a node, loops
def node_html(*args,**kwargs):
    # extract node_id from GET params
    node_id = int(args[0]['node_id'])
    # for faster access, get the DB object
    db = cache.get_raw()
    try:
        # fetch the current html data based on the html index of the node
        out = db['node_html'][node_id][db['html_index'][node_id]]
        # update the html_index and roll over
        db['html_index'][node_id] += 1
        db['html_index'][node_id] %= len(db['node_html'][node_id])
    except IndexError:
        out = ""
    return out


# Set force update property
def force_update(*args):
    cache.write(['force_update'],True)
    return "OK"


def windowtitle(*args):
    return cache.read(['title'])

def test(*args):
    return "You haz found the super secret mega epic GET endpoint... have a flag{wait_this_still_is_not_a_ctf_now_i_am_sad}\n\n"+str(args[0])

def test_upload(*args):
    print(args)
