import pygame
import random

#DEFINE GAME VARIABLES

#FOOD VARIABLES
LENGTH_PER_FOOD = 1
LENGTH_PER_SUPERFOOD = 10
SUPERFOOD_PERCENT = 50

FOOD_PER_CYCLE = 3

#GAME VARIABLES
GAME_SPEED = 10



# Initialize Pygame
pygame.init()

# Set the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)

# Set the font
font = pygame.font.SysFont(None, 30)

# Set the game clock
clock = pygame.time.Clock()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

class Snake:
    #start_x, start_y: starting coordinates of the snake
    def __init__(self, start_x, start_y): #Initialize the snake class
        self.length = 1
        self.positions = [(start_x, start_y)]

        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Randomly choose a direction as a tuple
        self.color = GREEN  # Snake color attribute


    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * CELL_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self): #reset snake after losing game
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([(0, -1), (0, 1), (-1, 0), (1, 0)])  # Reset direction randomly

    def draw(self, surface): #draw the snake
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn((0, -1))
                elif event.key == pygame.K_DOWN:
                    self.turn((0, 1))
                elif event.key == pygame.K_LEFT:
                    self.turn((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    self.turn((1, 0))

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.change_position()

    def change_position(self):
        self.position = (random.randint(0, (SCREEN_WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (SCREEN_HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

        self.isSuperFood = 1 if random.randint(0, 100) <= SUPERFOOD_PERCENT else 0
        if(self.isSuperFood):
            self.color = PINK
        else:
            self.color = RED

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Main function
def main():
    snake = Snake( (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2) )

    food = []

    for i in range(0, FOOD_PER_CYCLE):
        food.append(Food())
    #food = Food()

    while True:
        screen.fill(BLACK)
        snake.handle_keys()
        snake.move()

        for i in range (0, FOOD_PER_CYCLE):

            if snake.get_head_position() == food[i].position:
                if (food[i].isSuperFood == 1 ):
                    snake.length += LENGTH_PER_SUPERFOOD
                else:
                    snake.length += LENGTH_PER_FOOD

                food[i].change_position()
            
            food[i].draw(screen)


        snake.draw(screen)


        pygame.display.update()
        clock.tick(GAME_SPEED)

# Entry point
if __name__ == "__main__":
    main()
