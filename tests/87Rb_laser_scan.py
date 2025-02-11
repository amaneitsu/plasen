import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plasen import HFS_data, HFS_fit
from plasen import phys_calc

raw_data = HFS_data('Wavenumber')
raw_data.read_csv('example_data/1340&1341(laser scan)/scan_1340.csv')
raw_data.read_csv('example_data/1340&1341(laser scan)/scan_1341.csv')
raw_data.read_cali_csv('example_data/1340&1341(laser scan)/cali_1340.csv')
raw_data.read_cali_csv('example_data/1340&1341(laser scan)/cali_1341.csv')
raw_data.read_cali_csv('example_data/1340&1341(laser scan)/cali_1737189496.4011471_diode.csv', 'Diode', omit_value=-1)
raw_data.read_cali_csv('example_data/1340&1341(laser scan)/cali_1737189947.3715186_diode.csv', 'Diode', omit_value=-1)
raw_data.fill_cali('InitEnergy', 'ffill')
raw_data.fill_cali('Diode', 'ffill')
raw_data.dropna()
raw_data.voltage_cali()
raw_data.diode_cali(384227848.5512209 * phys_calc.MHz_to_invcm)
raw_data.doppler_shift(mass = 86.90918053)
raw_data.wavenumber_cut(12815,12817)
raw_data.tof_cut(5, 14)
raw_data.channel_cut([1])
# raw_data.draw_tof(bins=50)
raw_data.save_csv('tests/87Rb_laser_scan.csv')
rates = raw_data.count_rate(bin_width=10, is_draw=False, save_path='tests/87Rb_laser_scan_rates.csv')

fit = HFS_fit(rates)
fit.import_json('example_data/87Rb_I=1.5.json')
# fit.voigt_fit(df = 170, scale=350, bg = 0.2, is_fit = True)
# fit.crystalball_fit(df = -30, scale=340, bg = 8, is_fit = 1, fwhm=40, crystalballparams={'Taillocation': -0.5, 'Tailamplitude': 2.6}, Au_Al_ratio=84.29/3415.9)
fit.asymmlorentzian_fit(df = -30, scale=340, bg = 8, is_fit = 1, fwhm=40, asymmetryparams={'a': -0.5}, Au_Al_ratio=84.29/3415.9)
fit.brokenaxes_draw([(-3250, -1400), (3300, 5150)])