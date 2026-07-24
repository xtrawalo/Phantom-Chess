import tkinter as tk

window = tk.Tk()
window.title("Phantom Chess")
window.geometry("500x500")
window.configure(background="black")


class Piece:
    def __init__(self, piece_type, color, position):
        self._piece_type = piece_type
        self.color = color
        self.position = position
        self.is_revealed = False

    def reveal(self):
        self.is_revealed = True

    def get_display_type(self, viewer_color):
        if self.is_revealed or viewer_color == self.color:
            return self._piece_type
        else:
            return "?"

    def get_legal_moves(self, board):
        moves = []
        row, col = position_to_row_col(self.position)

        if self._piece_type == "rook":
            directions = [(1,0),(-1,0),(0,1),(0,-1)]
        elif self._piece_type == "bishop":
            directions = [(1,1),(1,-1),(-1,1),(-1,-1)]
        elif self._piece_type == "queen":
            directions = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        else:
            directions = []

        for direction in directions:
            d_row, d_col = direction
            step = 1
            while True:
                new_row = row + d_row * step
                new_col = col + d_col * step
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                target_position = row_col_to_position(new_row, new_col)
                target_piece = board.squares[target_position]
                if target_piece is None:
                    moves.append(target_position)
                else:
                    if target_piece.color != self.color:
                        moves.append(target_position)
                    break
                step += 1

        if self._piece_type in ("rook", "bishop", "queen"):
            return moves

        if self._piece_type == "knight":
            knight_offsets = [
                (2,1),(2,-1),(-2,1),(-2,-1),
                (1,2),(1,-2),(-1,2),(-1,-2)
            ]
            for offset in knight_offsets:
                d_row, d_col = offset
                new_row = row + d_row
                new_col = col + d_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_position = row_col_to_position(new_row, new_col)
                    target_piece = board.squares[target_position]
                    if target_piece is None or target_piece.color != self.color:
                        moves.append(target_position)
            return moves

        if self._piece_type == "king":
            king_offsets = [
                (1,0),(-1,0),(0,1),(0,-1),
                (1,1),(1,-1),(-1,1),(-1,-1)
            ]
            for offset in king_offsets:
                d_row, d_col = offset
                new_row = row + d_row
                new_col = col + d_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_position = row_col_to_position(new_row, new_col)
                    target_piece = board.squares[target_position]
                    if target_piece is None or target_piece.color != self.color:
                        moves.append(target_position)
            return moves

        if self._piece_type == "pawn":
            if self.color == "white":
                forward = -1
                start_row = 6
            else:
                forward = 1
                start_row = 1

            one_step_row = row + forward
            if 0 <= one_step_row < 8:
                one_step_pos = row_col_to_position(one_step_row, col)
                if board.squares[one_step_pos] is None:
                    moves.append(one_step_pos)

                    if row == start_row:
                        two_step_row = row + forward * 2
                        two_step_pos = row_col_to_position(two_step_row, col)
                        if board.squares[two_step_pos] is None:
                            moves.append(two_step_pos)

            for d_col in (-1,1):
                new_row = row + forward
                new_col = col + d_col
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_position = row_col_to_position(new_row, new_col)
                    target_piece = board.squares[target_position]
                    if target_piece is not None and target_piece.color != self.color:
                        moves.append(target_position)
            return moves

        return moves


board_canvas = tk.Canvas(window, bg="black", height= 400, width= 400)
board_canvas.pack()

square_size = 400/8

def draw_board():
    for r in range(8):
        for c in range(8):
            x1 = 1.4 + c * square_size
            y1 = 1.4 + r * square_size
            x2 = x1 + square_size
            y2 = y1 + square_size
            if (c+r) % 2 == 0:
                square_color = "white"
            else:
                square_color = "grey"
            board_canvas.create_rectangle(x1, y1, x2, y2, fill=square_color)

draw_board()

class Board:
    def __init__(self):
        self.squares = {}
        for col in range(8):
            letter = chr(97 + col)
            for row in range(1,9):
                position = letter + str(row)
                self.squares[position] = None

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = "white"

    def setup_pieces(self):
        left_black_rook = Piece(piece_type= "rook", color= "black", position= "a8")
        self.board.squares["a8"] = left_black_rook
        right_black_rook = Piece(piece_type= "rook", color= "black", position= "h8")
        self.board.squares["h8"] = right_black_rook
        left_white_rook = Piece(piece_type= "rook", color= "white", position= "a1")
        self.board.squares["a1"] = left_white_rook
        right_white_rook = Piece(piece_type= "rook", color= "white", position= "h1")
        self.board.squares["h1"] = right_white_rook

        left_black_knight = Piece(piece_type= "knight", color= "black", position= "b8")
        self.board.squares["b8"] = left_black_knight
        right_black_knight = Piece(piece_type= "knight", color= "black", position= "g8")
        self.board.squares["g8"] = right_black_knight
        left_white_knight = Piece(piece_type= "knight", color= "white", position= "b1")
        self.board.squares["b1"] = left_white_knight
        right_white_knight = Piece(piece_type= "knight", color= "white", position= "g1")
        self.board.squares["g1"] = right_white_knight

        left_black_bishop = Piece(piece_type= "bishop", color= "black", position= "c8")
        self.board.squares["c8"] = left_black_bishop
        right_black_bishop = Piece(piece_type= "bishop", color= "black", position= "f8")
        self.board.squares["f8"] = right_black_bishop
        left_white_bishop = Piece(piece_type= "bishop", color= "white", position= "c1")
        self.board.squares["c1"] = left_white_bishop
        right_white_bishop = Piece(piece_type= "bishop", color= "white", position= "f1")
        self.board.squares["f1"] = right_white_bishop

        white_queen = Piece(piece_type= "queen", color= "white", position= "d1")
        self.board.squares["d1"] = white_queen
        black_queen = Piece(piece_type= "queen", color= "black", position= "d8")
        self.board.squares["d8"] = black_queen

        white_king = Piece(piece_type= "king", color= "white", position= "e1")
        self.board.squares["e1"] = white_king
        black_king = Piece(piece_type= "king", color= "black", position= "e8")
        self.board.squares["e8"] = black_king

        for letter in "abcdefgh":
            position = f"{letter}2"
            self.board.squares[position] = Piece(piece_type= "pawn", color= "white", position= position)

        for letter in "abcdefgh":
            position = f"{letter}7"
            self.board.squares[position] = Piece(piece_type= "pawn", color= "black", position= position)

