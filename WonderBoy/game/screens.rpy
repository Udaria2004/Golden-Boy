################################################################################
## Initialization
################################################################################

init offset = -1

init -1 python:
    def toggle_mute():
        # Flips the mute state on and off
        preferences.mute = not preferences.mute
        # Forces the UI to redraw instantly
        renpy.restart_interaction()
    
    def is_auto_forward_on():
        return renpy.get_preference("auto-forward")
    

################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say


screen say(who, what):

    # --- 1. THE DARK VIGNETTE (Using your PNG image) ---
    add "assets/main_menu/TextboxGradient.png" xpos 1 yalign 1.0 xysize (1920, 1080)

    # --- 2. THE AVATAR (Your character sprite) ---
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0 yoffset -80

    # --- 3. THE TEXT WINDOW ---
    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

# --- NEW STYLES FOR THE DIALOGUE AREA ---

style window is default:
    xalign 0.5
    xfill True
    yalign 1.0
    ysize 380
    background None
    padding (475, 175, 400, 80)
    bottom_margin 60

style namebox is default:
    xpos 0
    xanchor 0.0
    ypos 0
    xsize 400
    ysize 40
    background None

style say_label is default:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 34
    # Removed hardcoded color. It will now inherit the Character's color!
    outlines [ (2, "#000000", 0, 0) ]
    xalign 0.0
    textalign 0.0
    yalign 0.5

style say_dialogue is default:
    font "assets/fonts/OpenSans-SemiBold.ttf"
    size 26
    color "#FFFFFF"
    outlines [ (2, "#000000", 0, 0) ]
    xpos 40
    ypos 50        # Increased spacing for better separation
    xanchor 0.0
    textalign 0.0
    line_spacing 8



## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

## Choice screen ###############################################################
##
## This screen is used to display in-game choices.

screen choice(items):
    style_prefix "choice"

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30  # Space between the choice buttons

        for i in items:
            textbutton i.caption:
                action i.action
                style "pref_button"  # Reuse your Settings button style
                xsize 400
                xalign 0.5


# --- STYLES FOR THE CHOICE MENU ---

# Because we used 'style "pref_button"', we don't need new styles!
# The text will automatically use style "pref_button_text" from your Settings menu.
# Meaning: White text, turns Yellow on hover, and physically lifts up when hovered.


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

## Quick Menu screen (Minimal Bottom Bar) ######################################
screen quick_menu():

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"
            style "quick_menu"
            xalign 0.5
            yalign 1.0
            spacing 25

            textbutton _("Back") action Rollback()

            textbutton _("Skip"):
                action Skip()
                alternate Skip(fast=True, confirm=True)
                selected renpy.is_skipping()   # ✅ This works perfectly

            textbutton _("Auto"):
                action Preference("auto-forward", "toggle")   # ✅ This toggles Auto, no highlight needed

            textbutton _("Save") action ShowMenu("save")
            textbutton _("Load") action ShowMenu("load")
            textbutton _("Settings") action ShowMenu("preferences")

## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True


# --- STYLES FOR THE MINIMAL BOTTOM BAR ---
style quick_menu is hbox:
    xalign 0.5
    yalign 1.0
    spacing 25

style quick_button is button:
    background None
    hover_background None
    xalign 0.5

style quick_button_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 20
    color "#FFFFFF"
    hover_color "#e5b620"
    selected_color "#e5b620"            # Turn yellow when active
    selected_hover_color "#e5b620"
    outlines [ (3, "#000000", 0, 0) ]   # Thick 3px outline as requested
    xalign 0.5
    textalign 0.5

################################################################################
## Main and Game Menu Screens
################################################################################

################################################################################
## Main Menu screen
################################################################################

transform button_glow:
    on idle:
        alpha 1.0
    on hover:
        alpha 1.0
        linear 0.1 blur 2.0
        linear 0.1 blur 0.0

transform tilt_1:
    rotate 1.5

transform tilt_2:
    rotate -1.5

transform tilt_3:
    rotate 2

transform tilt_4:
    rotate -2

transform tilt_5:
    rotate 0.5

transform tilt_6:
    rotate -0.5

