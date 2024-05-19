import numpy as np
from scipy.optimize import minimize
import open3d as o3d
from scipy.optimize import fsolve

def find_closest_point(point, A,B,C,D,E,F):
    #calculates displacement of every point
    def objective(xy):
        x, y = xy
        z = surface_function(x, y, A, B, C, D, E, F)
        s = np.array([x, y, z])
        return distance(point, s)
    
    result = minimize(objective, point[:2])  # Use px and py as initial guess
    sx, sy = result.x
    sz = surface_function(sx, sy, A, B, C, D, E, F)
    return np.array([sx, sy, sz])

def distance(p, s):
    return np.linalg.norm(p - s)


def visualize_point_cloud(points, view='xy'):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    
    axis_lines = [
        np.array([[-50,0, 0], [50, 0, 0]]),
        np.array([[0, 0, -50], [0, 0, 50]]),  # z-axis (red)
        np.array([[0,-50, 0], [0, 50, 0]]),  # y-axis (green)
    ]
    # Convert axis lines to Open3D geometry
    axis_line_geometries = [o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(axis_line), lines=o3d.utility.Vector2iVector([[0, 1]])) for axis_line in axis_lines]

    o3d.visualization.draw_geometries([pcd] + axis_line_geometries)

    
def surface_function(x, y, A, B, C, D, E, F):
    return A * x**2 + B * y**2 + C * x * y + D * x + E * y + F

def distance_function(params, px, py, pz, A, B, C, D, E, F):
    sx, sy = params
    sz = surface_function(sx, sy, A, B, C, D, E, F)
    return (sx - px)**2 + (sy - py)**2 + (sz - pz)**2

def partial_derivatives(x, y, A, B, C, D, E):
    fx = 2 * A * x + C * y + D
    fy = 2 * B * y + C * x + E
    return fx, fy

def second_derivatives(x, y, A, B, C):
    fxx = 2 * A
    fyy = 2 * B
    fxy = C
    return fxx, fyy, fxy

def find_critical_points(px, py, pz, A, B, C, D, E, F):
    def equations(params):
        x, y = params
        fx, fy = partial_derivatives(x, y, A, B, C, D, E)
        return [fx, fy]
    
    initial_guess = [px, py]
    critical_points = fsolve(equations, initial_guess)
    return critical_points

def check_minimum(critical_point, A, B, C):
    x, y = critical_point
    fxx, fyy, fxy = second_derivatives(x, y, A, B, C)
    D = fxx * fyy - fxy**2
    if D > 0 and fxx > 0:
        return True
    return False

def find_closest_point(P, A, B, C, D, E, F):
    px, py, pz = P
    critical_point = find_critical_points(px, py, pz, A, B, C, D, E, F)
    if check_minimum(critical_point, A, B, C):
        sx, sy = critical_point
        sz = surface_function(sx, sy, A, B, C, D, E, F)
        return np.array([sx, sy, sz])
    else:
        result = minimize(distance_function, critical_point, args=(px, py, pz, A, B, C, D, E, F))
        sx, sy = result.x
        sz = surface_function(sx, sy, A, B, C, D, E, F)
        return np.array([sx, sy, sz])


def calculate_displacement(point, A,B,C,D,E,F):
    px, py, pz = point
    initial_guess = [px, py]  # Start optimization from the projection of P onto the xy-plane
    result = minimize(distance_function, initial_guess, args=(px, py, pz, A, B, C, D, E, F))
    sx, sy = result.x
    sz = surface_function(sx, sy, A, B, C, D, E, F)
    return np.array([sx, sy, sz])

def main(parameters, points): 
    print("fixing curve...")

    A = parameters[0]
    B = parameters[1]
    C = parameters[2]
    D = parameters[3]
    E = parameters[4]
    F = parameters[5]

    new_points = []

    for P in points:
        S = find_closest_point(P, A, B, C, D, E, F)
        sx, sy, sz = S
        px, py, pz = P
        d = np.sqrt((sx - px)**2 + (sy - py)**2 + (sz - pz)**2)
        if pz < sz:
            d = -d
        new_points.append([px, py, d])

    visualize_point_cloud(points)
    visualize_point_cloud(new_points)

    return new_points
if __name__ == "__main__":
    main()