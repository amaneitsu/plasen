import sys,os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plasen import phys_calc

from matplotlib import pyplot as plt

from brokenaxes import brokenaxes
import numpy as np
import satlas2

plt.rcParams.update({
    "font.family": "Helvetica Neue",  # 主字体
    "mathtext.fontset": "custom",     # 数学字体自定义
    "mathtext.rm": "Helvetica Neue",  # 数学公式中的正常体
    "mathtext.it": "Helvetica Neue:italic",  # 数学公式中的斜体
    "mathtext.bf": "Helvetica Neue:bold"     # 数学公式中的粗体
})


sim = satlas2.HFS(1.5, [0.5,1.5], [4020.3, 126.7], [0,95.0], [0,0], fwhmg=40, fwhml = 80)
x_plot = np.linspace(-5000, 7000, 10000)
y_plot = sim.f(x_plot)

bax = brokenaxes(xlims=((-4, -2), (4, 5.5)))

# 在对象上画图
bax.plot(x_plot / 1000, y_plot, color='r', label='$^{145}$Ba')

# 设置坐标轴标签
bax.set_xlabel('Relative Frequency (GHz)', labelpad=20)
bax.legend(frameon=False)
plt.show()