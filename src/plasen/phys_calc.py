import numpy as np

mass_unit = 1.66053904 * 10**(-27)
q = 1.60217657 * (10 ** (-19))
c = 299792458.0
AMU2KG = 1.66053892 * 10 ** (-27)
MHz_to_invcm = 10**6 / c / 100
invcm_to_MHz = 1 / MHz_to_invcm

# print(invcm_to_MHz)

def beta(mass, V):
    mass = mass * AMU2KG
    top = mass ** 2. * c ** 4.
    bottom = (mass * c ** 2. + q * V) ** 2.
    beta = np.sqrt(1. - top / bottom)
    return beta

def dopplerfactor(mass, V):
    betaFactor = beta(mass, V)
    dopplerFactor = np.sqrt((1.0 + betaFactor) / (1.0 - betaFactor))
    return dopplerFactor
    
def dopplerfactor2Volt(mass, dopplerfactor):
    mass = mass * AMU2KG
    df2 = dopplerfactor ** 2
    beta = (df2 - 1) / (df2 + 1)
    prop = 1 / np.sqrt(1 - beta ** 2) - 1
    Volt = prop * mass * c ** 2 / q
    return Volt

def sigma2fwhm(sigma):
    return sigma * 2 * np.sqrt(2 * np.log(2))

def total_fwhm(fwhmg, fwhml):
    fwhm = 0.5346 * fwhml + np.sqrt(0.2166 * fwhml * fwhml + fwhmg * fwhmg)
    return fwhm