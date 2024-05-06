import pygame

class Text():
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, text: str, text_size: str = 25):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.font = pygame.font.SysFont('Arial', text_size)
        self.text_backgroud = pygame.Surface((self.width, self.height))
        self.text_backgroud_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text_surface = self.font.render(text, True, (255,255,255))

    def process(self):
        self.text_backgroud.fill((18, 18, 18, 0))
        self.text_backgroud.blit(self.text_surface, [
        self.text_backgroud_rect.width/2 - self.text_surface.get_rect().width/2,
        self.text_backgroud_rect.height/2 - self.text_surface.get_rect().height/2
        ])
        self.window.blit(self.text_backgroud, self.text_backgroud_rect)

class Button():
    def __init__(self, window, x, y, width, height, button_text='Button', onclick_function=None, one_press=False):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick_function = onclick_function
        self.one_press = one_press
        self.already_pressed = False
        self.font = pygame.font.SysFont('Arial', 25)
        self.fill_colors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.button_surf = self.font.render(button_text, True, (18, 18, 18))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])
        if self.button_rect.collidepoint(mousePos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])
                if self.one_press:
                    self.onclick_function()
                elif not self.already_pressed:
                    self.onclick_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False
        self.button_surface.blit(self.button_surf, [
        self.button_rect.width/2 - self.button_surf.get_rect().width/2,
        self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])
        self.window.blit(self.button_surface, self.button_rect)

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
    is_occupied: bool = False
    occupied_by: str = ''
    def __init__(self, rect: pygame.Rect, id: tuple[int, int]):
        self.rect = rect
        self.id = id