screen main_menu():

    tag menu

    # Your background image
    add "assets/main_menu/Main Menu.png" xysize (1920, 1080)

    # Your Title Logo (moved slightly higher to make room for buttons)
    add "assets/main_menu/Transparent Title.png" xalign 0.55 yalign 0.08 xsize 800 ysize 300

    # The UI Container
    vbox:
        style_prefix "main_menu_ui"
        xalign 0.5
        yalign 0.92  # Moves the text slightly higher than the very bottom
        spacing 25   # Space between the words

        # The Buttons (Action order: Start -> Load -> Settings -> Quit)
        textbutton _("Start") action Start() at button_glow
        textbutton _("Load") action ShowMenu("load") at button_glow
        textbutton _("Settings") action ShowMenu("preferences") at button_glow
        textbutton _("Quit") action Quit(confirm=False) at button_glow


# 1. The Container Style
style main_menu_ui_vbox is vbox:
    xalign 0.5
    yalign 0.5
    
# 2. The Button Style (Minimalism)
style main_menu_ui_button is button:
    xsize None
    ysize None
    background None
    hover_background None
    padding (20, 5)       # Added a bit more padding on the sides
    text_align 0.5        # Align the text in the center of that width

# 3. The Text Style (Includes Drop Shadow for Readability)
style main_menu_ui_button_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 48
    
    # Centered alignment
    xalign 0.5
    textalign 0.5
    
    color "#FFFFFF"
    
    # THE MIDDLE GROUND:
    # 1px outline ON the text, AND the offset shadow behind it.
    outlines [ (1, "#000000", 0, 0), (0, "#000000", 2, 2) ] 
    
    # HOVER STATE (Keep the gold and beef up the shadow slightly)
    hover_color "#e5b620" 
    hover_outlines [ (1, "#000000", 0, 0), (0, "#000000", 3, 3) ]


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    font "assets/fonts/BebasNeue-Regular.ttf"
    properties gui.text_properties("title")

style main_menu_version:
    font "assets/fonts/BebasNeue-Regular.ttf"
    properties gui.text_properties("version")

style main_menu_button_style is default_button:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 40
    idle_color "#FFFFFF"
    hover_color "#FFFF00"
    background None
    hover_background None
    xpadding 10
    ypadding 5

style main_menu_button_style_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    properties gui.text_properties("main_menu_button")
    outlines [(2, "#FFFF00", 0, 0)]

style bottom_menu_hbox is hbox:
    spacing 30

style bottom_menu_button is default_button:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 40
    idle_background Frame("assets/main_menu/button.png", xborder=0, yborder=0)
    hover_background Frame("assets/main_menu/button.png", xborder=0, yborder=0)
    xpadding 20
    ypadding 20
    xminimum 220
    yminimum 80
    xalign 0.5
    yalign 0.5

style bottom_menu_button_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 32
    color "#e5b620"
    idle_color "#e5b620"
    hover_color "#e5b620"
    xalign 0.5
    yalign 0.5


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


# ========== LOAD/SAVE SCREEN TRANSFORMS ==========

transform tilt_1:
    rotate 1.5

transform tilt_2:
    rotate -1.5

transform tilt_3:
    rotate 2

transform tilt_4:
    rotate -2

transform tilt_5:
    rotate 0.5

transform tilt_6:
    rotate -0.5

transform card_hover:
    on idle:
        yoffset 0
        zoom 1.0
    on hover:
        ease 0.2 yoffset -15  # Lifts up by 15 pixels
        ease 0.2 zoom 1.05    # Zooms in smoothly

# ========== LOAD/SAVE SCREEN ==========

