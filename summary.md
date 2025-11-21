# Dual Maze Navigator (P1)

## Overview
Two cooperative agents navigate a maze to collect all keys using BFS pathfinding and intelligent coordination.

## Objective
Agents explore different regions of a maze, collecting scattered keys while avoiding obstacles and coordinating to prevent overlap.

## How It Works

### Agents
- *Agent A*: Starts at position marked 'A'
- *Agent B*: Starts at position marked 'B'

### Maze Elements
- █ = Walls (obstacles)
- ⚷ = Keys to collect
- A B = Agent positions
- . = Visited paths
- ` ` = Empty walkable space

### Algorithm
1. *BFS Pathfinding*: Each agent uses Breadth-First Search to find shortest path to nearest key
2. *Cooperative Assignment*: Agent B avoids Agent A's target to explore different regions
3. *Collision Avoidance*: Agents treat each other as temporary obstacles
4. *Communication*: System displays coordination messages

### Coordination Logic
python
# Agent A targets nearest key
target_a = nearest_key(agent_a_position)

# Agent B targets nearest key excluding A's target
available_for_b = keys - {target_a}
target_b = nearest_key(agent_b_position, available_for_b)

# Special case: If only 1 key left, both agents can target it
if len(keys) == 1:
    both_agents_target_same_key()


## Features

✅ *BFS Exploration* - Optimal shortest path finding  
✅ *Cooperative Strategy* - Agents divide work intelligently  
✅ *Collision Avoidance* - Agents don't block each other  
✅ *Real-time Communication* - Shows agent coordination  
✅ *Path Tracking* - Visualizes explored areas  
✅ *Terminal-based* - No external dependencies  

## Usage

bash
python P1_dual_maze_navigator.py


## Example Output


Keys remaining: 3
Communication: Agent A targeting (1, 6), Agent B exploring other regions
------------------
█ █ █ █ █ █ █ █ █ 
█ . . . █ . A . █ 
█ . █ . █ . █ . █ 
█ ⚷ █ . . . . . █ 
█ . █ █ █ █ █ . █ 
█ . . . ⚷ . █ B █ 
█ █ █ █ █ █ █ █ █ 
------------------


## Configuration

Modify MAZE_LAYOUT to create custom mazes:
- 1 = Wall
- 0 = Empty space
- 'A' = Agent A start
- 'B' = Agent B start
- 'K' = Key location

## Key Metrics

- *Total keys collected*: Number of keys found
- *Path length*: Steps taken by agents
- *Completion time*: Total simulation steps

## Algorithm Complexity

- *Time*: O(n × m) per BFS where n×m is maze size
- *Space*: O(n × m) for visited tracking
- *Per step*: O(k) where k is number of keys

## Requirements

- Python 3.x
- collections (standard library)
- time (standard library)

## Related Projects

- *p5.py*: Rescue Bot Squad (similar BFS in maze)
- *p10.py*: Map Exploration (region partitioning)
- *aisi.py*: Enhanced version with better coordination


/////////////////////////////////////////////////////////////////////////////////////////////////////////

# Cleaning Crew Coordination (P2)

## Overview
Two cleaning bots divide a dirty grid and clean efficiently using A* pathfinding with non-overlapping paths.

## Objective
Design cleaning bots that divide rooms and clean efficiently without overlap, maximizing coverage and minimizing time.

## How It Works

### Bots
- *Bot 1 (🤖)*: Cleans top half (rows 0-2)
- *Bot 2 (🦾)*: Cleans bottom half (rows 3-5)

### Grid Elements
- 💩 = Dirty cells
- ⬜ = Clean/empty cells
- 🤖 🦾 = Bot positions
- ✨ = Cells cleaned by Bot 1
- 💎 = Cells cleaned by Bot 2

### Algorithm
1. *Grid Partitioning*: Horizontal division (50/50 split)
2. *A Pathfinding**: Optimal path to nearest dirty cell
3. *Greedy Strategy*: Always target closest dirty cell in assigned area
4. *Clean-as-you-go*: Bots clean cells they step on

## Features
✅ A* pathfinding for optimal routes  
✅ Non-overlapping task allocation  
✅ Real-time visualization  
✅ Efficiency scoring  
✅ 100% coverage guarantee  

## Usage
bash
python P2-cleaning_crew_coordination.py


