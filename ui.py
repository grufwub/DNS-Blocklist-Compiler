import curses

class MenuItem:
    """
    MenuItem class
    
    self.function MUST accept MenuInstance object as argument)
    """
    
    def __init__(self, text = "", function = None):
        self.text = text
        self.function = function

class MenuInstance:
    """
    MenuInstance class.
    Handles running curses interface, input handling etc
    """
    
    def __init__(self):
        """
        Initialization
        """
        self.screen = curses.initscr()
        
        self.header_message = None
        self.previous_header_message = None # TODO: turn this into a stack to handle >2 nested menus
        self.next_header_message = None
        
        self.menu_items = None
        self.previous_menu_items = None # TODO: turn this into a stack to handle >2 nested menus
        self.next_menu_items = None
        
        self.item_selected = 0
        self.previous_selected = -1
        
        self.next_function = None
    
    def init(self):
        """
        Start the curses session
        """
        
        self.screen.clear()
        self.screen.refresh()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.screen.keypad(True)
    
    def close(self):
        """
        Close the curses session
        """
        
        self.screen.clear()
        self.screen.refresh()
        self.screen.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    
    def set_menu_items(self, menu_items = list()):
        """
        Set menu items to be used for drawing / function calls on next run loop
        """
        
        if self.menu_items:
            self.previous_menu_items = self.menu_items
            self.previous_selected = self.item_selected
            self.item_selected = 0
        self.next_menu_items = menu_items
    
    def set_header(self, header_message = ""):
        """
        Set header message.
        Caches previous header message and sets next header ready under next_header_message
        """
        
        if self.header_message:
            self.previous_header_message = self.header_message
        self.next_header_message = header_message
    
    def get_and_reset_selected(self):
        """
        Returns + resets the selected item and caches it under previous_selected
        """
        
        self.previous_selected = self.item_selected
        self.item_selected = 0
        return self.previous_selected
    
    def run_loop(self):
        """
        Main run loop
        """
        
        # Handles case where we come back to menu from another screen
        if self.previous_selected != -1:
            self.item_selected = self.previous_selected
            self.previous_selected = -1 # resets
        
        # Grab next set of menu_items to use
        self.menu_items = self.next_menu_items
        self.next_menu_items = None
        
        # Grab header message to use
        self.header_message = self.next_header_message
        self.next_header_message = None
        
        # Initial menu draw
        self.screen.clear()
        self._draw_header()
        self._draw_menu()
        self.screen.refresh()
        
        # Main loop
        while True:
            result = self._handle_input()
            if result: break
            
            self.screen.clear()
            self._draw_header()
            self._draw_menu()
            self.screen.refresh()
            
        # Call function set by input handler
        # TODO: improve, hacky way of handling this...
        if self.next_function == self.run_loop:
            self.run_loop()
        else:
            self.next_function(self)
    
    def _handle_input(self):
        """
        Handle input from run loop. Loop stalls until getkey() returns a value.
        Only returns true if item selected, or 'back' button pressed
        """
        
        key = self.screen.getkey()
  
        if key == "KEY_UP":
            # Move up the list
            self._dec_selected_item()
        elif key == "KEY_DOWN":
            # Move down the list
            self._inc_selected_item()
        elif key == "KEY_LEFT":
            if self.previous_menu_items == None:
                return False
            
            self.next_menu_items = self.previous_menu_items
            self.previous_menu_items = None
            
            self.next_header_message = self.previous_header_message
            self.previous_header_message = None
            
            self.next_function = self.run_loop
            return True
        elif key == "KEY_RIGHT":
            self.next_function = self.menu_items[self.item_selected].function
            return True
        
        return False
    
    def _inc_selected_item(self):
        if self.item_selected == len(self.menu_items) - 1:
            self.item_selected = 0
        else:
            self.item_selected += 1
    
    def _dec_selected_item(self):
        if self.item_selected == 0:
            self.item_selected = len(self.menu_items) - 1
        else:
            self.item_selected -= 1
    
    def _draw_header(self):
        for line in self.header_message.split("\n"):
            text = ">>>\t" + line + "\n"
            self.screen.addstr(text, curses.A_BOLD)
        self.screen.addstr("\n")
    
    def _draw_menu(self):
        index = 0
        for item in self.menu_items:
            text = "> " + item.text + "\n"
            if index == self.item_selected:
                self.screen.addstr(text, curses.A_REVERSE)
            else:
                self.screen.addstr(text)
            index += 1
        
            
