import sys,os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plasen import phys_calc

for mass in []:
    phys_calc.dopplerfactor(mass, 29980)