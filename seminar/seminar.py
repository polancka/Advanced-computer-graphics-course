import import_to_point_cloud
import align
import curve_fix
import model_surface

#main file for crucial steps
#importing the .nii file and transforming it to a point cloud
points = import_to_point_cloud.main()

#aligning the point cloud with PCA and OBB
align.main(points)

#model surface (ellipse) to a projection of the uterus to XY plane (curvature is showing)
model_surface.main(points)

#fix curvature and return a new point cloud
curve_fix.main(points)

#calculate the srednji prerez of aligned uterus
#srednji_prerez.main(points)

