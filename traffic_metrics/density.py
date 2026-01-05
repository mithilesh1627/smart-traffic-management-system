class DensityCalculator:
    def __init__(self, roi_area_pixels):
        self.roi_area = roi_area_pixels

    def compute(self, num_vehicles):
        return round(num_vehicles / self.roi_area, 6)
