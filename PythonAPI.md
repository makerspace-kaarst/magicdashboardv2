# Python API
All features of the NodeBoard can be ccontrolled over http, or by the HTTP API that abstracts these calls away.

# Functions
|name|arguments|description
|---|---|---
upload_file|`filename`|uploads a file from the current working directory to the /uploads directory
delete_file|`filename`|deletes a file from /uploads
add_node|`node_id`| adds a new node anywhere into the stack
get_delay|`node_id`| returns node update delay in seconds
delete_node|`node_id`|delete any node
update_grid|`rows` `columns`|change the base grid size
add_html|`node_id` `html`|append a new state to any node use `index` to insert the state at any location, defaults to the end of the cycle
remove_html|`node_id` `index`| delete any state
update_html|`node_id` `index` `html`|change node state content
set_delay|`node_id` `delay`| how many seconds a node should display it's content before loading the next item
dump_db| |returns json representation of the current server state
overwrite_uuid|`uuid`|takes a uuid and replaces the currently authenticated one. leaving it blank allows anyone to connect.
update_title|`title`|change the board title
master_key_password_reset|`master_key` `password`|update the API password using the secret `master_key` defined in the server config. Updates the global PASSWORD variable.

# Setup
in order to connect to your board you have to change the constants **IP**, **PORT** and **PASSWORD**
to match your board endpoint

# Security
if you activate 'secure-api' on your server and set a password, any POST request without
the 'X-API-Auth' header set to the password will be ignored.

>**Please note that this service runns on unencypted http, the password is visible in plaintext.
This mode is supposed to stop 'the general public' and incompetent script kiddies from
changing stuff, not protect you from the NSA (or anyone with wireshark)**
