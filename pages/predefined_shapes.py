import streamlit as st
from grid_module import initialize_grid, display_grid
from pathfinding import move_agents_no_collision
from shapes_library import SHAPES, shift_shape_coords


rows, cols = st.session_state.get("grid_size", (10, 10))
obstacles = st.session_state.get("obstacles", [])

st.title("🎭 Predefined Shapes Mode - Pick from Dropdown")
grid_placeholder = st.empty()
grid, agent_positions, _ = initialize_grid(rows, cols, obstacles)
display_grid(grid, grid_placeholder)

shape_choice = st.selectbox("Choose a shape:", list(SHAPES.keys()), index=0)

def validate_targets(target_positions, rows, cols):
    """Ensure target positions are within bounds and not obstacles."""
    return [(r, c) for (r, c) in target_positions if 0 <= r < rows and 0 <= c < cols and (r, c) not in obstacles]

if st.button("Start Movement"):
    target_positions = shift_shape_coords(SHAPES[shape_choice], (rows, cols))
    target_positions = validate_targets(target_positions, rows, cols)
    
    if len(agent_positions) > len(target_positions):
        st.warning(f"⚠ Not enough valid target positions! {len(agent_positions)} agents but only {len(target_positions)} targets.")
    else:
        grid, agent_positions = move_agents_no_collision(grid, agent_positions, target_positions, grid_placeholder)

if st.button("🔙 Back to Home"):
    st.page_link("app.py", label="Return to Home", icon="🏠")
