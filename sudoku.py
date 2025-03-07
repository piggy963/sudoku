import pygame
import random

WIDTH = 900
HEIGHT = 900
CONTROLS_SPACE = 200
LINE_WIDTH = 5
LINE_COLOUR = (0, 0, 0)
GREY = (125, 125, 125)
DIFFICULTY = 60 # percent of the grid that will be unfilled
 
pygame.init()
random.seed()
FONT = pygame.font.SysFont("Arial", 60)
BUTTON_FONT = pygame.font.SysFont("Arial", 36)
screen = pygame.display.set_mode((WIDTH, HEIGHT + CONTROLS_SPACE))
pygame.display.set_caption('SUDOKU')

# draw lines to separate screen into grids
def draw_grid():
    for i in range(9):
        pygame.draw.line(screen, LINE_COLOUR, ((HEIGHT / 9) * i, 0), ((HEIGHT / 9) * i, WIDTH))
        pygame.draw.line(screen, LINE_COLOUR, (0, (WIDTH / 9) * i), (HEIGHT, (WIDTH / 9) * i))

    pygame.draw.line(screen, LINE_COLOUR, (HEIGHT / 3, 0), (HEIGHT / 3, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, ((HEIGHT / 3) * 2, 0), ((HEIGHT / 3) * 2, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (HEIGHT, 0), (HEIGHT, WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (0, WIDTH / 3), (HEIGHT, WIDTH / 3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (0, (WIDTH / 3) * 2), (HEIGHT, (WIDTH / 3) * 2), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOUR, (0, WIDTH), (HEIGHT, WIDTH), LINE_WIDTH)

    return 0

# initialise boards
board = [[0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
         [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0]]

solution = [[0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0]]

fixed_cells = [[0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0],
            [0 ,0 ,0 ,0 ,0 ,0, 0, 0, 0]]

# initialise solution
def initialise_grids():
    for i in range(9):
        for j in range(9):
            solution[i][j] = 0
            board[i][j] = 0
            fixed_cells[i][j] = 0

# check if a number can be placed at a cell
def is_safe(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
        
    startRow = (row // 3) * 3
    startCol = (col // 3) * 3

    for j in range(3):
        for k in range(3):
            if board[j + startRow][k + startCol] == num:
                return False
    
    return True

# initialise numbers set to be a random sequence so that a different puzzle is generated everytime
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
def shuffle_numbers():
    random.shuffle(numbers)
    return numbers

numbers = shuffle_numbers()

# given a board, try to solve it. return true when the entire board is solved.
def solve_sudoku(board, row=0, col=0):
    # Base case: If row exceeds 8, the board is fully filled
    if row == 9:
        return True
    
    # Move to the next row when column exceeds 8
    if col == 9:
        return solve_sudoku(board, row + 1, 0)
    
    # Skip already filled cells
    if board[row][col] != 0:
        return solve_sudoku(board, row, col + 1)
    
    # Try numbers 1 to 9
    for num in numbers:  # Numbers from 1 to 9
        if is_safe(board, row, col, num):  # Check if num is safe
            board[row][col] = num  # Place the number
            print(f"Trying {num} at {row}, {col}...")
            
            # Recursively solve for the next cell
            if solve_sudoku(board, row, col + 1):
                return True  # If solved, return True
            
            board[row][col] = 0  # Backtrack (reset the cell)
    
    return False  # Trigger backtracking

def generate_solved_grid():
    initialise_grids()
    print("Generating valid board...")

    numbers = shuffle_numbers()
    solve_sudoku(solution, 0, 0)
    print("Valid board generated! Solution:")
    print(solution)

    # copy solution to the board
    for k in range(9):
        for l in range(9):
            board[k][l] = solution[k][l]

    # randomly knock out cells according to difficulty
    for i in range(9):
        for j in range(9):
            num = random.randint(1, 100)
            if num < DIFFICULTY:
                board[i][j] = 0

    # mark computer generated cells in fixed_cells
    for a in range(9):
        for b in range(9):
            if board[a][b] != 0:
                fixed_cells[a][b] = 1

generate_solved_grid()
    
#handle cell selection and highlighting
def select_cell():
    global selected_cell
    mouse_x, mouse_y = pygame.mouse.get_pos()
    cell_x = mouse_x // (WIDTH // 9)
    cell_y = mouse_y // (HEIGHT // 9)

    selected_cell = (cell_x, cell_y)
    
def draw_selected_cell():
    if selected_cell is not None:
        cell_colour = (247, 243, 181)
        cell_x, cell_y = selected_cell
        pygame.draw.rect(screen, cell_colour, (cell_x * (WIDTH // 9) + 1, cell_y * (HEIGHT // 9) + 2, WIDTH // 9 - 2, HEIGHT // 9 - 2))

def draw_numbers():
    for row in range(9):
        for col in range(9):
            number = board[row][col]
            if number != 0:
                if fixed_cells[row][col] == 1:
                    text = FONT.render(str(number), True, GREY)
                else:
                    text = FONT.render(str(number), True, LINE_COLOUR)
                screen.blit(text, ((row * (WIDTH / 9) + 35), (col * (HEIGHT / 9)) + 20))

# checks if the board is the same as the solution
def check_win():
    for i in range(9):
        for j in range(9):
            if board[i][j] != solution[i][j]:
                return False
            
    return True

def display_win():
    # Draw a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Draw a rectangle for the win message
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH // 4, HEIGHT // 3, WIDTH // 2, HEIGHT // 3))
    
    # Draw "You Win!" text
    text = FONT.render("You Win!", True, LINE_COLOUR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text
    screen.blit(text, text_rect)
    
    # Update the display
    pygame.display.update()

# regenerate board, difficulty slider
def draw_buttons():
    # Draw "Regen" button
    regen_button_rect = pygame.Rect(WIDTH // 16, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)
    pygame.draw.rect(screen, (255, 255, 255), regen_button_rect)
    regen_text = BUTTON_FONT.render("Reset", True, LINE_COLOUR)
    regen_text_rect = regen_text.get_rect(center=regen_button_rect.center)
    screen.blit(regen_text, regen_text_rect)

    # Draw "Easy" button
    easy_button_rect = pygame.Rect((WIDTH // 8) * 2, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)
    pygame.draw.rect(screen, (255, 255, 255), easy_button_rect)
    easy_text = BUTTON_FONT.render("Easy", True, LINE_COLOUR)
    easy_text_rect = easy_text.get_rect(center=easy_button_rect.center)
    screen.blit(easy_text, easy_text_rect)

    # Draw "Medium" button
    medium_button_rect = pygame.Rect((WIDTH // 8) * 4, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)
    pygame.draw.rect(screen, (255, 255, 255), medium_button_rect)
    medium_text = BUTTON_FONT.render("Medium", True, LINE_COLOUR)
    medium_text_rect = medium_text.get_rect(center=medium_button_rect.center)
    screen.blit(medium_text, medium_text_rect)

    # Draw "Hard" button
    hard_button_rect = pygame.Rect((WIDTH // 8) * 6, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)
    pygame.draw.rect(screen, (255, 255, 255), hard_button_rect)
    hard_text = BUTTON_FONT.render("Hard", True, LINE_COLOUR)
    hard_text_rect = hard_text.get_rect(center=hard_button_rect.center)
    screen.blit(hard_text, hard_text_rect)

def handle_button_click(mouse_pos):
    regen_button_rect = pygame.Rect(WIDTH // 16, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)
    easy_button_rect = pygame.Rect((WIDTH // 8) * 2, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)
    medium_button_rect = pygame.Rect((WIDTH // 8) * 4, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)
    hard_button_rect = pygame.Rect((WIDTH // 8) * 6, HEIGHT + CONTROLS_SPACE // 4, WIDTH // 4, CONTROLS_SPACE // 3)

    if regen_button_rect.collidepoint(mouse_pos):
        return "regen"
    elif easy_button_rect.collidepoint(mouse_pos):
        return "easy"
    elif medium_button_rect.collidepoint(mouse_pos):
        return "medium"
    elif hard_button_rect.collidepoint(mouse_pos):
        return "hard"
    return None

# Run game loop
running = True
selected_cell = None  # Initialize selected cell

while running:
    screen.fill((255, 255, 255))  # Clear screen before redrawing

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < WIDTH and mouse_pos[1] < HEIGHT:
                select_cell()  # Update selected cell on mouse click
            action = handle_button_click(mouse_pos)
            if action == "regen":
                generate_solved_grid()
            elif action == "easy":
                DIFFICULTY = 30
            elif action == "medium":
                DIFFICULTY = 45
            elif action == "hard":
                DIFFICULTY = 60

        elif event.type == pygame.KEYDOWN:
            if selected_cell is not None:
                row, col = selected_cell
                if event.key == pygame.K_BACKSPACE:  # Handle backspace
                    board[row][col] = 0
                elif pygame.K_1 <= event.key <= pygame.K_9:  # Handle numbers 1-9
                    if fixed_cells[row][col] == 0:
                        num = event.key - pygame.K_0
                        board[row][col] = num
                elif pygame.K_KP1 <= event.key <= pygame.K_KP9:  # Handle numpad numbers 1-9
                    if fixed_cells[row][col] == 0:
                        num = event.key - pygame.K_0
                        board[row][col] = num

    draw_grid()  # Redraw grid every frame
    draw_selected_cell()  # Draw highlight if a cell is selected
    draw_numbers()
    draw_buttons()

    # check if the puzzle is complete
    if check_win():
        display_win()

    pygame.display.update()  # Refresh the display

pygame.quit()