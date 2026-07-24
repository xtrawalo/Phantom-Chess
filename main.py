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
        if self._piece_type == "rook":
            directions = [(1,0),(-1,0),(0,1),(0,-1)]
            row, col = position_to_row_col(self.position)
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
            return moves
        elif self._piece_type == "knight":
            return ["Placeholder: knight moves"]
        elif self._piece_type == "bishop":
            return ["Placeholder: bishop moves"]
        elif self._piece_type == "queen":
            return ["Placeholder: queen moves"]
        elif self._piece_type == "king":
            return ["Placeholder: king moves"]
        else:
            return ["Placeholder: generic moves"]



board_canvas = tk.Canvas(window, bg="black", height= 400, width= 400)
board_canvas.pack()

square_size = 400/8
for row in range(8):
    for col in range(8):
        x1 = 1.4 + col * square_size
        y1 = 1.4 + row * square_size
        x2 = x1 + square_size
        y2 = y1 + square_size
        if (col+row) % 2 == 0:
            color = "white"
        else:
            color = "grey"
        board_canvas.create_rectangle(x1, y1, x2, y2, fill=color)

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

def on_click(event):
    col = event.x // square_size
    row = event.y // square_size
    letter = chr(97 + int(col))
    position = letter + str(8 - int(row))
    print(position)
    clicked_piece = game.board.squares[position]
    if clicked_piece is not None:
        if clicked_piece.color != game.current_player:
            print("Not your turn!")
        else:
            print("Valid Piece, your turn!")

def switch_turn():
    if game.current_player == "white":
        game.current_player = "black"
    else:
        game.current_player = "white"
    print("Turn is now:",game.current_player)

switch_turn_button = tk.Button(window, text="End Turn", command=switch_turn)
switch_turn_button.pack()

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

board_canvas.bind("<Button-1>", on_click)

draw_pieces()

window.mainloop()
