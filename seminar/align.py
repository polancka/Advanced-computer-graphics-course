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

# def make_obb(points):
#     # Assuming 'points' is your numpy array of shape (n, 3)
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(points)

#     # Compute the principal axes of the point cloud
#     mean, covariance_matrix = pcd.compute_mean_and_covariance()

#     # Compute eigen vectors from covariance matrix
#     eigen_values, eigen_vectors = np.linalg.eigh(np.array(covariance_matrix))

#     # Ensure the eigen vectors are orthogonal
#     # If not orthogonal, you can use np.linalg.qr or Gram-Schmidt to orthogonalize them
#     eigen_vectors /= np.linalg.norm(eigen_vectors, axis=0)

#     # Rotate the point cloud so that the principal axes align with the global axes
#     rotation_matrix = eigen_vectors.T  # Transpose the eigen vectors to get the rotation matrix

#     # Apply the rotation to the point cloud
#     pcd.rotate(rotation_matrix, center=pcd.get_center())

#     # Compute the oriented bounding box after alignment
#     obb = pcd.get_oriented_bounding_box()

#     # Extract transformation matrix
#     T = obb.R  # Rotation matrix
#     translation = obb.center  # Translation vector

#     # Apply transformation to point cloud
#     aligned_points = (points - translation) @ T.T

#     # Visualize the aligned point cloud
#     pcd_aligned = o3d.geometry.PointCloud()
#     pcd_aligned.points = o3d.utility.Vector3dVector(aligned_points)
#     o3d.visualization.draw_geometries([pcd_aligned])
#     return aligned_points

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

    # Visualize the aligned point cloud
    pcd_aligned = o3d.geometry.PointCloud()
    pcd_aligned.points = o3d.utility.Vector3dVector(aligned_points)
    o3d.visualization.draw_geometries([pcd_aligned])
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

    # Visualize the projected point cloud
    o3d.visualization.draw_geometries([pcd_projected])
    return projected_points

def main(points): 
    print("aligning...")
    center_points = center_cloud(points) #not necessary, a precaution
    #aligned_points = make_obb(center_points)
    aligned_points = make_envelope_obb(center_points)
    xy_points = xy_project(aligned_points)
    return aligned_points, xy_points
  
    
if __name__ == "__main__":
    main()