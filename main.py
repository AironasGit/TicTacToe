import pygame

class WinningLine:
    color = (1, 100, 32)
    def __init__(self, start_pos, end_pos, width):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width

class Cell:
    id: tuple[int, int]
    rect: pygame.Rect
    background_colour = (128, 128, 128)
    sign_color = (27, 27, 27)
    is_occupied: bool = False
    occupied_by: str = ''
    def __init__(self, rect: pygame.Rect, id: tuple[int, int]):
        self.rect = rect
        self.id = id

class TicTacToe:
    current_player: str = 'o'
    window_width: int
    window_height: int
    window: pygame.Surface
    grid: list[list[Cell]] = []
    grid_size: int
    grid_size_px: int = 600
    current_hovered_cell: Cell
    winning_line: WinningLine = None
    def __init__(self, size: int):
        self.__init_window()
        self.grid_size = size
        self.__create_grid()
    
    def __init_window(self):
        window_background_colour = (18, 18, 18)
        ratio = 80
        self.window_width, self.window_height = 16*ratio, 9*ratio
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('TicTacToe')
        self.window.fill(window_background_colour)
        pygame.display.flip()
    
    def draw_grid(self):
        for row in self.grid:
            for cell in row:    
                self.__draw_cell(cell)
                self.__cell_hover(cell)
                if cell.occupied_by == 'x':
                    self.__draw_x(cell)
                if cell.occupied_by == 'o':
                    self.__draw_o(cell)
        if self.winning_line is not None:
            self.__draw_line()
            
    def place_sign(self):
        if not self.current_hovered_cell.is_occupied:
            self.current_hovered_cell.is_occupied = True
            self.current_hovered_cell.occupied_by = self.current_player
            self.__check_for_win()
            self.__swap_player()
    
    def __check_for_win(self):
        self.__check_horizontal(self.current_hovered_cell)
        self.__check_vertical(self.current_hovered_cell)
    
    def __check_vertical(self, cell: Cell):
        counter = 0
        for i in range(self.grid_size):
            if self.grid[cell.id[0]][i].occupied_by == self.current_player:
                counter += 1
        if counter == self.grid_size:
            padding = cell.rect.width/6
            line_width = int(cell.rect.width/15)
            line_start_pos = (self.grid[cell.id[0]][0].rect.topleft[0] + cell.rect.width/2, self.grid[cell.id[0]][0].rect.topleft[1] + padding)
            line_end_pos = (self.grid[cell.id[0]][self.grid_size - 1].rect.bottomleft[0] + cell.rect.width/2, self.grid[cell.id[0]][self.grid_size - 1].rect.bottomleft[1] - padding)
            self.winning_line = WinningLine(line_start_pos, line_end_pos, line_width)
    
    def __check_horizontal(self, cell: Cell):
        counter = 0
        for i in range(self.grid_size):
            if self.grid[i][cell.id[1]].occupied_by == self.current_player:
                counter += 1
        if counter == self.grid_size:
            padding = cell.rect.width/6
            line_width = int(cell.rect.width/15)
            line_start_pos = (self.grid[0][cell.id[1]].rect.topleft[0] + padding, self.grid[0][cell.id[1]].rect.topleft[1] + cell.rect.width/2)
            line_end_pos = (self.grid[self.grid_size - 1][cell.id[1]].rect.topright[0] - padding, self.grid[self.grid_size - 1][cell.id[1]].rect.topright[1] + cell.rect.width/2)
            self.winning_line = WinningLine(line_start_pos, line_end_pos, line_width)
    
    def __swap_player(self):
        if self.current_player == 'x':
            self.current_player = 'o'
        elif self.current_player == 'o':
            self.current_player = 'x'
    
    def __create_grid(self):
        padding = 10
        cell_size = self.grid_size_px / self.grid_size
        for x in range(self.grid_size):
            row = []
            for y in range(self.grid_size):
                rect_x = self.window_width/2 - self.grid_size_px/2 + cell_size*x
                rect_y = self.window_height/2 - self.grid_size_px/2 + cell_size*y
                rect_size = cell_size - padding
                rect = pygame.Rect(rect_x, rect_y, rect_size, rect_size)
                row.append(Cell(rect, (x, y)))
            self.grid.append(row)
        
    def __cell_hover(self, cell: Cell):
        if cell.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_hovered_cell = cell
        if cell.is_occupied:
            return
        if self.current_player == 'o':
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                self.__draw_o(cell)
        if self.current_player == 'x':
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                self.__draw_x(cell)
               
    def __draw_x(self, cell: Cell):
        padding = cell.rect.width/5
        line_width = int(cell.rect.width/10)
        line1_start_pos = (cell.rect.topleft[0] + padding, cell.rect.topleft[1] + padding)
        line1_end_pos = (cell.rect.bottomright[0] - padding, cell.rect.bottomright[1] - padding)
        pygame.draw.line(self.window, cell.sign_color, line1_start_pos, line1_end_pos, line_width)
        line2_start_pos = (cell.rect.topright[0] - padding, cell.rect.topright[1] + padding)
        line2_end_pos = (cell.rect.bottomleft[0] + padding, cell.rect.bottomleft[1] - padding)
        pygame.draw.line(self.window, cell.sign_color, line2_start_pos, line2_end_pos, line_width)
    
    def __draw_o(self, cell: Cell):
        center_coordinate = (cell.rect.left + cell.rect.width/2, cell.rect.top + cell.rect.height/2)
        radius = cell.rect.width/3.2
        width = int(cell.rect.width/14)
        pygame.draw.circle(self.window, cell.sign_color, center_coordinate, radius, width)
    
    def __draw_line(self):
        pygame.draw.line(self.window, self.winning_line.color, self.winning_line.start_pos, self.winning_line.end_pos, self.winning_line.width)
    
    def __draw_cell(self, cell: Cell):
        pygame.draw.rect(self.window, cell.background_colour, cell.rect)
            

def main():
    game = TicTacToe(3)
    running = True
    while running:
        game.draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # 1 == left button
                    game.place_sign()
        pygame.display.update()


if __name__ == '__main__':
    main()