import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as path_effects

def draw_chessboard(n, positions, ax):
    """
    Draw a chessboard with queens placed at given positions.

    :param n: Size of the chessboard (n x n)
    :param queens_positions: List of (row, col) positions for each queen
    """
    queens_positions = [(i, p) for i, p in enumerate(positions)]
    
    # Define colors
    light_color = '#f5cba7'  # Light square color
    dark_color = '#d35400'   # Dark square color

    # Create a chessboard pattern
    chessboard = np.zeros((n, n))
    chessboard[1::2, ::2] = 1
    chessboard[::2, 1::2] = 1

    # Use the defined colors
    ax.imshow(chessboard, cmap='copper', extent=(0, n, 0, n), vmin=0, vmax=1)
    ax.imshow(chessboard, cmap=plt.cm.colors.ListedColormap([light_color, dark_color]), extent=(0, n, 0, n), vmin=0, vmax=1)

    # Add the queens to the board
    for pos in queens_positions:
        text = ax.text(pos[1] + 0.5, n - pos[0] - 0.5, '♛', ha='center', va='center', fontsize=30, color='white')
        text.set_path_effects([path_effects.Stroke(linewidth=2, foreground='black'), path_effects.Normal()])
    
    # Add labels to the rows and columns
    ax.set_xticks(np.arange(n) + 0.5)
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_xticklabels(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    ax.set_yticklabels(range(1, n + 1)[::-1])

    ax.xaxis.tick_top()
    ax.tick_params(length=0)
    ax.grid(False)
    
    plt.show()