## Configuration
python
grid = [[1]*8 for _ in range(6)]  # 6x8 grid, all dirty
mid_row = len(grid) // 2  # Horizontal split


## Output Metrics
- Total cells cleaned
- Total steps taken
- Efficiency score (cells/step %)
- Per-bot statistics

## Requirements
- Python 3.x
- heapq, time (standard library)


//////////////////////////////////////////////////////////////////////////////////////////////////////////
# Cooperative Path Planner (P3)

## Overview
Two agents navigate from start to goal positions using A* pathfinding with reservation-based collision avoidance.

## Objective
Plan collision-free paths for multiple agents using time-aware A* and reservation tables to prevent conflicts.

## How It Works

### Agents
- *Agent A*: Plans first (priority agent)
- *Agent B*: Plans with collision avoidance

### Grid Elements
- . = Free space
- # = Obstacles
- A = Agent A position
- B = Agent B position
- 1 2 = Goal positions
- X = Collision (if occurs)

### Algorithm
1. *Agent A Planning: Standard A pathfinding
2. *Reservation Table*: Agent A's path reserved in time-space
3. *Agent B Planning: Time-aware A avoiding Agent A's reservations
4. *Conflict Resolution*: Insert waits if conflicts remain

### Collision Avoidance
python
# Vertex conflict: Same cell at same time
if agent_b_pos == agent_a_reserved_pos:
    insert_wait()

# Swap conflict: Agents swap positions
if (a_prev, a_cur) == (b_cur, b_prev):
    insert_wait()


## Features
✅ A* pathfinding  
✅ Time-aware planning  
✅ Reservation-based coordination  
✅ Collision detection & resolution  
✅ Terminal animation  
✅ Swap conflict prevention  

## Usage
bash
python P3-cooperative_path_planner.py


## Configuration
python
grid = [[0,0,0], [0,1,0], [0,0,0]]  # 0=free, 1=obstacle
a1_start, a1_goal = (0,0), (4,5)
a2_start, a2_goal = (0,5), (4,0)


## Output
- Step-by-step animation
- Final positions
- Complete paths for both agents
- Collision warnings (if any)

## Key Concepts
- *Time-aware A: Plans in (x,y,t) space
- *Reservations*: Prevent conflicts by blocking cells
- *Priority Planning*: Agent A plans first, B avoids

## Requirements
- Python 3.x
- heapq, time, collections (standard library)


//////////////////////////////////////////////////////////////////////////////////////////////////////


# Warehouse Pickup Team (P4)

## Overview
Two warehouse agents cooperatively pick up items and deliver them to a drop zone using BFS pathfinding.

## Objective
Collect scattered items from warehouse and deliver to drop zone efficiently while avoiding obstacles and collisions.

## How It Works

### Agents
- *Agent 1 (🤖)*: Starts at (0,0)
- *Agent 2 (🦾)*: Starts at (4,0)

### Warehouse Elements
- 🤖 🦾 = Agents
- 📦 = Items to pick up
- 🎯 = Drop zone
- ✅ = Delivered items
- ██ = Obstacles
- Colored ░░ = Agent paths

### Workflow
1. *Assignment*: Items assigned to nearest agent (greedy)
2. *Pickup*: Agent navigates to item location
3. *Delivery*: Agent carries item to drop zone
4. *Repeat*: Continue until all items delivered

### Algorithm
- *BFS Pathfinding*: Shortest path to items and drop zone
- *Collision Avoidance*: Agents avoid each other's positions
- *Greedy Assignment*: Nearest item first

## Features
✅ BFS pathfinding  
✅ Collision avoidance  
✅ Item tracking  
✅ Delivery confirmation  
✅ Performance chart  

## Usage
bash
python P4-warehouse_pickup_team.py


## Configuration
python
self.items = [(1,3), (3,2), (4,5), (2,7)]  # Item locations
self.drop_zone = (2, 9)  # Delivery destination


## Output Metrics
- Total time (steps)
- Items delivered per agent
- Delivery chart

## Requirements
- Python 3.x
- collections.deque, time (standard library)


////////////////////////////////////////////////////////////////////////////////////////////////////



# Rescue Bot Squad (P5)

## Overview
Two rescue bots navigate a maze to find and rescue trapped victims using BFS and logic-based zone assignment.

## Objective
Rescue all victims from maze efficiently by dividing rescue zones based on proximity.

## How It Works

