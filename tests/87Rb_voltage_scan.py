import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plasen import HFS_data, HFS_fit
from plasen import phys_calc

### This is only for example. You should replace the path with your own data path.

raw_data = HFS_data('Voltage')
raw_data.read_folder('data/1747&1748(voltage scan)/scan1747.0')
raw_data.read_folder('data/1747&1748(voltage scan)/scan1748.0')
raw_data.read_cali_txt('data/1747&1748(voltage scan)/cali_1747.0.txt')
raw_data.read_cali_txt('data/1747&1748(voltage scan)/cali_1748.0.txt')
raw_data.read_cali_txt('data/1747&1748(voltage scan)/cali_1747.0_wm.txt', 'Wavenumber', omit_value=-1)
raw_data.read_cali_txt('data/1747&1748(voltage scan)/cali_1748.0_wm.txt', 'Wavenumber', omit_value=-1)
raw_data.read_cali_txt('data/1747&1748(voltage scan)/cali_1747.0_diode.txt', 'Diode', omit_value=-1)
raw_data.read_cali_txt('data/1747&1748(voltage scan)/cali_1748.0_diode.txt', 'Diode', omit_value=-1)
raw_data.fill_cali('Wavenumber', 'ffill')
raw_data.fill_cali('InitEnergy', 'ffill')
raw_data.fill_cali('Diode', 'ffill')
raw_data.dropna()
raw_data.voltage_cali('data/1747&1748(voltage scan)/cali of BOP__scan_1745.0.csv', gain_factor=1)
raw_data.diode_cali(384227848.5512209 * phys_calc.MHz_to_invcm)
raw_data.doppler_shift(mass = 86.90918053)
raw_data.wavenumber_cut(12815,12817)
raw_data.tof_cut(5, 14)
raw_data.channel_cut([1])
# raw_data.draw_tof(bins=50)
raw_data.save_csv('87Rb_voltage_scan.csv')
rates = raw_data.count_rate(bin_width=10, is_draw=0, save_path='87Rb_voltage_scan_rates.csv')

fit = HFS_fit(rates)
fit.import_json('data/87Rb_I=1.5.json')
# fit.voigt_fit(df = 180, scale=340, bg = 8, is_fit = True, Au_Al_ratio=84.29/3415.9)
fit.crystalball_fit(df = 180, scale=340, bg = 8, is_fit = 1, fwhm=40, crystalballparams={'Taillocation': -0.5, 'Tailamplitude': 2.6}, Au_Al_ratio=84.29/3415.9)
fit.brokenaxes_draw([(-3250, -1400), (3300, 5150)])