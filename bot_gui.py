import pygame
import os
import time
from position import Position
from movegen import get_pseudo_legal_moves, filter_legal_moves
from schemas import ChessColor
from evaluation import evaluate_position
from bot import ChessBot

# Constants
BOARD_SIZE = 640
MARGIN_LEFT = 60
MARGIN_BOTTOM = 60
MARGIN_TOP = 40
MARGIN_RIGHT = 40
WIDTH = BOARD_SIZE + MARGIN_LEFT + MARGIN_RIGHT
HEIGHT = BOARD_SIZE + MARGIN_TOP + MARGIN_BOTTOM
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_SIZE // COLS
BOARD_COLOR_1 = (235, 236, 208)
BOARD_COLOR_2 = (119, 149, 86)
BG_COLOR = (32, 32, 32)
COORD_COLOR = (200, 200, 200)
COORD_FONT_SIZE = 28

PIECE_IMAGES = {
    "bR": "br.png", "bN": "bn.png", "bB": "bb.png", "bQ": "bq.png", "bK": "bk.png", "bP": "bp.png",
    "wR": "wr.png", "wN": "wn.png", "wB": "wb.png", "wQ": "wq.png", "wK": "wk.png", "wP": "wp.png"
}

def load_images():
    images = {}
    assets_path = os.path.join(os.path.dirname(__file__), "assets")
    for piece, filename in PIECE_IMAGES.items():
        img_path = os.path.join(assets_path, filename)
        image = pygame.image.load(img_path).convert_alpha()
        images[piece] = pygame.transform.smoothscale(image, (SQUARE_SIZE, SQUARE_SIZE))
    return images

def load_sounds():
    assets_path = os.path.join(os.path.dirname(__file__), "assets", "sound")
    move_sound = pygame.mixer.Sound(os.path.join(assets_path, "piece_move.wav"))
    ambient_sound = pygame.mixer.Sound(os.path.join(assets_path, "ambient.wav"))
    return move_sound, ambient_sound