### Bots
- *Bot 1 (🤖)*: Starts at (1,1)
- *Bot 2 (🦾)*: Starts at (5,10)

### Maze Elements
- 🤖 🦾 = Rescue bots
- 🆘 = Victims to rescue
- ██ = Walls
- ░░ = Paths/walkable areas
- Colored ░░ = Bot paths (blue/green)

### Algorithm
1. *BFS Pathfinding*: Find shortest path to victims
2. *Logic-based Assignment*: Victims assigned to nearest bot
3. *Dynamic Reassignment*: If unreachable, reassign to other bot
4. *Collision Avoidance*: Bots navigate around each other

### Rescue Process

1. Assign victims by proximity
2. Bot navigates to victim
3. Rescue victim on arrival
4. Move to next victim
5. Repeat until all rescued


## Features
✅ BFS exploration  
✅ Proximity-based assignment  
✅ Dynamic reassignment  
✅ Maze navigation  
✅ Rescue confirmation  

## Usage
bash
python p5.py


## Configuration
python
self.victims = [(1,3), (3,9), (5,5), (1,10)]  # Victim locations
# Modify maze layout in __init__


## Output
- Total steps
- Victims rescued per bot
- Rescue locations

## Requirements
- Python 3.x
- collections.deque, time (standard library)



//////////////////////////////////////////////////////////////////////////////////////////////////////


# Dual Drone Delivery (P6)

## Overview
Two drones deliver packages to different locations using A* pathfinding and greedy assignment to minimize delivery time.

## Objective
Deliver packages to goal locations efficiently with minimal overlap and optimal routing.

## How It Works

### Drones
- *Drone 1 (🚁)*: Starts at (0,0)
- *Drone 2 (🚂)*: Starts at (11,19)

### Delivery Elements
- 🚁 🚂 = Drones
- 🎯 = Delivery goals (destinations)
- 📦 = Delivered packages
- Blue/Green · = Drone paths

### Algorithm
1. *A Pathfinding**: Optimal routes to goals
2. *Greedy Assignment*: Nearest goal first
3. *Sequential Delivery*: One goal at a time per drone
4. *Goal Transformation*: 🎯 → 📦 on delivery

### Delivery Process

1. Assign goals by proximity
2. Drone navigates to goal
3. Mark as delivered (🎯 → 📦)
4. Move to next goal
5. Repeat until complete


## Features
✅ A* pathfinding  
✅ Greedy package assignment  
✅ Delivery confirmation  
✅ Coverage heatmap  
✅ Performance metrics  

## Usage
bash
python p6.py


## Configuration
python
self.goals = [(2,18), (5,3), (9,10), (7,15)]  # Delivery locations
self.rows, self.cols = 12, 20  # Grid size


## Output Metrics
- Total delivery time
- Path length per drone
- Coverage heatmap (visit frequency)

## Requirements
- Python 3.x
- heapq, time (standard library)




///////////////////////////////////////////////////////////////////////////////////////////////////



# Grid Painting Agents (P7)

## Overview
Two robots paint cells on a grid without overlapping using DFS and rule-based task allocation.

## Objective
Paint all grid cells cooperatively with color-coded coverage showing each agent's work area.

## How It Works

### Robots
- *Robot A (🤖)*: Starts at (0,0) - paints left half
- *Robot B (🦾)*: Starts at (0,8) - paints right half

### Grid Elements
- 🤖 🦾 = Robot positions
- ⬜ = Unpainted cells
- Blue ░░ = Robot A painted
- Green ░░ = Robot B painted

### Algorithm
1. *DFS (Depth-First Search)*: Systematic exploration and painting
2. *Vertical Partitioning*: Grid divided into left/right halves
3. *Rule-based Allocation*: Each robot has exclusive painting area
4. *Sequential Painting*: Robots paint one cell at a time

### Painting Process

1. Divide grid vertically (50/50)
2. Each robot explores its region using DFS
3. Paint cells as they're visited
4. Continue until entire region painted
5. Display final coverage


## Features
✅ DFS exploration algorithm  
✅ Zero overlap (100% coordination)  
✅ Color-coded visualization  
✅ Coverage statistics  
✅ Step-by-step animation  
✅ Bordered grid display  

## Usage
bash
python P7-grid_colour.py


## Configuration
python
self.rows, self.cols = 10, 16  # Grid size
mid_col = self.cols // 2  # Vertical split point