screen file_slots(title):

    fixed:
        # --- UNIFIED BACKGROUND ---
        add "assets/main_menu/Main Menu.png" xysize (1920, 1080)
        add Solid("#000000") alpha 0.5 xysize (1920, 1080)

        # --- HEADER ---
        text title:
            font "assets/fonts/BebasNeue-Regular.ttf"
            size 70
            color "#e5b620"
            outlines [ (2, "#000000", 0, 0), (0, "#000000", 2, 2) ]
            xalign 0.5
            ypos 40

        # --- POLAROID GRID ---
        grid 3 2:
            xalign 0.5
            ypos 70       
            spacing 5    
            
            for i in range(6):
                $ slot = i + 1
                
                if i == 0:
                    $ tilt_transform = tilt_1
                elif i == 1:
                    $ tilt_transform = tilt_2
                elif i == 2:
                    $ tilt_transform = tilt_3
                elif i == 3:
                    $ tilt_transform = tilt_4
                elif i == 4:
                    $ tilt_transform = tilt_5
                else:
                    $ tilt_transform = tilt_6 
                
                button:
                    action FileAction(slot)
                    # --- SIMPLIFIED: Kept the tilt, removed the hover animation/glow ---
                    at [tilt_transform]
                    background None
                    xsize 312
                    ysize 352
                    
                    # --- DROP SHADOW ---
                    add Solid("#000000", alpha=0.35):
                        xpos 6
                        ypos 6
                        xsize 300
                        ysize 340
                    
                    # --- WHITE POLAROID ---
                    frame:
                        xpos 6
                        ypos 6
                        xsize 300
                        ysize 340
                        background Solid("#FFFFFF")
                        padding (15, 15, 15, 35)

                        vbox:
                            xfill True
                            yfill True
                            spacing 10
                            
                            add FileScreenshot(slot) xalign 0.5 yalign 0.0 ysize 220 xsize 270
                            
                            text FileTime(slot, format=_("{#file_time}%b %d, %H:%M"), empty=_("Empty")):
                                xalign 0.5
                                textalign 0.5
                                font "assets/fonts/BebasNeue-Regular.ttf"
                                size 32
                                color "#ffffff"
                                outlines [ (1, "#000000", 0, 0) ]
                            
                            text FileSaveName(slot):
                                xalign 0.5
                                textalign 0.5
                                font "assets/fonts/BebasNeue-Regular.ttf"
                                size 18
                                color "#FFFFFF"
                                outlines [ (1, "#000000", 0, 0) ]

                            textbutton "X" action FileDelete(slot):
                                xalign 1.0
                                yalign 1.0
                                xoffset -5
                                yoffset -40
                                background None
                                text_color "#FFFFFF"
                                text_hover_color "#e5b620"
                                text_outlines [ (1, "#000000", 0, 0) ]
                                text_size 24

        # --- BOTTOM PAGE NAVIGATION ---
        hbox:
            xalign 0.5
            ypos 1000
            spacing 25

            textbutton "<":
                action FilePagePrevious()
                style "page_nav_button"
                at button_glow

            if config.has_autosave:
                textbutton "AUTO":
                    action FilePage("auto")
                    style "page_nav_button"
                    at button_glow
                    text_color ("#e5b620" if FileCurrentPage() == "auto" else "#FFFFFF")
                    text_hover_color "#e5b620"   # <-- CORRECT KEYWORD

            if config.has_quicksave:
                textbutton "QUICK":
                    action FilePage("quick")
                    style "page_nav_button"
                    at button_glow
                    text_color ("#e5b620" if FileCurrentPage() == "quick" else "#FFFFFF")
                    text_hover_color "#e5b620"   # <-- CORRECT KEYWORD
            
            for page in range(1, 10):
                textbutton str(page):
                    action FilePage(page)
                    style "page_nav_button"
                    at button_glow
                    text_color ("#e5b620" if FileCurrentPage() == str(page) else "#FFFFFF")
                    text_hover_color "#e5b620"   # <-- CORRECT KEYWORD

            textbutton ">":
                action FilePageNext()
                style "page_nav_button"
                at button_glow
        
        # --- RETURN BUTTON ---
        textbutton _("Return"):
            style "pref_return_button"
            action Return()
            xalign 1.0
            ypos 40
            xoffset -40
            at button_glow

# ========== LOAD/SAVE PAGINATION STYLES ==========

style page_nav_button is button:
    background None
    hover_background None
    idle_background None

style page_nav_button_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 36                    # <-- increased from 28
    color "#FFFFFF"
    hover_color "#e5b620"
    selected_color "#e5b620"
    selected_hover_color "#e5b620"
    outlines [ (1, "#000000", 0, 0) ]
    xalign 0.5
    textalign 0.5

# --- STYLES FOR THE LOAD/SAVE UI ---

# Pagination Bar Buttons
style page_nav_button is button:
    background None
    hover_background None
    idle_background None

