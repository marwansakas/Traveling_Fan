import pygame
from manager import *
from UI.init_ui import *

pygame.init()
manager = Manager()  # init the first manager.

real_stadiums = True
pause = True
started = False
right_mouse_clicked = False
generate_toggle = False
reset = False
selected_index = 2  # default generation is 300.
background_index = -1

pause_button.state = pause
reset_button.state = reset
generate_button.state = generate_toggle

show_ui = False
run = True

while run:

    manager.Background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # stop
                run = False
            if event.key == pygame.K_SPACE:
                pause = not pause
                started = True
            if event.key == pygame.K_RETURN:
                show_ui = not show_ui

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                right_mouse_clicked = True

    #  user will select what the limited generation
    if background_index == 1:
        manager.Background(White)
    elif background_index == 0:
        manager.Background(Black)
    else:
        manager.Background()

    if selected_index == 0:
        manager.generation = 100
        if not pause:
            manager.genetic_algorithm()
        manager.draw_stadiums()
        manager.draw_shortest_path()

    elif selected_index == 1:
        manager.generation = 200
        if not pause:
            manager.genetic_algorithm()
        manager.draw_stadiums()
        manager.draw_shortest_path()

    elif selected_index == 3:
        manager.generation = 400
        if not pause:
            manager.genetic_algorithm()
        manager.draw_stadiums()
        manager.draw_shortest_path()

    elif selected_index == 4:
        manager.generation = 500
        if not pause:
            manager.genetic_algorithm()
        manager.draw_stadiums()
        manager.draw_shortest_path()

    else:
        manager.generation = 300
        if not pause:
            manager.genetic_algorithm()
        manager.draw_stadiums()
        manager.draw_shortest_path()

    manager.text(started)

    if show_ui:  # user can do what he likes now.
        panel.render(manager.screen)
        limited_generation.render(manager.screen, right_mouse_clicked)
        background_color.render(manager.screen, right_mouse_clicked)
        if pause != pause_button.state:
            pause_button.state = pause

        pause_button.render(manager.screen, right_mouse_clicked)
        reset_button.render(manager.screen, right_mouse_clicked)
        generate_button.render(manager.screen, right_mouse_clicked)

        pause = pause_button.state
        reset = reset_button.state

        if reset:  # user want to reset all the stats, and start again.
            reset = False
            reset_button.state = False
            temp = manager.Stadiums.copy()
            manager = Manager(temp, real_stadiums)
            manager.reset_genetic()

        generate_toggle = generate_button.state
        if generate_toggle:  # user want to have random points.
            real_stadiums = False
            manager.random_points()
            manager.real_stadiums = False
            generate_toggle = False
            generate_button.state = False

        if pause:
            pause_button.text = "Continue"
        else:
            pause_button.text = "Pause"

        if right_mouse_clicked:
            selected_index = limited_generation.current_index
            background_index = background_color.current_index

    pygame.display.flip()
    right_mouse_clicked = False
pygame.quit()
