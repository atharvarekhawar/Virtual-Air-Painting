import numpy as np
from sklearn.decomposition import PCA

class PCAOptimizer:
    def __init__(self, n_components=2):
        """
        Initialize the PCA Optimizer with the specified number of components.
        """
        self.n_components = n_components
        self.pca = PCA(n_components=n_components)

    def fit(self, landmarks):
        """
        Fit the PCA model to the input landmarks.
        """
        landmarks_np = np.array(landmarks)
        self.pca.fit(landmarks_np)

    def transform(self, landmarks):
        """
        Transform the input landmarks using the fitted PCA model.
        """
        landmarks_np = np.array(landmarks)
        return self.pca.transform(landmarks_np)

    def fit_transform(self, landmarks):
        """
        Fit the PCA model and transform the landmarks in one step.
        """
        landmarks_np = np.array(landmarks)
        return self.pca.fit_transform(landmarks_np)

    def inverse_transform(self, reduced_data):
        """
        Reconstruct the original landmarks from reduced data.
        """
        return self.pca.inverse_transform(reduced_data)

    def reconstruction_error(self, original_landmarks):
        """
        Compute reconstruction error for debugging and evaluation.
        """
        reduced_data = self.fit_transform(original_landmarks)
        reconstructed = self.inverse_transform(reduced_data)
        error = np.mean((np.array(original_landmarks) - reconstructed) ** 2)
        return error
