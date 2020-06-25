# Server routes
This document list all supported routes exposed by the NodeBoard Webserver


# GET endpoints 
## Read-only
Routes that can be read without changing states or data

* /db returns a JSON dump of the server database.
* /grid_settings returns current colums,rows,node amount and the node template
[in order to save on request volume, the template is static and can be ignored].
* /windowtitle returns the current board title

## Reads with effect
Some routes return data and change an intrernal state
* /newContentAvailable returns an array of booleans, one for each node. true means that the
update timer has reached zero and has been reset. on true the next state should be read.
* /node_html takes `node_id` and returns html for the next node state, advances and internal
counter. if that counter reaches the end of the list it gets reset to 0.

# POST endpoints
These routes act as API endpoints, only returning OK or a traceback on error.
* /sync_file uses a custom 'filename' header, and saves the request data into /uploads/[header]
* /delete_file takes a `filename` and deletes it from /uploads.
* /add_node takes a `node_id` parameter and inserts a new node at that position.
* /delete_node takes a `node_id` parameter and deletes the specified node.
* /update_grid takes `row` and `coulums` and changes the grid display based on those values.
* /foce_update needs no arguments and sets the 'force update' flag so that all nodes are updated,
ignoring the timer system for the next tick. the flag gets reset automatically.
* /db same as the GET version, for the API
* /set_uuid takes a `auth` parameter with eather a UUID of the target or a blank string, 
	blank means anyone can connect
* /update_title changes the current page title to `title`
* /update_password uses the `password` argument to updates the API password to the new one.

	### Editing node data
	/manage_node takes `node_id`,`action` and command specific parameters. This endpoint is used to
	change any node value, add or remove states and more. Commands are aliased to some common
	replacements, to ensure functionality only use the official names.
	
	|action|[unique] parameters|description|
	|---|---|---|
	|add|`index` `html`|Inserts a new state into a node.
	|remove|`index`| removes a referenced state [counter gets reset to prevent overflow]
	|delay|`delay`|change the amount of seconds a state is shown, uses abs(delay)
	|update|`index` `html`| replaces the referenced html with the provided new data.
	
# Security
>**Please note that this service runns on unencypted http, the password is visible in plaintext.
This mode is supposed to stop 'the general public' and incompetent script kiddies from
changing stuff, not protect you from the NSA (or anyone with wireshark)**

### GET
if `secure-gets` is set to true all GET reuquests have to have an `auth` parameter set to the currently active UUID, this means 'in theory' only one webpage instance at a time is allowed
to connect

### POST

If `secure-api` is set in the config any POST reuqest without the X-API-Auth header set to the
paswords will we dropped