## Output Metrics
- Total cells painted
- Cells painted per robot
- Overlap count (should be 0)
- Coverage percentage

## Visualization

┌────────────────────────────────┐
│🤖░░░░░░░░░░░░░░░░🦾░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└────────────────────────────────┘


## Key Concepts
- *DFS*: Explores deeply before backtracking
- *Partitioning*: Prevents overlap by region assignment
- *Coordination*: 100% through exclusive areas

## Requirements
- Python 3.x
- time (standard library)

## Related Projects
- *P2: Cleaning Crew (A pathfinding)
- *P10*: Map Exploration (region partitioning)


//////////////////////////////////////////////////////////////////////////////////////////////////////


# Resource Collection Team (P8)

## Overview
Three agents cooperatively collect resources from a map using shared task queue and distributed decision logic.

## Objective
Collect scattered resources efficiently by assigning tasks to nearest available agent.

## How It Works

### Agents
- *Agent 1 (🤖)*: Starts at (0,0)
- *Agent 2 (🦾)*: Starts at (9,15)
- *Agent 3 (🚁)*: Starts at (0,15)

### Map Elements
- 🤖 🦾 🚁 = Agents
- 💎 = Resources to collect
- Colored · = Agent paths (blue/green/yellow)
- ⬜ = Empty cells

### Algorithm
1. *Shared Task Queue*: All resources in central queue
2. *Distributed Decision*: Assign to nearest agent
3. *BFS Pathfinding*: Shortest path to resource
4. *Dynamic Assignment*: Reassign on each collection

### Collection Process

1. Find nearest agent-resource pair
2. Assign resource to agent
3. Agent navigates to resource
4. Collect resource
5. Repeat until queue empty


## Features
✅ Shared task queue  
✅ Distributed decision logic  
✅ BFS pathfinding  
✅ Dynamic task assignment  
✅ Collection charts  

## Usage
bash
python p8.py


## Configuration
python
self.task_queue = [(1,3), (2,14), (4,8), ...]  # Resource locations
self.rows, self.cols = 10, 16  # Grid size


## Output
- Total time
- Resources per agent
- Bar chart
- Distribution graph

## Requirements
- Python 3.x
- collections.deque, time (standard library)



///////////////////////////////////////////////////////////////////////////////////////////////////////

# Cooperative Firefighters (P9)

## Overview
Two firefighter agents extinguish fires in different zones using BFS pathfinding and cooperative task allocation with fire spread simulation.

## Objective
Extinguish all fires efficiently while dealing with fire spread using coordinated zone assignment.

## How It Works

### Agents
- *Agent 1 (🚒)*: Starts at (0,0)
- *Agent 2 (🚑)*: Starts at (9,15)

### Fire Elements
- 🚒 🚑 = Firefighter agents
- 🔥 = Active fires
- Blue/Green · = Agent paths
- ⬜ = Empty cells

### Algorithm
1. *BFS Pathfinding*: Shortest path to fires
2. *Cooperative Assignment*: Fires divided by proximity
3. *Fire Spread Simulation*: Fires spread every 8 steps (BFS-based)
4. *Dynamic Reassignment*: New fires assigned to nearest agent

### Fire Spread Logic
python
# Every 8 steps, fires spread to adjacent cells
if step % 8 == 0:
    spread_fire()  # BFS to adjacent cells


### Firefighting Process

1. Assign fires by proximity
2. Agent navigates to fire
3. Extinguish on arrival
4. Handle fire spread
5. Repeat until all extinguished


## Features
✅ BFS pathfinding  
✅ Fire spread simulation  
✅ Cooperative task allocation  
✅ Dynamic reassignment  
✅ Progress graph  

## Usage
bash
python p9.py


## Configuration
python
self.fires = [(1,2), (3,8), (7,5), ...]  # Initial fires
self.spread_interval = 8  # Steps between spreads
self.rows, self.cols = 10, 16  # Grid size


## Output
- Total time
- Fires extinguished per agent
- Fire spread events
- ASCII progress graph

## Requirements
- Python 3.x
- collections.deque, time (standard library)

///////////////////////////////////////////////////////////////////////////////////////////////////


# Map Exploration Partners (p10)

## Overview
A cooperative multi-agent system where three autonomous agents explore an unknown map efficiently using grid partitioning and greedy exploration strategies.