class TicTacToe:
    running: bool = True
    current_player: str = 'o'
    player_o_wins = 0
    player_x_wins = 0
    window_width: int
    window_height: int
    window: pygame.Surface
    grid: list[list[Cell]] = []
    grid_size: int
    grid_size_px: int = 600
    current_hovered_cell: Cell = None
    winning_line: WinningLine = None
    is_game_finished: bool = False
    is_grid_full: bool = False
    def __init__(self, size: int):
        self.__init_window()
        self.grid_size = size
        self.__create_grid()
    
    def __init_window(self):
        pygame.init()
        self.window_background_colour = (18, 18, 18)
        ratio = 80
        self.window_width, self.window_height = 16*ratio, 9*ratio
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('TicTacToe')
        self.window.fill(self.window_background_colour)
        pygame.display.flip()
    
    def draw_grid(self):
        Button(self.window, 1100, 60, 110, 50, button_text='Restart', onclick_function=self.restart_game).process()
        Button(self.window, 1100, 120, 50, 50, button_text='3x3', onclick_function= lambda: self.__change_grid_size(3)).process()
        Button(self.window, 1100, 180, 50, 50, button_text='5x5', onclick_function= lambda: self.__change_grid_size(5)).process()
        Button(self.window, 1160, 120, 50, 50, button_text='7x7', onclick_function= lambda: self.__change_grid_size(7)).process()
        Button(self.window, 1160, 180, 50, 50, button_text='9x9', onclick_function= lambda: self.__change_grid_size(9)).process()
        Button(self.window, 1100, 600, 110, 50, button_text='Quit', onclick_function=self.__quit).process()
        Text(self.window, 50, 60, 200, 30, f"Player X wins: {self.player_x_wins}").process()
        Text(self.window, 50, 100, 200, 30, f"Player O wins: {self.player_o_wins}").process()
        if not self.is_game_finished:
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
                    self.is_game_finished = True
                    self.__add_win()
            if self.is_grid_full:
                Text(self.window, self.grid[-1][-1].rect.bottomright[0]/2, self.grid[-1][-1].rect.bottomright[1]/2, 350, 50, f"GAME OVER!", 50).process()
        else:
            Text(self.window, self.grid[-1][-1].rect.bottomright[0]/2, self.grid[-1][-1].rect.bottomright[1]/2, 350, 50, f"GAME OVER!", 50).process()
                
    def place_sign(self):
        if self.current_hovered_cell is not None:
            if not self.current_hovered_cell.is_occupied:
                self.current_hovered_cell.is_occupied = True
                self.current_hovered_cell.occupied_by = self.current_player
                self.__check_for_win()
                self.__swap_player()
    
    def __is_grid_full(self):
        counter = 0
        for row in self.grid:
            for cell in row:
                if cell.is_occupied:
                    counter += 1
        if counter == self.grid_size ** 2:
            self.is_grid_full = True
    
    def restart_game(self):
        self.is_game_finished = False
        self.is_grid_full = False
        self.winning_line = None
        self.current_hovered_cell = None
        self.window.fill(self.window_background_colour)
        self.grid = []
        self.__create_grid()
    
    def __change_grid_size(self, new_size: int):
        self.grid_size = new_size
        self.restart_game()
        
    def __add_win(self):
        if self.current_player == 'o':
            self.player_x_wins += 1
        if self.current_player == 'x':
            self.player_o_wins += 1
        
    def __quit(self):
        self.running = False
    
    def __check_for_win(self):
        self.__check_horizontal(self.current_hovered_cell)
        self.__check_vertical(self.current_hovered_cell)
        self.__check_diagonals(self.current_hovered_cell)
        self.__is_grid_full()
    
    def __check_diagonals(self, cell: Cell):
        # Top left to bottom right
        if cell.id[0] == cell.id[1]:
            counter = 0
            for i in range(self.grid_size):
                if self.grid[i][i].occupied_by == self.current_player:
                    counter += 1
            if counter == self.grid_size:
                padding = self.grid[0][0].rect.width/6
                line_width = int(self.grid[0][0].rect.width/15)
                line_start_pos = (self.grid[0][0].rect.topleft[0] + padding, self.grid[0][0].rect.topleft[1] + padding)
                line_end_pos = (self.grid[self.grid_size - 1][self.grid_size - 1].rect.bottomright[0] - padding, self.grid[self.grid_size - 1][self.grid_size - 1].rect.bottomright[1] - padding)
                self.winning_line = WinningLine(line_start_pos, line_end_pos, line_width)
        # Bottom left to top right
        if cell.id[0] + cell.id[1] == self.grid_size - 1:
            counter = 0
            for i in range(self.grid_size):
                if self.grid[0 + i][self.grid_size - 1 - i].occupied_by == self.current_player:
                    counter += 1
            if counter == self.grid_size:
                padding = self.grid[0][0].rect.width/6
                line_width = int(self.grid[0][0].rect.width/15)
                line_start_pos = (self.grid[0][self.grid_size - 1].rect.bottomleft[0] + padding, self.grid[0][self.grid_size - 1].rect.bottomleft[1] - padding)
                line_end_pos = (self.grid[self.grid_size - 1][0].rect.topright[0] - padding, self.grid[self.grid_size - 1][0].rect.topright[1] + padding)
                self.winning_line = WinningLine(line_start_pos, line_end_pos, line_width)
    
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
                self.__draw_o(cell, (209, 153, 148))
        if self.current_player == 'x':
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                self.__draw_x(cell, (129, 141, 199))
               
    def __draw_x(self, cell: Cell, color:tuple[int, int, int] = (23, 44, 150)):
        padding = cell.rect.width/5
        line_width = int(cell.rect.width/10)
        line1_start_pos = (cell.rect.topleft[0] + padding, cell.rect.topleft[1] + padding)
        line1_end_pos = (cell.rect.bottomright[0] - padding, cell.rect.bottomright[1] - padding)
        pygame.draw.line(self.window, color, line1_start_pos, line1_end_pos, line_width)
        line2_start_pos = (cell.rect.topright[0] - padding, cell.rect.topright[1] + padding)
        line2_end_pos = (cell.rect.bottomleft[0] + padding, cell.rect.bottomleft[1] - padding)
        pygame.draw.line(self.window, color, line2_start_pos, line2_end_pos, line_width)
    
    def __draw_o(self, cell: Cell, color:tuple[int, int, int] = (112, 42, 37)):
        center_coordinate = (cell.rect.left + cell.rect.width/2, cell.rect.top + cell.rect.height/2)
        radius = cell.rect.width/3.14
        width = int(cell.rect.width/14)
        pygame.draw.circle(self.window, color, center_coordinate, radius, width)
    
    def __draw_line(self):
        pygame.draw.line(self.window, self.winning_line.color, self.winning_line.start_pos, self.winning_line.end_pos, self.winning_line.width)
    
    def __draw_cell(self, cell: Cell):
        pygame.draw.rect(self.window, cell.background_colour, cell.rect)
            
def main():
    game = TicTacToe(3)
    while game.running:
        game.draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                game.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # 1 == left button
                    game.place_sign()
        pygame.display.update()

if __name__ == '__main__':
    main()