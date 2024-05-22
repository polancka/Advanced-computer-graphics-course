import import_to_point_cloud
import align
import curve_fix
import model_surface
import srednji_prerez
import numpy as np
import open3d as o3d

#main file for crucial steps
#importing the .nii file and transforming it to a point cloud
points = import_to_point_cloud.main('sample/sample/annotations//04_15.nii.gz')

#aligning the point cloud with PCA and OBB
aligned_points, xy_points = align.main(points)

#model surface  to a projection of the uterus to XY plane (curvature is showing)
parameters = model_surface.main(aligned_points)

#fix curvature and return a new point cloud
non_curved_points = curve_fix.main(parameters, aligned_points)
np_non_curved = np.array(non_curved_points)


np.savetxt('point_cloud.csv', np_non_curved, delimiter=',', fmt='%.8f')

loaded_point_cloud = np.loadtxt('point_cloud.csv', delimiter=',')

print("LOADED", loaded_point_cloud)

#calculate the srednji prerez of aligned uterus
srednji_prerez.main(non_curved_points)

