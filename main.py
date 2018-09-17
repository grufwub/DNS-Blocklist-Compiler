import curses
import host_compiler as hc
import source_handler as sh
import profile_handler as ph

PROFILE_SELECTED = ""
ITEM_SELECTED = -1
MAX_ID = -1
MENU_ITEMS = None

# TODO: in the future make 'running instance' class that you just hand list of menuitems, and header-drawer to ?
# TODO: alert box if no profile selected
# TODO: fix weird use case where compiling prints output to screen, then jumps cursor back to beginning of output on quit
# TODO: move some function defs to different files?
# TODO: left arrow key goes 'back'

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
        MenuItem(text = "Compile blocklist", funct = compile_blocklist),
        MenuItem(text = "Select profile", funct = profiles_loop),
        MenuItem(text = "Create / edit profile(s)", funct = edit_profiles_loop),
        MenuItem(text = "View / edit sources", funct = sources_loop),
        MenuItem(text = "Cleanup files", funct = clean_files),
        MenuItem(text = "Help", funct = help_funct),
        MenuItem(text = "Exit", funct = exit),
    ]

def gen_sources_menuitems(sources):
    pass

def gen_profiles_menuitems(profiles):
    menuitems = list()
    for item in profiles.keys():
        new_menuitem = MenuItem(item)
        menuitems.append(new_menuitem)
    return menuitems
        

def inc_selected_id():
    global ITEM_SELECTED
    
    if ITEM_SELECTED == MAX_ID:
        ITEM_SELECTED = 0
    else:
        ITEM_SELECTED += 1
    
def dec_selected_id():
    global ITEM_SELECTED
    
    if ITEM_SELECTED == 0:
        ITEM_SELECTED = MAX_ID
    else:
        ITEM_SELECTED -= 1

### Handle key inputs
def handle_main_input(scrn):
    global ITEM_SELECTED
    key_pressed = scrn.getkey()
    
    # Handles initial case of screen just created with no menu input
    if ITEM_SELECTED == -1:
        if key_pressed == "KEY_UP":
            ITEM_SELECTED = MAX_ID
        elif key_pressed == "KEY_DOWN":
            ITEM_SELECTED = 0
        return False
    
    if key_pressed == "KEY_UP":
        dec_selected_id()
        return False
    elif key_pressed == "KEY_DOWN":
        inc_selected_id()
        return False
    
    elif key_pressed == "KEY_RIGHT":
        MENU_ITEMS[ITEM_SELECTED].funct(scrn)
        return True

def handle_profiles_input(scrn):
    global ITEM_SELECTED
    global PROFILE_SELECTED
    key_pressed = scrn.getkey()
    
    # Handles initial case of screen just created with no menu input
    if ITEM_SELECTED == -1:
        if key_pressed == "KEY_UP":
            ITEM_SELECTED = MAX_ID
        elif key_pressed == "KEY_DOWN":
            ITEM_SELECTED = 0
        return False
    
    if key_pressed == "KEY_UP":
        dec_selected_id()
        return False
    elif key_pressed == "KEY_DOWN":
        inc_selected_id()
        return False
    elif key_pressed == "KEY_RIGHT":
        PROFILE_SELECTED = MENU_ITEMS[ITEM_SELECTED].text
        return True

### Main menuitem functions
def compile_blocklist(scrn):
    curses.nocbreak()
    scrn.keypad(False)
    curses.echo()
    curses.endwin()
    
    all_profiles = ph.load_profiles()
    profile = all_profiles[PROFILE_SELECTED]
    bl = get_blacklist_sources(profile)
    wl = get_whitelist_sources(profile)
    hc.run(bl, wl)
    print("\nFinished!")
    quit()

def clean_files(scrn):
    pass

def help_funct(scrn):
    pass

def exit(scrn):
    # Close curses interface
    curses.nocbreak()
    scrn.keypad(False)
    curses.echo()
    curses.endwin()
    quit()

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
	global MENU_ITEMS
	global ITEM_SELECTED
    
	# Draw menu items
	index = 0
	for item in MENU_ITEMS:
		if index == ITEM_SELECTED:
			scrn.addstr("> " + item.text + "\n", curses.A_REVERSE)
		else:
			scrn.addstr("> " + item.text + "\n")
		index += 1
        
