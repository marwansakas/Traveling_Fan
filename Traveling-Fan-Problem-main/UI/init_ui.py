from UI.ui import *
from manager import manual_width, manual_height, screen_height, screen_width

panel = Panel()

pause_button = Button("Pause", (screen_width - 270, panel.position[1] + 30), 150, 40, 2, (10, 10, 30), (255, 255, 255))
reset_button = Button("Reset", (screen_width - 270, panel.position[1] + 80), 150, 40, 2, (10, 10, 30), (255, 255, 255))
generate_button = Button("Generate", (screen_width - 270, panel.position[1] + 130), 150, 40, 2, (10, 10, 30),
                         (255, 255, 255))

limited_generation = DropDownButton("Select", (screen_width - 350, panel.position[1] + 230), 300, 40, 5, 2,
                                    (10, 10, 30), (255, 255, 255))
limited_generation.childs[0].text = "100"
limited_generation.childs[1].text = "200"
limited_generation.childs[2].text = "300"
limited_generation.childs[3].text = "400"
limited_generation.childs[4].text = "500"
limited_generation.currentIndex = 0

background_color = DropDownButton("Theme", (screen_width - 350, panel.position[1] + 580), 300, 40, 3, 2, (10, 10, 30),
                                  (255, 255, 255))
background_color.childs[0].text = "Black"
background_color.childs[1].text = "White"
background_color.childs[2].text = "Main"
background_color.currentIndex = -1
