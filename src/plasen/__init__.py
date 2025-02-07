import csv
import pandas as pd
from . import phys_calc
import matplotlib.pyplot as plt
import numpy as np
import os

class HFS_data:
    def __init__(self, x_axis_name: str = 'Wavenumber'):
        self.x_axis_name = x_axis_name
        self.df = pd.DataFrame(columns=['Timestamp', 'BunchNo', 'Channel', 'TOF', self.x_axis_name])
    
    def read_csv(self, file_path: str):
        """
        Parameters:
        - file_path: Path to the CSV file
        """
        timestamps = []
        wavenumbers = []
        signals = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                timestamps.append(float(row[0]))
                wavenumbers.append(float(row[1]))
                signals.append(eval(row[2]))
        data = []
        for i in range(len(signals)):
            for signal in signals[i]:
                data.append([timestamps[i], *signal, wavenumbers[i]])
        
        if self.df.empty:
            self.df = pd.DataFrame(data, columns=self.df.columns)
        else:
            self.df = pd.concat([self.df, pd.DataFrame(data, columns=self.df.columns)], ignore_index=True)

        self.df.sort_values(by='Timestamp', inplace=True)

    def read_folder(self, folder_path: str):
        """
        Only for old version. This will be removed after New DAQ is completed.

        Parameters:
        - folder_path: Path to the folder containing CSV files
        """
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        timestamps = []
        voltages = []
        signals = []
        for txt_file in txt_files:
            with open(os.path.join(folder_path, txt_file), mode='r', encoding='utf-8') as file:
                file_data = eval(file.readline())
                timestamps.append(float(file_data[0]))
                voltages.append(float(file_data[1]))
                signals.append(file_data[2])
        
        data = []
        for i in range(len(signals)):
            for signal in signals[i]:
                data.append([timestamps[i], *signal, voltages[i]])
        
        if self.df.empty:
            self.df = pd.DataFrame(data, columns=self.df.columns)
        else:
            self.df = pd.concat([self.df, pd.DataFrame(data, columns=self.df.columns)], ignore_index=True)

        self.df.sort_values(by='Timestamp', inplace=True)

    def save_csv(self, file_path: str):
        """
        Parameters:
        - file_path: Path to save the DataFrame
        """

        # self.df['BunchNo'] = self.df['BunchNo'].astype('int')
        # self.df['Channel'] = self.df['Channel'].astype('int')
        # self.df['TOF'] = self.df['TOF'].astype('int')
        # self.df.drop(columns=['BunchNo'], inplace=True)

        self.df.to_csv(file_path, index=False)

    def read_cali_csv(self, file_path: str, name: str = 'InitEnergy', omit_value = None):
        """
        Parameters:
        - file_path: Path to the calibration CSV file
        """
        calibration = pd.read_csv(file_path)
        calibration.columns = ['Timestamp', name]
        calibration.dropna(subset=[name], inplace=True)

        if omit_value is not None:
            calibration = calibration[calibration[name] != omit_value]

        # 合并calibration数据到self.df中，保留所有数据
        if name not in self.df.columns:
            self.df = pd.merge(self.df, calibration, on='Timestamp', how='outer')
        else:
            self.df = pd.merge(self.df, calibration, on=['Timestamp', name], how='outer')

    def read_cali_txt(self, file_path: str, name: str = 'InitEnergy', omit_value = None):
        """
        Only for the old version. This will be removed after New DAQ is completed.
        Parameters:
        - file_path: Path to the calibration text file
        """
        with open(file_path, mode='r', encoding='utf-8') as file:
            file_data = eval(file.readline())

        calibration = pd.DataFrame(file_data, columns = ['Timestamp', name])
        calibration.dropna(subset=[name], inplace=True)

        if omit_value is not None:
            calibration = calibration[calibration[name] != omit_value]

        # 合并calibration数据到self.df中，保留所有数据
        if name not in self.df.columns:
            self.df = pd.merge(self.df, calibration, on='Timestamp', how='outer')
        else:
            self.df = pd.merge(self.df, calibration, on=['Timestamp', name], how='outer')
    
    def fill_cali(self, col_name: str, method: str = 'ffill'):
        """
        Parameters:
        - col_name: Name of the column to fill
        - method: Method to fill the column, 'ffill', 'bfill' or 'interpolate'
        """
        if method == 'ffill':
            self.df[col_name] = self.df[col_name].ffill().bfill()
        elif method == 'bfill':
            self.df[col_name] = self.df[col_name].bfill().ffill()
        elif method == 'interpolate':
            self.df[col_name] = self.df[col_name].interpolate().ffill().bfill()
    
    def dropna(self):
        self.df = self.df.dropna(subset=['TOF'])

    def voltage_cali(self, BOP_file_path: str = None, gain_factor: float = 0.9988):
        
        self.df['InitEnergy'] = self.df['InitEnergy'] * gain_factor
        
        if BOP_file_path is not None:
            with open(BOP_file_path) as file:
                reader = csv.reader(file)
                volt_in = []
                volt_out = []
                next(reader)
                for row in reader:
                    volt_in.append(float(row[1]))
                    volt_out.append(float(row[2]))
            k, b = np.polyfit(volt_in, volt_out, 1)  # 1 表示线性拟合
            # est=sm.OLS(volt_out,sm.add_constant(volt_in)).fit()
            # b, k = est.params
            self.df['InitEnergy'] = self.df['InitEnergy'] - k * self.df['Voltage'] - b
            self.df.drop(columns=['Voltage'], inplace=True)
                

    def diode_cali(self, ref_freq: float):
        """
        This is a method to calibrate the wavenumber using the diode signal.

        Parameters:
        - ref_freq: Reference frequency for the calibration
        """
        self.df['Wavenumber'] = self.df['Diode'] - ref_freq + self.df['Wavenumber']
        self.df.drop(columns=['Diode'], inplace=True)

    def doppler_shift(self, mass: float):
        """
        This is a method to calculate the Doppler shift.

        Parameters:
        - mass: Mass of the atom
        """
        self.df['Wavenumber'] = phys_calc.dopplerfactor(mass, self.df['InitEnergy'] * 1000) * self.df['Wavenumber']
        self.df.drop(columns=['InitEnergy'], inplace=True)
    
    def wavenumber_cut(self, start: float, end: float):
        """
        This is a method to cut the DataFrame by wavenumber.

        Parameters:
        - start: Start of the wavenumber range (cm^-1)
        - end: End of the wavenumber range (cm^-1)
        """
        self.df = self.df[(self.df['Wavenumber'] >= start) & (self.df['Wavenumber'] <= end)]

    def tof_cut(self, start: float, end: float):
        """
        This is a method to cut the DataFrame by TOF.

        Parameters:
        - start: Start of the TOF range (μs)
        - end: End of the TOF range (μs)
        """
        self.df = self.df[((self.df['TOF'] >= start * 2000) & (self.df['TOF'] <= end * 2000)) | (self.df['TOF'] == -1)]
    
    def channel_cut(self, channel: list[int] = [1,2]):
        """
        This is a method to cut the DataFrame by channel.

        Parameters:
        - channel: List of channels to keep
        """
        self.df = self.df[self.df['Channel'].isin(channel+[-1])]
    
    def timestamp_cut(self, start: float, end: float):
        """
        This is a method to cut the DataFrame by timestamp.

        Parameters:
        - start: Start of the timestamp range (s)
        - end: End of the timestamp range (s)
        """
        self.df = self.df[(self.df['Timestamp'] >= start) & (self.df['Timestamp'] <= end)]

    def draw_tof(self, bins: int = 100):
        """
        This is a method to draw the TOF distribution.

        Parameters:
        - bins: Number of bins for the histogram
        """
        plt.hist(self.df[self.df['TOF'] != -1]['TOF'] / 2000, bins=bins)
        plt.show()
    
    def count_rate(self, bin_width: float = 20, bunch_per_second: float = 100 ,is_draw: bool = True, save_path: str = None) -> pd.DataFrame:
        """
        This is a method to calculate the count rate and error, and return the DataFrame.

        Parameters:
        - bin_width: Width of the bin (MHz)
        - bunch_per_second: Bunches per second
        """

        start = self.df['Wavenumber'].min()
        end = self.df['Wavenumber'].max()
        bin_num = int((end - start) / (bin_width * phys_calc.MHz_to_invcm)) + 1
        end = start + bin_num * bin_width * phys_calc.MHz_to_invcm

        bins = np.linspace(start, end, bin_num + 1)

        bunches = self.df[self.df['Channel'] == -1].copy()
        counts = self.df[self.df['Channel'] != -1].copy()
        bunches['binned'] = pd.cut(bunches['Wavenumber'], bins=bins, include_lowest=True)
        counts['binned'] = pd.cut(counts['Wavenumber'], bins=bins, include_lowest=True)
        
        # bunches.to_csv('bunches.csv')
        # counts.to_csv('counts.csv')

        bin_bunches = bunches['binned'].value_counts().sort_index()
        bin_counts = counts['binned'].value_counts().sort_index()

        rates = pd.merge(bin_bunches, bin_counts, left_index=True, right_index=True, how='left')
        rates.columns = ['Bunch', 'Count']
        rates.index = rates.index.map(lambda x: x.mid * phys_calc.invcm_to_MHz)

        rates = rates[rates['Bunch'] > 0]
        rates['y'] = rates['Count'] / rates['Bunch'] * bunch_per_second
        rates['yerr'] = rates['Count'] ** 0.5 / rates['Bunch'] * bunch_per_second
        rates.loc[rates['yerr'] == 0, 'yerr'] += 1 / rates['Bunch'] * bunch_per_second # 防止除零错误

        if save_path is not None:
            rates.to_csv(save_path)

        if is_draw == True:
            plt.errorbar(rates.index, rates['y'], yerr=rates['yerr'], fmt='o', color='black', markersize=3)
            plt.ylabel('Count Rate (cps)')
            plt.xlabel('Wavenumber (invcm)')
            plt.title('Count Rate vs. Wavenumber')
            plt.show()

        return rates

