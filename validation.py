from position import Position

def compare_positions(pos1: Position, pos2: Position) -> list[str]:
    diffs = []

    # Board
    for y in range(8):
        for x in range(8):
            p1 = pos1.board[y][x]
            p2 = pos2.board[y][x]
            if (p1 is None) != (p2 is None):
                diffs.append(f"Square {x},{y}: {p1} vs {p2}")
            elif p1 is not None and (
                type(p1) != type(p2) or p1.color != p2.color
            ):
                diffs.append(f"Square {x},{y}: {p1} vs {p2}")

    # En passant
    if pos1.en_passant_square != pos2.en_passant_square:
        diffs.append(f"En passant: {pos1.en_passant_square} vs {pos2.en_passant_square}")

    # Castling rights
    if pos1.castling_rights != pos2.castling_rights:
        diffs.append(f"Castling rights: {pos1.castling_rights} vs {pos2.castling_rights}")

    return diffs