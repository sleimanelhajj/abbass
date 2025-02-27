import time
import numpy as np
from collections import deque
from grid_module import display_grid

def bfs(start, goal, grid):
    """BFS pathfinding that avoids obstacles (`-1` cells)."""
    queue = deque([(start, [])])
    visited = set([start])

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] 
                and grid[nx, ny] != -1  # ✅ Avoid obstacles
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    return []  # No path found

def assign_targets_direct(agent_positions, target_positions, grid):
    """Assign each agent to a target based on their index in a sorted list."""
    assigned = []
    
    # Ensure lists are sorted to maintain correct shape
    agent_positions = sorted(agent_positions)
    target_positions = sorted(target_positions)

    for i in range(min(len(agent_positions), len(target_positions))):
        agent = agent_positions[i]
        target = target_positions[i]
        path = bfs(agent, target, grid)
        assigned.append((agent, target, path))

    return assigned

def move_agents(grid, agent_positions, target_positions, grid_placeholder, speed=0.3):
    """Moves agents while avoiding obstacles using BFS."""
    
    # ✅ Ensure targets are not obstacles
    valid_targets = [(r, c) for (r, c) in target_positions if grid[r, c] != -1]

    # ✅ Assign agents only to valid targets
    assigned = assign_targets_direct(agent_positions, valid_targets, grid)

    agents = [{'pos': agent, 'target': target, 'path': path} for agent, target, path in assigned]

    while True:
        # ✅ Clear old agent positions, but keep obstacles
        new_grid = np.where(grid == -1, -1, 0)  # Reset grid except obstacles
        new_agents = []
        all_reached = True
        new_positions = set()

        intended_moves = []
        for ag in agents:
            pos, tgt, path = ag['pos'], ag['target'], ag['path']

            if pos == tgt:
                intended_moves.append((pos, pos))  # ✅ Stay in place
                continue

            if not path:
                path = bfs(pos, tgt, grid)  # ✅ Recalculate path if lost
                ag['path'] = path

            if path:
                next_pos = path[0]
                intended_moves.append((pos, next_pos))
            else:
                intended_moves.append((pos, pos))  # Stay if stuck

        move_dict = {}
        conflicts = set()

        for i, (old_p, new_p) in enumerate(intended_moves):
            if new_p in move_dict.values() or new_p in new_positions:
                conflicts.add(new_p)
            move_dict[i] = (old_p, new_p)

        final_moves = []
        for i, (old_p, new_p) in move_dict.items():
            swap_conflict = any(
                move_dict[j] == (new_p, old_p) for j in move_dict if j != i
            )
            if new_p in conflicts or swap_conflict:
                final_moves.append(old_p)  # Stay in place
            else:
                final_moves.append(new_p)
                new_positions.add(new_p)

        # ✅ Update Grid & Agents
        for idx, new_pos in enumerate(final_moves):
            ag = agents[idx]
            old_pos = ag['pos']

            if new_pos != old_pos:
                if ag['path'] and ag['path'][0] == new_pos:
                    ag['path'] = ag['path'][1:]
                all_reached = False

            if new_grid[new_pos[0], new_pos[1]] != -1:  # ✅ Do not overwrite obstacles
                new_grid[new_pos[0], new_pos[1]] = 1  

            new_agents.append({
                'pos': new_pos,
                'target': ag['target'],
                'path': ag['path']
            })

        grid = new_grid
        agents = new_agents
        agent_positions = [a['pos'] for a in agents]

        display_grid(grid, grid_placeholder)  # ✅ Ensure visualization updates

        if all_reached:
            break

        time.sleep(speed)

    return grid, agent_positions
