"""
RenPy_Custom_Save_Load
A player customizable save/load screens with file page bookmarks for Ren'Py.

By Ticlock (2021) 2ticlock@gmail.com
https://github.com/ticlock/RenPy_Custom_Save_Load

MIT License

Copyright (c) 2021 ticlock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

init offset = 999

# Variables for save/load screen customization #################################
default persistent._page_numbers = 10
default persistent._file_current_page = 1
default persistent._bookmark_file_page = []
default persistent._bookmark_jump_end = True
default persistent._enable_save_name = True

default persistent._slot_button_width = gui.slot_button_width
default persistent._slot_button_height = gui.slot_button_height
default persistent._slot_button_text_size = gui.slot_button_text_size
default persistent._slot_button_text_size_adjust = 0
default persistent._file_slot_cols = gui.file_slot_cols
default persistent._file_slot_rows = gui.file_slot_rows

default persistent._thumbnail_width = config.thumbnail_width
default persistent._thumbnail_height = config.thumbnail_height

if persistent._thumbnail_width != None:
    define config.thumbnail_width = persistent._thumbnail_width
    define config.thumbnail_height = persistent._thumbnail_height


## Load and Save screens #######################################################
screen save():
    tag menu

    use file_slots(_("Save"))


screen load():
    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            order_reverse True

            button:
                style "page_label"

                key_events True
                xalign 0.0
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value


            grid persistent._file_slot_cols persistent._file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(persistent._file_slot_cols * persistent._file_slot_rows):

                    $ slot = i + 1

                    button:
                        xsize persistent._slot_button_width
                        ysize persistent._slot_button_height
                        padding (0, 0)
                        background _file_button_background("gui/button/slot_idle_background.png")
                        hover_background _file_button_background("gui/button/slot_hover_background.png")


                        if persistent._enable_save_name:

                            action If(renpy.get_screen("save"), true=Show("save_name_slot", accept=FileSave(slot)), false=FileLoad(slot))

                        else:

                            action FileAction(slot)

                        has vbox:
                            yoffset _file_screenshot_offset()

                        add _file_screenshot(slot):
                            xoffset _file_screenshot_offset()
                            # yoffset _file_screenshot_offset()

                        text FileSaveName(slot):
                            style "slot_name_text"
                            size (persistent._slot_button_text_size + persistent._slot_button_text_size_adjust)

                        hbox:
                            xsize persistent._slot_button_width

                            text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                                style "slot_time_text"
                                size (persistent._slot_button_text_size + persistent._slot_button_text_size_adjust)

                            key "save_delete" action FileDelete(slot)


            python:
                _file_current_page_number()

            hbox:
                xalign 1.0
                yalign 0.0
                textbutton _("Bookmark") action Show("create_bookmark_file_page")
                textbutton _("Options") action Show("save_load_settings")




            text _bookmark_current_name():
                style "page_label_text"
                xalign 0.5
                yalign 0.0

            ## Buttons to access other pages.
            hbox:
                xalign 1.0
                yalign 0.05
                for bm in persistent._bookmark_file_page:
                    if persistent._bookmark_jump_end:
                        textbutton "[bm[2]]" action FilePage(bm[2])
                    else:
                        textbutton "[bm[1]]" action FilePage(bm[1])
                textbutton "#" action ToggleField(persistent, '_bookmark_jump_end', True, False)



            $ _jump_file_page_num = _file_page_left_range(100)-100
            if _jump_file_page_num > 0:
                textbutton "{}".format(_jump_file_page_num):
                    action FilePage(_jump_file_page_num)
                    xalign 0.8
                    yalign 0.95
            else:
                textbutton "{}".format(1):
                    action FilePage(1)
                    xalign 0.8
                    yalign 0.95

            textbutton "{}".format(_file_page_left_range(100)):
                action FilePage(_file_page_left_range(100))
                xalign 0.9
                yalign 0.95
            textbutton "{}".format(_file_page_right_range(100)):
                action FilePage(_file_page_right_range(100))
                xalign 1.0
                yalign 0.95

            textbutton "Select Page":
                action Show("go_to_file_page_number")
                xalign 0.5
                yalign 0.95

            $ _jump_file_page_num = _file_page_left_range(persistent._page_numbers)-persistent._page_numbers
            if _jump_file_page_num > 0:
                textbutton "{}".format(_jump_file_page_num):
                    action FilePage(_jump_file_page_num)
                    xalign 0.0
                    yalign 0.95
            else:
                textbutton "{}".format(1):
                    action FilePage(1)
                    xalign 0.0
                    yalign 0.95
            textbutton "{}".format(_file_page_left_range(persistent._page_numbers)):
                action FilePage(_file_page_left_range(persistent._page_numbers))
                xalign 0.1
                yalign 0.95
            textbutton "{}".format(_file_page_right_range(persistent._page_numbers)):
                action FilePage(_file_page_right_range(persistent._page_numbers))
                xalign 0.2
                yalign 0.95

            hbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")


                for page in range(_file_page_left_range(persistent._page_numbers), _file_page_right_range(persistent._page_numbers)):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label_text:
    text_align 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


screen save_name_slot(accept=NullAction()):
    modal True
    add Solid("#000000") alpha 0.8
    style_prefix "saveload"

    frame:
        has vbox:
            xalign 0.5
            spacing gui.pref_spacing
            xsize int(config.screen_width/2)

        label _("Please name your save:")

        input:
            style "saveload_input"
            default store.save_name
            changed set_save_name
            length 40

        textbutton _("Save game"):
            action [accept, Hide("save_name_slot")]

        key "game_menu" action Hide("save_name_slot")


screen go_to_file_page_number():
    modal True
    default go_to_page = str(persistent._file_current_page)
    add Solid("#000000") alpha 0.8
    style_prefix "saveload"

    frame:
        has vbox:
            xalign 0.5
            spacing gui.pref_spacing

        label _("Please enter page number:")

        input:
            style "saveload_input"
            length 6
            allow "0123456789"
            value ScreenVariableInputValue('go_to_page')

        textbutton _("Enter"):
            action [Hide("go_to_file_page_number"),
                FilePage((go_to_page if (go_to_page != '' and go_to_page != '0') else 1))]

        key "game_menu" action Hide("go_to_file_page_number")


screen save_load_settings():
    modal True
    add Solid("#000000") alpha 0.8
    style_prefix "saveload"
    frame:
        has vbox:
            xalign 0.5
            spacing gui.pref_spacing
        label _("Naming save files:")
        textbutton (_("Enabled") if persistent._enable_save_name else _("Disabled")):
            action ToggleField(persistent, '_enable_save_name', True, False)
        label _("Bookmarks: Jumping to start/end page:")
        textbutton (_("End") if persistent._bookmark_jump_end else _("Start")):
            action ToggleField(persistent, '_bookmark_jump_end', True, False)
        label _("Number of file page links at bottom:")
        hbox:
            bar:
                value FieldValue(persistent, '_page_numbers', 6, offset = 4, step = 1)
            label str(persistent._page_numbers)
        label _("File Slots: Cols and Rows:")
        hbox:
            bar:
                value FieldValue(persistent, '_file_slot_cols', 4, offset = 1, step = 1, action = [Function(_adjust_slot_size), renpy.restart_interaction])
            label str(persistent._file_slot_cols)
        hbox:
            bar:
                value FieldValue(persistent, '_file_slot_rows', 3, offset = 1, step = 1, action = [Function(_adjust_slot_size), renpy.restart_interaction])
            label str(persistent._file_slot_rows)
        label _("File slot - text font size:")
        hbox:
            bar:
                value FieldValue(persistent, '_slot_button_text_size_adjust', persistent._slot_button_text_size, offset = -int(persistent._slot_button_text_size/2), step = 1)
            label str(persistent._slot_button_text_size + persistent._slot_button_text_size_adjust)

    key "game_menu" action Hide("save_load_settings")



screen create_bookmark_file_page():
    modal True
    add Solid("#000000") alpha 0.8
    style_prefix "saveload"
    default name = ''
    default s_page = str(persistent._file_current_page)
    default e_page = str(persistent._file_current_page)
    default selected_bm = None
    default input_on = None

    frame:
        xsize int(config.screen_width*2/3)
        ysize int(config.screen_height*3/4) + 50
        hbox:
            side "c r":
                area (0, 0, int(config.screen_width/3), int(config.screen_height*3/4))

                viewport id "bm":
                    draggable True
                    mousewheel True
                    vbox:
                        for i, bm in enumerate(persistent._bookmark_file_page):
                            textbutton bm[0] + '  :  ' + bm[1]+ '-'+ bm[2]:
                                selected i==selected_bm
                                action SetScreenVariable('selected_bm', i), SetScreenVariable('name', bm[0]), SetScreenVariable('s_page', bm[1]), SetScreenVariable('e_page', bm[2])

                vbar value YScrollValue("bm")

            vbox:
                xalign 0.5
                spacing gui.pref_spacing
                xsize int(config.screen_width/3)

                label _("Bookmark name:")

                button:
                    key_events True
                    yalign 1.0
                    xalign 0.5
                    xsize int(config.screen_width/4)
                    if input_on == 0:
                        input:
                            style "saveload_input"
                            length 30
                            value ScreenVariableInputValue('name')
                        action SetScreenVariable("input_on", None)
                    else:
                        text name xalign 0.5
                        action SetScreenVariable("input_on", 0)

                label _("Starting Page:")

                button:
                    key_events True
                    yalign 1.0
                    xalign 0.5
                    xsize int(config.screen_width/4)
                    if input_on == 1:
                        input:
                            style "saveload_input"
                            length 15
                            allow "0123456789"
                            value ScreenVariableInputValue('s_page')
                        action SetScreenVariable("input_on", None)
                    else:
                        text s_page xalign 0.5
                        action SetScreenVariable("input_on", 1)

                label _("Ending Page:")

                button:
                    key_events True
                    yalign 1.0
                    xalign 0.5
                    xsize int(config.screen_width/4)
                    if input_on == 2:
                        input:
                            style "saveload_input"
                            length 15
                            allow "0123456789"
                            value ScreenVariableInputValue('e_page')
                        action SetScreenVariable("input_on", None)
                    else:
                        text e_page xalign 0.5
                        action SetScreenVariable("input_on", 2)

                textbutton _("Create"):
                    action Function(_add_bookmark_file_page, name, s_page, e_page), renpy.restart_interaction

                textbutton _("Modify"):
                    action Function(_del_bookmark_file_page, selected_bm), SetScreenVariable("selected_bm", None), Function(_add_bookmark_file_page, name, s_page, e_page), renpy.restart_interaction

                textbutton _("Delete"):
                    action Function(_del_bookmark_file_page, selected_bm), SetScreenVariable("selected_bm", None), renpy.restart_interaction

                if selected_bm != None:
                    textbutton _("Select"):
                        action FilePage(persistent._bookmark_file_page[selected_bm][2])
                else:
                    textbutton _("Select")

                textbutton _("Close"):
                    action Hide("create_bookmark_file_page")

        key "game_menu" action Hide("create_bookmark_file_page")

style saveload_frame:
    padding gui.confirm_frame_borders.padding
    xsize int(config.screen_width/2)
    xalign 0.5
    yalign 0.5

style saveload_input:
    size gui.label_text_size
    color gui.hover_color
    yalign 0.5
    xalign 0.5

style saveload_bar is slider
style saveload_button is button
style saveload_button_text is button_text

style saveload_button:
    xalign 0.5
style saveload_button_text:
    xalign 0.5

style saveload_label:
    xalign 0.5

style saveload_label_text:
    color gui.text_color

init python:
    def _file_page_left_range(n):
        result = persistent._file_current_page - persistent._file_current_page % n
        if result == 0:
            return 1
        else:
            return persistent._file_current_page - persistent._file_current_page % n
    def _file_page_right_range(n):
        return persistent._file_current_page - persistent._file_current_page % n + n
    def _file_current_page_number():
        try:
            persistent._file_current_page = int(FileCurrentPage())
        except:
            pass

    def set_save_name(new_name):
        def quote(s):
            s = s.replace("{", "{{")
            s = s.replace("[", "[[")
            return s
        store.save_name = quote(new_name)

    def _add_bookmark_file_page(name, s_page, e_page):
        def quote(s):
            s = s.replace("{", "{{")
            s = s.replace("[", "[[")
            return s
        if s_page == '' or s_page == '0':
            s_page = '1'
        if e_page == '' or e_page == '0':
            e_page = '1'
        persistent._bookmark_file_page.append([quote(name),s_page,e_page])
        persistent._bookmark_file_page.sort(key = lambda x: int(x[1]))
    def _del_bookmark_file_page(n):
        if n != None:
            persistent._bookmark_file_page.pop(n)
    def _bookmark_current_name():
        result = ''
        for bm in persistent._bookmark_file_page:
            if int(bm[1]) <= persistent._file_current_page and int(bm[2]) >= persistent._file_current_page:
                result = bm[0]
        return result
    def _file_screenshot_offset():
        return int(_slot_size_factor()*5*config.screen_width/128)
    def _slot_size_factor():
        cols = [0.4,0.3,0.2,0.1375,0.1125,0.1]
        rows = [0.4,0.2,0.1375,0.1]
        col = cols[persistent._file_slot_cols - 1]
        row = rows[persistent._file_slot_rows - 1]
        return min(col,row)
    def _adjust_slot_size():
        f = _slot_size_factor()
        config.thumbnail_width = int(f*config.screen_width)
        config.thumbnail_height = int(f*config.screen_height)
        persistent._thumbnail_width = config.thumbnail_width
        persistent._thumbnail_height = config.thumbnail_height
        persistent._slot_button_width = int(persistent._thumbnail_width/0.9275362319)
        persistent._slot_button_height = int(persistent._thumbnail_height/0.6990291262)
        persistent._slot_button_text_size = int(gui.slot_button_text_size*f*5)
        persistent._slot_button_text_size_adjust = 0

    def _file_screenshot(slot):
        return Transform(child = FileScreenshot(slot), size = (persistent._thumbnail_width, persistent._thumbnail_height))
    def _file_button_background(img):
        return Transform(child = img, size = (persistent._slot_button_width, persistent._slot_button_height))
