import heapq
import time

class CleaningBot:
    def _init_(self, bot_id, start_pos, color):
        self.id = bot_id
        self.pos = start_pos
        self.color = color
        self.cleaned = []
        self.path = []
    
    def a_star(self, start, goal, grid, occupied):
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
                
                if (0 <= neighbor[0] < len(grid) and 0 <= neighbor[1] < len(grid[0]) 
                    and neighbor not in occupied):
                    
                    tentative_g = g_score[current] + 1
                    
                    if neighbor not in g_score or tentative_g < g_score[neighbor]:
                        g_score[neighbor] = tentative_g
                        f_score = tentative_g + h(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
                        came_from[neighbor] = current
        
        return []

def visualize(grid, bot1, bot2, step):
    print("\n" * 2)
    print(f"{'='*50}")
    print(f"CLEANING BOTS COORDINATION - Step {step}")
    print(f"{'='*50}\n")
    
    for i in range(len(grid)):
        row = ""
        for j in range(len(grid[0])):
            if (i, j) == bot1.pos:
                row += "🤖 "
            elif (i, j) == bot2.pos:
                row += "🦾 "
            elif (i, j) in bot1.cleaned:
                row += "✨ "
            elif (i, j) in bot2.cleaned:
                row += "💎 "
            elif grid[i][j] == 1:
                row += "💩 "
            else:
                row += "⬜ "
        print(row)
    
    print(f"\n🤖 Bot 1 cleaned: {len(bot1.cleaned)} | 🦾 Bot 2 cleaned: {len(bot2.cleaned)}")
    time.sleep(0.3)

def main():
    grid = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]
    
    bot1 = CleaningBot(1, (0, 0), "blue")
    bot2 = CleaningBot(2, (3, 0), "green")  
    
    mid_row = len(grid) // 2
    bot1_area = [(i, j) for i in range(mid_row) for j in range(len(grid[0]))]
    bot2_area = [(i, j) for i in range(mid_row, len(grid)) for j in range(len(grid[0]))]
    
    step = 0
    visualize(grid, bot1, bot2, step)
    
    while True:
        step += 1
        moved = False
        
        dirty_bot1 = [cell for cell in bot1_area if grid[cell[0]][cell[1]] == 1]
        if dirty_bot1:
            moved = True
            target = min(dirty_bot1, key=lambda c: abs(c[0]-bot1.pos[0]) + abs(c[1]-bot1.pos[1]))
            if bot1.pos == target:
                bot1.cleaned.append(bot1.pos)
                grid[bot1.pos[0]][bot1.pos[1]] = 0
            else:
                path = bot1.a_star(bot1.pos, target, grid, set())
                if path:
                    bot1.pos = path[0]
                    if grid[bot1.pos[0]][bot1.pos[1]] == 1:
                        bot1.cleaned.append(bot1.pos)
                        grid[bot1.pos[0]][bot1.pos[1]] = 0
        
        dirty_bot2 = [cell for cell in bot2_area if grid[cell[0]][cell[1]] == 1]
        if dirty_bot2:
            moved = True
            target = min(dirty_bot2, key=lambda c: abs(c[0]-bot2.pos[0]) + abs(c[1]-bot2.pos[1]))
            if bot2.pos == target:
                bot2.cleaned.append(bot2.pos)
                grid[bot2.pos[0]][bot2.pos[1]] = 0
            else:
                path = bot2.a_star(bot2.pos, target, grid, set())
                if path:
                    bot2.pos = path[0]
                    if grid[bot2.pos[0]][bot2.pos[1]] == 1:
                        bot2.cleaned.append(bot2.pos)
                        grid[bot2.pos[0]][bot2.pos[1]] = 0
        
        if not moved:
            break
            
        visualize(grid, bot1, bot2, step)
    
    total_cells = len(bot1.cleaned) + len(bot2.cleaned)
    efficiency = (total_cells / step) * 100 if step > 0 else 0
    
    print(f"\n{'='*50}")
    print(f"CLEANING COMPLETE!")
    print(f"{'='*50}")
    print(f"Total cells cleaned: {total_cells}")
    print(f"Total steps: {step}")
    print(f"Efficiency score: {efficiency:.2f}%")
    print(f"\033[94mBot 1\033[0m: {len(bot1.cleaned)} cells")
    print(f"\033[92mBot 2\033[0m: {len(bot2.cleaned)} cells")
    print(f"{'='*50}\n")

if _name_ == "_main_":
    main()