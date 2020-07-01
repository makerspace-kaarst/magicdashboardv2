String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.split(search)
        .join(replacement);
};

var CONTEXT = {}
var CONTEXT_META = [0, 0]

var SIDEBAR_NODE = `<div class="node link" onclick="hub_builder([node_id])">
  <h1 class="mono nodeval">node_id: <span class="value">[node_id]</span></h1>
  <h1 class="mono nodeval">slides: <span class="value">[slides]</span></h1>
</div>
`

var NODE_HUB_GRID_NODE = `<div class="node lightgrey-bg mono hidden-flex" style="min-height:14rem">
<div class="force-fill link" onclick="edit_slide([node_id],[slide_id])">
<h1>Slide slide_id: <span class="value">[slide_id]</span></h1>
  </div>
  <button type="button" name="button" class="minusbutton" style="width:100%;margin-top:auto;" onclick="delete_slide([node_id],[slide_id])">-</button>
</div>
`

var NODE_HUB_ADD_NODE = `<div class="plusbutton node lightgrey-bg mono flex" style="min-height:14rem" onclick="add_slide([node_id])">
  <span>+</span>
</div>`

function updateContext() {
    APIRequest('/db', {}, function (source) {
        source = JSON.parse(source);
        CONTEXT = source;
        document.getElementById('sidebar-content')
            .innerHTML = update_sidebar(source['node_html'])
    });
    APIRequest('/windowtitle', {}, function (title) {
        document.getElementById('page-title')
            .innerText = title;
    })
}

function update_sidebar(node_html) {
    let out = "";
    for (var i = 0; i < node_html.length; i++) {
        out += SIDEBAR_NODE.replace('[slides]', node_html[i].length)
            .replaceAll('[node_id]', '' + i) + '\n';
    }
    return out;
}

function hub_builder(node_id) {

    APIRequest('/get_delay', {
        'node_id': node_id
    }, function (delay) {
        document.getElementById('slide-timer')
            .value = parseInt(delay);
    });

    document.getElementById('delete-node')
        .onclick = function () {
        let tmp = document.getElementById('node-hub-node-id')
            .innerText.split(' ')
        delete_node(tmp[tmp.length - 1]);
    }
    try {
        document.getElementById('node-hub')
            .classList.remove("hidden")
    } catch (e) {
    }
    let slides = CONTEXT['node_html'][node_id];
    document.getElementById('node-hub-node-id')
        .innerText = 'node_id: ' + node_id;
    document.getElementById('node-hub-slides')
        .innerText = 'slides: ' + slides.length;

    let grid_content = ""
    for (var i = 0; i < slides.length; i++) {
        grid_content += NODE_HUB_GRID_NODE.replace('[type]', categorize_html(slides[i]))
            .replaceAll('[slide_id]', '' + i)
            .replaceAll('[node_id]', '' + node_id);
    }
    grid_content += NODE_HUB_ADD_NODE.replace('[node_id]', '' + node_id);
    document.getElementById('node-hub-grid')
        .innerHTML = grid_content;
}

function categorize_html(html) {
    out = "raw"
    return out;
}

function add_slide(node_id) {
    APIRequest("/manage_node", {
        'node_id': node_id,
        'action': 'add',
        'index': 99999,
        'html': ""
    }, function () {
        updateContext();
        setTimeout(function (node_id) {
            hub_builder(node_id);
        }, 30, node_id);
    })
}

function edit_slide(node_id, slide_id) {
    CONTEXT_META = [node_id, slide_id]
    document.getElementById('slide')
        .classList.remove('hidden');
    document.getElementById('node-hub')
        .classList.add("hidden")
    let current_code = CONTEXT['node_html'][node_id][slide_id];
    document.getElementById('node-content-raw')
        .innerText = current_code;
}

function delete_slide(node_id, slide_id) {
    APIRequest("/manage_node", {
        'node_id': node_id,
        'action': 'remove',
        'index': slide_id,
    }, function () {
        updateContext();
        setTimeout(function (node_id) {
            hub_builder(node_id);
        }, 30, node_id);
    })
}

function add_node() {
    APIRequest("/add_node", {
        'node_id': 99
    }, updateContext)
}

function delete_node(node_id) {
    APIRequest("/delete_node", {
        'node_id': node_id
    }, updateContext)
    if (node_id != 0) {
        hub_builder(node_id - 1);
    } else {
        document.getElementById('node-hub')
            .classList.add("hidden")
    }
}

function save_slide_data() {
    APIRequest('/manage_node', {
        'node_id': CONTEXT_META[0],
        'action': 'update',
        'index': CONTEXT_META[1],
        'html': document.getElementById('node-content-raw')
            .innerText
    }, updateContext);
}

function update_title(text) {
    APIRequest('/update_title', {
        'title': text
    }, sinkhole);
}

function save_slide_time() {
    APIRequest('/manage_node', {
        'node_id': CONTEXT_META[0],
        'action': 'delay',
        'index': CONTEXT_META[1],
        'delay': parseInt(document.getElementById('slide-timer')
            .value)
    }, updateContext);
}