def draw_board(win, selected=None, moves=None):
    win.fill(BG_COLOR)
    shadow_offset = 8
    shadow_rect = (MARGIN_LEFT + shadow_offset, MARGIN_TOP + shadow_offset, BOARD_SIZE, BOARD_SIZE)
    pygame.draw.rect(win, (20, 20, 20), shadow_rect, border_radius=12)
    board_rect = (MARGIN_LEFT, MARGIN_TOP, BOARD_SIZE, BOARD_SIZE)
    pygame.draw.rect(win, (50, 50, 50), board_rect, border_radius=12)
    for row in range(ROWS):
        for col in range(COLS):
            color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2
            rect = (MARGIN_LEFT + col * SQUARE_SIZE, MARGIN_TOP + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(win, color, rect)
            if selected == (col, row):
                pygame.draw.rect(win, (246, 246, 105), rect, 6, border_radius=8)
    if moves:
        dot_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(dot_surface, (120,120,120,120), (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 6)
        for move in moves:
            tx, ty = move.target.x, move.target.y
            x = MARGIN_LEFT + tx * SQUARE_SIZE
            y = MARGIN_TOP + ty * SQUARE_SIZE
            win.blit(dot_surface, (x, y))

def draw_coordinates(win, font):
    for col in range(COLS):
        letter = chr(ord('a') + col)
        text = font.render(letter, True, COORD_COLOR)
        x = MARGIN_LEFT + col * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2
        y = MARGIN_TOP + BOARD_SIZE + 12
        win.blit(text, (x, y))
    for row in range(ROWS):
        number = str(8 - row)
        text = font.render(number, True, COORD_COLOR)
        x = MARGIN_LEFT - text.get_width() - 12
        y = MARGIN_TOP + row * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_height() // 2
        win.blit(text, (x, y))

def draw_pieces(win, board, images):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                color = 'w' if piece.color == ChessColor.WHITE else 'b'
                ptype = {
                    'Pawn': 'P',
                    'Knight': 'N',
                    'Bishop': 'B',
                    'Rook': 'R',
                    'Queen': 'Q',
                    'King': 'K'
                }.get(piece.__class__.__name__, '?')
                img_key = color + ptype
                x = MARGIN_LEFT + col * SQUARE_SIZE
                y = MARGIN_TOP + row * SQUARE_SIZE
                win.blit(images[img_key], (x, y))


def animate_move(win, images, position, move, piece_map, font):
    origin_x = MARGIN_LEFT + move.origin.x * SQUARE_SIZE
    origin_y = MARGIN_TOP + move.origin.y * SQUARE_SIZE
    target_x = MARGIN_LEFT + move.target.x * SQUARE_SIZE
    target_y = MARGIN_TOP + move.target.y * SQUARE_SIZE
    color = 'w' if position.board[move.origin.y][move.origin.x].color == ChessColor.WHITE else 'b'
    ptype = piece_map.get(position.board[move.origin.y][move.origin.x].__class__.__name__, '?')
    img_key = color + ptype
    frames = 12
    for i in range(frames):
        x = origin_x + (target_x - origin_x) * i / frames
        y = origin_y + (target_y - origin_y) * i / frames
        draw_board(win)
        for row in range(ROWS):
            for col in range(COLS):
                if (row, col) == (move.origin.y, move.origin.x):
                    continue
                piece = position.board[row][col]
                if piece:
                    c = 'w' if piece.color == ChessColor.WHITE else 'b'
                    pt = piece_map.get(piece.__class__.__name__, '?')
                    k = c + pt
                    win.blit(images[k], (MARGIN_LEFT + col * SQUARE_SIZE, MARGIN_TOP + row * SQUARE_SIZE))
        win.blit(images[img_key], (x, y))
        draw_coordinates(win, font)
        pygame.display.flip()
        pygame.time.delay(20)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess.com Style Chess GUI")
    images = load_images()
    font = pygame.font.SysFont("arial", COORD_FONT_SIZE, bold=True)
    pygame.mixer.init()
    move_sound, ambient_sound = load_sounds()
    ambient_sound.play(loops=-1)

    position = Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    turn = ChessColor.WHITE

    selected = None
    legal_moves = []
    piece_map = {'Pawn': 'P', 'Knight': 'N', 'Bishop': 'B', 'Rook': 'R', 'Queen': 'Q', 'King': 'K'}

    bot = ChessBot()
    BOT_DEPTH = 2

    move_num = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn == ChessColor.WHITE:
                mx, my = event.pos
                bx = (mx - MARGIN_LEFT) // SQUARE_SIZE
                by = (my - MARGIN_TOP) // SQUARE_SIZE
                if 0 <= bx < 8 and 0 <= by < 8:
                    piece = position.board[by][bx]
                    if selected:
                        for move in legal_moves:
                            if move.target.x == bx and move.target.y == by:
                                animate_move(win, images, position, move, piece_map, font)
                                position.move(move)
                                move_num += 1
                                score = evaluate_position(position)
                                print("Player evaluation:", score)
                                move_sound.play()
                                turn = ChessColor.BLACK
                                selected = None
                                legal_moves = []
                                break
                        else:
                            if piece and piece.color == turn:
                                selected = (bx, by)
                                pseudo_moves = get_pseudo_legal_moves(position, turn)
                                filtered_moves = [m for m in pseudo_moves if m.origin.x == bx and m.origin.y == by]
                                legal_moves = filter_legal_moves(position, turn, filtered_moves)
                            else:
                                selected = None
                                legal_moves = []
                    else:
                        if piece and piece.color == turn:
                            selected = (bx, by)
                            pseudo_moves = get_pseudo_legal_moves(position, turn)
                            filtered_moves = [m for m in pseudo_moves if m.origin.x == bx and m.origin.y == by]
                            legal_moves = filter_legal_moves(position, turn, filtered_moves)
                        else:
                            selected = None
                            legal_moves = []

                    draw_board(win, selected, legal_moves)
                    draw_pieces(win, position.board, images)
                    draw_coordinates(win, font)
                    pygame.display.flip()

        # Bot move
        if turn == ChessColor.BLACK:
            pygame.time.delay(300)
            if move_num >= 50:
                #BOT_DEPTH = 3
                pass
            bot_move = bot.find_best_move(position, BOT_DEPTH, ChessColor.BLACK)
            if bot_move:
                animate_move(win, images, position, bot_move, piece_map, font)
                position.move(bot_move)
                print(f"bot move for depth {BOT_DEPTH}")
                move_num += 1
                score = evaluate_position(position)
                print("Bot evaluation:", score)
                move_sound.play()
            turn = ChessColor.WHITE

        draw_board(win, selected, legal_moves)
        draw_pieces(win, position.board, images)
        draw_coordinates(win, font)
        pygame.display.flip()

    ambient_sound.stop()
    pygame.quit()

if __name__ == "__main__":
    main()