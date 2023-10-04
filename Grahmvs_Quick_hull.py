import random
import matplotlib.pyplot as plt
import time
from math import atan2

# --- Data Generation ---

def generate_random_points(num_points=100):
    """Generate random 2D points."""
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_points)]

def import_points_from_file(filename):
    """Import points from a file."""
    with open(filename, 'r') as file:
        num_points = int(file.readline().strip())
        points = [tuple(map(float, line.strip().split(','))) for line in file]
    return points

# --- Graham's Scan Algorithm ---

def orientation(p, q, r):
    """Return orientation of triplet (p, q, r)."""
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def graham_scan(points):
    """Implement Graham's Scan algorithm."""
    n = len(points)
    if n < 3:
        return points

    # Find the bottom-most point
    l = min(range(n), key=lambda i: (points[i][1], points[i][0]))
    p0 = points[l]

    # Sort points based on polar angle with respect to p0
    sorted_points = sorted(points, key=lambda p: (atan2(p[1]-p0[1], p[0]-p0[0]), p))

    # Build the convex hull
    hull = []
    for point in sorted_points:
        while len(hull) > 1 and orientation(hull[-2], hull[-1], point) != 1:
            hull.pop()
        hull.append(point)
    return hull

# --- Quickhull Algorithm ---

def side(p1, p2, p):
    """Return side of point p with respect to line joining p1 and p2."""
    return (p[1] - p1[1]) * (p2[0] - p1[0]) - (p2[1] - p1[1]) * (p[0] - p1[0])

def quickhull_util(points, p1, p2, side_flag):
    """Recursive utility function for Quickhull algorithm."""
    max_dist = 0
    max_point = None
    n = len(points)
    for i in range(n):
        temp = abs(side(p1, p2, points[i]))
        if side(p1, p2, points[i]) == side_flag and temp > max_dist:
            max_dist = temp
            max_point = points[i]

    if max_point is None:
        return []

    return (quickhull_util(points, p1, max_point, -side(p1, max_point, p2)) +
            [max_point] +
            quickhull_util(points, max_point, p2, -side(max_point, p2, p1)))

def quickhull(points):
    """Implement Quickhull algorithm."""
    if len(points) < 3:
        return points

    # Find the baseline
    min_point = min(points, key=lambda p: p[0])
    max_point = max(points, key=lambda p: p[0])

    # Recursive hull construction
    hull = []
    hull.extend(quickhull_util(points, min_point, max_point, 1))
    hull.extend(quickhull_util(points, min_point, max_point, -1))
    hull.append(min_point)
    hull.append(max_point)
    return hull

# --- Visualization ---

def visualize_step_by_step(points, hull_graham, hull_quickhull):
    """Visualize the points and the convex hulls step by step."""
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Graham\'s Scan vs Quickhull')
    
    # Plot points
    ax1.scatter([p[0] for p in points], [p[1] for p in points], c='blue')
    ax2.scatter([p[0] for p in points], [p[1] for p in points], c='blue')
    
    # Plot Graham's Scan step by step
    for i in range(1, len(hull_graham)):
        ax1.plot([hull_graham[i-1][0], hull_graham[i][0]], [hull_graham[i-1][1], hull_graham[i][1]], c='red')
        plt.draw()
        input("Press Enter to continue to the next step for Graham's Scan...")
    
    # Plot Quickhull step by step
    for i in range(1, len(hull_quickhull)):
        ax2.plot([hull_quickhull[i-1][0], hull_quickhull[i][0]], [hull_quickhull[i-1][1], hull_quickhull[i][1]], c='green')
        plt.draw()
        input("Press Enter to continue to the next step for Quickhull...")
    
    plt.show()

# --- Comparison Function ---

def compare_algorithms(points):
    """Compare the results and execution times of the two algorithms."""
    
    # Graham's Scan
    start_time = time.time()
    hull_graham = graham_scan(points)
    end_time = time.time()
    graham_time = end_time - start_time
    print(f"Graham's Scan took {graham_time:.4f} seconds")

    # Quickhull
    start_time = time.time()
    hull_quickhull = quickhull(points)
    end_time = time.time()
    quickhull_time = end_time - start_time
    print(f"Quickhull took {quickhull_time:.4f} seconds")

    # Visualize step by step
    visualize_step_by_step(points, hull_graham, hull_quickhull)

    return graham_time, quickhull_time

if __name__ == "__main__":
    points = generate_random_points(15)
    hull_graham = graham_scan(points)
    hull_quickhull = quickhull(points)
    visualize_step_by_step(points, hull_graham, hull_quickhull)