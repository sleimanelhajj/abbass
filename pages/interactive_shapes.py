import streamlit as st
from grid_module import initialize_grid, display_grid
from pathfinding import move_agents
from shapes_library import SHAPES

rows, cols = st.session_state.get("grid_size", (10, 10))
obstacles = st.session_state.get("obstacles", [])

st.title("🟦 Interactive Mode - Select Shape from UI")
grid_placeholder = st.empty()
grid, agent_positions, _ = initialize_grid(rows, cols, obstacles)
display_grid(grid, grid_placeholder)

st.subheader("Select a shape by clicking on the buttons below:")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🟥 Square"):
        grid, agent_positions = move_agents(grid, agent_positions, SHAPES["Square"], grid_placeholder)
with col2:
    if st.button("🔵 Circle"):
        grid, agent_positions = move_agents(grid, agent_positions, SHAPES["Circle"], grid_placeholder)
with col3:
    if st.button("🔺 Triangle"):
        grid, agent_positions = move_agents(grid, agent_positions, SHAPES["Triangle"], grid_placeholder)
with col4:
    if st.button("❤️ Heart"):
        grid, agent_positions = move_agents(grid, agent_positions, SHAPES["Heart"], grid_placeholder)
with col5:
    if st.button("⭐ Star"):
        grid, agent_positions = move_agents(grid, agent_positions, SHAPES["Star"], grid_placeholder)

if st.button("🔙 Back to Home"):
    st.page_link("app.py", label="Return to Home", icon="🏠")
