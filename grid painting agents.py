import time

class PaintingRobot:
    def _init_(self, robot_id, start_pos, color, symbol):
        self.id = robot_id
        self.pos = start_pos
        self.color = color
        self.symbol = symbol
        self.painted = []
        self.stack = [start_pos]
        self.visited = set()
    
    def paint_next(self, grid, area):
        while self.stack:
            r, c = self.stack.pop()
            
            if (r, c) in self.visited or (r, c) not in area:
                continue
            
            self.visited.add((r, c))
            self.pos = (r, c)
            
            if grid[r][c] == 0:
                grid[r][c] = self.id
                self.painted.append((r, c))
                
                # Add neighbors to stack
                for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                        if (nr, nc) not in self.visited and (nr, nc) in area:
                            self.stack.append((nr, nc))
                
                return True
        
        return False


class GridPaintingSystem:
    def _init_(self):
        self.rows = 8
        self.cols = 16
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Both robots start from specific points
        self.robot_a = PaintingRobot(1, (0, 0), "blue", "🤖")
        self.robot_b = PaintingRobot(2, (self.rows-1, self.cols-1), "green", "🦾")
        
        # Divide grid vertically: left half for A, right half for B
        mid_col = self.cols // 2
        self.area_a = [(i, j) for i in range(self.rows) for j in range(mid_col)]
        self.area_b = [(i, j) for i in range(self.rows) for j in range(mid_col, self.cols)]
        self.step = 0
    
    def visualize(self):
        print("\n" * 2)
        print(f"{'='*60}")
        print(f"GRID PAINTING AGENTS - Step {self.step}")
        print(f"{'='*60}\n")
        
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                if (i, j) == self.robot_a.pos:
                    row += "🤖 "
                elif (i, j) == self.robot_b.pos:
                    row += "🦾 "
                elif self.grid[i][j] == 1:
                    row += "\033[94m█\033[0m "  # Blue for Robot A
                elif self.grid[i][j] == 2:
                    row += "\033[92m█\033[0m "  # Green for Robot B
                else:
                    row += "⬜ "
            print(row)
        
        print(f"\n🤖 Robot A at {self.robot_a.pos}, painted: {len(self.robot_a.painted)} cells")
        print(f"🦾 Robot B at {self.robot_b.pos}, painted: {len(self.robot_b.painted)} cells")
        time.sleep(0.2)
    
    def run(self):
        print("\nStarting Grid Painting...")
        print(f"🤖 Robot A starts at {self.robot_a.pos}")
        print(f"🦾 Robot B starts at {self.robot_b.pos}")
        self.visualize()
        
        # Paint one cell at a time alternating between robots
        while True:
            self.step += 1
            painted = False
            
            # Robot A paints next cell
            if self.robot_a.paint_next(self.grid, self.area_a):
                painted = True
            
            # Robot B paints next cell
            if self.robot_b.paint_next(self.grid, self.area_b):
                painted = True
            
            if not painted:
                break
            
            self.visualize()
        
        self.show_results()
    
    def show_results(self):
        total_cells = len(self.robot_a.painted) + len(self.robot_b.painted)
        total_grid = self.rows * self.cols
        coverage = (total_cells / total_grid) * 100
        
        print(f"\n{'='*60}")
        print(f"PAINTING COMPLETE!")
        print(f"{'='*60}")
        print(f"Total cells painted: {total_cells}/{total_grid}")
        print(f"Coverage: {coverage:.1f}%")
        print(f"\033[94m█\033[0m Robot A: {len(self.robot_a.painted)} cells (left half)")
        print(f"\033[92m█\033[0m Robot B: {len(self.robot_b.painted)} cells (right half)")
        print(f"Overlap: 0 cells (100% coordination)")
        print(f"{'='*60}\n")


if _name_ == "_main_":
    system = GridPaintingSystem()
    system.run()