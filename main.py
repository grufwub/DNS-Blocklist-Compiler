import os
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
        ui.MenuItem(text = "View / edit sources", function = view_sources),
        ui.MenuItem(text = "Cleanup files", function = clean_files),
        ui.MenuItem(text = "Exit", function = exit),
    ]

def sources_menuitems():
    menuitems = list()
    for key in get_sources().keys():
        url = get_sources()[key]
        menutext = ""
        if key.startswith(sh.BL_PRFX):
            menutext += "Blacklist"
        if key.startswith(sh.WL_PRFX):
            menutext += "Whitelist"
        menutext += ": " + url
        item = ui.MenuItem(text = menutext, function = edit_source)
        menuitems.append(item)

    return menuitems

def profile_menuitems(func):
    menuitems = list()
    for name in get_profiles().keys():
        new_menuitem = ui.MenuItem(text = name, function = func)
        menuitems.append(new_menuitem)
    return menuitems

def set_profile(instance):
    global profile_selected

    # TODO: set 'selected profile' up in header somehow (UI takes header arguments??)
    profile_selected = get_profile_at(instance.get_returned_index())["NAME"]
    instance.goto_previous()

def delete_profile(instance):
    selected_name = get_profile_at(instance.get_returned_index())["NAME"]
    del profiles[selected_name]
    os.remove("profiles/" + selected_name + ".profile")
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
    instance.set_menu_items(profile_menuitems(set_profile))
    instance.set_header(profile_header)
    instance.run_loop()

def edit_profiles(instance):
    menuitems = profile_menuitems(edit_profile)
    createprofile_item = ui.MenuItem(text = "[ Create new profile ]", function = create_profile)
    menuitems.append(createprofile_item)

    instance.set_menu_items(menuitems)
    instance.set_header(profile_editor_header)
    instance.run_loop()

def create_profile(instance):
    # Create new ProfileEditorInstance and pass control to it
    profile = dict()
    profile["NAME"] = ""
    profile["SOURCES"] = list()
    editor = ui.ProfileEditorInstance(curses_screen = instance.screen)
    editor.set_profile(profile)
    editor.set_sources(get_sources())
    profile = editor.run_loop()
    
    if profile["NAME"] != "" and len(profile["SOURCES"]) > 0:
        get_profiles()[profile["NAME"]] = profile
        ph.write_profiles(profiles)
    
    # Pass control back to MenuInstance
    instance.goto_previous()

def edit_profile(instance):
    # Same sort of issue with mess code here as in 'create_profile'
    editor = ui.ProfileEditorInstance(curses_screen = instance.screen)
    index = instance.get_returned_index()
    editor.set_profile(get_profile_at(index))
    editor.set_sources(get_sources())
    result = editor.run_loop()
    
    if result["NAME"] != "" and len(result["SOURCES"]) > 0:
        profiles[index] = result
        ph.write_profiles(profiles)
    
    instance.goto_previous()

def view_sources(instance):
    instance.set_menu_items(sources_menuitems())
    instance.set_header(sources_header)
    instance.run_loop()

def edit_source(instance):
    # Same sort of issue with mess code here as in 'create_profile'
    pass

def clean_files(instance):
    instance.close()

    print("Cleaning up files.")
    print("Removing /backups directory...")
    try:
        files = os.listdir("backups")
        for f in files:
            os.remove("backups/" + f)
    except OSError:
        print("FAILED DELETING FILES IN /backups")
    try:
        os.rmdir("backups")
    except OSError:
        print("FAILED DELETING DIRECTORY /backups")

    print("Removing /compiled directory...")
    try:
        files = os.listdir("compiled")
        for f in files:
            os.remove("compiled/" + f)
    except OSError:
        print("FAILED DELETING FILES IN /compiled")
    try:
        os.rmdir("compiled")
    except OSError:
        print("FAILED DELETING DIRECTORY /compiled")

    print("Finished Cleaning!")
    quit()

def exit(instance):
    instance.close()
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

def get_sources():
    global sources
    if not sources:
        sources = sh.read_sources_file()
    return sources

def get_profiles():
    global profiles
    if not profiles:
        profiles = ph.load_profiles()
    return profiles

def get_profile_at(i):
    keys = list(get_profiles().keys())
    return profiles[keys[i]]

### Menu functions
def loop_main(instance):
    instance.set_header(main_header)
    instance.set_menu_items(main_menuitems())
    instance.run_loop()

### Main 'run' sequence
def run():
    try:
        instance = ui.MenuInstance(debug = False)
        instance.init()
        loop_main(instance)
    finally:
        if instance:
            instance.close()

if __name__ == "__main__":
    run()
