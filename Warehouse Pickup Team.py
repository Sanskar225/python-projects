import time
from collections import deque

class WarehouseAgent:
    def __init__(self, agent_id, start_pos, symbol):
        self.id, self.pos, self.symbol, self.collected, self.path = agent_id, start_pos, symbol, [], []
    
    def bfs(self, start, goal, grid, obstacles):
        if not goal: return []
        queue, visited = deque([(start, [])]), {start}
        while queue:
            pos, path = queue.popleft()
            if pos == goal: return path + [pos]
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                if (0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and 
                    grid[nx][ny] == 0 and (nx, ny) not in visited and (nx, ny) not in obstacles):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [pos]))
        return []


class WarehouseSystem:
    def _init_(self):
        # Warehouse grid: 0=path, 1=obstacle
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        
        self.rows, self.cols = len(self.grid), len(self.grid[0])
        
        # Drop-off zone
        self.drop_zone = (2, 9)
        
        # Items to pick up
        self.items = [(1, 3), (3, 2), (4, 5), (2, 7)]
        self.delivered = []
        
        # Agents
        self.agent1 = WarehouseAgent(1, (0, 0), "🤖")
        self.agent2 = WarehouseAgent(2, (4, 0), "🦾")
        
        self.agents = [self.agent1, self.agent2]
        self.step = 0
        
        self.assign_items()
    
    def assign_items(self):
        # Greedy assignment: nearest items
        available = list(self.items)
        self.agent1_items = []
        self.agent2_items = []
        
        while available:
            # Agent 1's turn
            if available:
                nearest = min(available, key=lambda i: abs(i[0]-self.agent1.pos[0]) + abs(i[1]-self.agent1.pos[1]))
                self.agent1_items.append(nearest)
                available.remove(nearest)
            
            # Agent 2's turn
            if available:
                nearest = min(available, key=lambda i: abs(i[0]-self.agent2.pos[0]) + abs(i[1]-self.agent2.pos[1]))
                self.agent2_items.append(nearest)
                available.remove(nearest)
    
    def visualize(self):
        print("\n" * 2)
        print(f"{'='*50}")
        print(f"WAREHOUSE PICKUP TEAM - Step {self.step}")
        print(f"{'='*50}\n")
        
        # Top border
        print("┌" + "──" * self.cols + "┐")
        
        for i in range(self.rows):
            row = "│"
            for j in range(self.cols):
                if (i, j) == self.agent1.pos:
                    row += "🤖"
                elif (i, j) == self.agent2.pos:
                    row += "🦾"
                elif (i, j) == self.drop_zone:
                    row += "🎯"
                elif (i, j) in self.items:
                    row += "📦"
                elif (i, j) in self.delivered:
                    row += "✅"
                elif (i, j) in self.agent1.path:
                    row += "\033[94m░░\033[0m"
                elif (i, j) in self.agent2.path:
                    row += "\033[92m░░\033[0m"
                elif self.grid[i][j] == 1:
                    row += "██"
                else:
                    row += "  "
            row += "│"
            print(row)
        
        # Bottom border
        print("└" + "──" * self.cols + "┘")
        
        print(f"\n🤖 Agent 1: {len(self.agent1.collected)} delivered | 🦾 Agent 2: {len(self.agent2.collected)} delivered")
        print(f"📦 Items remaining: {len(self.items)} | ✅ Delivered: {len(self.delivered)}")
        time.sleep(0.15)
    
    def deliver_item(self, agent, item_list, symbol):
        if not item_list: return False
        
        item = item_list[0]
        
        # Get other agent's position to avoid collision
        other_pos = [a.pos for a in self.agents if a.id != agent.id]
        
        # Go to item
        path_to_item = agent.bfs(agent.pos, item, self.grid, other_pos)
        if not path_to_item: return False
        
        for pos in path_to_item:
            self.step += 1
            agent.pos = pos
            if pos not in agent.path:
                agent.path.append(pos)
            self.visualize()
        
        # Pick up item
        self.items.remove(item)
        print(f"\n{symbol} Agent {agent.id} picked up item at {item}!")
        time.sleep(0.3)
        
        # Go to drop zone
        path_to_drop = agent.bfs(agent.pos, self.drop_zone, self.grid, other_pos)
        if not path_to_drop: return False
        
        for pos in path_to_drop:
            self.step += 1
            agent.pos = pos
            if pos not in agent.path:
                agent.path.append(pos)
            self.visualize()
        
        # Deliver item
        agent.collected.append(item)
        self.delivered.append(item)
        item_list.pop(0)
        print(f"\n{symbol} Agent {agent.id} delivered item to drop zone!")
        time.sleep(0.3)
        
        return True
    
    def run(self):
        print("\nStarting Warehouse Pickup Team...")
        print(f"🤖 Agent 1: {self.agent1.pos}")
        print(f"🦾 Agent 2: {self.agent2.pos}")
        print(f"🎯 Drop zone: {self.drop_zone}")
        print(f"📦 Items: {self.items}")
        print(f"Agent 1 assigned: {self.agent1_items}")
        print(f"Agent 2 assigned: {self.agent2_items}\n")
        
        self.visualize()
        
        # Deliver all items
        while self.agent1_items or self.agent2_items:
            # Agent 1 delivery
            if not self.deliver_item(self.agent1, self.agent1_items, "🤖"):
                if self.agent1_items:
                    self.agent1_items.pop(0)
            
            # Agent 2 delivery
            if not self.deliver_item(self.agent2, self.agent2_items, "🦾"):
                if self.agent2_items:
                    self.agent2_items.pop(0)
        
        self.show_results()
    
    def show_results(self):
        total = len(self.agent1.collected) + len(self.agent2.collected)
        
        print(f"\n{'='*50}\nALL ITEMS DELIVERED!\n{'='*50}")
        print(f"Total time: {self.step} steps")
        print(f"Total items delivered: {total}")
        print(f"🤖 Agent 1: {len(self.agent1.collected)} items")
        print(f"🦾 Agent 2: {len(self.agent2.collected)} items")
        
        # Delivery chart
        print(f"\n{'='*50}\nDELIVERY CHART\n{'='*50}\n")
        
        max_items = max(len(self.agent1.collected), len(self.agent2.collected))
        
        for agent in self.agents:
            bar = "█" * len(agent.collected)
            print(f"{agent.symbol} Agent {agent.id}: {bar} ({len(agent.collected)})")
        
        print(f"\n{'='*50}\n")


if __name__ == "__main__":
    system = WarehouseSystem()
    system.run()