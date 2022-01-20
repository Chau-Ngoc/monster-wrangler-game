import pygame

from objects import *
from settings import *


# initialize pygame
pygame.init()

# create knight Group
knight = Knight()
knight.reset_position()
knight_group = pygame.sprite.Group()
knight_group.add(knight)

# create monster Group
monster_group = pygame.sprite.Group()

# create Game object
game = Game(knight, monster_group)
game.catch_sound.set_volume(0.1)
game.die_sound.set_volume(0.1)
game.next_level_sound.set_volume(0.1)
game.warp_sound.set_volume(0.1)

game.populate_monsters()
game.select_a_target()

# create a clock to control fps
clock = pygame.time.Clock()

# the main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("quit")
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                knight.warp()
                game.warp_sound.play()

            elif event.key == pygame.K_RETURN:
                game.pause_game()

    # fill the background color
    display_surface.fill(BACKGROUND_COLOR)

    # blit the text on the display surface
    game.blit()
    game.update()

    # draw the knight group and monster group
    knight_group.draw(display_surface)
    knight_group.update()

    # bounce the monsters and move the knight
    game.bounce_monsters()
    game.constrain_knight_area()

    monster_group.draw(display_surface)
    monster_group.update()

    collided_monster = game.return_collided()

    # if collided monster is not None
    if collided_monster:

        # if the knight collided with the target monster
        if collided_monster.type == game.target_monster_type:
            game.score += 1
            game.catch_sound.play()
            game.monster_group.remove(collided_monster)

            # check if there are any monsters left in the group
            if game.monsters_in_group():
                game.monsters_on_knight()
                game.select_a_target()

            # if there are no more monsters left in the group
            else:
                game.next_level_sound.play()
                game.current_round += 1
                game.round_time = 0
                game.frame_count = 0
                knight.warps = WARPS_COUNT
                game.populate_monsters()
                game.select_a_target()
                knight.reset_position()

        # if the knight collided with the wrong monster
        else:
            knight.lives -= 1
            game.die_sound.play()
            knight.reset_position()

            # if the players has no lives left
            if knight.lives == 0:
                is_paused = True
                while is_paused:
                    game.blit_gameover()

                    for event in pygame.event.get():
                        # if the player wants to reset the game
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                game.reset_game()
                                is_paused = False

                        # if the player wants to quit
                        elif event.type == pygame.QUIT:
                            is_paused = False
                            running = False

    # update the display
    pygame.display.update()

    # tick the clock
    clock.tick(FPS)

# quit the game
pygame.quit()
