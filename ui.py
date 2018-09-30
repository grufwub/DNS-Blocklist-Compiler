import curses

profile_header = "Profile Editor Form"
profile_name_field = "Name: "
profile_sources_field = "Sources: "

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
    
    def __init__(self, debug = False):
        """
        Initialization
        """
        self.screen = curses.initscr()
        
        self.header_message = None
        self.previous_header_message = None # TODO: turn this into a stack to handle >2 nested menus
        self._next_header_message = None
        
        self.menu_items = None
        self.previous_menu_items = None # TODO: turn this into a stack to handle >2 nested menus
        self._next_menu_items = None
        
        self._item_selected = 0
        self._previous_selected = -1
        self._return_item_index = -1
        
        self._next_function = None
        
        self.debug = debug
    
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
        self._next_menu_items = menu_items
    
    def set_header(self, header_message = ""):
        """
        Set header message.
        Caches previous header message and sets next header ready under next_header_message
        """
        
        if self.header_message:
            self.previous_header_message = self.header_message
        self._next_header_message = header_message
    
    def get_returned_index(self):
        """
        Returns + resets the selected item and caches it under previous_selected
        """
        
        temp = self._return_item_index
        self._return_item_index = -1
        return temp

    def goto_previous(self):
        """
        Set MenuInstance to go back to the previous menu screen at the end of the loop
        """

        # TODO: find more elegant way of doing this
        # Sets up next menu items to use
        self._next_menu_items = self.previous_menu_items
        self.previous_menu_items = None

        # Sets up next header to use
        self._next_header_message = self.previous_header_message
        self.previous_header_message = None

        # Sets up previously selected item index + resets previously selected
        self._item_selected = self._previous_selected
        self._previous_selected = -1

        # TODO: clear next
        # Sets to go back to run_loop
        self.run_loop()
    
    def run_loop(self):
        """
        Main run loop
        """
        
        # Grab next set of menu_items to use
        self.menu_items = self._next_menu_items
        self._next_menu_items = None
        
        # Grab header message to use
        self.header_message = self._next_header_message
        self._next_header_message = None
        
        # Initial draw
        self.screen.clear()
        self._draw_header()
        self._draw_menu()
        if self.debug: self._draw_debug()
        self.screen.refresh()
        # Main loop
        while True:
            result = self._handle_input()
            if result: break

            self.screen.clear()
            self._draw_header()
            self._draw_menu()
            if self.debug: self._draw_debug()
            self.screen.refresh()
            
        # Call function set by input handler
        # TODO: improve, hacky way of handling this...
        if self._next_function == self.run_loop:
            self.run_loop()
        else:
            self._next_function(self)
    
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
            if not self.previous_menu_items:
                return False

            # Sets up next menu items to use
            self._next_menu_items = self.previous_menu_items
            self.previous_menu_items = None

            # Sets up next header to use
            self._next_header_message = self.previous_header_message
            self.previous_header_message = None

            # Sets up previously selected item index + resets previously selected
            self._item_selected = self._previous_selected
            self._previous_selected = -1

            # Sets to go back to run_loop
            self._next_function = self.run_loop
            return True
        elif key == "KEY_RIGHT":
            # Sets up next function to call
            self._next_function = self.menu_items[self._item_selected].function
            
            # saves currently selected item value for return in case needed
            self._return_item_index = self._item_selected
            
            # resets item selected index for next screen
            self._previous_selected = self._item_selected
            self._item_selected = 0
            
            return True
        
        return False
    
    def _inc_selected_item(self):
        if self._item_selected == len(self.menu_items) - 1:
            self._item_selected = 0
        else:
            self._item_selected += 1
    
    def _dec_selected_item(self):
        if self._item_selected == 0:
            self._item_selected = len(self.menu_items) - 1
        else:
            self._item_selected -= 1
    
    def _draw_header(self):
        for line in self.header_message.split("\n"):
            text = ">>>\t" + line + "\n"
            self.screen.addstr(text, curses.A_BOLD)
        self.screen.addstr("\n")
    
    def _draw_menu(self):
        index = 0
        for item in self.menu_items:
            text = "> " + item.text + "\n"
            if index == self._item_selected:
                self.screen.addstr(text, curses.A_REVERSE)
            else:
                self.screen.addstr(text)
            index += 1
    
    def _draw_debug(self):
        for i in range(3):
            # Keep 3 blank lines after menu
            self.screen.addstr("\n")
        self.screen.addstr("----------------------------------\n")
        self.screen.addstr("item_selected = %d\nprevious_selected = %d\nreturn_item_index = %d" % (self._item_selected, self._previous_selected, self._return_item_index))
        
