# 🟥 Square Shape (16 positions)
SQUARE = [
    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
    (1, 7), (2, 7), (3, 7), (4, 7),
    (4, 6), (4, 5), (4, 4), (4, 3),
    (3, 3), (2, 3), (1, 3)
]

# 🔵 Circle Shape (16 positions)
CIRCLE = [
    (1, 4), (1, 5),
    (2, 3), (2, 6),
    (3, 2), (3, 7),
    (4, 1), (4, 8),
    (5, 1), (5, 8),
    (6, 2), (6, 7),
    (7, 3), (7, 6),
    (8, 4), (8, 5)
]

# 🔺 Triangle Shape
TRIANGLE = [
    (2, 5),
    (3, 4), (3, 5), (3, 6),
    (4, 3), (4, 4), (4, 5), (4, 6), (4, 7),
    (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8)
]

# ❤️ Heart Shape
HEART = [
    (1, 4), (1, 5),
    (2, 3), (2, 6),
    (3, 2), (3, 7),
    (4, 2), (4, 7),
    (5, 3), (5, 6),
    (6, 4), (6, 5),
    (7, 4), (7, 5)
]

# ⭐ Star Shape
STAR = [
    (0, 4), (0, 5),
    (1, 4), (1, 5),
    (2, 2), (2, 3), (2, 6), (2, 7),
    (3, 1), (3, 8),
    (4, 0), (4, 9),
    (5, 1), (5, 8),
    (6, 2), (6, 3), (6, 6), (6, 7),
    (7, 4), (7, 5)
]

# 🎭 Store all shapes in a dictionary
SHAPES = {
    "Square": SQUARE,
    "Circle": CIRCLE,
    "Triangle": TRIANGLE,
    "Heart": HEART,
    "Star": STAR
}

def shift_shape_coords(shape_coords, grid_size):
    """Move shape to be centered in the grid and ensure it stays within bounds."""
    rows, cols = grid_size

    min_r = min(r for r, _ in shape_coords)
    min_c = min(c for _, c in shape_coords)
    
    row_offset = (rows - (max(r for r, _ in shape_coords) - min_r)) // 2
    col_offset = (cols - (max(c for _, c in shape_coords) - min_c)) // 2

    # Ensure the shape stays inside the grid
    shifted_coords = [
        (max(0, min(rows - 1, r + row_offset)), max(0, min(cols - 1, c + col_offset)))
        for r, c in shape_coords
    ]

    return shifted_coords

