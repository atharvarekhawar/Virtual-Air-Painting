import numpy as np

class KalmanFilter:
    def __init__(self, process_noise=1e-5, measurement_noise=1e-1):
        self.state = np.zeros((4, 1))  # [x, y, dx, dy] where dx and dy are velocities
        self.P = np.eye(4)  # Covariance matrix
        self.Q = np.eye(4) * process_noise  # Process noise covariance
        self.R = np.eye(2) * measurement_noise  # Measurement noise covariance
        self.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])  # Observation model
        self.F = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]])  # State transition matrix

    def update(self, measurement):
        # Prediction step
        self.state = np.dot(self.F, self.state)  # Predicted state
        self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q  # Predicted covariance

        # Measurement update
        y = measurement - np.dot(self.H, self.state[:2])  # Innovation
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R  # Innovation covariance
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # Kalman gain

        # Update the state and covariance
        self.state = self.state + np.dot(K, y)
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)

        return self.state[:2].flatten()  # Return the updated position (x, y)

