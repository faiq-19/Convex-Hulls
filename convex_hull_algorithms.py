from math import atan2
def brute_force(points):
    n = len(points)
    if n < 3:
        return points

    hull = []
    for i in range(n):
        for j in range(n):
            if i != j:
                line = [points[i], points[j]]
                is_convex = True
                for k in range(n):
                    if k != i and k != j:
                        orientation = (line[1][1] - line[0][1]) * (points[k][0] - line[1][0]) - \
                                       (line[1][0] - line[0][0]) * (points[k][1] - line[1][1])
                        if orientation > 0:
                            is_convex = False
                            break
                if is_convex:
                    hull.append(line[0])
                    hull.append(line[1])

    return hull

def jarvis_march(points):
    n = len(points)
    if n < 3:
        return points

    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear
        return 1 if val > 0 else 2  # clock or counterclock-wise

    hull = []
    start_point = min(points)
    current_point = start_point
    next_point = None

    while next_point != start_point:
        hull.append(current_point)
        next_point = points[0]
        for candidate_point in points[1:]:
            if next_point == current_point or orientation(current_point, candidate_point, next_point) == 2:
                next_point = candidate_point

        current_point = next_point

    return hull


def graham_scan(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear
        return 1 if val > 0 else 2  # clock or counterclock-wise

    def graham_scan_cmp(p1, p2):
        o = orientation(p0, p1, p2)
        if o == 0:
            return -1 if (p0[0], p0[1]) < (p1[0], p1[1]) else 1
        return -1 if o == 2 else 1

    n = len(points)
    if n < 3:
        return points

    p0 = min(points)
    points.sort(key=lambda point: (atan2(point[1] - p0[1], point[0] - p0[0]), point))

    # Check if there are enough points for the initial stack
    if n < 3:
        return points
    else:
        stack = [points[0], points[1], points[2]]

    for i in range(3, n):
        while len(stack) >= 2 and orientation(stack[-2], stack[-1], points[i]) != 2:
            stack.pop()
        stack.append(points[i])

    return stack


def quick_elimination(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear
        return 1 if val > 0 else 2  # clock or counterclock-wise

    def compare(p1, p2):
        o = orientation(points[0], p1, p2)
        if o == 0:
            return -1 if (p1[0] + p1[1]) < (p2[0] + p2[1]) else 1
        return -1 if o == 2 else 1

    # Sort points based on polar angle with respect to the first point
    points.sort(key=lambda p: (p[1], p[0]))

    # Initialize the convex hull with the first two points
    convex_hull = [points[0], points[1]]

    # Eliminate points inside the convex hull
    for i in range(2, len(points)):
        while len(convex_hull) > 1 and orientation(convex_hull[-2], convex_hull[-1], points[i]) != 2:
            convex_hull.pop()
        convex_hull.append(points[i])

    return convex_hull

def chan_algorithm(points):
    def graham_scan(points, m):
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # collinear
            return 1 if val > 0 else 2  # clock or counterclock-wise

        def graham_scan_cmp(p1, p2):
            o = orientation(p0, p1, p2)
            if o == 0:
                return -1 if (p0[0], p0[1]) < (p1[0], p1[1]) else 1
            return -1 if o == 2 else 1

        p0 = min(points)
        points.sort(key=lambda point: (atan2(point[1] - p0[1], point[0] - p0[0]), point))

        if m < 3:
            return points
        else:
            stack = [points[0], points[1], points[2]]

        for i in range(3, m):
            while len(stack) >= 2 and orientation(stack[-2], stack[-1], points[i]) != 2:
                stack.pop()
            stack.append(points[i])

        return stack

    n = len(points)
    if n < 6:
        return graham_scan(points, n)

    # Step 1: Divide the points into sqrt(n) groups
    num_groups = int(n**0.5)
    group_size = n // num_groups

    groups = [points[i:i + group_size] for i in range(0, n, group_size)]

    # Step 2: Find convex hull of each group using Graham's scan
    group_hulls = [graham_scan(group, len(group)) if len(group) >= 3 else group for group in groups]

    # Step 3: Find the lowest point in each group hull
    lowest_points = [min(group_hull) for group_hull in group_hulls]

    # Step 4: Find the convex hull of the lowest points using Graham's scan
    final_hull = graham_scan(lowest_points, len(lowest_points))

    # Step 5: Merge the convex hulls of each group
    for i in range(1, len(final_hull) - 1):
        x1, y1 = final_hull[i]
        x2, y2 = final_hull[i + 1]
        group_index = -1

        for j, group in enumerate(groups):
            if min(group) == final_hull[i] and max(group) == final_hull[i + 1]:
                group_index = j
                break

        # Add the convex hull of the corresponding group to the final hull
        final_hull.extend(group_hulls[group_index][1:-1])

    return final_hull