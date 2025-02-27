import streamlit as st
from grid_module import initialize_grid, display_grid
from pathfinding import move_agents

# 🔹 Ensure grid size and obstacles are initialized
if "grid_size" not in st.session_state:
    st.session_state["grid_size"] = (10, 10)
if "obstacles" not in st.session_state:
    st.session_state["obstacles"] = []

rows, cols = st.session_state["grid_size"]
obstacles = st.session_state["obstacles"]  # Load obstacles

st.title("🖊 Custom Shape Mode - Draw Your Own Shape")
grid_placeholder = st.empty()

# Initialize grid with obstacles
grid, agent_positions, _ = initialize_grid(rows, cols, obstacles)
display_grid(grid, grid_placeholder)

st.subheader("Draw your shape on the grid:")
cell_states = []
for i in range(rows):
    row_cols = st.columns(cols)
    row_state = [
        row_cols[j].checkbox(
            "", key=f"cell_{i}_{j}", value=False, disabled=(i, j) in obstacles
        )
        for j in range(cols)
    ]
    cell_states.append(row_state)

if st.button("Start Movement"):
    # Exclude obstacle cells
    custom_targets = [
        (i, j) for i in range(rows) for j in range(cols)
        if cell_states[i][j] and (i, j) not in obstacles
    ]

    if not custom_targets:
        st.warning("⚠ Please select at least one valid target (not an obstacle).")
    else:
        # Optional: If you have 16 agents, ensure exactly 16 targets
        if len(agent_positions) != len(custom_targets):
            st.warning(f"Please select exactly {len(agent_positions)} target cells (you selected {len(custom_targets)}).")

        st.write(f"Selected Targets: {custom_targets}")
        grid, agent_positions = move_agents(grid, agent_positions, custom_targets, grid_placeholder)

if st.button("🔙 Back to Mode Selection"):
    st.switch_page("pages/mode_selection.py")
