#based on Master thesis, do a OBB and PCA to align the uteri in a similar direction
#that way XY plane will show the curvature of the uterus

import numpy as np
import model_surface
import open3d as o3d

def center_cloud(points): 
    # Assuming 'points' is your numpy array of shape (n, 3)
    centroid = np.mean(points, axis=0)  # Compute centroid

    # Translate points to center at the origin
    centered_points = points - centroid

    return centered_points


def make_envelope_obb(points):
    # Assuming 'points' is your numpy array of shape (n, 3)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.estimate_normals()
    # Surface reconstruction
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)

    # Remove vertices with low density
    vertices_to_remove = densities < np.quantile(densities, 0.01)
    mesh.remove_vertices_by_mask(vertices_to_remove)

    # Compute the oriented bounding box of the surface mesh
    obb = mesh.get_oriented_bounding_box()

    # Extract transformation matrix
    T = obb.R  # Rotation matrix
    translation = obb.center  # Translation vector

    # Apply transformation to the original point cloud
    aligned_points = (points - translation) @ T.T

    # Compute the mean and covariance matrix using numpy
    mean = np.mean(aligned_points, axis=0)
    covariance_matrix = np.cov(aligned_points, rowvar=False)

    # computations for rotation if necessary
    Mx, _, _ = mean
    Ox, _, _ = obb.center
    diff_x = Mx - Ox
    print(diff_x)

    # If the difference is positive, rotate the uterus about the x-axis by 180 degrees
    if diff_x > 0:
        rotation_matrix_x = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])  # 180 degree rotation about x-axis
        aligned_points = np.dot(aligned_points, rotation_matrix_x.T)

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
    pcd_aligned.points = o3d.utility.Vector3dVector(aligned_points)
    o3d.visualization.draw_geometries([pcd_aligned] + axis_line_geometries)

    return aligned_points

def xy_project(aligned_points):
    # Assuming 'aligned_points' is your numpy array of shape (n, 3)
    pcd_aligned = o3d.geometry.PointCloud()
    pcd_aligned.points = o3d.utility.Vector3dVector(aligned_points)

    # Project the aligned point cloud onto the XY plane
    projected_points = np.array(pcd_aligned.points)
    projected_points[:, 2] = 0  # Set z-coordinates to zero

    # Create a new point cloud with the projected points
    pcd_projected = o3d.geometry.PointCloud()
    pcd_projected.points = o3d.utility.Vector3dVector(projected_points)
    axis_lines = [
        np.array([[-50, 0, 0], [50, 0, 0]]),  # x-axis (red)
        np.array([[0,-50, 0], [0, 50, 0]]),  # y-axis (green)
    ]
    # Convert axis lines to Open3D geometry
    axis_line_geometries = [o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(axis_line), lines=o3d.utility.Vector2iVector([[0, 1]])) for axis_line in axis_lines]
    # Visualize the projected point cloud
    o3d.visualization.draw_geometries([pcd_projected] + axis_line_geometries)
    return projected_points


def main(points): 
    print("aligning...")
    center_points = center_cloud(points) #not necessary, a precaution
    aligned_points = make_envelope_obb(center_points)
    xy_points = xy_project(aligned_points)
    return aligned_points, xy_points
  
    
if __name__ == "__main__":
    main()