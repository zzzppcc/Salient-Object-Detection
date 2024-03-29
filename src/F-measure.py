# 代码用于F-measure Threshod Curve 绘制
import os
import xlrd
from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator
from utils import *

other_data_path = r'path to other_data path ..../other_path'
save_path = r'path to save  .../FT'


model = ['F3Net', 'ITSD', 'DCN', 'RCSB', 'ICON-R', 'EDNet', 'GFINet', 'DCNet-R']

datasets = {
    "ECSSD": [0.8, 1.0, 0.05],
    "PASCAL-S": [0.76, 0.9, 0.02],
    "DUTS-TE": [0.7, 0.95, 0.05],
    "HKU-IS": [0.7, 1.0, 0.05],
    "DUT-OMRON": [0.6, 0.9, 0.05],
}

for dataset in datasets:
    for item in model:
        P, R, F = [], [], []
        file_path = os.path.join(other_data_path, item, 'ECEL', f'{item}_{dataset}_f_p_r.xlsx')
        print(file_path)
        datavalue = []
        f = open_xls(file_path)
        x = getshnum(f)
        for shnum in range(x):
            rvalue = getFile(file_path, shnum)
        for i in range(1, len(rvalue)):
            P.append(rvalue[i][0])
            R.append(rvalue[i][1])
            F.append(rvalue[i][2])
        print(len(P), len(R), len(F))
        if item == model[-1]:
            plt.plot([i for i in range(256)], F, 'r', linewidth=2.0, label='Our', )
        else:
            plt.plot([i for i in range(256)], F, '--', label=item)
        plt.title(dataset, fontsize=15)
        num1 = 0
        num2 = 0
        num3 = 3
        num4 = 0
        plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4)
        plt.grid(axis='both', ls='--', lw=1)
        plt.ylim([datasets[dataset][0], datasets[dataset][1]])
        x_set = MultipleLocator(100)
        y_set = MultipleLocator(datasets[dataset][2])
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_set)
        ax.yaxis.set_major_locator(y_set)
        plt.xlabel('Threshold', fontsize=15)
        plt.ylabel('F-measure', fontsize=15)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        plt.savefig(f'{save_path}/{dataset}.png', dpi=600)
    plt.close()