style page_nav_button_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 32
    color "#FFFFFF"       # White idle (readable on dark background)
    hover_color "#e5b620" # Yellow hover
    outlines [ (1, "#000000", 0, 0) ] # Outline added for visibility
    xalign 0.5
    textalign 0.5


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():
    tag menu

    # 1. Main Menu Background
    add "assets/main_menu/Main Menu.png" xysize (1920, 1080)
    # 2. Dark overlay
    add Solid("#000000") alpha 0.5 xysize (1920, 1080)

    # --- TOP RIGHT RETURN BUTTON ---
    textbutton "RETURN":
        style "pref_return_button"
        action Return()
        xalign 1.0
        ypos 40
        xoffset -40
        at button_glow

    # Main Vertical Container
    vbox:
        xalign 0.5
        yalign 0.5
        yoffset 40
        spacing 50

        # Title
        text "SETTINGS" style "pref_menu_title" 

        null height -40

        # --- TOP ROW (Display, Music, Sound) ---
        hbox:
            xalign 0.5
            spacing 100

            # COLUMN 1: DISPLAY
            vbox:
                xalign 0.56
                spacing 20
                text "DISPLAY" style "pref_sketch_header"
                textbutton "Windowed" action Preference("display", "window") style "pref_button" selected (not preferences.fullscreen) at button_glow
                textbutton "Fullscreen" action Preference("display", "fullscreen") style "pref_button" selected preferences.fullscreen at button_glow

            # COLUMN 2: MUSIC
            vbox:
                xalign 0.5
                spacing 20
                if config.has_music:
                    text "MUSIC" style "pref_sketch_header"
                    # MATCHED SIZES: Bar height is 24, Dot height is 24. Perfectly centered.
                    bar value Preference("music volume") xsize 280 ysize 24 left_bar Solid("#e5b620" if not preferences.mute else "#555555", ysize=24) right_bar Solid("#555555", ysize=24) thumb Solid("#e5b620" if not preferences.mute else "#555555", xsize=24, ysize=24, xradius=12, yradius=12)

            # COLUMN 3: SOUND
            vbox:
                xalign 0.5
                spacing 20
                if config.has_sound:
                    text "SOUND" style "pref_sketch_header"
                    bar value Preference("sound volume") xsize 280 ysize 24 left_bar Solid("#e5b620" if not preferences.mute else "#555555", ysize=24) right_bar Solid("#555555", ysize=24) thumb Solid("#e5b620" if not preferences.mute else "#555555", xsize=24, ysize=24, xradius=12, yradius=12)

        # Spacer
        null height 40

        # --- BOTTOM ROW (Skip, Text Speed, Auto-Forward) ---
        hbox:
            xalign 0.5
            spacing 100

            # COLUMN 1: SKIP
            vbox:
                xalign 0.5
                spacing 20
                text "SKIP" style "pref_sketch_header"
                textbutton "Unseen Text" action Preference("skip", "toggle") style "pref_button" selected preferences.skip_unseen at button_glow
                textbutton "After Choices" action Preference("after choices", "toggle") style "pref_button" selected preferences.skip_after_choices at button_glow
                textbutton "Transitions" action InvertSelected(Preference("transitions", "toggle")) style "pref_button" selected (not preferences.transitions) at button_glow

            # COLUMN 2: TEXT SPEED
            vbox:
                xalign 0.5
                spacing 20
                text "TEXT SPEED" style "pref_sketch_header"
                bar value Preference("text speed") xsize 280 ysize 24 left_bar Solid("#e5b620", ysize=24) right_bar Solid("#555555", ysize=24) thumb Solid("#e5b620", xsize=24, ysize=24, xradius=12, yradius=12)

            # COLUMN 3: AUTO-FORWARD TIME
            vbox:
                xalign 0.5
                spacing 20
                text "AUTO-FORWARD TIME" style "pref_sketch_header"
                bar value Preference("auto-forward time") xsize 280 ysize 24 left_bar Solid("#e5b620", ysize=24) right_bar Solid("#555555", ysize=24) thumb Solid("#e5b620", xsize=24, ysize=24, xradius=12, yradius=12)

        # Spacer
        null height 20

        # --- BOTTOM BUTTONS ---
        vbox:
            xalign 0.5
            spacing 20
            if config.has_music or config.has_sound or config.has_voice:
                textbutton ( "UNMUTE ALL" if preferences.mute else "MUTE ALL" ):
                    action toggle_mute
                    style "pref_button"
                    selected preferences.mute
                    xalign 0.5

# --- STYLES FOR THE PREFERENCES MENU ---

# HEADERS: Used for DISPLAY, SKIP, MUSIC, SOUND, TEXT SPEED, AUTO-FORWARD
style pref_sketch_header is text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 43     # <--- Increased by 5 (was 38)
    color "#e5b620" 
    outlines [ (1, "#000000", 0, 0), (0, "#000000", 2, 2) ]
    xalign 0.5
    textalign 0.5

