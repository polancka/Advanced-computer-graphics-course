import numpy as np
from scipy.optimize import least_squares
import open3d as o3d

def surface_function(params, x, z):
    A, B, C, D, E, F = params
    return A*x**2 + B*z**2 + C*x*z + D*x + E*z + F

def residual(params, x, y, z):
    return y - surface_function(params, x, z)

def fit_surface(x, y, z, initial_guess):
    result = least_squares(residual, initial_guess, method='lm', args=(x, y, z))
    return result.x

def visualize_surface(parameters, x_range, z_range, num_points, point_cloud):
   # Generate a grid of points in the XY plane
    x_values = np.linspace(x_range[0], x_range[1], num_points)
    z_values = np.linspace(z_range[0], z_range[1], num_points)
    x_grid, z_grid = np.meshgrid(x_values, z_values)
    
    # Evaluate the surface function at the grid points
    y_grid = surface_function(parameters, x_grid, z_grid)
    
    # Create an Open3D point cloud from the grid points
    pcd_surface = o3d.geometry.PointCloud()
    pcd_surface.points = o3d.utility.Vector3dVector(np.column_stack((x_grid.flatten(), y_grid.flatten(), z_grid.flatten())))
    
    # Create Open3D point cloud from the input point cloud data
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    axis_lines = [
        np.array([[-50, 0, 0], [50, 0, 0]]), 
        np.array([[0,-50, 0], [0, 50, 0]]), 
        np.array([[0,0,-50], [0,0,50]]) 
    ]

    axis_line_geometries = [o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(axis_line), lines=o3d.utility.Vector2iVector([[0, 1]])) for axis_line in axis_lines]
    # Visualize the point cloud and the surface
    o3d.visualization.draw_geometries([pcd_surface, pcd] + axis_line_geometries)
    return pcd_surface.points

def visualize_surface_2D(points, plane_points):

   # Assuming 'aligned_points' is your numpy array of shape (n, 3)
    pcd_aligned = o3d.geometry.PointCloud()
    pcd_aligned.points = o3d.utility.Vector3dVector(points)
    pcd_plane = o3d.geometry.PointCloud()
    pcd_plane.points = o3d.utility.Vector3dVector(plane_points)

    # Project the aligned point cloud onto the XY plane
    projected_points = np.array(pcd_aligned.points)
    projected_points[:, 2] = 0  # Set z-coordinates to zero

    projected_points_plane = np.array(pcd_plane.points)
    #projected_points_plane[:,2] = 0

    # Create a new point cloud with the projected points
    pcd_projected = o3d.geometry.PointCloud()
    pcd_projected.points = o3d.utility.Vector3dVector(projected_points)

    pcd_plane_projected = o3d.geometry.PointCloud()
    pcd_plane_projected.points = o3d.utility.Vector3dVector(projected_points_plane)
    pcd_plane_projected.paint_uniform_color([1, 0, 0])


    axis_lines = [
        np.array([[-50, 0, 0], [50, 0, 0]]),  # x-axis (red)
        np.array([[0,-50, 0], [0, 50, 0]]),  # y-axis (green)
    ]

    axis_line_geometries = [o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(axis_line), lines=o3d.utility.Vector2iVector([[0, 1]])) for axis_line in axis_lines]
    # Visualize the projected point cloud
    o3d.visualization.draw_geometries([pcd_projected, pcd_plane_projected] + axis_line_geometries)
    return projected_points


def extract_surface_points(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals()
    
    # Surface reconstruction
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
    
    # Remove vertices with low density
    vertices_to_remove = densities < np.quantile(densities, 0.01)
    mesh.remove_vertices_by_mask(vertices_to_remove)
    
    # Get the surface points from the mesh
    surface_points = np.asarray(mesh.vertices)
    
    return surface_points

def main(points): 
    print("modeling surface...")
    surface_points = extract_surface_points(points)
    initial_guess = np.zeros(6) 
    x = surface_points[:, 0]  # Extract x coordinates from the first column
    y = surface_points[:, 1]  # Extract y coordinates from the second column
    z = surface_points[:, 2]  # Extract z coordinates from the third column
    parameters = fit_surface(x, y, z, initial_guess)
    x_range = (-40, 40)  # Range of x values
    y_range = (-40, 40)  # Range of y values
    num_points = 100  # Number of points in the grid
    plane_points = visualize_surface(parameters, x_range, y_range, num_points, points)

    #visualize_surface_2D(points, plane_points)
    return parameters

if __name__ == "__main__":
    main()