## Objective
Agents explore unknown regions together by dividing the map into non-overlapping zones and systematically covering all cells with minimal redundancy.

## Features

### Core Functionality
- *3 Cooperative Agents*: Work simultaneously to explore the entire map
- *Grid Partitioning*: Map divided into 3 vertical regions for efficient coverage
- *Greedy Exploration*: Each agent moves to nearest unexplored cell in its region
- *Real-time Visualization*: Terminal-based display with color-coded exploration
- *Efficiency Metrics*: Coverage percentage, cells/step efficiency, overlap analysis

### Algorithms Used
- *Grid Partitioning Logic*: Vertical division of map into equal regions
- *Greedy Nearest-Neighbor*: Agents prioritize closest unexplored cells
- *Manhattan Distance*: Used for proximity calculations

## How It Works

1. *Initialization*
   - 8×12 grid (96 total cells)
   - Agent 1 (🤖) starts at top-left (0,0) - explores left region
   - Agent 2 (🦾) starts at bottom-right (7,11) - explores middle region
   - Agent 3 (🚁) starts at top-right (0,11) - explores right region

2. *Exploration Process*
   - Each agent identifies unexplored cells in its assigned region
   - Moves one step towards nearest unexplored cell
   - Marks cell as explored upon visit
   - Continues until entire map is covered

3. *Coordination*
   - Non-overlapping regions prevent conflicts
   - Shared exploration state tracks all visited cells
   - Agents work in parallel for maximum efficiency

## Visualization

### During Exploration

┌────────────────────────┐
│🤖░░░░░░░░██████████████│
│░░░░░░░░░░██████████🚁│
│░░░░░░░░░░██████████░░│
│░░░░░░░░░░██████████░░│
│░░░░░░░░░░██████████░░│
│░░░░░░░░░░██████████░░│
│░░░░░░░░░░██████████░░│
│░░░░░░░░░░🦾░░░░░░░░░░│
└────────────────────────┘


*Legend:*
- 🤖 🦾 🚁 = Agent positions
- ██ = Unexplored (dark blocks)
- ░░ = Explored (light shaded, color-coded by agent)
- Blue = Agent 1's path
- Green = Agent 2's path
- Yellow = Agent 3's path

### Efficiency Heatmap
Shows exploration efficiency with color-coded visit frequency:
- ██ Unexplored (black)
- 🟩 Explored once (efficient)
- 🟨 Explored twice (some overlap)
- 🟥 Explored 3+ times (inefficient overlap)

### Progress Graph
ASCII chart showing cells explored over time.

## Output

### Final Statistics
- *Total steps*: Time taken to complete exploration
- *Coverage*: Percentage of map explored (target: 100%)
- *Efficiency*: Cells explored per step
- *Per-agent stats*: Cells explored by each agent
- *Heatmap*: Visual representation of exploration efficiency
- *Progress graph*: Exploration timeline

## Usage

bash
python p10.py


## Requirements
- Python 3.x
- time module (standard library)

## Configuration

Modify these parameters in MapExplorationSystem.__init__():
python
self.rows, self.cols = 8, 12  # Grid size


Adjust number of agents by modifying the agents list initialization.

## Key Metrics

- *Coverage*: Should reach 100% for complete exploration
- *Efficiency*: Higher is better (optimal ≈ 3.0 cells/step with 3 agents)
- *Overlap*: Lower is better (shown in heatmap)

## Algorithm Complexity

- *Time*: O(n × m) where n×m is grid size
- *Space*: O(n × m) for tracking explored cells
- *Per-step*: O(k × r) where k = agents, r = region size

## Example Output


EXPLORATION COMPLETE!
======================================================================
Total steps: 35
Coverage: 100.0% (96/96)
Efficiency: 2.74 cells/step
🤖 Agent 1: 32 cells
🦾 Agent 2: 32 cells
🚁 Agent 3: 32 cells


## Notes

- Agents explore their assigned regions independently
- Grid partitioning ensures minimal overlap
- Greedy strategy provides fast but not optimal exploration
- Visual feedback shows real-time progress
- Terminal must support Unicode and ANSI colors

## Related Projects

- *p5.py*: Rescue Bot Squad (BFS pathfinding in maze)
- *p6.py: Dual Drone Delivery (A pathfinding)
- *p8.py*: Resource Collection Team (shared task queue)
- *p9.py*: Cooperative Firefighters (fire spread simulation)