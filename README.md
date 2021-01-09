# RenPy_Custom_Save_Load
A player customizable save/load screens with file page bookmarks for Ren'Py.

## Features
* Customizable save/load options by player
* Naming each save file (can be disabled by player)
* Creating/Editing named bookmarks for each playthrough route:

   Created bookmarks automatically display its name for file pages that are in range listed in the bookmark.
* Select file page button with player input for fast navigation. Also additional buttons for fast navigation through file pages by 10-100 pages and by bookmarks.
* Changeable number of save slots per file page (at cost of slot size) and font size  (customizable by player)
* It can be also used as a mod for finished games (at your own risk) if they use fileslot screen in similar way.

## Adding the module to the Ren'Py project
* Just put [customizable_save_load.rpy](../blob/master/game/customizable_save_load.rpy) in game directory
* (Optional) Delete save, load and fileslot screens in **screens.rpy**

## Screenshots
![screenshot](/game/images/001.png)
![screenshot](/game/images/003.png)
![screenshot](/game/images/004.png)
![screenshot](/game/images/005.png)
![screenshot](/game/images/006.png)
## NOTE
Since number of save slots per file page is changable, the *save screenshots (thumbnails)* and slot button images (**slot_idle_background.png** and **slot_hover_background.png**) needs to be resized. Thus, two things should be considered:
* *Save screenshots* may drop in quality when resizing. It is recomended for player to set the preferred cols and rows number of save slots before playing to avoid future resizing.
* Resizing is implemented based on default Ren'Py screen aspect ratio and default size ratios of save screenshot and slot button and their relative position

### Recomended size for **slot_idle_background.png** and **slot_hover_background.png** and positioning of blank screenshot image
Resolution aspect ratio (16:9). For example: 1024x576, 1280x720, 1920x1080
![screenshot](/game/images/007.png)
![screenshot](/game/images/008.png)
![screenshot](/game/images/009.png)
#### Option 1 - Default size:
   This size equals to the size for 2 rows and 3 cols settings. In this case the largest image (1 row x 1 col) is doubled and the smallest (4 rows x 5 cols) is halved.

* Width of save screenshots = screen_width * 0.2
* Height of save screenshots = screen_height * 0.2
* Width of file slot (width of slot_idle_background.png) = screen_width * (0.2 + 1/64)
* Height of file slot (height of slot_idle_background.png) = screen_height * (0.2 + 62/720)
* Save screenshot offset (x and y) = screen_width * (1/128)

##### Examples:
* Resolution 1024x576
  * Screenshot_width = 205
  * Screenshot_height = 116
  * file_slot_width = 221
  * file_slot_height = 165
  * Offset = 8
* Resolution 1280x720
  * Screenshot_width = 256
  * Screenshot_height = 144
  * file_slot_width = 276
  * file_slot_height = 206
  * Offset = 10
* Resolution 1920x1080
  * Screenshot_width = 384
  * Screenshot_height = 216
  * file_slot_width = 414
  * file_slot_height = 309
  * Offset = 15

#### Option 2 - Large size:
   This size equals to the size for 1 rows and 1 cols settings. In this case the medium image (2 row x 3 col) is halved and the smallest (4 rows x 5 cols) is quartered.

All default sizes are doubled

##### Examples:
* Resolution 1024x576
  * Screenshot_width = 410
  * Screenshot_height = 232
  * file_slot_width = 442
  * file_slot_height = 330
  * Offset = 16
* Resolution 1280x720
  * Screenshot_width = 512
  * Screenshot_height = 288
  * file_slot_width = 552
  * file_slot_height = 412
  * Offset = 20
* Resolution 1920x1080
  * Screenshot_width = 768
  * Screenshot_height = 432
  * file_slot_width = 828
  * file_slot_height = 618
  * Offset = 30
   
