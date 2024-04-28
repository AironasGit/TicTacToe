import pygame
from dataclasses import dataclass

class Cell:
    rect: pygame.Rect
    background_colour = (128, 128, 128)
    sign_color = (27, 27, 27)
    is_occupied: bool = False
    occupied_by: str = ''
    def __init__(self, rect: pygame.Rect):
        self.rect = rect


class TicTacToe:
    current_player: str = 'o'
    window_width: int
    window_height: int
    window: pygame.Surface
    grid: list[Cell] = []
    grid_size: int
    currect_hovered_cell: Cell
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
        for cell in self.grid:
            self.__draw_cell(cell)
            self.__cell_hover(cell)
            if cell.occupied_by == 'x':
                self.__draw_x(cell)
            if cell.occupied_by == 'o':
                self.__draw_o(cell)
    
    def place_sign(self):
        if not self.currect_hovered_cell.is_occupied:
            self.currect_hovered_cell.is_occupied = True
            self.currect_hovered_cell.occupied_by = self.current_player
            self.__swap_player()
        
    def __swap_player(self):
        if self.current_player == 'x':
            self.current_player = 'o'
        elif self.current_player == 'o':
            self.current_player = 'x'
    
    def __create_grid(self):
        padding = 10
        grid_size_px = 600
        cell_size = grid_size_px / self.grid_size
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect_x = self.window_width/2 - grid_size_px/2 + cell_size*x
                rect_y = self.window_height/2 - grid_size_px/2 + cell_size*y
                rect_size = cell_size - padding
                rect = pygame.Rect(rect_x, rect_y, rect_size, rect_size)
                self.grid.append(Cell(rect))
        
        
    def __cell_hover(self, cell: Cell):
        if cell.rect.collidepoint(pygame.mouse.get_pos()):
            self.currect_hovered_cell = cell
        if cell.is_occupied:
            return
        if self.current_player == 'o':
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                self.__draw_o(cell)
        if self.current_player == 'x':
            if cell.rect.collidepoint(pygame.mouse.get_pos()):
                self.__draw_x(cell)
               
    
    def __draw_x(self, cell: Cell):
        a = cell.rect.width/5
        pygame.draw.line(self.window, cell.sign_color, (cell.rect.topleft[0] + a, cell.rect.topleft[1] + a), (cell.rect.bottomright[0] - a, cell.rect.bottomright[1] - a), int(cell.rect.width/10))
        pygame.draw.line(self.window, cell.sign_color, (cell.rect.topright[0] - a, cell.rect.topright[1] + a), (cell.rect.bottomleft[0] + a, cell.rect.bottomleft[1] - a), int(cell.rect.width/10))
    
    def __draw_o(self, cell: Cell):
        pygame.draw.circle(self.window, cell.sign_color, (cell.rect.left + cell.rect.width/2, cell.rect.top + cell.rect.height/2), cell.rect.width/3.2, int(cell.rect.width/14))
    
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