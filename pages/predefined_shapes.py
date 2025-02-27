import streamlit as st
from grid_module import initialize_grid, display_grid
from pathfinding import move_agents
from shapes_library import SHAPES, shift_shape_coords

rows, cols = st.session_state.get("grid_size", (10, 10))
obstacles = st.session_state.get("obstacles", [])

st.title("🎭 Predefined Shapes Mode - Pick from Dropdown")
grid_placeholder = st.empty()
grid, agent_positions, _ = initialize_grid(rows, cols, obstacles)
display_grid(grid, grid_placeholder)

shape_choice = st.selectbox("Choose a shape:", list(SHAPES.keys()), index=0)

if st.button("Start Movement"):
    target_positions = shift_shape_coords(SHAPES[shape_choice], (rows, cols))

    # ✅ Ensure target positions are within the grid bounds
    target_positions = [(r, c) for (r, c) in target_positions if 0 <= r < rows and 0 <= c < cols]

    grid, agent_positions = move_agents(grid, agent_positions, target_positions, grid_placeholder)

if st.button("🔙 Back to Home"):
    st.page_link("app.py", label="Return to Home", icon="🏠")
