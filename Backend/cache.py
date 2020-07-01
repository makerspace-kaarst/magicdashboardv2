_DB = {}  # Cache data store, clobal


# get data form _db
def read(item_location):
    global _DB
    out = _DB
    for layer in item_location:
        out = out[layer]
    return out


# write to _DB
def write(item_location, value):
    global _DB
    out = _DB
    for layer in item_location[:-1]:
        out = out[layer]
    out[item_location[-1]] = value


# delete item from _DB
def delete(item_location):
    global _DB
    out = _DB
    for layer in item_location[:-1]:
        out = out[layer]
    del out[item_location[-1]]


def hard_set(db):  # Set _DB to dict, use for init
    global _DB
    _DB = db


def get_raw():
    global _DB
    return _DB
