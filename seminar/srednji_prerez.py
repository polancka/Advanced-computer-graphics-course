import open3d as o3d
import numpy as np

def calculate_mid_sagittal_plane(points):
    # Calculate the mean y-coordinate for the mid-sagittal plane
    
    mean_y = np.mean(points[:, 1])
    sd_y = np.std(points[:,1])
    return mean_y, sd_y

def create_sagittal_plane(mean_y, x_range, z_range):
    # Create a plane geometry at the mean_y position
    vertices = [
        [x_range[0], mean_y, z_range[0]],
        [x_range[1], mean_y, z_range[0]],
        [x_range[1], mean_y, z_range[1]],
        [x_range[0], mean_y, z_range[1]],
    ]
    triangles = [[0, 1, 2], [0, 2, 3]]
    plane = o3d.geometry.TriangleMesh(
        vertices=o3d.utility.Vector3dVector(vertices),
        triangles=o3d.utility.Vector3iVector(triangles)
    )
    plane.paint_uniform_color([0.1, 0.9, 0.1])  # Color the plane green
    return plane

def few_points(points, mean_y, sd_y):
    new_points = []
    for point in points:
        if point[1] <= (mean_y + sd_y) and point[1] >= (mean_y - sd_y):
            new_points.append(point)

    # Visualize the aligned point cloud
    # Create axis lines
    axis_lines = [
        np.array([[-50, 0, 0], [50, 0, 0]]),  # x-axis (red)
        np.array([[0,-50, 0], [0, 50, 0]]),  # y-axis (green)
        np.array([[0, 0, -50], [0, 0, 50]])   # z-axis (blue)
    ]
    # Convert axis lines to Open3D geometry
    axis_line_geometries = [o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(axis_line), lines=o3d.utility.Vector2iVector([[0, 1]])) for axis_line in axis_lines]

    pcd_aligned = o3d.geometry.PointCloud()
    pcd_aligned.points = o3d.utility.Vector3dVector(new_points)
    o3d.visualization.draw_geometries([pcd_aligned] + axis_line_geometries)
    
def main(): #change back to (points) when excetuing the semianr.py file
    points = np.loadtxt('point_cloud.csv', delimiter=',')
    print("calculating the mid-sagittal plane ...")
    points_array = np.array(points)
    mean_y, sd_y = calculate_mid_sagittal_plane(points_array)
    x_range = [np.min(points_array[:, 0]), np.max(points_array[:, 0])]
    z_range = [np.min(points_array[:, 2]), np.max(points_array[:, 2])]
    few_points(points, mean_y, sd_y)
    sagittal_plane = create_sagittal_plane(mean_y, x_range, z_range)

if __name__ == "__main__":
    main()