import time
import numpy as np
from collections import deque
from scipy.optimize import linear_sum_assignment  # Hungarian Algorithm

from grid_module import display_grid  # Custom visualization

def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def bfs_dynamic(start, goal, grid, agents):
    """
    BFS that treats other agents as obstacles.
    `agents` is a set of all current agent positions (except this agent's own position).
    Returns a list of steps from start->goal (excluding start, including goal).
    If no path, returns [].
    """
    rows, cols = grid.shape
    queue = deque([(start, [])])
    visited = set([start])
    
    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == goal:
            return path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # Treat agent cells as obstacles
                if (nr, nc) not in agents and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), path + [(nr, nc)]))
    return []

def hungarian_assignment(agent_positions, target_positions):
    """
    Assign each agent to a unique target using Hungarian Algorithm.
    Returns list of (agent, target) pairs.
    """
    agent_positions = sorted(agent_positions)
    target_positions = sorted(target_positions)
    n_agents = len(agent_positions)
    n_targets = len(target_positions)
    size = max(n_agents, n_targets)

    cost_matrix = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            if i < n_agents and j < n_targets:
                cost_matrix[i, j] = manhattan_dist(agent_positions[i], target_positions[j])
            else:
                cost_matrix[i, j] = 999999

    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    assignments = []
    for i in range(size):
        if row_ind[i] < n_agents and col_ind[i] < n_targets:
            agent = agent_positions[row_ind[i]]
            target = target_positions[col_ind[i]]
            assignments.append((agent, target))
    return assignments

def move_agents_no_collision(grid, agent_positions, target_positions, grid_placeholder, speed=0.3):
    """
    1) Assign each agent to a unique target (Hungarian).
    2) Repeatedly:
       - For each agent, BFS around other agents to find one-step path
       - Move if possible, else wait
       - Resolve collisions (no same cell, no swaps)
    3) Stop when all agents at targets
    """
    # -------- Step A: Optimal assignment
    assignments = hungarian_assignment(agent_positions, target_positions)

    # Store agent states
    agents = []
    for (agent, target) in assignments:
        agents.append({'pos': agent, 'target': target})

    # Initialize grid to zeros
    new_grid = np.zeros_like(grid)
    for a in agent_positions:
        new_grid[a[0], a[1]] = 1
    grid = new_grid

    while True:
        new_grid = np.zeros_like(grid)
        move_dict = {}
        conflict_positions = set()
        all_reached = True

        # Sort by distance to target (not strictly necessary,
        # but can help reduce deadlocks).
        agents = sorted(agents, key=lambda ag: manhattan_dist(ag['pos'], ag['target']))

        # Positions of all agents, used as obstacles in BFS
        agent_set = set(ag['pos'] for ag in agents)

        # -------- Step B: For each agent, plan 1-step BFS
        for ag in agents:
            current = ag['pos']
            target = ag['target']
            if current == target:
                move_dict[current] = current  # Already there
                continue
            all_reached = False
            # BFS around other agents
            agent_set_except_self = agent_set - {current}
            path = bfs_dynamic(current, target, grid, agent_set_except_self)
            if path:
                next_step = path[0]
                # Attempt to move there if free
                if next_step not in conflict_positions:
                    move_dict[current] = next_step
                    conflict_positions.add(next_step)
                else:
                    # conflict -> stay
                    move_dict[current] = current
            else:
                # No path -> stay
                move_dict[current] = current

        # -------- Step C: Resolve direct swaps
        final_moves = {}
        for old_p, new_p in move_dict.items():
            # check if new_p wants old_p
            if new_p in move_dict and move_dict[new_p] == old_p:
                final_moves[old_p] = old_p
            else:
                final_moves[old_p] = new_p

        # -------- Step D: Update agent positions
        updated_agents = []
        for ag in agents:
            old_pos = ag['pos']
            new_pos = final_moves[old_pos]
            updated_agents.append({'pos': new_pos, 'target': ag['target']})
            new_grid[new_pos[0], new_pos[1]] = 1

        agents = updated_agents
        grid = new_grid

        # -------- Step E: Visualization
        display_grid(grid, grid_placeholder)

        if all_reached:
            break

        time.sleep(0.4)

    return grid, [a['pos'] for a in agents]
