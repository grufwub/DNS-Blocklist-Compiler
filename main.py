import curses
import host_compiler as hc
import source_handler as sh
import profile_handler as ph

PROFILE_SELECTED = ""
ID_SELECTED = -1
MAX_ID = -1
MENU_ITEMS = None

# TODO: in the future make 'running instance' class that you just hand list of menuitems, and header-drawer to ?

### UI Helpers
class MenuItem:
    """
    Very simple class for now. But easier to add functionalities in the future
    """
    def __init__(self, text = "", funct = None):
        self.text = text
        self.funct = funct

def main_menuitems():
    return [
        MenuItem(text = "> Compile blocklist", funct = compile_blocklist),
        MenuItem(text = "> Select profile", funct = profiles_loop),
        MenuItem(text = "> Create / edit profile(s)", funct = edit_profiles_loop),
        MenuItem(text = "> View / edit sources", funct = sources_loop),
        MenuItem(text = "> Cleanup files", funct = clean_files),
        MenuItem(text = "> Help", funct = help_funct),
        MenuItem(text = "> Exit", funct = exit),
    ]

def gen_sources_menuitems(sources):
    pass

def gen_profiles_menuitems(profiles):
    pass

def inc_selected_id():
    if ID_SELECTED == MAX_ID:
        ID_SELECTED = 0
    else:
        ID_SELECTED += 1
    
def dec_selected_id():
    if ID_SELECTED == 0:
        ID_SELECTED = MAX_ID
    else:
        ID_SELECTED -= 1

def main_handle_input(scrn):
    key_pressed = scrn.getkey()
    
    # Handles initial case of screen just created with no menu input
    if ID_SELECTED == -1:
        if key_pressed == curses.KEY_UP:
            ID_SELECTED = MAX_ID
        elif key_pressed == curses.KEY_DOWN:
            ID_SELECTED = 0
    
    if key_pressed == curses.KEY_UP:
        inc_selected_id()
    elif key_pressed == curses.KEY_DOWN:
        dec_selected_id()
    
    elif key_pressed == curses.KEY_ENTER:
        MENU_ITEMS[ITEM_SELECTED].funct()

### Main menuitem functions
def compile_blocklist():
    # Close curses interface
    curses.nocbreak()
    std_scrn.keypad(False)
    curses.echo()
    curses.endwin()
    
    all_profiles = ph.load_profiles()
    profile = all_profiles[PROFILE_SELECTED]
    bl = get_blacklist_sources(profile)
    wl = get_whitelist_sources(profile)
    hc.run(bl, wl)
    print("\nFinished!")

def clean_files():
    pass

def help_funct():
    pass

def exit():
    # Close curses interface
    curses.nocbreak()
    std_scrn.keypad(False)
    curses.echo()
    curses.endwin()

### Data Handling
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

### Main UI Drawing
def draw_menuitems(scrn):	
	# Draw menu items
	index = 0
	for item in MENU_ITEMS:
		if index == ITEM_SELECTED:
			scrn.addstr(item.text, curses.A_REVERSE)
		else:
			scrn.addstr(item.text)
		index += 1
        
def draw_profiles_header(scrn):
    pass

def profiles_loop(scrn):
    pass

def draw_edit_profiles_header(scrn):
    pass

def edit_profiles_loop(scrn):
    MENU_ITEMS = gen_profiles_menuitems(profiles)
    MAX_ID = len(MENU_ITEMS) - 1
    PROFILE_SELECTED = ""
    
    # Initial screen draw
    draw_sources_header(scrn)
    draw_menuitems(scrn)
    scrn.refresh()
    
    while True:
        # Handle input
        result = handle_key_input(scrn)
        if result: break
        
        draw_profiles_header(scrn)
        draw_menuitems(scrn)
        scrn.refresh()

def draw_sources_header(scrn):
    pass

def sources_loop(scrn):
    MENU_ITEMS = gen_sources_menuitems(sources)
    MAX_ID = len(MENU_ITEMS) - 1
    PROFILE_SELECTED = ""
    
    # Initial screen draw
    draw_sources_header(scrn)
    draw_menuitems(scrn)
    scrn.refresh()
    
    while True:
        # Handle input
        result = handle_key_input(scrn)
        if result: break
    
        draw_sources_header(scrn)
        draw_menuitems(scrn)
        scrn.refresh()

def draw_main_header(scrn):
    scrn.addstr("----------< DNS Blocklist Compiler by @grufwub >----------", curses.A_BOLD)
    scrn.addstr("\n")
    scrn.addstr("Profile selected: [%s]" % PROFILE_SELECTED)
    scrn.addstr("\n")

def main_loop(scrn):
    MENU_ITEMS = main_menuitems()
    MAX_ID = len(MENU_ITEMS) - 1
    PROFILE_SELECTED = ""
    
    # Initial screen draw
    draw_main_header(scrn)
    draw_menuitems(scrn)
    scrn.refresh()
    
    # Main menu loop!
    while True:       
        # Handle input
        result = handle_key_input(scrn)
        if result: break
        
        # Draw main menu
        draw_main_header(scrn)
        draw_menuitems(scrn)
        scrn.refresh()
	
def run():
	e = None
	try:
		std_scrn = curses.initscr()
    
    	# Clear the screen initially
		std_scrn.clear()
		std_scrn.refresh()

		# Setup curses interface
		curses.noecho()
		curses.cbreak()
		std_scrn.keypad(True)
	
		# Draw and start accepting input!
		main_loop(std_scrn)
	except Exception as exc:
		e = exc
	finally:
		# Close curses interface
		curses.nocbreak()
		std_scrn.keypad(False)
		curses.echo()
		curses.endwin()
		if e:
			print("[!!] Closed with exception: < %s >" % e)

if __name__ == "__main__":
    run()
