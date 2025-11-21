import time

class ExplorerAgent:
    def __init__(self, agent_id, start_pos, symbol):
        self.id, self.pos, self.symbol, self.explored = agent_id, start_pos, symbol, [start_pos]
    
    def explore_next(self, region, explored_all):
        # Find nearest unexplored cell in assigned region
        unexplored = [cell for cell in region if cell not in explored_all]
        if not unexplored: return None
        
        nearest = min(unexplored, key=lambda c: abs(c[0]-self.pos[0]) + abs(c[1]-self.pos[1]))
        
        # Move towards nearest (greedy)
        dr = 1 if nearest[0] > self.pos[0] else (-1 if nearest[0] < self.pos[0] else 0)
        dc = 1 if nearest[1] > self.pos[1] else (-1 if nearest[1] < self.pos[1] else 0)
        
        new_pos = (self.pos[0] + dr, self.pos[1] + dc)
        self.pos = new_pos
        
        if new_pos not in self.explored:
            self.explored.append(new_pos)
        
        return new_pos


class MapExplorationSystem:
    def __init__(self):
        self.rows, self.cols = 8, 12
        self.total_cells = self.rows * self.cols
        
        # Agents
        self.agent1 = ExplorerAgent(1, (0, 0), "🤖")
        self.agent2 = ExplorerAgent(2, (self.rows-1, self.cols-1), "🦾")
        self.agent3 = ExplorerAgent(3, (0, self.cols-1), "🚁")
        
        self.agents = [self.agent1, self.agent2, self.agent3]
        self.step = 0
        self.exploration_log = []
        
        self.partition_regions()
    
    def partition_regions(self):
        # Grid partitioning logic: divide map into 3 regions
        all_cells = [(i, j) for i in range(self.rows) for j in range(self.cols)]
        
        # Vertical partitioning
        third = self.cols // 3
        
        self.region1 = [(i, j) for i in range(self.rows) for j in range(third)]
        self.region2 = [(i, j) for i in range(self.rows) for j in range(third, 2*third)]
        self.region3 = [(i, j) for i in range(self.rows) for j in range(2*third, self.cols)]
        
        self.regions = [self.region1, self.region2, self.region3]
    
    def visualize(self):
        print("\n" * 2)
        print(f"{'='*50}")
        print(f"MAP EXPLORATION - Step {self.step}")
        print(f"{'='*50}\n")
        
        explored_all = set()
        for agent in self.agents:
            explored_all.update(agent.explored)
        
        # Top border
        print("┌" + "──" * self.cols + "┐")
        
        for i in range(self.rows):
            row = "│"
            for j in range(self.cols):
                if (i, j) == self.agent1.pos:
                    row += "🤖"
                elif (i, j) == self.agent2.pos:
                    row += "🦾"
                elif (i, j) == self.agent3.pos:
                    row += "🚁"
                elif (i, j) in self.agent1.explored:
                    row += "\033[94m░░\033[0m"
                elif (i, j) in self.agent2.explored:
                    row += "\033[92m░░\033[0m"
                elif (i, j) in self.agent3.explored:
                    row += "\033[93m░░\033[0m"
                else:
                    row += "██"
            row += "│"
            print(row)
        
        # Bottom border
        print("└" + "──" * self.cols + "┘")
        
        coverage = (len(explored_all) / self.total_cells) * 100
        print(f"\n🤖 Agent 1: {len(self.agent1.explored)} | 🦾 Agent 2: {len(self.agent2.explored)} | 🚁 Agent 3: {len(self.agent3.explored)}")
        print(f"Coverage: {coverage:.1f}% ({len(explored_all)}/{self.total_cells})")
        time.sleep(0.1)
    
    def run(self):
        print(f"\nStarting Map Exploration System...")
        print(f"Map size: {self.rows}x{self.cols} = {self.total_cells} cells")
        print(f"🤖 Agent 1: {self.agent1.pos} (Region 1)")
        print(f"🦾 Agent 2: {self.agent2.pos} (Region 3)")
        print(f"🚁 Agent 3: {self.agent3.pos} (Region 3)\n")
        
        self.visualize()
        
        explored_all = set()
        for agent in self.agents:
            explored_all.update(agent.explored)
        
        while len(explored_all) < self.total_cells:
            self.step += 1
            moved = False
            
            for i, agent in enumerate(self.agents):
                pos = agent.explore_next(self.regions[i], explored_all)
                if pos:
                    explored_all.add(pos)
                    moved = True
            
            if not moved:
                break
            
            self.exploration_log.append(len(explored_all))
            self.visualize()
        
        self.show_results()
    
    def show_results(self):
        explored_all = set()
        for agent in self.agents:
            explored_all.update(agent.explored)
        
        coverage = (len(explored_all) / self.total_cells) * 100
        efficiency = (len(explored_all) / self.step) if self.step > 0 else 0
        
        print(f"\n{'='*70}\nEXPLORATION COMPLETE!\n{'='*70}")
        print(f"Total steps: {self.step}")
        print(f"Coverage: {coverage:.1f}% ({len(explored_all)}/{self.total_cells})")
        print(f"Efficiency: {efficiency:.2f} cells/step")
        print(f"🤖 Agent 1: {len(self.agent1.explored)} cells")
        print(f"🦾 Agent 2: {len(self.agent2.explored)} cells")
        print(f"🚁 Agent 3: {len(self.agent3.explored)} cells")
        
        # Exploration heatmap
        print(f"\n{'='*70}\nEXPLORATION EFFICIENCY HEATMAP\n{'='*70}\n")
        
        # Create visit count map
        visit_map = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for agent in self.agents:
            for pos in agent.explored:
                visit_map[pos[0]][pos[1]] += 1
        
        max_visits = max(max(row) for row in visit_map)
        
        print("Legend: ██ Unexplored | 🟩 Low | 🟨 Medium | 🟥 High\n")
        
        # Top border
        print("┌" + "──" * self.cols + "┐")
        
        for i in range(self.rows):
            row = "│"
            for j in range(self.cols):
                visits = visit_map[i][j]
                if visits == 0:
                    row += "██"
                elif visits == 1:
                    row += "\033[92m░░\033[0m"  # Green - explored once
                elif visits == 2:
                    row += "\033[93m▒▒\033[0m"  # Yellow - explored twice
                else:
                    row += "\033[91m▓▓\033[0m"  # Red - explored 3+ times
            row += "│"
            print(row)
        
        # Bottom border
        print("└" + "──" * self.cols + "┘")
        
        # Exploration progress graph
        print(f"\n{'='*70}\nEXPLORATION PROGRESS\n{'='*70}\n")
        
        if self.exploration_log:
            max_cells = self.total_cells
            step_interval = max(1, len(self.exploration_log) // 20)
            
            print("Cells")
            for level in range(max_cells, -1, -max_cells//10):
                line = f"{level:3d} |"
                for idx, cells in enumerate(self.exploration_log):
                    if idx % step_interval == 0:
                        line += "█" if cells >= level else " "
                print(line)
            
            print("    +" + "-" * (len(self.exploration_log) // step_interval + 1))
            print("     Time (steps)")
        
        print(f"\n{'='*70}\n")


if __name__ == "__main__":
    system = MapExplorationSystem()
    system.run()