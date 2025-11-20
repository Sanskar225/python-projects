# warehouse_pickup_team.py
# Simple terminal-run Warehouse Pickup Team simulator (pure Python 3)

import heapq
import time
import os
from collections import defaultdict, deque

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def astar_grid(start, goal, grid):
    R,C = len(grid), len(grid[0])
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start,goal), 0, start, None))
    came = {}
    gscore = {start:0}
    while open_heap:
        f,g,pos,parent = heapq.heappop(open_heap)
        if pos in came:
            continue
        came[pos] = parent
        if pos == goal:
            path=[]
            cur = pos
            while cur is not None:
                path.append(cur)
                cur = came[cur]
            return list(reversed(path))
        r,c = pos
        for dr,dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nr,nc = r+dr, c+dc
            if 0<=nr<R and 0<=nc<C and grid[nr][nc]==0:
                ng = g+1
                neigh = (nr,nc)
                if ng < gscore.get(neigh,1e9):
                    gscore[neigh]=ng
                    heapq.heappush(open_heap,(ng + heuristic(neigh,goal), ng, neigh, pos))
    return None

def astar_time_aware(start, goal, grid, reservations, start_time=0, max_time=1000):
    R,C = len(grid), len(grid[0])
    start_state = (start[0], start[1], start_time)
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start,goal)+start_time, 0, start_state, None))
    came = {}
    gscore = {start_state:0}
    while open_heap:
        f,g,state,parent = heapq.heappop(open_heap)
        if state in came:
            continue
        came[state] = parent
        r,c,t = state
        if (r,c) == goal and t >= start_time:
            path=[]
            cur = state
            while cur is not None:
                path.append((cur[0],cur[1],cur[2]))
                cur = came[cur]
            path.reverse()
            return [(p[0],p[1]) for p in path]
        if t+1 > max_time:
            continue
        for dr,dc in ((-1,0),(1,0),(0,-1),(0,1),(0,0)):
            nr,nc = r+dr, c+dc
            nt = t+1
            if not (0<=nr<R and 0<=nc<C): 
                continue
            if grid[nr][nc]==1:
                continue
            if nt in reservations and (nr,nc) in reservations[nt]:
                continue
            if nt in reservations and ('edge',(nr,nc,r,c)) in reservations[nt]:
                continue
            next_state = (nr,nc,nt)
            ng = g+1
            if ng < gscore.get(next_state, 1e9):
                gscore[next_state]=ng
                heapq.heappush(open_heap,(ng + heuristic((nr,nc),goal), ng, next_state, state))
    return None

def reserve_path_timed(path, reservations, hold_time=30):
    for t,pos in enumerate(path):
        reservations[t].add(pos)
        if t>0:
            prev = path[t-1]
            reservations[t].add(('edge',(prev[0],prev[1],pos[0],pos[1])))
    final = path[-1]
    for future in range(len(path), len(path)+hold_time):
        reservations[future].add(final)

def pad(plans):
    L = max(len(p) for p in plans)
    return [p + [p[-1]]*(L-len(p)) for p in plans]

def compute_metrics(plans, drop, tasks_count):
    L = max(len(p) for p in plans) - 1
    distances = [0]*len(plans)
    deliveries = 0
    # track deliveries by counting arrivals at drop from non-drop
    for t in range(1, L+1):
        for i,p in enumerate(plans):
            prev = p[t-1]
            cur  = p[t]
            if cur != prev:
                distances[i]+=1
            if cur == drop and prev != drop:
                deliveries += 1
    total_distance = sum(distances)
    makespan = L
    total_items = min(deliveries, tasks_count)
    throughput = total_items / makespan if makespan>0 else 0
    efficiency = total_items / total_distance if total_distance>0 else 0
    return {
        'total_items': total_items,
        'makespan': makespan,
        'total_distance': total_distance,
        'throughput': throughput,
        'efficiency': efficiency
    }

def print_table(metrics):
    print("\nResults:")
    print(f"{'Total Items':<15}{'Makespan':<12}{'Total Dist':<14}{'Throughput':<12}{'Efficiency':<12}")
    print(f"{metrics['total_items']:<15}{metrics['makespan']:<12}{metrics['total_distance']:<14}"
          f"{metrics['throughput']:<12.3f}{metrics['efficiency']:<12.3f}")

