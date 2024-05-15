import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def xy_projection(points):
    # Assuming 'points' is your numpy array of shape (n, 3)
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    plt.figure(figsize=(15, 5))

    # XY Projection
    plt.subplot(1, 3, 1)
    plt.scatter(x, y, alpha=0.6, edgecolors='w', s=50)
    plt.title("XY Projection")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.grid(True)

    # XZ Projection
    plt.subplot(1, 3, 2)
    plt.scatter(x, z, alpha=0.6, edgecolors='w', s=50)
    plt.title("XZ Projection")
    plt.xlabel("X coordinate")
    plt.ylabel("Z coordinate")
    plt.grid(True)

    # YZ Projection
    plt.subplot(1, 3, 3)
    plt.scatter(y, z, alpha=0.6, edgecolors='w', s=50)
    plt.title("YZ Projection")
    plt.xlabel("Y coordinate")
    plt.ylabel("Z coordinate")
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main(points): 
    print("modeling surface...")
    xy_projection(points)


if __name__ == "__main__":
    main()