import json,colorsys

templates = {
    "text":"""<div class="center"><h1 class="headline">[headline]</h1><h3 class="simple-text">[content]</h3></div>""",
    "image":"""<div class="center"><h1 class="headline">[headline]</h1><img src="[file]" alt=""></div>""",
    "bargraph-base":"""<div style="display:flex;height:100%;flex-direction:column"><h1 class="headline">[headline]</h1><div class="box" style="display:flex;align-items:flex-end;justify-content:center">[content]</div></div>""",
    "bargraph-element":"""<div style="background-color:[color];width:30px;height:[value]%;margin-left:5px;margin-right:5px"></div>""",
    "stacked-bargraph-base":"""<div style="display:flex;height:100%;flex-direction:column"><h1 class="headline">[headline]</h1><div class="box" style="display:flex;align-items:flex-end;justify-content:center;align-items:center">[content]</div></div>""",
    "stacked-bargraph-element":"""<div style="background-color:[color];height:50px;flex-grow: [value]"></div>"""
}
def debug_node
def colorgen(cid,divisions):
    return [int(x*255) for x in colorsys.hsv_to_rgb((1/divisions)*cid,0.8,1)]

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(rgb)

def bar_graph(data):
    out = ""
    maxval = 0
    for bar in data["data"]:
        maxval = max(maxval,bar)
    factor = (100/maxval) if data['display_scale'] == 'auto' else data['display_scale']
    for barid,bar in enumerate(data["data"]):
        out += templates[data['node_type']+'-element'].replace("[value]",str(factor*bar)).replace("[color]",rgb_to_hex(colorgen(barid,len(data["data"]))))+"\n"
    return templates[data['node_type']+'-base'].replace("[content]",out).replace("[headline]",data["headline"])

def node_maker(data):
    if not data:  # If file is empty, return RESET file
        return "0\nreset"

    # Defaults to 10, can be customized
    duration = 10
    if 'duration' in data.keys():
        duration = data["duration"]

    if data['node_type'] in ['bargraph','stacked-bargraph']:
        out = bar_graph(data)
    else:
        out = templates[data['node_type']]
        for key in data.keys():
            if key == 'node_type': continue  # ignore this key
            if '['+key+']' not in out:
                continue
            out = out.replace('['+key+']',data[key])
    return str(duration)+'\n'+out

def node_string(data):
    out = []
    for state in data:
        out.append(node_maker(state))
    return '\nEND_OF_HTML_NODE_SECTION\n'.join(out)

# Load files
raw = []
for i in range(6):
    with open(f'nodes/{i}.json','r') as f:
        out = node_string(json.loads(f.read()))

    with open(f'nodes_html/{i}.txt','w') as f2:
        f2.write(out)