import heapq
import time

class Drone:
    def _init_(self, drone_id, start_pos):
        self.id = drone_id
        self.pos = start_pos
        self.path = []
        self.target = None
    
    def a_star(self, start, goal, grid):
        def h(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]
            
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0])):
                    tentative_g = g_score[current] + 1
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + h(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
                        came_from[neighbor] = current
        
        return []


class DeliverySystem:
    def _init_(self):
        self.rows = 12
        self.cols = 20
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.drone1 = Drone(1, (0, 0))
        self.drone2 = Drone(2, (self.rows-1, self.cols-1))
        
        # Delivery goals (destinations)
        self.goals = [(2, 18), (5, 3), (9, 10), (7, 15)]
        self.delivered = []  # Track delivered packages
        self.coverage = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.step = 0
        
        self.assign_packages()
    
    def assign_packages(self):
        # Greedy assignment: assign nearest goals
        available = list(self.goals)
        
        # Drone 1 gets nearest goal
        dist1 = [(self.manhattan(self.drone1.pos, p), p) for p in available]
        dist1.sort()
        self.drone1.target = dist1[0][1]
        available.remove(self.drone1.target)
        
        # Drone 2 gets nearest from remaining
        dist2 = [(self.manhattan(self.drone2.pos, p), p) for p in available]
        dist2.sort()
        self.drone2.target = dist2[0][1]
        available.remove(self.drone2.target)
        
        # Assign remaining goals
        self.drone1_goals = [self.drone1.target]
        self.drone2_goals = [self.drone2.target]
        
        for goal in available:
            d1 = self.manhattan(self.drone1.target, goal)
            d2 = self.manhattan(self.drone2.target, goal)
            if d1 < d2:
                self.drone1_goals.append(goal)
            else:
                self.drone2_goals.append(goal)
    
    def manhattan(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def visualize(self):
        print("\n" * 2)
        print(f"{'='*70}")
        print(f"DUAL DRONE DELIVERY - Step {self.step}")
        print(f"{'='*70}\n")
        
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                if (i, j) == self.drone1.pos:
                    row += "🚁 "
                elif (i, j) == self.drone2.pos:
                    row += "🚂 "
                elif (i, j) in self.delivered:
                    row += "📦 "  # Delivered package
                elif (i, j) in self.goals:
                    row += "🎯 "  # Delivery goal
                elif (i, j) in self.drone1.path:
                    row += "\033[94m·\033[0m "
                elif (i, j) in self.drone2.path:
                    row += "\033[92m·\033[0m "
                else:
                    row += "⬜ "
            print(row)
        
        print(f"\n🚁 Drone 1 at {self.drone1.pos}, target: {self.drone1.target}")
        print(f"🚂 Drone 2 at {self.drone2.pos}, target: {self.drone2.target}")
        print(f"🎯 Goals remaining: {len(self.goals)} | 📦 Delivered: {len(self.delivered)}")
        time.sleep(0.15)
    
    def run(self):
        print("\nStarting Dual Drone Delivery System...")
        print(f"🚁 Drone 1 starts at {self.drone1.pos}")
        print(f"🚂 Drone 2 starts at {self.drone2.pos}")
        print(f"\n🎯 Delivery goals: {self.goals}")
        print(f"Drone 1 assigned: {self.drone1_goals}")
        print(f"Drone 2 assigned: {self.drone2_goals}")
        
        self.visualize()
        
        total_time = 0
        
        # Deliver to all goals
        while self.drone1_goals or self.drone2_goals:
            # Drone 1 delivery
            if self.drone1_goals:
                target = self.drone1_goals[0]
                path = self.drone1.a_star(self.drone1.pos, target, self.grid)
                
                for pos in path:
                    self.step += 1
                    self.drone1.pos = pos
                    self.drone1.path.append(pos)
                    self.coverage[pos[0]][pos[1]] += 1
                    self.visualize()
                
                # Mark as delivered
                self.goals.remove(target)
                self.delivered.append(target)
                self.drone1_goals.pop(0)
                print(f"\n🚁 Drone 1 delivered to {target}!")
                time.sleep(0.5)
                total_time = max(total_time, self.step)
            
            # Drone 2 delivery
            if self.drone2_goals:
                target = self.drone2_goals[0]
                path = self.drone2.a_star(self.drone2.pos, target, self.grid)
                
                for pos in path:
                    self.step += 1
                    self.drone2.pos = pos
                    self.drone2.path.append(pos)
                    self.coverage[pos[0]][pos[1]] += 1
                    self.visualize()
                
                # Mark as delivered
                self.goals.remove(target)
                self.delivered.append(target)
                self.drone2_goals.pop(0)
                print(f"\n🚂 Drone 2 delivered to {target}!")
                time.sleep(0.5)
                total_time = max(total_time, self.step)
        
        self.show_results(total_time)
    
    def show_results(self, total_time):
        print(f"\n{'='*70}")
        print(f"DELIVERY COMPLETE!")
        print(f"{'='*70}")
        print(f"Total delivery time: {total_time} steps")
        print(f"🚁 Drone 1 path length: {len(self.drone1.path)} steps")
        print(f"🚂 Drone 2 path length: {len(self.drone2.path)} steps")
        
        # Coverage heatmap
        print(f"\n{'='*70}")
        print("COVERAGE HEATMAP")
        print(f"{'='*70}\n")
        
        max_visits = max(max(row) for row in self.coverage)
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                visits = self.coverage[i][j]
                if visits == 0:
                    row += "⬜ "
                elif visits <= max_visits // 3:
                    row += "\033[92m█\033[0m "  # Light
                elif visits <= 2 * max_visits // 3:
                    row += "\033[93m█\033[0m "  # Medium
                else:
                    row += "\033[91m█\033[0m "  # Heavy
            print(row)
        
        print(f"\n\033[92m█\033[0m Low coverage  \033[93m█\033[0m Medium coverage  \033[91m█\033[0m High coverage")
        print(f"{'='*70}\n")


if _name_ == "_main_":
    system = DeliverySystem()
    system.run()