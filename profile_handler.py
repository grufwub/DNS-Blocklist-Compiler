import source_handler
import pickle, os

_PROFILE_DIR = 'profiles/'
_PROFILE_EXT = '.profile'
_PROFILE_KEY_NAME = 'NAME'
_PROFILE_KEY_SOURCES = 'SOURCES'
_LOADED_PROFILES = None

# TODO: handle case of null profiles! e.g. when trying to delete one
# TODO: optimise
# TODO: ensure consistent use of variable names, underscores etc throughout entire project

if not os.path.isdir(_PROFILE_DIR):
	os.mkdir(_PROFILE_DIR)

def get_profile_files():
	profile_list = list()
	dirlist = os.listdir(_PROFILE_DIR)
	for item in dirlist:
		path = _PROFILE_DIR + item
		if os.path.isfile(path):
			if path.endswith(_PROFILE_EXT):
				profile_list.append(path)
	return profile_list

def write_profiles():
	for profile_name in _LOADED_PROFILES.keys():
		profile = _LOADED_PROFILES[profile_name]
		name = profile[_PROFILE_KEY_NAME]
		file_path = _PROFILE_DIR + name + _PROFILE_EXT
		f = open(file_path, 'w')
		pickle.dump(profile, f)
		f.close()

def load_profiles():
	_LOADED_PROFILES = dict()
	profiles = get_profile_files()

	for profile in profiles:
		f = open(profile, 'r')
		str = f.read()
		raw = pickle.loads(str)
		name = raw[_PROFILE_KEY_NAME]
		_LOADED_PROFILES[name] = raw
		f.close()

def get_profiles():
	if not _LOADED_PROFILES:
		raise ValueError('Please use load_profiles() before attempting to get profiles!')
	return _LOADED_PROFILES

def add_profile(name, sources_active):
	profile_dict = dict()
	profile_dict[_PROFILE_KEY_NAME] = name
	profile_dict[_PROFILE_KEY_SOURCES] = sources_active
	_LOADED_PROFILES[name] = profile_dict

def edit_profile(name, new_profile):
	if name not in _LOADED_PROFILES:
		raise ValueError('Cannot edit profile by the name %s as it does not exist!' % name)
	_LOADED_PROFILES[name] = new_profile