def draw_profiles_header(scrn):
    scrn.addstr("----------< Profile Selection Screen >----------\n", curses.A_BOLD)
    scrn.addstr("\n")

def profiles_loop(scrn):
    global MENU_ITEMS
    global MAX_ID
    global ITEM_SELECTED
    
    ITEM_SELECTED = -1
    MENU_ITEMS = gen_profiles_menuitems( ph.load_profiles() )
    MAX_ID = len (MENU_ITEMS) - 1
    
    # Initial screen draw
    scrn.clear()
    draw_profiles_header(scrn)
    draw_menuitems(scrn)
    scrn.refresh()
    
    while True:
        # Handle input
        result = handle_profiles_input(scrn)
        scrn.clear()
        if result: break
    
        draw_profiles_header(scrn)
        draw_menuitems(scrn)
        scrn.refresh()

def draw_edit_profiles_header(scrn):
    pass

def edit_profiles_loop(scrn):
    global MENU_ITEMS
    global MAX_ID
    
    MENU_ITEMS = gen_profiles_menuitems(profiles)
    MAX_ID = len(MENU_ITEMS) - 1
    
    # Initial screen draw
    scrn.clear()
    draw_sources_header(scrn)
    draw_menuitems(scrn)
    scrn.refresh()
    
    while True:
        # Handle input
        handle_key_input(scrn)
        
        scrn.clear()
        draw_profiles_header(scrn)
        draw_menuitems(scrn)
        scrn.refresh()

def draw_sources_header(scrn):
    pass

def sources_loop(scrn):
    global MENU_ITEMS
    global MAX_ID
    
    MENU_ITEMS = gen_sources_menuitems(sources)
    MAX_ID = len(MENU_ITEMS) - 1
    
    # Initial screen draw
    scrn.clear()
    draw_sources_header(scrn)
    draw_menuitems(scrn)
    scrn.refresh()
    
    while True:
        # Handle input
        handle_key_input(scrn)

        scrn.clear()
        draw_sources_header(scrn)
        draw_menuitems(scrn)
        scrn.refresh()

def draw_main_header(scrn):
    global PROFILE_SELECTED
    
    scrn.addstr("----------< DNS Blocklist Compiler by @grufwub >----------\n", curses.A_BOLD)
    scrn.addstr("\n")
    scrn.addstr("Profile selected: [%s]\n" % PROFILE_SELECTED)
    scrn.addstr("\n")

def main_loop(scrn):
	global MENU_ITEMS
	global MAX_ID
	global ITEM_SELECTED
    
	MENU_ITEMS = main_menuitems()
	MAX_ID = len(MENU_ITEMS) - 1
	ITEM_SELECTED = -1
    
	# Initial screen draw
	scrn.clear()
	draw_main_header(scrn)
	draw_menuitems(scrn)
	scrn.refresh()
    
	# Main menu loop!
	while True:        
		# Handle input
		result = handle_main_input(scrn)
		if result: break
        
		# Draw main menu
		scrn.clear()
		draw_main_header(scrn)
		draw_menuitems(scrn)
		scrn.refresh()

	# Reaaaaaaally hacky way of doing this. TODO: improve when neatening code in future
	main_loop(scrn)

### Main 'run' sequence
def run():
	# Set initially. TODO: is this the best place to put this?
	global PROFILE_SELECTED
	PROFILE_SELECTED = ""

	e = None
	try:
		std_scrn = curses.initscr()
    
    	# Clear the screen initially
		std_scrn.clear()
		std_scrn.refresh()

		# Setup curses interface
		curses.noecho()
		curses.cbreak()
		curses.curs_set(0)
		std_scrn.keypad(True)
	
		# Draw and start accepting input!
		main_loop(std_scrn)
#	except Exception as exc:
#		e = exc
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
