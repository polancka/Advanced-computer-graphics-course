import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import least_squares

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the NIfTI file
def load_nifti(file_path):
    print("loading nifti...")
    img = nib.load(file_path)
    data = img.get_fdata()
    # print(data)
    return data

# Visualization of the black/white volume
def visualize_volume(data):
    print("visualizing...")
    plt.figure()
    plt.imshow(data[:, :, data.shape[2] // 2], cmap='gray')
    plt.title('Middle Slice of the Volume')
    plt.axis('off')
    plt.show()

# Convert volume to point cloud
def volume_to_point_cloud(volume, threshold=None):
    if threshold is not None:
        # Apply a threshold to focus on regions of interest
        mask = volume > threshold
    else:
        mask = volume > 0  # Default to non-zero values if no threshold is specified

    # Get the coordinates of the points
    points = np.argwhere(mask)
    # Get the values at these points
    values = volume[mask]
    
    return points, values

# Assuming `points` is the array of coordinates and `values` is the array of voxel values
def plot_point_cloud(points, values):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot: using voxel values for color mapping
    sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=values, cmap='viridis', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.title('3D Point Cloud Visualization')
    plt.show()


def main(): 
    file_path = 'sample/sample/annotations//04_13.nii.gz'  # Update this with the path to your .nii file
    volume_data = load_nifti(file_path)
    points, values = volume_to_point_cloud(volume_data, threshold=0.5)
    #plot_point_cloud(points, values)
    return points

if __name__ == "__main__":
    main()