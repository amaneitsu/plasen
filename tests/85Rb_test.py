import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plasen import HFS_data, HFS_fit
from plasen import phys_calc

raw_data = HFS_data('Wavenumber')
raw_data.read_new_csv('example_data/newDAQtest/scan_588.csv', x_axis_name='First')
raw_data.read_new_csv('example_data/newDAQtest/scan_589.csv', x_axis_name='First')
raw_data.read_cali_csv('example_data/newDAQtest/cali_588.csv')
raw_data.read_cali_csv('example_data/newDAQtest/cali_589.csv')
raw_data.fill_cali('InitEnergy', 'ffill')
# raw_data.fill_cali('Diode', 'ffill')
raw_data.dropna()
raw_data.voltage_cali()
# raw_data.diode_cali(384227848.5512209 * phys_calc.MHz_to_invcm)
raw_data.doppler_shift(mass = 84.91178974)
raw_data.wavenumber_cut(12812,12818)
raw_data.tof_cut(2, 15)
# raw_data.draw_tof(bins=50)
raw_data.channel_cut([1])
raw_data.save_csv('tests/test.csv')
rates = raw_data.count_rate(bin_width=12, is_draw=False, save_path='tests/85Rb_laser_scan_rates.csv')

fit = HFS_fit(rates)
fit.import_json('example_data/85Rb_I=2.5.json')
fit.voigt_fit(df = -115, scale=1200, bg = 10, is_fit = True, Au_Al_ratio=25.0020/1011.9108130, is_B_fixed=False, fwhmg = 328, fwhml = 74, use_racah=False)
# fit.asymmlorentzian_fit(df = -108, scale=1200, bg = 8.0, is_fit = 0, fwhm=500, asymmetryparams={'a': -0.1}, Au_Al_ratio=25.3/1011.9)
fit.brokenaxes_draw([(-2000, -600), (800, 2200)])