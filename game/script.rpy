image m_m = "gui/game_menu.jpg"

default hint = 0

default params = {
    "text": [_("File page name/number"),
        _("File page bookmark name"),
        _("Default navigation through the file pages"),
        _("Select file page button with player input for fast navigation"),
        _("Additional navigation through the file pages"),
        _("Even more navigation through the file pages"),
        _("Navigation using bookmarks"),
        _("Open Bookmark screen"),
        _("Open save/load menu settings")],
    "xpos": [315,680, 340, 695, 305, 1020, 1100, 1040, 1150],
    "ypos": [120,120, 655, 618, 615, 615, 150, 125, 125],
    "zoom": [0.5,0.5, 0.5, 0.4, 0.6, 0.6, 0.4, 0.3, 0.3]
    }

transform oval_blink:
    alpha 1.0
    easein 0.5 alpha 0.0
    easein 0.5 alpha 1.0
    repeat

screen overview():
    style_prefix "hint"
    frame:
        at transform:
            yalign 0.0
            easein 0.2 yalign 0.05
            easein 0.4 yalign -0.01
            easein 0.2 yalign 0.0
        text params["text"][hint]

    add "oval.png":
        xpos params["xpos"][hint]
        ypos params["ypos"][hint]
        if hint >=6:
            yzoom 0.3
            xzoom params["zoom"][hint]
        elif hint != 2:
            yzoom 0.4
            xzoom params["zoom"][hint]
        else:
            xzoom 2.0
            yzoom 0.3
        at oval_blink
    button:
        xsize 1280
        ysize 720
        action SetVariable('hint', hint + 1), Return()

screen click():
    button:
        xsize 1280
        ysize 720
        action Return()

screen summary(n):
    if n == 1:
        default summary_text = _("""{b}Short summary of features:{/b}\n\n
1) Customizable save/load options by player.\n\n
2)  Naming each save file (can be disabled by the player).\n\n
3) Creating/Editing named bookmarks for each playthrough route:\n
    Created bookmarks automatically display their name for file pages that are in the range listed in the bookmark.\n\n
4) Select file page button with player input for fast navigation.  Also, additional buttons for quick navigation through file pages by 10-100 pages and by bookmarks.\n\n
5) Changeable number of save slots per file page (at the cost of slot size) and font size  (customizable by the player).\n\n
6) it can also be used as a mod for finished games (at your own risk) if they use fileslot screen in similar way.\n\n
\n
Adding the module to the Ren'Py project:\n
    Just put customizable_save_load.rpy in game directory\n
    {color=#666}(Optional) Delete save, load and fileslot screens in screens.rpy{/color}""")
    elif n == 2:
        default summary_text = _("""Recommended size for {b}slot_idle_background.png{/b} and {b}slot_hover_background.png{/b}:\n\n
Option 1 - Default size:\n\n
This size equals to the size for 2 rows and 3 cols settings. In this case, the largest image (1 row x 1 col) is doubled and the smallest (4 rows x 5 cols) is halved.\n\n
{i}{b}Width of save screenshots = screen_width * 0.2\n
Height of save screenshots = screen_height * 0.2\n
Width of file slot (width of slot_idle_background.png) = screen_width * (0.2 + 1/64)\n
Height of file slot (height of slot_idle_background.png) = screen_height * (0.2 + 62/720)\n
Save screenshot offset (x and y) = screen_width * (1/128)\n\n{/i}{/b}

Option 2 - Large size:\n\n
This size equals to the size for 1 rows and 1 cols settings. In this case, the medium image (2 row x 3 col) is halved and the smallest (4 rows x 5 cols) is quartered.\n\n

All default sizes are doubled""")
    frame:
        xsize 1280
        ysize 720
        background Solid("#fffc")
    text summary_text:
        xsize 800
        yalign 0.5
        xalign 0.5
        color "#000"
    textbutton _("Close"):
        xalign 1.0
        yalign 0.0
        action Return()
        text_size 30

style hint_frame is gui_frame
style hint_frame:
    xalign 0.5

style hint_text is gui_text
style hint_text:
    size 30
    color "#ED7D31"

label main_menu:
    return
label start:
    scene m_m
    "This is a short overview of player customizable save/load menu with file page bookmarks."
    "Players who loves organizing save files for different routes might find it very convenient if they see something like this in games."
    scene 000 with pushleft
    "Here is an example of the save/load menu with a default gui template."
    "Let's consider an example with some gui images\
    ({color=#0099ff}slot_idle_background.png{/color} and {color=#0099ff}slot_hover_background.png{/color})."
    scene 001 with pushleft
    "Now, let's consider the elements and features of the customizable save/load menu."

label l_hints:
    call screen overview
    if hint == 4:
        scene 002 with pushleft
        "Player input screen to select file page."
        scene 001 with pushleft
    if hint <= 8:
        jump l_hints

label l_routes:
    scene m_m with dissolve
    "Let's assume the game has 3 routes:"
    scene good with dissolve
    "Good route."
    scene bad with dissolve
    "Bad route."
    scene good_bad with dissolve
    "Neutral route."
    "Using bookmarks we can easily separate save files for each route."
    "Let's open bookmark screen."
    scene 003 with pushleft
    "Here on left we can see all saved bookmarks (names and corresponding file pages)."
    "The right part of screen allows to create, modify, delete, jump to corresponding bookmark"
    "There is a starting and ending page. If the file page is in the range, the bookmark name \
    automatically appears on save/load screen."

label checkpoint_2:
    scene 001 with pushleft
    "Bookmark navigation allows to jump to starting or ending page of bookmarks."
    show oval at oval_blink:
        xpos 1225
        ypos 160
        xzoom 0.1
        yzoom 0.2
    "This button allows to toggle between starting and ending page when navigating."
    "Let's open Options screen."
    scene 004 with pushleft
    "Here, player can enable/disable naming each individual save file."
    "Also, toggle between starting and ending page for bookmarks when navigating."
    "Player can also change number of save files per file page, by changing number of rows and columns."
    scene 005 with pushleft
    "Here is an example of 20 save files per file page."
    scene 006 with pushleft
    "Player might prefer having bigger save images and less save files per file page."
    scene 004 with pushleft
    "Finally, in Options screen the font size of save/load menu can be adjusted. It affects the font size of save file name and date."
    scene m_m with dissolve
    "NOTE: Since the number of save slots per file page is changeable, the {i}save screenshots (thumbnails){/i} and slot button images ({b}slot_idle_background.png{/b} and {b}slot_hover_background.png{/b}) needs to be resized."
    "Thus, two things should be considered:"
    "1) {i}Save screenshots{/i} may drop in quality when resizing. It is recommended that the player set the preferred cols and rows number of save slots before playing to avoid future resizing."
    "2) Resizing is implemented based on default Ren'Py screen aspect ratio and default size ratios of the save screenshot and slot button and their relative position"
    "The next three images represent recomended size for {b}slot_idle_background.png{/b} and {b}slot_hover_background.png{/b} and positioning of blank scrennshot inside"
    scene 007 with pushleft
    call screen click
    scene 008 with pushleft
    call screen click
    scene 009 with pushleft
    call screen click
    scene m_m with dissolve
    call screen summary(1)
    call screen summary(2)
    return
