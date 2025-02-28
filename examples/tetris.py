from matrix_library import shapes as s, canvas as c
import time
import random
import keyboard  # Klavye girişleri için

# Ekran boyutu
WIDTH, HEIGHT = 10, 20  # Tetris grid dimensions

# Blok şekilleri
TETROMINOS = {
    "I": [[(0, 1), (1, 1), (2, 1), (3, 1)]],  
    "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]],  
    "T": [[(0, 1), (1, 0), (1, 1), (2, 1)]],  
    "L": [[(0, 0), (0, 1), (1, 1), (2, 1)]],  
    "J": [[(2, 0), (0, 1), (1, 1), (2, 1)]],  
    "S": [[(1, 0), (2, 0), (0, 1), (1, 1)]],  
    "Z": [[(0, 0), (1, 0), (1, 1), (2, 1)]]  
}

# Renkler (RGB formatında)
COLORS = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (128, 0, 128),
    "L": (255, 165, 0),
    "J": (0, 0, 255),
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
}

class Tetris:
    def __init__(self):
        self.canvas = c.Canvas()
        self.board = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]
        self.current_piece = self.get_new_piece()
        self.game_over = False

    def get_new_piece(self):
        """Rastgele yeni bir tetromino oluşturur."""
        shape = random.choice(list(TETROMINOS.keys()))
        color = COLORS[shape]
        piece = TETROMINOS[shape][0]  
        x_offset, y_offset = WIDTH // 2 - 1, 0  
        return {"shape": shape, "coords": [(x + x_offset, y + y_offset) for x, y in piece], "color": color}

    def move_piece(self, dx, dy):
        """Blokları sola, sağa veya aşağı hareket ettirir."""
        new_coords = [(x + dx, y + dy) for x, y in self.current_piece["coords"]]
        if self.is_valid_position(new_coords):
            self.current_piece["coords"] = new_coords

    def rotate_piece(self):
        """Blokları döndürür."""
        shape = self.current_piece["shape"]
        if shape == "O":
            return
        
        pivot = self.current_piece["coords"][1]  
        new_coords = [(pivot[0] - (y - pivot[1]), pivot[1] + (x - pivot[0])) for x, y in self.current_piece["coords"]]

        if self.is_valid_position(new_coords):
            self.current_piece["coords"] = new_coords

    def is_valid_position(self, coords):
        """Blokların çarpışma ve sınır kontrolü."""
        for x, y in coords:
            if x < 0 or x >= WIDTH or y >= HEIGHT or (y >= 0 and self.board[y][x] is not None):
                return False
        return True

    def place_piece(self):
        """Blok yere çarptığında onu tahtaya ekler."""
        for x, y in self.current_piece["coords"]:
            if y < 0:  
                self.game_over = True
                return
            
            self.board[y][x] = self.current_piece["color"]

        self.clear_lines()
        self.current_piece = self.get_new_piece()

    def clear_lines(self):
        """Tam dolu satırları temizler."""
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared_lines = HEIGHT - len(new_board)
        self.board = [[None for _ in range(WIDTH)] for _ in range(cleared_lines)] + new_board

    def draw(self):
        """Canvas'ı günceller."""
        self.canvas.clear()
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.board[y][x]:
                    square = s.Polygon(
                        [(x * 6, y * 6), (x * 6 + 6, y * 6), (x * 6 + 6, y * 6 + 6), (x * 6, y * 6 + 6)],
                        self.board[y][x]
                    )
                    self.canvas.add(square)

        for x, y in self.current_piece["coords"]:
            if y >= 0:
                square = s.Polygon(
                    [(x * 6, y * 6), (x * 6 + 6, y * 6), (x * 6 + 6, y * 6 + 6), (x * 6, y * 6 + 6)],
                    self.current_piece["color"]
                )
                self.canvas.add(square)

        self.canvas.draw()

    def update(self):
        """Oyun güncellemesi."""
        if not self.is_valid_position([(x, y + 1) for x, y in self.current_piece["coords"]]):
            self.place_piece()
        else:
            self.move_piece(0, 1)

    def handle_input(self):
        """Kullanıcıdan tuş girişlerini alır."""
        if keyboard.is_pressed("left"):
            self.move_piece(-1, 0)
        if keyboard.is_pressed("right"):
            self.move_piece(1, 0)
        if keyboard.is_pressed("down"):
            self.move_piece(0, 1)
        if keyboard.is_pressed("up"):
            self.rotate_piece()

    def play(self):
        """Oyun döngüsü."""
        while not self.game_over:
            self.handle_input()  # Kullanıcı girişlerini kontrol et
            self.update()
            self.draw()
            time.sleep(0.5)

        self.canvas.clear()
        self.canvas.add(s.Phrase("GAME OVER", [16, 64], (255, 0, 0)))
        self.canvas.draw()
        time.sleep(2)

if __name__ == "__main__":
    tetris = Tetris()
    tetris.play()