def draw_pieces():
    for position, piece in game.board.squares.items():
        if piece is not None:
            row, col = position_to_row_col(position)
            x = col * square_size + square_size / 2
            y = row * square_size + square_size / 2
            label = piece.get_display_type(piece.color)
            board_canvas.create_text(x,y,text=label,font=("Arial",16,"bold"))

game = Game()
game.setup_pieces()

setup_mode = True
first_selected = None
selected_piece = None
game_over = False

def position_to_row_col(position):
    letter = position[0]
    number = position[1]
    col = ord(letter) - 97
    row = 8 - int(number)
    return row, col

def row_col_to_position(row, col):
    letter = chr(97 + col)
    position = letter + str(8 - row)
    return position

def swap_pieces(board, position_a, position_b):
    piece_a = board.squares[position_a]
    piece_b = board.squares[position_b]

    board.squares[position_a] = piece_b
    board.squares[position_b] = piece_a

    if piece_a is not None:
        piece_a.position = position_b
    if piece_b is not None:
        piece_b.position = position_a

def is_king_in_check(board, king_color):
    king_position = None
    for position, piece in board.squares.items():
        if piece is not None and piece._piece_type == "king" and piece.color == king_color:
            king_position = position
    for position, piece in board.squares.items():
        if piece is not None and piece.color != king_color:
            enemy_moves = piece.get_legal_moves(board)
            if king_position in enemy_moves:
                return True
    return False

def is_checkmate(board, player_color):
    if not is_king_in_check(board, player_color):
        return False

    for position, piece in list(board.squares.items()):
        if piece is not None and piece.color == player_color:
            legal_moves = piece.get_legal_moves(board)
            for move in legal_moves:
                old_position = piece.position
                captured_piece = board.squares[move]

                board.squares[old_position] = None
                board.squares[move] = piece
                piece.position = move

                still_in_check = is_king_in_check(board, player_color)

                board.squares[old_position] = piece
                board.squares[move] = captured_piece
                piece.position = old_position

                if not still_in_check:
                    return False

    return True

def redraw_everything():
    board_canvas.delete("all")
    draw_board()
    draw_pieces()

def on_click(event):
    global first_selected, selected_piece, game_over
    if game_over:
        return

    col = event.x // square_size
    row = event.y // square_size
    letter = chr(97 + int(col))
    position = letter + str(8-int(row))

    if setup_mode:
        if first_selected is None:
            first_selected = position
            print("Selected", position)
        else:
            swap_pieces(game.board, first_selected, position)
            print("Swapped", first_selected,"and",position)
            first_selected = None
            redraw_everything()
        return

    if selected_piece is None:
        clicked_piece = game.board.squares[position]
        if clicked_piece is not None and clicked_piece.color == game.current_player:
            selected_piece = clicked_piece
            print("Selected piece at", position)
        else:
            print("Invalid Selection")
    else:
        legal_moves = selected_piece.get_legal_moves(game.board)
        if position in legal_moves:
            old_position = selected_piece.position
            game.board.squares[old_position] = None
            game.board.squares[position] = selected_piece
            selected_piece.position = position

            if not selected_piece.is_revealed:
                selected_piece.reveal()

            switch_turn()
            redraw_everything()
            if is_checkmate(game.board, game.current_player):
                game_over = True
                print("Checkmate!", game.current_player, "loses.")
        else:
            print("Illegal Move")

        selected_piece = None

def switch_turn():
    if game.current_player == "white":
        game.current_player = "black"
    else:
        game.current_player = "white"
    print("Turn is now:", game.current_player)

def end_setup():
    global setup_mode, first_selected
    setup_mode = False
    first_selected = None
    print("Setup Completed! Game Starting. White's turn")

switch_turn_button = tk.Button(window, text="End Turn", command=switch_turn)
switch_turn_button.pack()

end_setup_button = tk.Button(window, text="Done Arranging", command=end_setup)
end_setup_button.pack()

board_canvas.bind("<Button-1>", on_click)

draw_pieces()

window.mainloop()
