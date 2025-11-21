import time
from collections import deque

class RescueBot:
    def _init_(self, bot_id, start_pos, symbol):
        self.id = bot_id
        self.pos = start_pos
        self.symbol = symbol
        self.rescued = []
        self.path = []
    
    def bfs(self, start, goals, grid):
        if not goals:
            return None, []
        
        queue = deque([(start, [])])
        visited = {start}
        
        while queue:
            pos, path = queue.popleft()
            
            if pos in goals:
                return pos, path + [pos]
            
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                neighbor = (nx, ny)
                
                if (0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and 
                    grid[nx][ny] != 1 and neighbor not in visited):
                    visited.add(neighbor)
                    queue.append((neighbor, path + [pos]))
        
        return None, []


class RescueSystem:
    def _init_(self):
        # Maze: 0=path, 1=wall - fully connected maze
        self.maze = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        
        # Place victims in accessible locations
        self.victims = [(1, 3), (3, 9), (5, 5), (1, 10)]
        
        # Initialize bots
        self.bot1 = RescueBot(1, (1, 1), "🤖")
        self.bot2 = RescueBot(2, (5, 10), "🦾")
        
        self.step = 0
        self.assign_zones()
    
    def assign_zones(self):
        # Logic-based assignment: divide victims evenly by proximity
        victims_with_dist = []
        
        for victim in self.victims:
            dist1 = abs(victim[0] - self.bot1.pos[0]) + abs(victim[1] - self.bot1.pos[1])
            dist2 = abs(victim[0] - self.bot2.pos[0]) + abs(victim[1] - self.bot2.pos[1])
            victims_with_dist.append((victim, dist1, dist2))
        
        # Sort by which bot is closer
        victims_with_dist.sort(key=lambda x: x[1] - x[2])
        
        # Assign half to each bot
        mid = len(victims_with_dist) // 2
        self.bot1_victims = [v[0] for v in victims_with_dist[:mid]]
        self.bot2_victims = [v[0] for v in victims_with_dist[mid:]]
    
    def visualize(self):
        print("\n" * 2)
        print(f"{'='*50}")
        print(f"RESCUE BOT SQUAD - Step {self.step}")
        print(f"{'='*50}\n")
        
        # Top border
        print("┌" + "─" * (self.cols * 2) + "┐")
        
        for i in range(self.rows):
            row = "│"
            for j in range(self.cols):
                if (i, j) == self.bot1.pos:
                    row += "🤖"
                elif (i, j) == self.bot2.pos:
                    row += "🦾"
                elif (i, j) in self.victims:
                    row += "🆘"
                elif (i, j) in self.bot1.path:
                    row += "\033[94m░░\033[0m"
                elif (i, j) in self.bot2.path:
                    row += "\033[92m░░\033[0m"
                elif self.maze[i][j] == 1:
                    row += "██"
                else:
                    row += "░░"
            row += "│"
            print(row)
        
        # Bottom border
        print("└" + "─" * (self.cols * 2) + "┘")
        
        print(f"\n🤖 Bot 1 at {self.bot1.pos}, rescued: {len(self.bot1.rescued)}")
        print(f"🦾 Bot 2 at {self.bot2.pos}, rescued: {len(self.bot2.rescued)}")
        time.sleep(0.2)
    
    def run(self):
        print("\nStarting Rescue Bot Squad...")
        print(f"🤖 Bot 1 starts at {self.bot1.pos}")
        print(f"🦾 Bot 2 starts at {self.bot2.pos}")
        print(f"\nVictims at: {self.victims}")
        print(f"Bot 1 assigned: {self.bot1_victims}")
        print(f"Bot 2 assigned: {self.bot2_victims}")
        
        self.visualize()
        
        # Rescue all victims - alternate between bots
        while self.victims:
            moved = False
            
            # Bot 1 rescue
            if self.bot1_victims:
                target, path = self.bot1.bfs(self.bot1.pos, self.bot1_victims, self.maze)
                
                if target and path:
                    moved = True
                    for pos in path:
                        self.step += 1
                        self.bot1.pos = pos
                        if pos not in self.bot1.path:
                            self.bot1.path.append(pos)
                        self.visualize()
                    
                    self.bot1.rescued.append(target)
                    self.victims.remove(target)
                    self.bot1_victims.remove(target)
                    print(f"\n🤖 Bot 1 rescued victim at {target}!")
                    time.sleep(0.5)
                else:
                    # Can't reach, reassign to bot 2
                    if self.bot1_victims:
                        unreachable = self.bot1_victims[0]
                        self.bot1_victims.remove(unreachable)
                        self.bot2_victims.append(unreachable)
                        print(f"\n🤖 Bot 1 can't reach {unreachable}, reassigning to Bot 2")
            
            # Bot 2 rescue
            if self.bot2_victims:
                target, path = self.bot2.bfs(self.bot2.pos, self.bot2_victims, self.maze)
                
                if target and path:
                    moved = True
                    for pos in path:
                        self.step += 1
                        self.bot2.pos = pos
                        if pos not in self.bot2.path:
                            self.bot2.path.append(pos)
                        self.visualize()
                    
                    self.bot2.rescued.append(target)
                    self.victims.remove(target)
                    self.bot2_victims.remove(target)
                    print(f"\n🦾 Bot 2 rescued victim at {target}!")
                    time.sleep(0.5)
                else:
                    # Can't reach, reassign to bot 1
                    if self.bot2_victims:
                        unreachable = self.bot2_victims[0]
                        self.bot2_victims.remove(unreachable)
                        self.bot1_victims.append(unreachable)
                        print(f"\n🦾 Bot 2 can't reach {unreachable}, reassigning to Bot 1")
            
            if not moved:
                print("\nNo bot can reach remaining victims!")
                break
        
        self.show_results()
    
    def show_results(self):
        print(f"\n{'='*50}")
        print(f"ALL VICTIMS RESCUED!")
        print(f"{'='*50}")
        print(f"Total steps: {self.step}")
        print(f"🤖 Bot 1 rescued: {len(self.bot1.rescued)} victims")
        print(f"   Victims: {self.bot1.rescued}")
        print(f"🦾 Bot 2 rescued: {len(self.bot2.rescued)} victims")
        print(f"   Victims: {self.bot2.rescued}")
        print(f"{'='*50}\n")


if _name_ == "_main_":
    system = RescueSystem()
    system.run()