class ProfileEditorInstance:
    def __init__(self, curses_screen = None, debug = False):
        self.screen = curses_screen

        self._profile = None
        self._sources = None

        self._item_selected = 0
        self._input_enabled = True
        self._unsaved_name = None

        self.debug = debug
    
    def set_profile(self, profile = None):
        self._profile = profile
    
    def set_sources(self, sources = list()):
        self._sources = sources
    
    def run_loop(self):
        # Initial draw
        self.screen.clear()
        self._draw_header()
        self._draw_profile_form()
        if self.debug: self._draw_debug()
        self.screen.refresh()
        
        while True:
            result = self._handle_input()
            if result: break
            
            self.screen.clear()
            self._draw_header()
            self._draw_profile_form()
            if self.debug: self._draw_debug()
            self.screen.refresh()
        
        return self._profile
    
    def _draw_header(self):
        for line in profile_header.split("\n"):
            text = ">>>\t" + line + "\n"
            self.screen.addstr(text, curses.A_BOLD)
        self.screen.addstr("\n")
    
    def _draw_profile_form(self):
        self.screen.addstr("> " + profile_name_field + "\n")
        name_text = "--| " + self._profile["NAME"]
        
        if self._item_selected == 0:
            self.screen.addstr(name_text, curses.A_REVERSE)
            self._input_enabled = True # time to enable input! This flag needs to be set here so _handle_input() can act appropriately on next loop
        else:
            self.screen.addstr(name_text)

        self.screen.addstr("\n")
        self.screen.addstr("> " + profile_sources_field + "\n")
        index = 1
        for key in self._sources.keys():
            text = " ["
            if key in self._profile["SOURCES"]:
                text += "x"
            else:
                text += " "
            text += "] "
            if key.startswith("b_"):
                text += "Blacklist: "
            if key.startswith("w_"):
                text += "Whitelist: "
            text += self._sources[key] + "\n"        
            if self._item_selected == index:
                self.screen.addstr(text, curses.A_REVERSE)
            else:
                self.screen.addstr(text)
            index += 1
            
    def _draw_debug(self):
        for i in range(3):
            # Keep 3 blank lines after menu
            self.screen.addstr("\n")
        self.screen.addstr("----------------------------------\n")
        self.screen.addstr("item_selected = %d\nprevious_selected = %d\nreturn_item_index = %d" % (self._item_selected, self._previous_selected, self._return_item_index))

    def _inc_selected_item(self):
        if self._item_selected == len(self._sources):
            self._item_selected = 0
        else:
            self._item_selected += 1
    
    def _dec_selected_item(self):
        if self._item_selected == 0:
            self._item_selected = len(self._sources)
        else:
            self._item_selected -= 1

    def _handle_input(self):
        """
        Handle input from run loop. Stalls until getkey() returns a value.
        Only returns true if 'back' button pressed and no chars to delete
        """
        
        key = self.screen.getkey()
  
        if key == "KEY_UP":
            # Move up the list
            self._dec_selected_item()
            if self._input_enabled: self._input_enabled = False
        elif key == "KEY_DOWN":
            # Move down the list
            self._inc_selected_item()
            if self._input_enabled: self._input_enabled = False
        elif key == "KEY_LEFT":
            # Need to end loop and go back to previous screen (pass control back over to MenuInstance)
            if self._item_selected == 0:
                length = len(self._profile["NAME"])
                if length > 1:
                    self._profile["NAME"] = self._profile["NAME"][:length - 1]
                    return False
                elif length == 1:
                    self._profile["NAME"] = ""
                    return False
            return True
        elif key == "KEY_RIGHT":
            if self._item_selected == 0: # do nothing on name editing line
                return False
            # If a source item is highlighted, then allow enabling / disabling of it
            y_line = len(profile_header.split("\n")) + 3 + self._item_selected
            source = list(self._sources.keys())[self._item_selected - 1] # -1 since sources start on 1st line, not 0th
            if source in self._profile["SOURCES"]:
                self._profile["SOURCES"].remove(source)
                text = " "
            else:
                self._profile["SOURCES"].append(source)
                text = "x"
            self.screen.addnstr(y_line, 2, text, 1)
            self.screen.redrawln(y_line, 1)
        else:
            if self._item_selected != 0:
                return False
            # Time to start accepting input!
            # (need to draw the text box on the correct line)
            y_line = len(profile_header.split("\n")) + 2
            self.screen.redrawln(y_line, 1)
            
            if key.isalpha() or key.isdigit() or key in "+-=_":
                self._profile["NAME"] += key
            
            self.screen.addnstr(y_line, 3, self._profile["NAME"] + " ", len(self._profile["NAME"]) + 1) # Add whitespace char at end to ensure we always overwrite previous even if backspaced
            return self._handle_input()
        
        return False
