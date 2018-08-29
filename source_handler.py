SOURCE_FILE = 'sources.txt'
BL_PRFX = 'b_'
WL_PRFX = 'w_'
_ID_SPRTR = '::'

# TODO: use more efficient ID system. Current system is very eh...
# TODO: make this so much more efficient than the way this just passes around a dict...
# TODO: use pickle??

# Reads blacklist and whitelist entries from file and simply returns them. Nothing more
def read_sources_file():
	srcs = dict()
	f = open(SOURCE_FILE, 'r')
	for line in f.read().split('\n'):
		if not line or line == '\n': continue
		src = line.split(_ID_SPRTR)
		srcs[src[0]] = src[1]
	f.close()
	return srcs

# Writes edited changes to file
def write_sources_to_file(src_dict):
	f = open(SOURCE_FILE, 'w')
	for id in src_dict:
		url = src_dict[id]
		entry = id + _ID_SPRTR + url
		f.write(entry + '\n')
	f.close()

def edit_source(src_dict, url_id, new_url):
	if url_id in src_dict:
		src_dict[url_id] = new_url
	raise ValueError('Supplied url could not be found in either  blacklist or whitelist!')

def add_source(src_dict, id, url):
	if id in src_dict:
		raise ValueError('A url with id %s already exists in dictionary!' % id)
	if not id.startswith(_BL_PRFX) or not id.startswith(_WL_PRFX):
		raise ValueError('Url id must start with either b_ or w_ to denote blacklist/whitelist')
	src_dict[id] = url