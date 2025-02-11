import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plasen import HFS_simulation

# sim = HFS_simulation(100, 1 / 400, 10/1640, time = 60 * 60 * 12, bin_num=200, scan_range = [-1750,2050], fit_ini={"type": "scan_ranges", "name": "85Rb", "I": 2.5, "J": [0.5, 1.5], "ABC": [1011.0, 25.3, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 90.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391})
# sim = HFS_simulation(100, 1 / 400, 10/1640, time = 60 * 60 * 12, bin_num=100, scan_range = [-1750,-750], fit_ini={"type": "scan_ranges", "name": "85Rb", "I": 2.5, "J": [0.5, 1.5], "ABC": [1011.0, 25.3, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 90.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391})
sim = HFS_simulation(100, 1 / 400, 10/1640, time = 60 * 60 * 12, bin_num=100, scan_range = [1200,2200], fit_ini={"type": "scan_ranges", "name": "85Rb", "I": 2.5, "J": [0.5, 1.5], "ABC": [1011.0, 25.3, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 90.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391})