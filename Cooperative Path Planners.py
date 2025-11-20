import heapq
import time
import os
from collections import defaultdict

def clear_screen():
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except:
        pass
    print("\n" * 3)

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_grid(start, goal, grid):
    R, C = len(grid), len(grid[0])
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, goal), 0, start, None))
    came_from = {}
    gscore = {start: 0}

    while open_heap:
        f, g, pos, parent = heapq.heappop(open_heap)
        if pos in came_from:
            continue
        came_from[pos] = parent

        if pos == goal:
            path = []
            cur = pos
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            return list(reversed(path))

        r, c = pos
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                ng = g + 1
                neigh = (nr, nc)
                if ng < gscore.get(neigh, 1e9):
                    gscore[neigh] = ng
                    heapq.heappush(open_heap, (ng + heuristic(neigh, goal), ng, neigh, pos))
    return None

def astar_time_aware(start, goal, grid, reservations, max_time=400):
    R, C = len(grid), len(grid[0])
    start_state = (start[0], start[1], 0)
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, goal), 0, start_state, None))
    came_from = {}
    gscore = {start_state: 0}

    while open_heap:
        f, g, state, parent = heapq.heappop(open_heap)
        if state in came_from:
            continue
        came_from[state] = parent
        r, c, t = state

        if (r, c) == goal:
            path = []
            cur = state
            while cur is not None:
                path.append((cur[0], cur[1]))
                cur = came_from[cur]
            return list(reversed(path))

        if t + 1 > max_time:
            continue

        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1),(0,0)):
            nr, nc = r + dr, c + dc
            nt = t + 1
            if not (0 <= nr < R and 0 <= nc < C):
                continue
            if grid[nr][nc] == 1:
                continue

            if nt in reservations and (nr, nc) in reservations[nt]:
                continue
            if nt in reservations and ('edge', (nr, nc, r, c)) in reservations[nt]:
                continue

            next_state = (nr, nc, nt)
            ng = g + 1
            if ng < gscore.get(next_state, 1e9):
                gscore[next_state] = ng
                heapq.heappush(open_heap, (ng + heuristic((nr, nc), goal), ng, next_state, state))
    return None

def reserve_from_path(path, reservations, hold_time=50):
    for t, pos in enumerate(path):
        reservations[t].add(pos)
        if t > 0:
            prev = path[t-1]
            reservations[t].add(('edge', (prev[0], prev[1], pos[0], pos[1])))
    final = path[-1]
    final_t = len(path)
    for future in range(final_t, final_t + hold_time):
        reservations[future].add(final)

def pad_paths(p1, p2):
    L = max(len(p1), len(p2))
    p1p = p1 + [p1[-1]] * (L - len(p1))
    p2p = p2 + [p2[-1]] * (L - len(p2))
    return p1p, p2p

def resolve_conflicts(p1, p2, max_iter=500):
    changed = True
    iterations = 0
    while changed and iterations < max_iter:
        changed = False
        iterations += 1
        L = max(len(p1), len(p2))
        if len(p1) < L:
            p1 += [p1[-1]]*(L - len(p1))
        if len(p2) < L:
            p2 += [p2[-1]]*(L - len(p2))

        for t in range(1, L):
            p1_prev, p1_cur = p1[t-1], p1[t]
            p2_prev, p2_cur = p2[t-1], p2[t]
            if p1_cur == p2_cur:
                p2.insert(t, p2[t-1])
                changed = True
                break
            if p1_prev == p2_cur and p2_prev == p1_cur:
                p2.insert(t, p2[t-1])
                changed = True
                break
    return p1, p2

def render_frame(grid, a1_pos, a2_pos, a1_goal, a2_goal):
    R, C = len(grid), len(grid[0])
    disp = [['.' if grid[r][c] == 0 else '#' for c in range(C)] for r in range(R)]
    disp[a1_goal[0]][a1_goal[1]] = '1'
    disp[a2_goal[0]][a2_goal[1]] = '2'
    if a1_pos == a2_pos:
        disp[a1_pos[0]][a1_pos[1]] = 'X'
    else:
        disp[a1_pos[0]][a1_pos[1]] = 'A'
        disp[a2_pos[0]][a2_pos[1]] = 'B'
    return "\n".join("".join(row) for row in disp)

def animate(grid, path1, path2, a1_goal, a2_goal, pause=0.25):
    path1, path2 = pad_paths(path1, path2)
    for t in range(len(path1)):
        clear_screen()
        print(f"Time step {t} / {len(path1)-1}\n")
        print(render_frame(grid, path1[t], path2[t], a1_goal, a2_goal))
        print("\nLegend: . free, # obstacle, A agent1, B agent2, 1 goal1, 2 goal2, X collision")
        time.sleep(pause)
    print("\nFinished.")
    print("Final positions: Agent1", path1[-1], "Agent2", path2[-1])
    print("\nAgent1 path:", path1)
    print("Agent2 path:", path2)

def main():
    grid = [
        [0,0,0,0,0,0],
        [0,1,1,0,1,0],
        [0,0,0,0,0,0],
        [0,1,0,1,1,0],
        [0,0,0,0,0,0],
    ]

    a1_start = (0,0); a1_goal = (4,5)
    a2_start = (0,5); a2_goal = (4,0)

    path1 = astar_grid(a1_start, a1_goal, grid)
    if not path1:
        print("Agent1: No path.")
        return

    reservations = defaultdict(set)
    reserve_from_path(path1, reservations, hold_time=50)

    path2 = astar_time_aware(a2_start, a2_goal, grid, reservations, max_time=400)
    if not path2:
        static = astar_grid(a2_start, a2_goal, grid)
        if not static:
            print("Agent2: No path.")
            return
        p2_exec = [static[0]]
        for step in static[1:]:
            t = len(p2_exec)
            if step in reservations.get(t, set()):
                p2_exec.append(p2_exec[-1])
            else:
                p2_exec.append(step)
        path2 = p2_exec

    p1, p2 = pad_paths(path1, path2)
    p1, p2 = resolve_conflicts(p1[:], p2[:])
    p1, p2 = pad_paths(p1, p2)

    animate(grid, p1, p2, a1_goal, a2_goal, pause=0.25)

if __name__ == "__main__":
    main()