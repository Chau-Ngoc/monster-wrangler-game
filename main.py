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

        self.reset_position()

    def update(self) -> None:
        """Update the Knight object. Override the update method of the parent class."""
        self.move()

        # something wrong with the below code
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("key pressed")
                if event.key == pygame.K_SPACE:
                    self.warp()
                    print("Warped")

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

    def __init__(self, image, x, y, monster_type) -> None:
        """Initialize a Monster."""
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

    def __init__(self, player: Knight, monster_group: Monster) -> None:
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

        # game font and text
        self.font = pygame.font.Font(
            "./monster_wrangler_assets/Abrushow.ttf", FONT_SIZE
        )

    def update(self):
        """Update the game object."""
        pass

    def blit(self):
        """Blit the HUD and other game assets onto the display."""
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

        current_catch_text = self.font.render("Current Catch", True, TEXT_COLOR)
        current_catch_text_rect = current_catch_text.get_rect()
        current_catch_text_rect.centerx = WINDOW_WIDTH // 2
        current_catch_text_rect.top = PADY

        time_text = self.font.render(f"Round Time: {self.round_time}", True, TEXT_COLOR)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (WINDOW_WIDTH - PADX, PADY)

        warps_text = self.font.render(f"Warps: {self.player.warps}", True, TEXT_COLOR)
        warps_text_rect = warps_text.get_rect()
        warps_text_rect.topright = (WINDOW_WIDTH - PADX, PADY + FONT_SIZE + 10)

        display_surface.blit(score_text, score_text_rect)
        display_surface.blit(lives_text, lives_text_rect)
        display_surface.blit(round_text, round_text_rect)
        display_surface.blit(current_catch_text, current_catch_text_rect)
        display_surface.blit(time_text, time_text_rect)
        display_surface.blit(warps_text, warps_text_rect)

    def check_collision(self):
        """Check for the collision between player and monsters."""
        pass

    def start_new_round(self):
        """Populate new monsters for new round."""
        pass

    def choose_new_target(self):
        """Choose new target monster for player."""
        pass

    def pause_game(self):
        """Pause the game."""
        pass

    def reset_game(self):
        """Reset the game."""
        pass

    def play_sound(self):
        """Play sound effects and background music."""
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
KNIGHT_VELOCITY = 5

# game values
player_lives = PLAYER_STARTING_LIVES
warps_count = WARPS_COUNT

# initialize pygame
pygame.init()

# create a display surface
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Monster Wrangler")

# create knight Group
knight = Knight()
knight_group = pygame.sprite.Group()
knight_group.add(knight)

# create monster Group
monster_group = pygame.sprite.Group()
test_monster = Monster(
    pygame.image.load("./monster_wrangler_assets/green_monster.png"), 500, 500, "green"
)
test_monster_2 = Monster(
    pygame.image.load("./monster_wrangler_assets/blue_monster.png"), 1000, 500, "blue"
)
monster_group.add(test_monster, test_monster_2)

# create Game object
game = Game(knight, monster_group)

# create a clock to control fps
clock = pygame.time.Clock()

# the main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the background color
    display_surface.fill(BACKGROUND_COLOR)

    # blit the text on the display surface
    game.blit()

    # draw the gameplay area rectangle
    gameplay_area_rect = display_surface.get_rect()
    gameplay_area_rect.width = GAMEPLAY_AREA_WIDTH
    gameplay_area_rect.height = GAMEPLAY_AREA_HEIGHT
    gameplay_area_rect.centerx = WINDOW_WIDTH // 2
    gameplay_area_rect.top = 3 * (FONT_SIZE + 20)
    pygame.draw.rect(
        display_surface, GAMEPLAY_AREA_BORDER_COLOR, gameplay_area_rect, width=5
    )
    # draw the knight group and monster group
    knight_group.draw(display_surface)
    knight_group.update()

    monster_group.draw(display_surface)
    monster_group.update()

    # update the display
    pygame.display.update()

    # tick the clock
    clock.tick(FPS)

# quit the game
pygame.quit()