def run_simulation(grid, agents, tasks, drop, pause=0.05):
    # assign tasks greedily by proximity: always assign next nearest task to the agent whose endpoint is closest
    remaining = list(tasks)
    for a in agents:
        a['assigned'] = []
    # initial endpoints are agent starts
    endpoints = [a['pos'] for a in agents]
    while remaining:
        best_agent = None
        best_task = None
        best_dist = 1e9
        for ti,task in enumerate(remaining):
            for ai,ep in enumerate(endpoints):
                d = heuristic(ep, task)
                if d < best_dist:
                    best_dist = d
                    best_agent = ai
                    best_task = ti
        agents[best_agent]['assigned'].append(remaining.pop(best_task))
        endpoints[best_agent] = agents[best_agent]['assigned'][-1]
    # prioritized time-aware planning: plan agents sequentially, reserving earlier agents
    reservations = defaultdict(set)
    plans = []
    for ai,a in enumerate(agents):
        cur_time = 0
        cur_pos = a['pos']
        plan = [(cur_pos[0],cur_pos[1])]  # includes t=0
        for task in a['assigned']:
            # plan to pickup
            seg1 = astar_time_aware(cur_pos, task, grid, reservations, start_time=cur_time, max_time=1000)
            if seg1 is None:
                # fallback to static A* then insert waits to avoid reservations
                seg1_static = astar_grid(cur_pos, task, grid)
                if seg1_static is None:
                    raise RuntimeError("No path to pickup found")
                # simulate with waits
                for step in seg1_static[1:]:
                    t = cur_time + 1
                    if t in reservations and step in reservations[t]:
                        plan.append(plan[-1])
                        cur_time += 1
                    else:
                        plan.append(step)
                        cur_time += 1
                cur_pos = plan[-1]
            else:
                # seg1 is list of positions with times starting at cur_time ... return includes time progression
                for pos in seg1[1:]:
                    plan.append(pos)
                    cur_time += 1
                cur_pos = plan[-1]
            # now plan pickup -> drop
            seg2 = astar_time_aware(cur_pos, drop, grid, reservations, start_time=cur_time, max_time=1000)
            if seg2 is None:
                seg2_static = astar_grid(cur_pos, drop, grid)
                if seg2_static is None:
                    raise RuntimeError("No path to drop found")
                for step in seg2_static[1:]:
                    t = cur_time + 1
                    if t in reservations and step in reservations[t]:
                        plan.append(plan[-1])
                        cur_time += 1
                    else:
                        plan.append(step)
                        cur_time += 1
                cur_pos = plan[-1]
            else:
                for pos in seg2[1:]:
                    plan.append(pos)
                    cur_time += 1
                cur_pos = plan[-1]
        # reserve this plan into reservations
        for t,pos in enumerate(plan):
            reservations[t].add(pos)
            if t>0:
                prev = plan[t-1]
                reservations[t].add(('edge',(prev[0],prev[1],pos[0],pos[1])))
        # extend final hold
        final = plan[-1]
        for ft in range(len(plan), len(plan)+30):
            reservations[ft].add(final)
        plans.append(plan)
    # pad plans to equal length
    plans = pad(plans)
    # print a quick animation (optional)
    for t in range(len(plans[0])):
        clear_screen()
        print(f"Time step {t} / {len(plans[0])-1}")
        R,C = len(grid), len(grid[0])
        disp = [['.' if grid[r][c]==0 else '#' for c in range(C)] for r in range(R)]
        for idx,p in enumerate(plans):
            r,c = p[t]
            disp[r][c] = str(idx+1)
        disp[drop[0]][drop[1]] = 'D'
        for row in disp:
            print("".join(row))
        time.sleep(pause)
    metrics = compute_metrics(plans, drop, len(tasks))
    print_table(metrics)
    return plans, metrics

if __name__ == "__main__":
    # example warehouse map: 0 free, 1 obstacle
    grid = [
        [0,0,0,0,0,0,0],
        [0,1,1,0,1,1,0],
        [0,0,0,0,0,0,0],
        [0,1,0,1,0,1,0],
        [0,0,0,0,0,0,0],
    ]
    agents = [
        {'id':1, 'pos':(0,0)},
        {'id':2, 'pos':(0,6)}
    ]
    tasks = [(2,1),(2,5),(4,2),(4,4),(0,3)]
    drop = (0,0)
    plans, metrics = run_simulation(grid, agents, tasks, drop, pause=0.08)
