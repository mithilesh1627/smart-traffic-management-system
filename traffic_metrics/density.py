class DensityCalculator:
    def __init__(self, roi_area_pixels: int):
        """
        roi_area_pixels: area of road region in pixels
        """
        self.roi_area = roi_area_pixels

    def compute(self, total_vehicles: int):
        """
        Returns normalized density
        """
        density = total_vehicles / self.roi_area

        if density < 0.0005:
            level = "LOW"
        elif density < 0.0015:
            level = "MEDIUM"
        else:
            level = "HIGH"

        return {
            "density_value": density,
            "density_level": level
        }
