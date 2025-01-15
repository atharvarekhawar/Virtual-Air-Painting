import numpy as np
import cv2
from scipy.interpolate import CubicSpline

class VectorDraw:
    @staticmethod
    def interpolate_line(start, end, num_points=10):
        """
        Generate interpolated points between two points using linear interpolation.
        """
        x_values = np.linspace(start[0], end[0], num_points)
        y_values = np.linspace(start[1], end[1], num_points)
        return np.array(list(zip(x_values, y_values)), dtype=np.int32)

    @staticmethod
    def smooth_curve(points, resolution=100):
        """
        Generate a smooth curve using cubic splines from a list of points.
        """
        points = np.array(points)
        if len(points) < 3:
            return points  # Not enough points for spline interpolation
        
        x = points[:, 0]
        y = points[:, 1]
        t = np.arange(len(points))
        
        cs_x = CubicSpline(t, x)
        cs_y = CubicSpline(t, y)
        
        t_fine = np.linspace(0, len(points) - 1, resolution)
        smooth_points = np.array([cs_x(t_fine), cs_y(t_fine)]).T
        return smooth_points.astype(np.int32)

    @staticmethod
    def draw_vectorized_line(canvas, start, end, color, thickness, smooth=False):
        """
        Draw a line between two points with optional smoothing.
        """
        if smooth:
            # If smooth is True, use spline-based smoothing
            points = VectorDraw.smooth_curve([start, end], resolution=30)
        else:
            points = VectorDraw.interpolate_line(start, end)
        
        for i in range(len(points) - 1):
            cv2.line(canvas, tuple(points[i]), tuple(points[i + 1]), color, thickness)
