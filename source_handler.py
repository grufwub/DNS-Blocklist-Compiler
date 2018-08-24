SOURCE_FILE = 'sources.txt'
_BL_PRFX = 'b_'
_WL_PRFX = 'w_'
_ID_SPRTR = '::'
_BL_DICT = None
_WL_DICT = None

# Reads blacklist and whitelist entries from file and simply returns them. Nothing more
def read_sources_file():
        bl = dict()
        wl = dict()
	if len(_BL_PREFIX) != len(_WL_PREFIX):
		# Just checking for weird edge cases
		raise ValueError('Blacklist and whitelist prefix lengths should be equal!')

	pre_len = len(_BL_PRFX)
        f = open(SOURCE_FILE, 'r')
        for line in f.read().split('\n'):
                if line.startswith('#'):
                        continue
                # TODO: improve by this to be more accepting of issues?? --> extracting actual URL instead of just removing first 10/11 characters
                if line.startswith(_BL_PRFX):
			src = line[pre_len:].split(_ID_SPRTR)
			id = src[0]
			url = src[1]
			bl[id] = url
		if line.startswith(_WL_PRFX):
			src = line[pre_len:].split(_ID_SPRTR)
			id = src[0]
			url = src[1]
			wl[id] = url
        f.close()
        return bl, wl

# Opens for editing and saves blacklist/whitelist entries in local dictionaries
def load_sources_file():
	_BL_DICT = dict()
	_WL_DICT = dict()
	_BL_DICT, _WL_DICT = read_sources_file()

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
	if _BL_DICT == None:
		raise ValueError('Please initialize internal source lists with \'open_sources_file()\' first')
	return _BL_DICT

def get_whitelist():
	if _WL_DICT == None:
		raise ValueError('Please initialize internal source lists with \'open_sources_file()\' first')
	return _WL_DICT

def edit_source(url_id, new_url):
	if url_id in _BL_DICT:
		_BL_DICT[url_id] = new_url
		return
	if url_id in _WL_DICT:
		_WL_DICT[url_id] = new_url
		return
	raise ValueError('Supplied url could not be found in either  blacklist or whitelist!')
