import collections
import time
import os

MAZE_LAYOUT = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 'A', 0, 0, 1, 0, 'K', 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 'K', 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 'K', 0, 1, 'B', 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class CooperativeMaze:
    def _init_(self, layout):
        self.grid = [row[:] for row in layout]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.agents = {}
        self.keys = []
        self.visited_paths = set()

        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r][c]
                if val == 'A':
                    self.agents['A'] = (r, c)
                elif val == 'B':
                    self.agents['B'] = (r, c)
                elif val == 'K':
                    self.keys.append((r, c))

    def print_maze(self, message=""):
        print("\n" * 2)
        print(f"Keys remaining: {len(self.keys)}")
        if message:
            print(f"Communication: {message}")
        print("-" * (self.cols * 2))

        for r in range(self.rows):
            line = ""
            for c in range(self.cols):
                val = self.grid[r][c]
                # Visualization logic
                if (r, c) in self.agents.values():
                    # Identify which agent
                    agent_name = [k for k, v in self.agents.items() if v == (r, c)][0]
                    line += f"{agent_name} "
                elif val == 1:
                    line += "█ "
                elif val == 'K':
                    line += "⚷ "
                elif (r, c) in self.visited_paths:
                    line += ". "
                else:
                    line += "  "
            print(line)
        print("-" * (self.cols * 2))
        time.sleep(0.5)

    def bfs_path(self, start, goals):

        if not goals: return None, []

        queue = collections.deque([(start, [])])
        visited = {start}

        while queue:
            (cur_r, cur_c), path = queue.popleft()

            if (cur_r, cur_c) in goals:
                return (cur_r, cur_c), path + [(cur_r, cur_c)]

            # Directions: Up, Down, Left, Right
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dr, dc in moves:
                nr, nc = cur_r + dr, cur_c + dc

                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    cell_content = self.grid[nr][nc]
                    is_obstacle = cell_content == 1

                    other_agent_pos = list(self.agents.values())
                    if (nr, nc) in other_agent_pos and (nr, nc) not in goals:
                        is_obstacle = True

                    if not is_obstacle and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(((nr, nc), path + [(cur_r, cur_c)]))

        return None, []

    def run_simulation(self):
        self.print_maze()
        total_keys = len(self.keys)

        while self.keys:
            message = ""
            
            # Agent A looks for nearest key
            target_a, path_a = self.bfs_path(self.agents['A'], self.keys)

            # Agent B looks for nearest key, excludes A's target
            available_for_b = [k for k in self.keys if k != target_a]

            if not available_for_b and self.keys:
                available_for_b = self.keys
                message = "Agent B: Assisting Agent A with last key"
            elif target_a:
                message = f"Agent A targeting {target_a}, Agent B exploring other regions"

            target_b, path_b = self.bfs_path(self.agents['B'], available_for_b)

            # Move Agent A
            if path_a and len(path_a) > 1:
                next_pos = path_a[1]
                old_r, old_c = self.agents['A']
                self.grid[old_r][old_c] = 0
                self.visited_paths.add((old_r, old_c))
                self.agents['A'] = next_pos
                
                if next_pos in self.keys:
                    self.keys.remove(next_pos)
                    self.grid[next_pos[0]][next_pos[1]] = 0
                    message = f"Agent A collected key at {next_pos}!"
            elif target_a and self.agents['A'] == target_a:
                if target_a in self.keys:
                    self.keys.remove(target_a)
                    self.grid[target_a[0]][target_a[1]] = 0
                    message = f"Agent A collected key at {target_a}!"

            # Move Agent B
            if path_b and len(path_b) > 1:
                next_pos = path_b[1]
                if next_pos != self.agents['A']:
                    old_r, old_c = self.agents['B']
                    self.grid[old_r][old_c] = 0
                    self.visited_paths.add((old_r, old_c))
                    self.agents['B'] = next_pos
                    
                    if next_pos in self.keys:
                        self.keys.remove(next_pos)
                        self.grid[next_pos[0]][next_pos[1]] = 0
                        message = f"Agent B collected key at {next_pos}!"
            elif target_b and self.agents['B'] == target_b:
                if target_b in self.keys:
                    self.keys.remove(target_b)
                    self.grid[target_b[0]][target_b[1]] = 0
                    message = f"Agent B collected key at {target_b}!"

            self.print_maze(message)
            time.sleep(0.5)

        print("\n" + "="*50)
        print("All keys collected! Mission Complete.")
        print(f"Total keys collected: {total_keys}")
        print(f"Agent A path length: {len([p for p in self.visited_paths if p])}")
        print("="*50)


# --- Execution ---
if _name_ == "_main_":
    game = CooperativeMaze(MAZE_LAYOUT)
    game.run_simulation()