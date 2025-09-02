import pygame
import os

# Constants
BOARD_SIZE = 640
MARGIN_LEFT = 40
MARGIN_BOTTOM = 40
MARGIN_TOP = 20
MARGIN_RIGHT = 20
WIDTH = BOARD_SIZE + MARGIN_LEFT + MARGIN_RIGHT
HEIGHT = BOARD_SIZE + MARGIN_TOP + MARGIN_BOTTOM
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS
BOARD_COLOR_1 = (240, 217, 181)
BOARD_COLOR_2 = (181, 136, 99)
BG_COLOR = (19, 19, 19)
COORD_COLOR = (130, 130, 130)

# Piece symbols and their image filenames
PIECE_IMAGES = {
    "bR": "br.png", "bN": "bn.png", "bB": "bb.png", "bQ": "bq.png", "bK": "bk.png", "bP": "bp.png",
    "wR": "wr.png", "wN": "wn.png", "wB": "wb.png", "wQ": "wq.png", "wK": "wk.png", "wP": "wp.png"
}

# Starting board setup
START_BOARD = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP"] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ["wP"] * 8,
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

def load_images():
    images = {}
    assets_path = os.path.join(os.path.dirname(__file__), "assets")
    for piece, filename in PIECE_IMAGES.items():
        img_path = os.path.join(assets_path, filename)
        image = pygame.image.load(img_path)
        images[piece] = pygame.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
    return images

def draw_board(win):
    # Draw background
    win.fill(BG_COLOR)
    # Draw chessboard
    for row in range(ROWS):
        for col in range(COLS):
            color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2
            rect = (
                MARGIN_LEFT + col * SQUARE_SIZE,
                MARGIN_TOP + row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
            pygame.draw.rect(win, color, rect)

def draw_pieces(win, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                x = MARGIN_LEFT + col * SQUARE_SIZE
                y = MARGIN_TOP + row * SQUARE_SIZE
                win.blit(images[piece], (x, y))

def draw_coordinates(win, font):
    # Letters (a-h) below the board
    for col in range(COLS):
        letter = chr(ord('a') + col)
        text = font.render(letter, True, COORD_COLOR)
        x = MARGIN_LEFT + col * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2
        y = MARGIN_TOP + BOARD_SIZE + 5
        win.blit(text, (x, y))
    # Numbers (1-8) to the left of the board
    for row in range(ROWS):
        number = str(8 - row)
        text = font.render(number, True, COORD_COLOR)
        x = MARGIN_LEFT - text.get_width() - 5
        y = MARGIN_TOP + row * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2
        win.blit(text, (x, y))

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess GUI")
    images = load_images()
    board = [row[:] for row in START_BOARD]
    font = pygame.font.SysFont("arial", 24, bold=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(win)
        draw_pieces(win, board, images)
        draw_coordinates(win, font)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()