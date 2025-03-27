import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plasen import HFS_simulation

import pandas as pd

time_one_side = 60 * 60 * 8
bg_ratio = 1/150
# fit_ini = {"name": "97Rb", "I": 1.5, "J": [0.5, 1.5], "ABC": [2286.2, 55.2, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 90.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391}
sim_1 = HFS_simulation(100, 1 / 200 * 0.6, bg_ratio, time = time_one_side, bin_num=50, scan_range = [-1750,-750], fit_ini={"type": "scan_ranges", "name": "85Rb", "I": 2.5, "J": [0.5, 1.5], "ABC": [1011.0, 25.3, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 50.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391})
x_1,y_1,yerr_1 = sim_1.get_result()

bg = bg_ratio * 100* 1 / 200 * 0.6 * time_one_side / 50


sim_2 = HFS_simulation(100, 1 / 200 * 0.6, bg_ratio, time = time_one_side, bin_num=50, scan_range = [1200,2200], fit_ini={"type": "scan_ranges", "name": "85Rb", "I": 2.5, "J": [0.5, 1.5], "ABC": [1011.0, 25.3, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 50.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391})
x_2,y_2,yerr_2 = sim_2.get_result()
# sim = HFS_simulation(100, 1 / 400, 10/1640, time = 60 * 60 * 12, bin_num=100, scan_range = [-1750,-750], fit_ini={"type": "scan_ranges", "name": "85Rb", "I": 2.5, "J": [0.5, 1.5], "ABC": [1011.0, 25.3, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 90.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391})
# sim = HFS_simulation(100, 1 / 400, 10/1640, time = 60 * 60 * 12, bin_num=100, scan_range = [1200,2200], fit_ini={"type": "scan_ranges", "name": "85Rb", "I": 2.5, "J": [0.5, 1.5], "ABC": [1011.0, 25.3, 0.0, 21.4, 0.0, 0.0], "trans": 12816.545, "fwhm": [20.0, 90.0], "range": 2000, "V": 29980.0, "mass": 84.91179, "laser": 12805.391})

x = list(x_1) + list(x_2)
y = list(y_1) + list(y_2)

yerr = list(yerr_1) + list(yerr_2)

df = pd.DataFrame({"x": x, "y": y, "yerr": yerr})
df.to_csv("simulation_8h.csv", index=False)


import matplotlib.pyplot as plt
from brokenaxes import brokenaxes
import numpy as np

# y = np.array(y) - bg
print(sim_1.model.hfs.pos(), sim_1.model.background_params)

n_s = sim_1.model.f(sim_1.model.hfs.pos()[3])[0]
n_b = sim_1.model.background_params[0]
n_s = n_s - n_b
print(n_s, n_b)

print(np.sqrt(2 * ((n_s+n_b)*np.log(1+n_s/n_b)- n_s)))

fig = plt.figure(figsize=(5, 5))
bax = brokenaxes(xlims=((-1750, -750), (1200, 2200)))
bax.errorbar(x, y, yerr, fmt='o', label='scan1', color='k', markersize=3)

x_plot = np.linspace(-1750, 2200, 5000)
y_plot = sim_1.model.f(x_plot)
bax.plot(x_plot, y_plot, color='r')

df_plot = pd.DataFrame({"x": x_plot, "y": y_plot})
df_plot.to_csv("spec.csv", index=False)

plt.show()

# print(x,y,yerr)