class HFS_fit:
    def __init__(self, data: pd.DataFrame, fit_ini: dict = None):
        '''
        Parameters:
        - data: HFS_data object
        - fit_ini: Initial guess for the fit parameters: I, J, ABC, transition wavenumber in invcm
        - df: Shift of the data in MHz
        - fwhmg: FWHM of the Gaussian in MHz
        - fwhml: FWHM of the Lorentzian in MHz
        - scale: Scaling factor for the fit
        - bg: Background level for the fit

        Example:
            fit_ini = {
                "I": 0,
                "J": [0, 0],
                "ABC": [0, 0, 0, 0, 0, 0],
                "trans": 0
            }
        '''
        self.data = data
        self.x = np.array(self.data.index)
        self.y = np.array(self.data['y'])
        self.yerr = np.array(self.data['yerr'])

        if fit_ini:
            self.fit_ini = fit_ini
        else:
            self.fit_ini = {"I": 0, "J": [0, 0], "ABC": [0, 0, 0, 0, 0, 0], "trans": 0}

    def import_json(self, file_path: str):
        import json
        with open(file_path, 'r') as file:
            self.fit_ini = json.load(file)
            if 'I' not in self.fit_ini:
                self.fit_ini['I'] = 0
            if 'J' not in self.fit_ini:
                self.fit_ini['J'] = [0, 0]
            if 'ABC' not in self.fit_ini:
                self.fit_ini['ABC'] = [0, 0, 0, 0, 0, 0]
            if 'trans' not in self.fit_ini:
                self.fit_ini['trans'] = 0

    def crystalball_fit(self, df: float = 0, fwhm: float = 30, scale: float = 1, bg: float = 0, is_fit: bool = True, is_AB_fixed: bool = False, Au_Al_ratio: float = None, crystalballparams: dict = { 'Taillocation': -0.25,'Tailamplitude': 6}):
        import satlas as sat
        x = self.x - self.fit_ini['trans'] * phys_calc.invcm_to_MHz

        s_main = sat.HFSModel(self.fit_ini['I'], self.fit_ini['J'], self.fit_ini['ABC'], df, fwhm, scale, [bg], shape='crystalball', crystalballparams=crystalballparams)
        if is_AB_fixed:        
            s_main.params['Au'].vary = False
            s_main.params['Al'].vary = False
            s_main.params['Bu'].vary = False
            s_main.params['Bl'].vary = False
        s_main.params['Cu'].vary = False
        s_main.params['Cl'].vary = False

        if Au_Al_ratio is not None: s_main.fix_ratio(Au_Al_ratio, target='upper', parameter='A')
        
        if is_fit:
            sat.chisquare_fit(s_main, x, self.y, self.yerr)
            s_main.display_chisquare_fit()

        self.fit_result_x = np.linspace(min(x), max(x), 1000)
        self.fit_result_y = s_main(self.fit_result_x)


    def voigt_fit(self, df: float = 0, fwhmg: float = 30, fwhml: float = 20, scale: float = 1, bg: float = 0, is_fit: bool = True, is_AB_fixed: bool = False, Au_Al_ratio: float = None):
        import satlas2 as sat
        x = self.x - self.fit_ini['trans'] * phys_calc.invcm_to_MHz

        datasource = sat.Source(x, self.y, yerr=self.yerr, name='Data')
        f = sat.Fitter()

        s_main = sat.HFS(self.fit_ini['I'], self.fit_ini['J'], self.fit_ini['ABC'][:2], self.fit_ini['ABC'][2:4], self.fit_ini['ABC'][4:],df = df, fwhmg=fwhmg, fwhml=fwhml, name='main', scale=scale, racah=False)
        bg = sat.Polynomial([bg], 'bg')

        if is_AB_fixed:        
            s_main.params['Au'].vary = False
            s_main.params['Al'].vary = False
            s_main.params['Bu'].vary = False
            s_main.params['Bl'].vary = False
        s_main.params['Cu'].vary = False
        s_main.params['Cl'].vary = False
        # s_main.params['FWHMG'].vary = False

        if Au_Al_ratio is not None: f.setExpr(["Data___main___Au"], "Data___main___Al * " + str(Au_Al_ratio))

        datasource.addModel(s_main)
        datasource.addModel(bg)
        f.addSource(datasource)
        
        if is_fit:
            f.fit()
            print(f.reportFit())

        self.fit_result_x = np.linspace(min(x), max(x), 1000)
        self.fit_result_y = datasource.evaluate(self.fit_result_x)

    def draw(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(self.fit_result_x, self.fit_result_y, '-',lw=1., c= 'r', label='Fitting')
        ax.errorbar(self.x - self.fit_ini['trans'] * phys_calc.invcm_to_MHz, self.y, self.yerr, fmt='ko', markersize=3., label='Data')
        ax.set_xlabel("Relative Frequency (MHz)")
        ax.set_ylabel("Rate (cps)")
        ax.legend()
        plt.show()

    def brokenaxes_draw(self, range: tuple):

        import brokenaxes

        fig = plt.figure(figsize=(8, 6))
        bax = brokenaxes.brokenaxes(xlims=range)

        bax.plot(self.fit_result_x, self.fit_result_y, '-',lw=1., c= 'r', label='Fitting')
        # 绘图
        bax.errorbar(self.x - self.fit_ini['trans'] * phys_calc.invcm_to_MHz, self.y, self.yerr, fmt='ko', markersize=3., label='Data')
        bax.set_xlabel("Relative Frequency (MHz)")
        bax.set_ylabel("Rate (cps)")

        bax.legend()
        plt.show()