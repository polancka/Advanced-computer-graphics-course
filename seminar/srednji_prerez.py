import open3d as o3d
import numpy as np

def calculate_mid_sagittal_plane(points):
    # Calculate the mean y-coordinate for the mid-sagittal plane
    
    mean_y = np.mean(points[:, 1])
    return mean_y

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


def filter_points_on_plane(points, mean_y, tol=1e-6):
    # Filter points with y-coordinate close to mean_y
    filtered_points = [p for p in points if abs(p[1] - mean_y) < tol]
    return np.array(filtered_points)

def visualize_points_on_plane(points_on_plane):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points_on_plane)

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)

    vis.run()
    vis.destroy_window()


def visualize_point_cloud_with_plane(points, plane):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    # Calculate the range of points
    x_range = [np.min(points[:, 0]) - 1, np.max(points[:, 0]) + 1]
    y_range = [np.min(points[:, 1]) -1 , np.max(points[:, 1])+ 1 ]
    z_range = [np.min(points[:, 2]) - 1, np.max(points[:, 2])+ 1 ]
   

    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.add_geometry(plane)


    vis.run()
    vis.destroy_window()

def main(points): 
    print("calculating the mid-sagittal plane ...")
    points_array = np.array(points)
    mean_y = calculate_mid_sagittal_plane(points_array)
    x_range = [np.min(points_array[:, 0]), np.max(points_array[:, 0])]
    z_range = [np.min(points_array[:, 2]), np.max(points_array[:, 2])]
    sagittal_plane = create_sagittal_plane(mean_y, x_range, z_range)

    visualize_point_cloud_with_plane(points_array, sagittal_plane)
    # Filter points lying on the mid-sagittal plane
    points_on_plane = filter_points_on_plane(points_array, mean_y)

    visualize_points_on_plane(points_on_plane)



if __name__ == "__main__":
    main()