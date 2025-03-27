import lmfit
import numpy as np

def multi_voigt(x, fwhmg, fwhml, baseline, heights, positions):
    model = np.zeros_like(x) + baseline
    for height, position in zip(heights, positions):
        model += height * lmfit.models.VoigtModel().eval(x=x, center=position, sigma=fwhmg, gamma=fwhml)
    return model

class VoigtFitModel:
    def __init__(self, heights, positions):
        self.heights = heights
        self.positions = positions
        self.model = lmfit.Model(multi_voigt, independent_vars=['x'])
    
    def fit(self, x, y, fwhmg=1, fwhml=1, baseline=0, scale=1):
        params = self.model.make_params(fwhmg=1, fwhml=1, baseline=0)
        for i, (height, position) in enumerate(zip(self.heights, self.positions)):
            params.add(f'heights{i}', value=height*scale)
            params.add(f'positions{i}', value=position)
        result = self.model.fit(y, params, x=x)
        return result

def voigt_fit_with_known_frequency(centroid: float, measured_frequency: list, relative_intensity: list):
    model = VoigtFitModel(relative_intensity, measured_frequency)
    result = model.fit(measured_frequency, relative_intensity, fwhmg=27, fwhml=3, baseline=10, scale=350)