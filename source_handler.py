SOURCE_FILE = 'sources.txt'
_BL_PRFX = 'b_'
_WL_PRFX = 'w_'
_ID_SPRTR = '::'
_SRC_DICT = None

# Reads blacklist and whitelist entries from file and simply returns them. Nothing more
def read_sources_file():
        srcs = dict()

        f = open(SOURCE_FILE, 'r')
        for line in f.read().split('\n'):
		src = line.split(_ID_SPRTR)
		_SRC_DICT[src[0]] = src[1]
        f.close()
        return srcs

# Opens for editing and saves blacklist/whitelist entries in local dictionaries
def load_sources_file():
	_SRC_DICT = read_sources_file()

# Writes edited changes to file
# MAKE UP TO DATE!!!!!!!!!!!!!!!!!!!!!!!!!
def write_sources_to_file():
	f = open(SOURCE_FILE, 'w')
	for url in _BL_DICT.keys():
		entry = ''
		if not _BL_DICT[url]:
			entry += _UNMOD_PREFIX
		entry += 'blacklist:' + url + '\n'
		f.write(entry)
	for url in _WL_DICT.keys():
		entry = ''
		if not _WL_DICT[url]:
			entry += _UNMOD_PREFIX
		entry += 'whitelist:' + url + '\n'
		f.write(entry)
	f.close()

def get_blacklist():
	if _SRC_DICT == None:
		raise ValueError('Please initialize internal source lists with \'open_sources_file()\' first')
	return_dict = dict()
	for item in _SRC_DICT.keys():
		if item .startswith(_BL_PRFX):
			return_dict[item] = _SRC_DICT[item]
	return return_dict

def get_whitelist():
	if _SRC_DICT == None:
		raise ValueError('Please initialize internal source lists with \'open_sources_file()\' first')
	return_dict = dict()
	for item in _SRC_DICT.keys():
		if item.startswith(_WL_PRFX):
			return_dict[item] = _SRC_DICT[item]
	return return_dict

def edit_source(url_id, new_url):
	if url_id in _SRC_DICT:
		_SRC_DICT[url_id] = new_url
	raise ValueError('Supplied url could not be found in either  blacklist or whitelist!')

def add_source(id, url):
	if id in _SRC_DICT:
		raise ValueError('A url with id %s already exists in dictionary!' % id)
	if not id.startswith(_BL_PRFX) or not id.startswith(_WL_PRFX):
		raise ValueError('Url id must start with either b_ or w_ to denote blacklist/whitelist')
	_SRC_DICT[id] = url
