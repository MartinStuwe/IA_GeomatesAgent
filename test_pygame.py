import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('World Renderer with Rolling & Jumping Navmesh')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
NAVMESH_COLOR = (0, 255, 0)  # Green for walkable areas

# World data (as per your description)
world_data = {
    'RECT': {'middle_x': 70.0, 'middle_y': 25.0, 'width': 8.0, 'height': 8.0, 'rotation': -0.0, 'id': 0},
    'DISC': {'x': 10.0, 'y': 22.5, 'radius': 1.5, 'id': 0},
    'DIAMONDS': [{'x': 20, 'y': 26}, {'x': 60, 'y': 26}, {'x': 35, 'y': 10}],
    'PLATFORMS': [{'x_start': 0, 'y_start': 0, 'x_end': 80, 'y_end': 1}, 
                  {'x_start': 0, 'y_start': 39, 'x_end': 80, 'y_end': 40}, 
                  {'x_start': 0, 'y_start': 1, 'x_end': 1, 'y_end': 40}, 
                  {'x_start': 79, 'y_start': 1, 'x_end': 80, 'y_end': 40}, 
                  {'x_start': 1, 'y_start': 20, 'x_end': 30, 'y_end': 21}, 
                  {'x_start': 40, 'y_start': 20, 'x_end': 79, 'y_end': 21}]
}

# Grid dimensions and step size
GRID_SIZE = 10  # size of each grid cell in pixels
JUMP_HEIGHT = 10  # max jump height the disc can handle

# Function to convert world coordinates to screen coordinates
def world_to_screen(x, y):
    return int(x * GRID_SIZE), screen_height - int(y * GRID_SIZE)

# Function to create a 2D side-view navmesh with reachable positions
def generate_reachable_positions():
    # Get the disc's current position
    disc_x = world_data['DISC']['x']
    disc_y = world_data['DISC']['y']

    reachable_positions = []

    # Rolling: Check if the disc can move to the left or right along the current platform
    for platform in world_data['PLATFORMS']:
        # Check if the disc is currently on this platform
        if platform['x_start'] <= disc_x <= platform['x_end'] and platform['y_start'] <= disc_y <= platform['y_end']:
            # The disc can roll left or right along the platform
            for dx in [-1, 1]:  # Roll left (-1) or right (1)
                new_x = disc_x + dx * 1  # Move 1 unit in the x-direction
                if platform['x_start'] <= new_x <= platform['x_end']:
                    reachable_positions.append((new_x, disc_y))

    # Jumping Up: Check if the disc can jump up to another platform above it
    for platform in world_data['PLATFORMS']:
        if platform['y_end'] > disc_y:  # Check if platform is above the disc
            x_gap = abs(disc_x - (platform['x_start'] + platform['x_end']) / 2)
            y_gap = platform['y_end'] - disc_y  # Vertical distance to jump (platform is above the disc)

            if x_gap <= 30 and y_gap <= JUMP_HEIGHT:  # Jump up if the gap is small enough
                reachable_positions.append((platform['x_start'] + platform['x_end']) / 2, platform['y_end'])

    # Falling Down: Check if the disc is falling and find the closest platform below it
    for platform in world_data['PLATFORMS']:
        if platform['y_start'] < disc_y:  # Platform is below the disc
            x_gap = abs(disc_x - (platform['x_start'] + platform['x_end']) / 2)
            y_gap = disc_y - platform['y_start']  # Vertical distance to fall (platform is below the disc)

            if x_gap <= 30 and y_gap <= JUMP_HEIGHT:  # Fall down if the gap is small enough
                reachable_positions.append(((platform['x_start'] + platform['x_end']) / 2, platform['y_start']))

    return reachable_positions

# Function to render the world and reachable positions
def render_world(reachable_positions):
    screen.fill(WHITE)  # Fill screen with white

    # Render the reachable positions (green for walkable areas)
    for pos in reachable_positions:
        screen_x, screen_y = world_to_screen(pos[0], pos[1])
        pygame.draw.circle(screen, NAVMESH_COLOR, (screen_x, screen_y), 5)

    # Render the platforms as rectangles (side view)
    for platform in world_data['PLATFORMS']:
        platform_width = (platform['x_end'] - platform['x_start']) * GRID_SIZE
        platform_height = (platform['y_end'] - platform['y_start']) * GRID_SIZE
        pygame.draw.rect(screen, BLACK, 
                         (platform['x_start'] * GRID_SIZE, screen_height - int(platform['y_end'] * GRID_SIZE), 
                          platform_width, platform_height))

    # Render the disc
    pygame.draw.circle(screen, BLUE, world_to_screen(world_data['DISC']['x'], world_data['DISC']['y']),
                       int(world_data['DISC']['radius'] * GRID_SIZE))

    # Render the diamonds
    for diamond in world_data['DIAMONDS']:
        pygame.draw.circle(screen, GOLD, world_to_screen(diamond['x'], diamond['y']), 5)

    # Render the rectangle (the main object)
    rect = world_data['RECT']
    pygame.draw.rect(screen, RED, 
                     (int((rect['middle_x'] - rect['width'] / 2) * GRID_SIZE), 
                      screen_height - int((rect['middle_y'] + rect['height'] / 2) * GRID_SIZE),
                      int(rect['width'] * GRID_SIZE), 
                      int(rect['height'] * GRID_SIZE)))

    pygame.display.update()

# Main game loop
def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Generate reachable positions based on the current disc position
        reachable_positions = generate_reachable_positions()

        # Render the world and reachable positions
        render_world(reachable_positions)

        pygame.time.Clock().tick(60)  # Limit to 60 frames per second

    pygame.quit()
    sys.exit()

# Start the game loop
game_loop()



    