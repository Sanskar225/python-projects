import time
from collections import deque

class CollectorAgent:
    def __init__(self, agent_id, start_pos, symbol):
        self.id, self.pos, self.symbol, self.collected, self.path = agent_id, start_pos, symbol, [], []
    
    def bfs(self, start, goals, grid):
        if not goals: return None, []
        queue, visited = deque([(start, [])]), {start}
        while queue:
            pos, path = queue.popleft()
            if pos in goals: return pos, path + [pos]
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [pos]))
        return None, []


class ResourceCollectionSystem:
    def __init__(self):
        self.rows, self.cols = 10, 16
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Shared task queue - resources
        self.task_queue = [(1, 3), (2, 14), (4, 8), (6, 5), (7, 12), (8, 2), (3, 10), (5, 15)]
        self.all_resources = list(self.task_queue)
        
        # Agents
        self.agent1 = CollectorAgent(1, (0, 0), "🤖")
        self.agent2 = CollectorAgent(2, (self.rows-1, self.cols-1), "🦾")
        self.agent3 = CollectorAgent(3, (0, self.cols-1), "🚁")
        
        self.agents = [self.agent1, self.agent2, self.agent3]
        self.step = 0
    
    def assign_task(self):
        # Distributed decision logic: assign nearest resource from queue
        if not self.task_queue: return None, None
        
        best_agent, best_resource, min_dist = None, None, float('inf')
        for agent in self.agents:
            for resource in self.task_queue:
                dist = abs(resource[0] - agent.pos[0]) + abs(resource[1] - agent.pos[1])
                if dist < min_dist:
                    min_dist, best_agent, best_resource = dist, agent, resource
        
        # Don't remove from queue yet - remove when actually collected
        return best_agent, best_resource
    
    def visualize(self):
        print("\n" * 2)
        print(f"{'='*60}")
        print(f"RESOURCE COLLECTION TEAM - Step {self.step}")
        print(f"{'='*60}\n")
        
        for i in range(self.rows):
            row = ""
            for j in range(self.cols):
                if (i, j) == self.agent1.pos:
                    row += "🤖 "
                elif (i, j) == self.agent2.pos:
                    row += "🦾 "
                elif (i, j) == self.agent3.pos:
                    row += "🚁 "
                elif (i, j) in self.task_queue:
                    row += "💎 "
                elif (i, j) in self.agent1.collected:
                    row += "\033[94m·\033[0m "
                elif (i, j) in self.agent2.collected:
                    row += "\033[92m·\033[0m "
                elif (i, j) in self.agent3.collected:
                    row += "\033[93m·\033[0m "
                else:
                    row += "⬜ "
            print(row)
        
        print(f"\n🤖 Agent 1: {len(self.agent1.collected)} | 🦾 Agent 2: {len(self.agent2.collected)} | 🚁 Agent 3: {len(self.agent3.collected)}")
        print(f"💎 Resources remaining: {len(self.task_queue)}")
        time.sleep(0.15)
    
    def run(self):
        print(f"\nStarting Resource Collection System...")
        print(f"🤖 Agent 1: {self.agent1.pos} | 🦾 Agent 2: {self.agent2.pos} | 🚁 Agent 3: {self.agent3.pos}")
        print(f"💎 Total resources: {len(self.all_resources)}\n")
        
        self.visualize()
        
        while self.task_queue:
            agent, resource = self.assign_task()
            
            if not agent or not resource:
                break
            
            path = agent.bfs(agent.pos, [resource], self.grid)[1]
            
            if path:
                for pos in path:
                    self.step += 1
                    agent.pos = pos
                    if pos not in agent.path:
                        agent.path.append(pos)
                    self.visualize()
                
                # Remove from queue when actually collected
                if resource in self.task_queue:
                    self.task_queue.remove(resource)
                agent.collected.append(resource)
                print(f"\n{agent.symbol} Agent {agent.id} collected resource at {resource}!")
                time.sleep(0.3)
        
        self.show_results()
    
    def show_results(self):
        total = sum(len(agent.collected) for agent in self.agents)
        print(f"\n{'='*60}\nALL RESOURCES COLLECTED!\n{'='*60}")
        print(f"Total time: {self.step} steps\nTotal resources: {total}")
        
        # Bar chart
        print(f"\n{'='*60}\nRESOURCE COLLECTION CHART\n{'='*60}\n")
        max_collected = max(len(agent.collected) for agent in self.agents)
        
        for agent in self.agents:
            bar = "█" * len(agent.collected)
            print(f"{agent.symbol} Agent {agent.id}: {bar} ({len(agent.collected)})")
        
        # Horizontal bar graph
        print(f"\n{'='*60}\nCOLLECTION DISTRIBUTION\n{'='*60}\n")
        print("Resources")
        for level in range(max_collected, -1, -1):
            line = f"{level:2d} |"
            for agent in self.agents:
                line += " 💎 " if len(agent.collected) >= level else "   "
            print(line)
        print("   +" + "---" * len(self.agents))
        print("     " + "  ".join([f"A{agent.id}" for agent in self.agents]))
        
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    system = ResourceCollectionSystem()
