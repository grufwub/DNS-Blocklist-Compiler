import curses
import host_compiler as hc
import source_handler as sh
import profile_handler as ph

def draw_main_menu(scrn):
	scrn.addstr('----------< DNS Blocklist Compiler by @grufwub >----------', curses.A_BOLD)
	scrn.addstr('\n')
	scrn.addstr('1) An option might go here')
	# do some more stuff
	scrn.refresh()
	
def move_cursor_up(scrn):
	# stuff
	print("stuff")

def move_cursor_down(scrn):
	# stuff
	print("stuff")

def main(std_scrn):
	# Clear the screen initially
	std_scrn.clear()
	std_scrn.refresh()
	
	# Setup curses interface
	curses.noecho()
	curses.cbreak()
	std_scrn.keypad(True)
	
	draw_main_menu(std_scrn)
	
	# Start accepting input loop!
	while True:
		print("while true!")

def get_blacklist_sources(profile):
	all_sources = sh.read_sources_file()
	bl = list()
	srcs = profile[ph.PROFILE_KEY_SOURCES]
	for src_id in srcs:
		if src_id.startswith(sh.BL_PRFX):
			source = all_sources[src_id]
			bl.append(source)
	return bl

def get_whitelist_sources(profile):
	all_sources = sh.read_sources_file()
	wl = list()
	srcs = profile[ph.PROFILE_KEY_SOURCES]
	for src_id in srcs:
		if src_id.startswith(sh.WL_PRFX):
			source = all_sources[src_id]
			wl.append(source)
	return wl

if __name__ == '__main__':
	# curses.wrapper(main)
	all_profiles = ph.load_profiles()
	profile = all_profiles['default-mobile']
	bl = get_blacklist_sources(profile)
	wl = get_whitelist_sources(profile)
	hc.run(bl, wl)
	print('Finished!')