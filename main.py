from typing import Union
import pygame, random


class Knight(pygame.sprite.Sprite):
    """A Knight class that the user can control."""

    def __init__(self) -> None:
        """Initialize the player."""
        super().__init__()
        self.image = pygame.image.load("./monster_wrangler_assets/knight.png")
        self.rect = self.image.get_rect()

        self.velocity = KNIGHT_VELOCITY
        self.warps = WARPS_COUNT
        self.lives = PLAYER_STARTING_LIVES

    def update(self) -> None:
        """Update the Knight object. Override the update method of the parent class."""
        self.move()

    def warp(self):
        """Teleport the knight out of the gameplay area."""
        if self.warps > 0:
            self.warps -= 1
            self.reset_position()

    def reset_position(self):
        """Reset the player position."""
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT

    def move(self):
        """Move the knight."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity


class Monster(pygame.sprite.Sprite):
    """A Monster class that represents the enemy."""

    def __init__(self, image, x, y, monster_type: str) -> None:
        """Initialize a Monster

        Args:
            image (pygame.Surface): the image Surface of the Monster
            x (int): the x coordinate used to position the topleft corner of the rect attribute of the Monster
            y (int): the y coordinate used to position the topleft corner of the rect attribute of the Monster
            monster_type (str): the string code represents the color of the Monster
        """
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.type = monster_type

        # set random motion
        self.velocity = random.randint(1, 5)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def update(self) -> None:
        """Update the Monster object. Override the update method of the parent class."""
        # move the monster
        self.rect.x += self.velocity * self.dx
        self.rect.y += self.velocity * self.dy

        # bounce the monster
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.dy *= -1


class Game:
    """A class to control gameplay."""

    def __init__(self, player: Knight, monster_group: pygame.sprite.Group) -> None:
        """Initialize a Knight that the player controls.

        Args:
            player (Knight): the Knight that the player controls
            monster_group (pygame.sprite.Group): pygame.sprite.Group that contains the Monsters. Each Monster in
                this group has a monster_type attribute that can be used to assign new target monster.
        """
        self.player = player
        self.monster_group = monster_group

        self.score = 0
        self.current_round = 1
        self.round_time = 0
        self.frame_count = 0

        # game sound effects
        self.next_level_sound = pygame.mixer.Sound(
            "./monster_wrangler_assets/next-level.wav"
        )
        self.catch_sound = pygame.mixer.Sound("./monster_wrangler_assets/catch.wav")
        self.die_sound = pygame.mixer.Sound("./monster_wrangler_assets/die.wav")

        self.next_level_sound.set_volume(0.1)
        self.catch_sound.set_volume(0.1)
        self.die_sound.set_volume(0.1)

        # game font and text
        self.font = pygame.font.Font(
            "./monster_wrangler_assets/Abrushow.ttf", FONT_SIZE
        )

        # monster types
        blue_monster = pygame.image.load("./monster_wrangler_assets/blue_monster.png")
        green_monster = pygame.image.load("./monster_wrangler_assets/green_monster.png")
        purple_monster = pygame.image.load(
            "./monster_wrangler_assets/purple_monster.png"
        )
        yellow_monster = pygame.image.load(
            "./monster_wrangler_assets/yellow_monster.png"
        )

        self.monster_types = {
            "blue": blue_monster,
            "green": green_monster,
            "purple": purple_monster,
            "yellow": yellow_monster,
        }
        self.target_monster_type = random.choice(
            [type for type in self.monster_types.keys()]
        )
        self.target_monster_image = self.monster_types[self.target_monster_type]
        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH // 2
        self.target_monster_rect.top = PADY + FONT_SIZE + 10

        # gameplay area rect
        self.gameplay_area_rect = display_surface.get_rect()
        self.gameplay_area_rect.width = GAMEPLAY_AREA_WIDTH
        self.gameplay_area_rect.height = GAMEPLAY_AREA_HEIGHT
        self.gameplay_area_rect.centerx = WINDOW_WIDTH // 2
        self.gameplay_area_rect.top = 3 * (FONT_SIZE + 20)

    def update(self):
        """Update the time."""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.frame_count = 0
            self.round_time += 1

    def blit(self):
        """Blit the HUD and other game assets onto the display."""
        colors = {"blue": BLUE, "green": GREEN, "purple": PURPLE, "yellow": YELLOW}

        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (PADX, PADY)

        lives_text = self.font.render(f"Lives: {self.player.lives}", True, TEXT_COLOR)
        lives_text_rect = lives_text.get_rect()
        lives_text_rect.topleft = (PADX, PADY + FONT_SIZE + 10)

        round_text = self.font.render(
            f"Current Round: {self.current_round}", True, TEXT_COLOR
        )
        round_text_rect = round_text.get_rect()
        round_text_rect.topleft = (PADX, PADY + 2 * (FONT_SIZE + 10))

        current_catch_text = self.font.render("Current Target", True, TEXT_COLOR)
        current_catch_text_rect = current_catch_text.get_rect()
        current_catch_text_rect.centerx = WINDOW_WIDTH // 2
        current_catch_text_rect.top = PADY

        time_text = self.font.render(f"Round Time: {self.round_time}", True, TEXT_COLOR)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (WINDOW_WIDTH - PADX, PADY)

        warps_text = self.font.render(f"Warps: {self.player.warps}", True, TEXT_COLOR)
        warps_text_rect = warps_text.get_rect()
        warps_text_rect.topright = (WINDOW_WIDTH - PADX, PADY + FONT_SIZE + 10)

        # blit the assets and the target monster image
        display_surface.blit(self.target_monster_image, self.target_monster_rect)
        display_surface.blit(score_text, score_text_rect)
        display_surface.blit(lives_text, lives_text_rect)
        display_surface.blit(round_text, round_text_rect)
        display_surface.blit(current_catch_text, current_catch_text_rect)
        display_surface.blit(time_text, time_text_rect)
        display_surface.blit(warps_text, warps_text_rect)

        pygame.draw.rect(
            display_surface,
            colors[self.target_monster_type],
            self.target_monster_rect,
            width=2,
        )
        pygame.draw.rect(
            display_surface,
            colors[self.target_monster_type],
            self.gameplay_area_rect,
            width=5,
        )

    def monsters_in_group(self) -> bool:
        """Check if there are any Monsters in the monster group.
        Return True if there are Monsters in the group, False if there are none."""
        num_monsters = len(self.monster_group)
        if num_monsters > 0:
            return True
        else:
            return False

    def return_collided(self) -> Union[Monster, None]:
        """Check for the collision between player and monsters.
        Return the collided monster in the monster group.

        If there are no collisions, then return None."""
        collided_monster = pygame.sprite.spritecollideany(
            self.player, self.monster_group
        )
        return collided_monster

    def populate_monsters(self):
        """Populate new monsters each round."""
        lower_limit = self.current_round + 1
        upper_limit = self.current_round + 3
        num_monsters = random.randint(lower_limit, upper_limit)

        for _ in range(num_monsters):
            monster_type = random.choice([type for type in self.monster_types.keys()])
            monster_image = self.monster_types[monster_type]
            x = random.randint(0, WINDOW_WIDTH - 64)
            y = random.randint(0, WINDOW_HEIGHT - 64)
            new_monster = Monster(monster_image, x, y, monster_type)
            self.monster_group.add(new_monster)

    def select_a_target(self):
        """Choose new target monster for player. The new selected monster has to come from the monster group."""

        # for example we have the following group:
        # [blue monster, green monster, green monster, purple monster, yellow monster]
        # pick a random integer number to index the selected monster from this list.
        selected_idx = random.randint(0, len(self.monster_group) - 1)
        selected_monster = self.monster_group.sprites()[selected_idx]

        # assign target_monster_image to this monster image.
        self.target_monster_image = selected_monster.image
        self.target_monster_type = selected_monster.type

    def pause_game(self):
        """Pause the game."""
        pass

    def reset_game(self):
        """Reset the game."""
        pass


# game settings
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 900
GAMEPLAY_AREA_WIDTH = 1450
GAMEPLAY_AREA_HEIGHT = 600
GAMEPLAY_AREA_BORDER_COLOR = "#4FBDBA"
PADX = 20
PADY = 20
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = "#FFEEAD"
FONT_SIZE = 32
FPS = 60

PLAYER_STARTING_LIVES = 5
WARPS_COUNT = 3
KNIGHT_VELOCITY = 10

# monster colors
BLUE = "#0ba9e9"
GREEN = "#58d136"
PURPLE = "#ed54fb"
YELLOW = "#f59d19"

# initialize pygame
pygame.init()

# create a display surface
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

# create knight Group
knight = Knight()
knight.reset_position()
knight_group = pygame.sprite.Group()
knight_group.add(knight)

# create monster Group
monster_group = pygame.sprite.Group()

# create Game object
game = Game(knight, monster_group)
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

    # fill the background color
    display_surface.fill(BACKGROUND_COLOR)

    # blit the text on the display surface
    game.blit()
    game.update()

    # draw the knight group and monster group
    knight_group.draw(display_surface)
    knight_group.update()

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
                game.select_a_target()

            # if there are no more monsters left in the group
            else:
                game.next_level_sound.play()
                game.current_round += 1
                knight.warps = WARPS_COUNT
                game.populate_monsters()
                game.select_a_target()
                knight.reset_position()

        # if the knight collided with the wrong monster
        else:
            knight.lives -= 1
            game.die_sound.play()
            knight.reset_position()

    # update the display
    pygame.display.update()

    # tick the clock
    clock.tick(FPS)

# quit the game
pygame.quit()
