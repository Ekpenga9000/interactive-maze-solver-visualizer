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
        self.font = pygame.font.Font(None, 28)
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
        
        # Animation control
        self.is_solving = False
        self.solving_step = 0
        self.animation_speed = 50  # milliseconds between steps (lower = faster)
        self.last_step_time = 0
        self.solution_path = []
        self.current_visited = set()
        self.solving_complete = False
        
        # Real-time solving
        self.solving_generator = None
        self.current_path = []
        self.algorithm_stack = []  # For DFS backtracking visualization
        self.exploring_cell = None
        
        # Generate initial maze
        self.generate_new_maze()
    
    def generate_new_maze(self):
        """Generate a new random maze"""
        self.maze = self.maze_generator.generate()
        self.maze_solver = MazeSolver(self.maze)
        self.start_pos = self.maze_generator.get_start_position()
        self.end_pos = self.maze_generator.get_end_position()
        self._reset_solution()
    
    def solve_maze(self):
        """Start animated solving of the current maze using the selected algorithm"""
        if self.maze_solver and self.start_pos and self.end_pos and not self.is_solving:
            # Reset animation state
            self.is_solving = True
            self.solving_step = 0
            self.current_visited = set()
            self.solution_path = []
            self.current_path = []
            self.algorithm_stack = []
            self.solving_complete = False
            self.exploring_cell = None
            self.last_step_time = pygame.time.get_ticks()
            
            # Start the solving generator based on selected algorithm
            if self.current_algorithm == Algorithm.DFS:
                self.solving_generator = self._solve_dfs_animated()
            elif self.current_algorithm == Algorithm.BFS:
                self.solving_generator = self._solve_bfs_animated()
            elif self.current_algorithm == Algorithm.DIJKSTRA:
                self.solving_generator = self._solve_dijkstra_animated()
            
            # Initialize with start position
            self.current_visited.add(self.start_pos)
    
    def update_solving_animation(self):
        """Update the real-time solving process"""
        if not self.is_solving or self.solving_complete or not self.solving_generator:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_step_time >= self.animation_speed:
            try:
                # Get the next step from the algorithm generator
                next(self.solving_generator)
                self.last_step_time = current_time
            except StopIteration:
                # Algorithm finished
                self.solving_complete = True
                self.is_solving = False
                self.solving_generator = None
    
    def _solve_dfs_animated(self):
        """Real-time animated DFS using generator"""
        stack = [self.start_pos]
        parent = {self.start_pos: None}
        
        while stack:
            current = stack[-1]  # Peek at top of stack
            self.exploring_cell = current
            yield  # Pause for animation
            
            # Mark as visited
            if current not in self.current_visited:
                self.current_visited.add(current)
                yield  # Pause to show exploration
            
            # Check if we found the end
            if current == self.end_pos:
                # Reconstruct path
                path_cell = current
                while path_cell is not None:
                    self.solution_path.append(path_cell)
                    path_cell = parent[path_cell]
                self.solution_path.reverse()
                return
            
            # Find unvisited neighbors
            neighbors = self.maze_solver._get_neighbors(current[0], current[1])
            unvisited_neighbors = [n for n in neighbors if n not in self.current_visited]
            
            if unvisited_neighbors:
                # Choose first unvisited neighbor
                next_cell = unvisited_neighbors[0]
                parent[next_cell] = current
                stack.append(next_cell)
            else:
                # Backtrack
                stack.pop()
                yield  # Pause to show backtracking
    
    def _solve_bfs_animated(self):
        """Real-time animated BFS using generator"""
        from collections import deque
        queue = deque([self.start_pos])
        parent = {self.start_pos: None}
        
        while queue:
            current = queue.popleft()
            self.exploring_cell = current
            yield  # Pause for animation
            
            # Mark as visited
            if current not in self.current_visited:
                self.current_visited.add(current)
                yield  # Pause to show exploration
            
            # Check if we found the end
            if current == self.end_pos:
                # Reconstruct path
                path_cell = current
                while path_cell is not None:
                    self.solution_path.append(path_cell)
                    path_cell = parent[path_cell]
                self.solution_path.reverse()
                return
            
            # Add unvisited neighbors to queue
            neighbors = self.maze_solver._get_neighbors(current[0], current[1])
            for neighbor in neighbors:
                if neighbor not in self.current_visited and neighbor not in parent:
                    parent[neighbor] = current
                    queue.append(neighbor)
    
    def _solve_dijkstra_animated(self):
        """Real-time animated Dijkstra using generator"""
        import heapq
        pq = [(0, self.start_pos)]
        distances = {self.start_pos: 0}
        parent = {self.start_pos: None}
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            self.exploring_cell = current
            yield  # Pause for animation
            
            # Skip if we've already processed this cell with a shorter distance
            if current in self.current_visited:
                continue
            
            # Mark as visited
            self.current_visited.add(current)
            yield  # Pause to show exploration
            
            # Check if we found the end
            if current == self.end_pos:
                # Reconstruct path
                path_cell = current
                while path_cell is not None:
                    self.solution_path.append(path_cell)
                    path_cell = parent[path_cell]
                self.solution_path.reverse()
                return
            
            # Process neighbors
            neighbors = self.maze_solver._get_neighbors(current[0], current[1])
            for neighbor in neighbors:
                if neighbor not in self.current_visited:
                    new_distance = current_dist + 1
                    if neighbor not in distances or new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        parent[neighbor] = current
                        heapq.heappush(pq, (new_distance, neighbor))
    
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
        for x, y in self.current_visited:
            if (x, y) not in self.solution_path:  # Don't overwrite solution path
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, self.LIGHT_BLUE, rect)
        
        # Highlight currently exploring cell
        if self.exploring_cell and self.is_solving:
            x, y = self.exploring_cell
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                             self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.ORANGE, rect)
    
    def draw_path(self):
        """Draw the solution path"""
        for x, y in self.solution_path:
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
        
        # Current algorithm and status (top line)
        algorithm_text = f"Algorithm: {self.current_algorithm.value}"
        if self.is_solving:
            algorithm_text += " (SOLVING...)"
        elif self.solving_complete:
            algorithm_text += " (COMPLETE)"
        text_surface = self.font.render(algorithm_text, True, self.BLACK)
        self.screen.blit(text_surface, (10, ui_y))
        
        # Path length and progress (right side, same line as algorithm)
        if self.is_solving:
            progress_text = f"Progress: {len(self.current_visited)} explored | {len(self.solution_path)} path"
            if self.exploring_cell:
                progress_text += f" | Exploring: {self.exploring_cell}"
        elif self.solving_complete and self.solution_path:
            progress_text = f"Result: {len(self.solution_path)} steps | {len(self.current_visited)} cells explored"
        elif hasattr(self, 'path') and self.path:
            progress_text = f"Last: {len(self.path)} steps | {len(self.visited_cells)} cells"
        else:
            progress_text = "Ready to solve"
        
        text_surface = self.small_font.render(progress_text, True, self.BLACK)
        self.screen.blit(text_surface, (self.display_width - 400, ui_y + 5))
        
        # Instructions (second line)
        instructions = [
            "Keys: G=Generate, S=Solve, R=Reset, +/-=Speed, 1/2/3=Algorithm, Q=Quit",
            f"Animation Speed: {self.animation_speed}ms (Level: {11 - self.animation_speed//50}/10)"
        ]
        
        for i, instruction in enumerate(instructions):
            text_surface = self.small_font.render(instruction, True, self.BLACK)
            self.screen.blit(text_surface, (10, ui_y + 35 + i * 20))
    
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
                elif event.key == pygame.K_r:
                    # Reset/stop current solving
                    self.is_solving = False
                    self.solving_complete = False
                    self.current_visited = set()
                    self.solution_path = []
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Increase speed (decrease delay)
                    self.animation_speed = max(10, self.animation_speed - 10)
                elif event.key == pygame.K_MINUS:
                    # Decrease speed (increase delay)
                    self.animation_speed = min(500, self.animation_speed + 10)
                elif event.key == pygame.K_1:
                    self.current_algorithm = Algorithm.DFS
                    self._reset_solution()
                elif event.key == pygame.K_2:
                    self.current_algorithm = Algorithm.BFS
                    self._reset_solution()
                elif event.key == pygame.K_3:
                    self.current_algorithm = Algorithm.DIJKSTRA
                    self._reset_solution()
        
        return True
    
    def _reset_solution(self):
        """Reset all solution-related state"""
        self.path = []
        self.visited_cells = set()
        self.is_solving = False
        self.solving_complete = False
        self.current_visited = set()
        self.solution_path = []
        self.current_path = []
        self.algorithm_stack = []
        self.exploring_cell = None
        self.solving_generator = None
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        print("Maze Solver & Visualizer Started!")
        print("Controls:")
        print("  G - Generate new maze")
        print("  S - Solve current maze (animated)")
        print("  R - Reset/stop current solving")
        print("  + - Increase animation speed")
        print("  - - Decrease animation speed")
        print("  1 - Use Depth-First Search")
        print("  2 - Use Breadth-First Search") 
        print("  3 - Use Dijkstra's Algorithm")
        print("  Q - Quit")
        
        while running:
            running = self.handle_events()
            
            # Update animation
            self.update_solving_animation()
            
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