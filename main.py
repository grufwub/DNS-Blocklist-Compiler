import curses

def draw_main_menu(scrn):
	scrn.addstr('----------< DNS Blocklist Compiler by @grufwub >----------', curses.A_BOLD)
	scrn.addstr('\n')
	scrn.addstr('1) An option might go here')
	# do some more stuff
	scrn.refresh()
	
def move_cursor_up(scrn):
	# stuff

def move_cursor_down(scrn):
	# stuff

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
		

if __name__ == '__main__':
	curses.wrapper(main)