# INTERACTIVE OPTIONS: Used for Windowed, Fullscreen, Unseen Text, etc.
style pref_button is button:
    background None
    hover_background None
    selected_background None
    xalign 0.5
    xsize 280

style pref_button_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 29
    color "#FFFFFF"
    hover_color "#e5b620"
    selected_color "#e5b620"
    selected_hover_color "#e5b620"
    
    # 1px solid outline + 2px drop shadow (Idle - Flat)
    outlines [ (1, "#000000", 0, 0), (0, "#000000", 2, 2) ] 
    
    # 1px solid outline + 3px drop shadow (Hover - Lifts up)
    hover_outlines [ (1, "#000000", 0, 0), (0, "#000000", 3, 3) ]
    selected_outlines [ (1, "#000000", 0, 0), (0, "#000000", 3, 3) ]
    
    xalign 0.5
    textalign 0.5

# TITLE (Kept at 80, exactly as you wanted)
style pref_menu_title is text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 80
    color "#e5b620"
    outlines [ (2, "#000000", 0, 0), (0, "#000000", 3, 3) ]
    xalign 0.5
    textalign 0.5
    ypadding 15

# RETURN BUTTON
style pref_return_button is button:
    background None
    hover_background None
    xalign 0.5

style pref_return_button_text is button_text:
    font "assets/fonts/BebasNeue-Regular.ttf"
    size 47
    color "#FFFFFF"       
    hover_color "#e5b620" 
    
    # Idle (2px shadow)
    outlines [ (2, "#000000", 0, 0), (0, "#000000", 2, 2) ]
    
    # Hover (3px shadow, lifts up!)
    hover_outlines [ (2, "#000000", 0, 0), (0, "#000000", 3, 3) ]
    
    xalign 0.5
    textalign 0.5


################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

## Confirm screen ##############################################################
screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    add Solid("#000000") alpha 0.75 xysize (1920, 1080)

    frame:
        xalign .5
        yalign .5
        xsize 650
        ysize 250
        background Solid("#181818") 
        padding (50, 40)

        vbox:
            xalign .5
            yalign .5
            spacing 0

            # 1. Top spacer (pushes the message down a bit)
            null height 50

            # --- THE MESSAGE ---
            text "[message!tq]":
                xalign 0.5
                xmaximum 550
                font "assets/fonts/OpenSans-Regular.ttf"
                size 24
                color "#e5b620"
                outlines [ ]
                textalign 0.5

            # 2. Middle spacer (separates the message from the buttons)
            null height 50

            # --- YES / NO BUTTONS ---
            hbox:
                xalign 0.5
                spacing 100

                textbutton _("Yes"):
                    action yes_action
                    style "confirm_button"
                    xsize 150
                    xalign 0.5

                textbutton _("No"):
                    action no_action
                    style "confirm_button"
                    xsize 150
                    xalign 0.5

            # 3. Bottom spacer (balances the bottom perfectly)
            null height 50

# --- STYLES FOR THE CUSTOM CONFIRM BUTTONS ---
style confirm_button is button:
    background None
    hover_background None
    xalign 0.5

style confirm_button_text is button_text:
    font "assets/fonts/OpenSans-Regular.ttf"
    size 22                # Lowered size
    color "#FFFFFF"
    hover_color "#e5b620"
    outlines [ (1, "#000000", 0, 0) ]          # Flat outline
    hover_outlines [ (1, "#000000", 0, 0), (0, "#000000", 3, 3) ] # Lifts on hover
    xalign 0.5
    textalign 0.5

## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

## Notify screen ###############################################################
screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        xalign 1.0           # Pinned to the right edge
        yalign 0.0           # Pinned to the top edge
        xoffset -20          # Small gap from the right side
        yoffset 20           # Small gap from the top

        text "[message!tq]":
            xalign 0.5
            textalign 0.5
            font "assets/fonts/OpenSans-Regular.ttf"
            size 22
            color "#FFFFFF"
            outlines [ (1, "#000000", 0, 0) ]  # Subtle black outline for readability

    # Fades out automatically after 3.25 seconds (just like default)
    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


# --- STYLES FOR THE NOTIFY POPUP ---
style notify_frame is empty:
    background Solid("#181818")               # Matches your Confirm screen box
    padding (20, 12, 20, 12)                  # Cozy inner spacing
    xsize 500                                 # Fixed width so it doesn't stretch too far


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


################################################################################
## Mobile Variants
################################################################################

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 1305
