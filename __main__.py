import time
import tkinter as tk
from tkinter import filedialog, simpledialog, StringVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from convex_hull_algorithms import brute_force, jarvis_march, graham_scan, quick_elimination, chan_algorithm


class GeometricAlgorithmsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geometric Algorithms Demo")

        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.result_frame = tk.Frame(root)
        self.result_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Canvas for drawing points and segments
        self.canvas = tk.Canvas(self.canvas_frame, width=1000, height=1000, bg="black")
        self.canvas.pack()

        # Buttons
        self.load_button = tk.Button(self.result_frame, text="Load Points", command=self.load_points)
        self.load_button.pack()

        self.manual_input_button = tk.Button(self.result_frame, text="Manual Input", command=self.manual_input_points)
        self.manual_input_button.pack()

        self.intersect_button = tk.Button(self.result_frame, text="Check Intersection", command=self.check_intersection)
        self.intersect_button.pack()

        self.line_intersect_algorithm_var = StringVar(root)
        self.line_intersect_algorithm_var.set("Jarvis March")  # Default algorithm
        line_intersect_algorithms = ["Brute Force", "Jarvis March"]
        self.line_intersect_algorithm_dropdown = tk.OptionMenu(self.result_frame, self.line_intersect_algorithm_var, *line_intersect_algorithms)
        self.line_intersect_algorithm_dropdown.pack()

        self.result_label = tk.Label(self.result_frame, text="")
        self.result_label.pack()

        self.convex_hull_button = tk.Button(self.result_frame, text="Convex Hull", command=self.compute_convex_hull)
        self.convex_hull_button.pack()

        self.algorithm_var = StringVar(root)
        self.algorithm_var.set("Jarvis March")  # Default algorithm
        algorithms = ["Jarvis March", "Graham Scan", "Quick Elimination", "Brute Force", "Chan Algorithm"]
        self.algorithm_dropdown = tk.OptionMenu(self.result_frame, self.algorithm_var, *algorithms)
        self.algorithm_dropdown.pack()

        # Points data
        self.points = []

    def load_points(self):
        file_path = filedialog.askopenfilename(title="Select Points File", filetypes=[("Text files", "*.txt")])
        if file_path:
            self.points = self.read_points_from_file(file_path)
            self.draw_points()

    def manual_input_points(self):
        num_points = simpledialog.askinteger("Manual Input", "Enter the number of points:")
        if num_points is not None:
            self.points = []
            for _ in range(num_points):
                x = simpledialog.askfloat("Manual Input", "Enter x-coordinate:")
                y = simpledialog.askfloat("Manual Input", "Enter y-coordinate:")
                self.points.append((x, y))
            self.draw_points()

    def read_points_from_file(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            points = [tuple(map(float, line.strip().split())) for line in lines]
        return points

    def draw_points(self):
        self.canvas.delete("all")
        for point in self.points:
            self.canvas.create_oval(point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4, fill="white")

    def check_intersection(self):
        if len(self.points) < 4:
            self.result_label.config(text="Need at least 4 points for line segments")
            return

        selected_algorithm = self.line_intersect_algorithm_var.get()

        line_segments = [(self.points[i], self.points[i + 1]) for i in range(len(self.points) - 1)]
        line_segments.append((self.points[-1], self.points[0]))  # Closing the polygon

        # Call the different line intersection methods

        if selected_algorithm == "Jarvis March":
            if self.segments_intersect_jarvis_march(line_segments) == True:
                self.result_label.config(text="Line segments intersect via Jarvis March!")
            elif self.segments_intersect_brute_force(line_segments):
                self.result_label.config(text="Line segments intersect via Brute Force")
            else:
                self.result_label.config(text="No intersection found")
        elif selected_algorithm == "Brute Force":
            if self.segments_intersect_brute_force(line_segments) == True:
                self.result_label.config(text="Line segments intersect via Brute Force!")
            elif self.segments_intersect_jarvis_march(line_segments):
                self.result_label.config(text="Line segments intersect via Jarvis March")
            else:
                self.result_label.config(text="No intersection found")
        else:
            self.result_label.config(text="No intersection found")

    def compute_convex_hull(self):
        if len(self.points) < 3:
            self.result_label.config(text="Need at least 3 points for convex hull")
            return

        selected_algorithm = self.algorithm_var.get()

        if selected_algorithm == "Jarvis March":
            start_time = time.time()
            convex_hull = jarvis_march(self.points)
            end_time = time.time()
        elif selected_algorithm == "Graham Scan":
            start_time = time.time()
            convex_hull = graham_scan(self.points)
            end_time = time.time()
        elif selected_algorithm == "Quick Elimination":
            start_time = time.time()
            convex_hull = quick_elimination(self.points)
            end_time = time.time()
        elif selected_algorithm == "Brute Force":
            start_time = time.time()
            convex_hull = brute_force(self.points)
            end_time = time.time()
        elif selected_algorithm == "Chan Algorithm":
            start_time = time.time()
            convex_hull = chan_algorithm(self.points)
            end_time = time.time()
        else:
            # Handle unknown algorithm (optional)
            self.result_label.config(text="Unknown convex hull algorithm")
            return

        time_taken = end_time - start_time
        self.result_label.config(text=f"Convex Hull ({selected_algorithm}): {convex_hull}, \nTime: {time_taken:.8f} seconds")

        # Visualize the convex hull
        self.draw_convex_hull_animation(convex_hull)

    def draw_convex_hull_animation(self, convex_hull):
        self.canvas.delete("convex_hull")
        for i in range(len(convex_hull) - 1):
            x1, y1 = convex_hull[i]
            x2, y2 = convex_hull[i + 1]
            self.animate_line(x1, y1, x2, y2, fill="red", width=2, tags="convex_hull")

        # Connect the last and first points to close the convex hull
        self.animate_line(convex_hull[-1][0], convex_hull[-1][1], convex_hull[0][0], convex_hull[0][1], fill="red",
                          width=2, tags="convex_hull")

    def animate_line(self, x1, y1, x2, y2, **kwargs):
        line = self.canvas.create_line(x1, y1, x1, y1, **kwargs)

        steps = 10  # Number of animation steps
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        for _ in range(steps):
            self.canvas.move(line, dx, dy)
            self.root.update()
            self.root.after(50)  # Adjust the delay as needed

        # Move the line to its final position
        self.canvas.coords(line, x1, y1, x2, y2)

    def segments_intersect_brute_force(self, line_segments):
        for i in range(len(line_segments) - 1):
            for j in range(i + 1, len(line_segments)):
                if self.do_segments_intersect(line_segments[i], line_segments[j]):
                    self.draw_intersecting_lines(line_segments[i], line_segments[j])
                    return True
        return False

    def segments_intersect_jarvis_march(self, line_segments):
        for i in range(len(line_segments) - 1):
            for j in range(i + 2, len(line_segments) - 1):
                if i != 0 or j != len(line_segments) - 1:  # Skip adjacent segments in the polygon
                    if self.do_segments_intersect(line_segments[i], line_segments[j]):
                        self.draw_intersecting_lines(line_segments[i], line_segments[j])
                        return True
        return False

    def do_segments_intersect(self, segment1, segment2):
        p1, q1 = segment1
        p2, q2 = segment2

        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # collinear
            return 1 if val > 0 else 2  # clock or counterclock-wise

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and self.on_segment(p1, p2, q1):
            return True

        if o2 == 0 and self.on_segment(p1, q2, q1):
            return True

        if o3 == 0 and self.on_segment(p2, p1, q2):
            return True

        if o4 == 0 and self.on_segment(p2, q1, q2):
            return True

        return False

    def on_segment(self, p, q, r):
        return (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]))

    def draw_intersecting_lines(self, segment1, segment2):
        x1, y1 = segment1[0]
        x2, y2 = segment1[1]
        x3, y3 = segment2[0]
        x4, y4 = segment2[1]

        self.canvas.create_line(x1, y1, x2, y2, fill="orange", width=2, tags="intersecting_lines")
        self.canvas.create_line(x3, y3, x4, y4, fill="orange", width=2, tags="intersecting_lines")

def main():
    root = tk.Tk()
    app = GeometricAlgorithmsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
