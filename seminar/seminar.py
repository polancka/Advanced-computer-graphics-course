import import_to_point_cloud
import align
import curve_fix
import model_surface

#main file for crucial steps
#importing the .nii file and transforming it to a point cloud
points = import_to_point_cloud.main('sample/sample/annotations//04_15.nii.gz')

#aligning the point cloud with PCA and OBB
aligned_points, xy_points = align.main(points)

#model surface  to a projection of the uterus to XY plane (curvature is showing)
model_surface.main(aligned_points)

#fix curvature and return a new point cloud
#curve_fix.main(points)

#calculate the srednji prerez of aligned uterus
#srednji_prerez.main(points)

