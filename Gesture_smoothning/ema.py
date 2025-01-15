class EMA:
    def __init__(self, alpha=0.1):
        self.alpha = alpha  # Smoothing factor (0 < alpha <= 1)
        self.value = None  # To store the previous value

    def update(self, measurement):
        if self.value is None:
            self.value = measurement  # Initialize with the first measurement
        else:
            self.value = self.alpha * measurement + (1 - self.alpha) * self.value  # EMA formula
        return self.value
