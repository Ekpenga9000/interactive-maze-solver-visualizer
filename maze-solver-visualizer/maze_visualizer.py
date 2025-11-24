"""
Maze Visualizer Module
Handles the graphical display and user interaction for the maze solver
"""

import pygame
import sys
from typing import List, Tuple, Set, Optional
from maze_generator import MazeGenerator
from maze_solver import MazeSolver, Algorithm

class MazeVisualizer:
    """Handles visualization and user interaction for the maze solver"""
    
    def __init__(self, window_width: int = 800, window_height: int = 600, 
                 maze_width: int = 41, maze_height: int = 31):
        """
        Initialize the maze visualizer
        
        Args:
            window_width: Width of the display window
            window_height: Height of the display window
            maze_width: Width of the maze (should be odd)
            maze_height: Height of the maze (should be odd)
        """
        self.window_width = window_width
        self.window_height = window_height
        self.maze_width = maze_width
        self.maze_height = maze_height
        
        # Calculate cell size to fit maze in window
        self.cell_size = min(window_width // maze_width, window_height // maze_height)
        
        # Adjust window size to fit maze perfectly
        self.display_width = maze_width * self.cell_size
        self.display_height = maze_height * self.cell_size
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.display_width, self.display_height + 100))
        pygame.display.set_caption("Maze Solver & Visualizer")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (128, 0, 128)
        self.ORANGE = (255, 165, 0)
        self.GRAY = (128, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        
        # Font for text
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize maze and solver
        self.maze_generator = MazeGenerator(maze_width, maze_height)
        self.maze = None
        self.maze_solver = None
        self.current_algorithm = Algorithm.DFS
        self.path = []
        self.visited_cells = set()
        self.start_pos = None
        self.end_pos = None
        
        # Generate initial maze
        self.generate_new_maze()
    
    def generate_new_maze(self):
        """Generate a new random maze"""
        self.maze = self.maze_generator.generate()
        self.maze_solver = MazeSolver(self.maze)
        self.start_pos = self.maze_generator.get_start_position()
        self.end_pos = self.maze_generator.get_end_position()
        self.path = []
        self.visited_cells = set()
    
    def solve_maze(self):
        """Solve the current maze using the selected algorithm"""
        if self.maze_solver and self.start_pos and self.end_pos:
            self.path, self.visited_cells = self.maze_solver.solve(
                self.start_pos, self.end_pos, self.current_algorithm
            )
    
    def draw_maze(self):
        """Draw the maze on the screen"""
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                if self.maze[y][x] == 1:  # Wall
                    pygame.draw.rect(self.screen, self.BLACK, rect)
                else:  # Path
                    pygame.draw.rect(self.screen, self.WHITE, rect)
    
    def draw_visited_cells(self):
        """Draw visited cells during pathfinding"""
        for x, y in self.visited_cells:
            if (x, y) not in self.path:  # Don't overwrite solution path
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.LIGHT_BLUE, rect)
    
    def draw_path(self):
        """Draw the solution path"""
        for x, y in self.path:
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                             self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.YELLOW, rect)
    
    def draw_start_end(self):
        """Draw start and end positions"""
        if self.start_pos:
            x, y = self.start_pos
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                             self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.GREEN, rect)
        
        if self.end_pos:
            x, y = self.end_pos
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                             self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.RED, rect)
    
    def draw_ui(self):
        """Draw user interface elements"""
        ui_y = self.display_height + 10
        
        # Current algorithm
        algorithm_text = f"Algorithm: {self.current_algorithm.value}"
        text_surface = self.font.render(algorithm_text, True, self.BLACK)
        self.screen.blit(text_surface, (10, ui_y))
        
        # Instructions
        instructions = [
            "Keys: G=Generate New, S=Solve, 1=DFS, 2=BFS, 3=Dijkstra, Q=Quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.small_font.render(instruction, True, self.BLACK)
            self.screen.blit(text_surface, (10, ui_y + 40 + i * 25))
        
        # Path length
        if self.path:
            path_text = f"Path Length: {len(self.path)} steps"
            text_surface = self.font.render(path_text, True, self.BLACK)
            self.screen.blit(text_surface, (self.display_width - 200, ui_y))
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_g:
                    self.generate_new_maze()
                elif event.key == pygame.K_s:
                    self.solve_maze()
                elif event.key == pygame.K_1:
                    self.current_algorithm = Algorithm.DFS
                    self.path = []
                    self.visited_cells = set()
                elif event.key == pygame.K_2:
                    self.current_algorithm = Algorithm.BFS
                    self.path = []
                    self.visited_cells = set()
                elif event.key == pygame.K_3:
                    self.current_algorithm = Algorithm.DIJKSTRA
                    self.path = []
                    self.visited_cells = set()
        
        return True
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        print("Maze Solver & Visualizer Started!")
        print("Controls:")
        print("  G - Generate new maze")
        print("  S - Solve current maze")
        print("  1 - Use Depth-First Search")
        print("  2 - Use Breadth-First Search") 
        print("  3 - Use Dijkstra's Algorithm")
        print("  Q - Quit")
        
        while running:
            running = self.handle_events()
            
            # Clear screen
            self.screen.fill(self.WHITE)
            
            # Draw everything
            self.draw_maze()
            self.draw_visited_cells()
            self.draw_path()
            self.draw_start_end()
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()