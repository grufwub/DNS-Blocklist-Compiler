import ui
import host_compiler as hc
import source_handler as sh
import profile_handler as ph

main_header = "DNS Blocklist Compiler\nBy @grufwub"
profile_header = "Profile Selection"
profile_editor_header = "Profile Editor"
sources_header = "Sources Editor"

sources = None
profiles = None
profile_selected = ""

# TODO: alert box if no profile selected
# TODO: fix weird use case where compiling prints output to screen, then jumps cursor back to beginning of output on quit
# TODO: fix inconsistent use of underscores, especially with term 'menuitems'

### Helper functions
def main_menuitems():
    return [
        ui.MenuItem(text = "Compile blocklist", function = compile_blocklist),
        ui.MenuItem(text = "Select profile", function = view_profiles),
        ui.MenuItem(text = "Create / edit profile(s)", function = edit_profiles),
        ui.MenuItem(text = "View / edit sources", function = edit_sources),
        ui.MenuItem(text = "Cleanup files", function = clean_files),
        ui.MenuItem(text = "Help", function = help_funct),
        ui.MenuItem(text = "Exit", function = exit),
    ]

def sources_menuitems():
    global sources

    sources = sh.read_sources_file()
    menuitems = list()
    for key in sources.keys():
        url = sources[key]
        menutext = ""
        if key.startswith(sh.BL_PRFX):
            menutext += "Blacklist"
        if key.startswith(sh.WL_PRFX):
            menutext += "Whitelist"
        menutext += ": " + url
    return menuitems

def profile_menuitems():
    global profiles
    
    profiles = ph.load_profiles()
    menuitems = list()
    for name in profiles.keys():
        new_menuitem = ui.MenuItem(text = name, function = set_profile)
        menuitems.append(new_menuitem)
    return menuitems

def set_profile(instance):
    global profile_selected, main_header

    # TODO: set 'selected profile' up in header somehow (UI takes header arguments??)
    profile_selected = list(profiles.keys())[instance.get_returned_index()]
    instance.goto_previous()

### MenuItem functions
def compile_blocklist(instance):
    instance.close()
    
    # TODO: check we won't run into an issue here where 'profiles' isn't up to date but 'profile_selected' is name of new profile
    profile = profiles[profile_selected]
    bl = get_blacklist_sources(profile)
    wl = get_whitelist_sources(profile)
    hc.run(bl, wl)
    print("\nFinished!")
    quit()

def view_profiles(instance):
    instance.set_menu_items(profile_menuitems())
    instance.set_header(profile_header)
    instance.run_loop()

def edit_profiles(instance):
    pass

def edit_sources(instance):
    pass

def clean_files(scrn):
    pass

def help_funct(scrn):
    pass

def exit(instance):
    instance.close()
    quit()

def name_editor(scrn):
    pass

def source_selector(scrn):
    pass

def profile_creator(scrn):
    pass

def profile_editor(scrn):
    pass

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

### Menu functions
def loop_main(instance):
    instance.set_header(main_header)
    instance.set_menu_items(main_menuitems())
    instance.run_loop()

### Main 'run' sequence
def run():
    try:
        instance = ui.MenuInstance(debug = True)
        instance.init()
        loop_main(instance)
    finally:
        if instance:
            instance.close()

if __name__ == "__main__":    
    run()
