#  PR Curves 绘制
import os
from utils import  *
from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator

other_data_path = r'path to other_data path ..../other_path'
save_path = r'path to save  .../PR'

model = ['F3Net', 'ITSD', 'DCN', 'RCSB', 'ICON-R', 'EDNet', 'GFINet', 'DCNet-R']
datasets = {
            "ECSSD": [0.8, 1.0, 0.05],
            "PASCAL-S": [0.5, 1.0, 0.05],
            "DUTS-TE": [0.5, 1.0, 0.05],
            "HKU-IS": [0.8, 1.0, 0.05],
            "DUT-OMRON": [0.5, 0.95, 0.05]
         }
for dataset in datasets :
    for item in model:
      P,R,F=[],[],[]
      file_path = os.path.join(other_data_path,item,'ECEL',f'{item}_{dataset}_f_p_r.xlsx')
      print(file_path)
      f=open_xls(file_path)
      x=getshnum(f)
      for shnum in range(x):
        rvalue=getFile(file_path,shnum)
      for i in range(1,len(rvalue)):
        P.append(rvalue[i][0])
        R.append(rvalue[i][1])
        F.append(rvalue[i][2])
      print(len(P),len(R),len(F))

      if item == model[-1]:
          plt.plot(R,P,'r',linewidth=2.0,label='Our',)
      else:
          plt.plot(R,P,'--',label=item)
      plt.title(dataset)
      num1 = 0
      num2 = 0
      num3 = 3
      num4 = 0
      plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4) 
    #   plt.legend()
      plt.grid(axis='both',ls='--',lw=1) 
      plt.ylim([datasets[dataset][0],datasets[dataset][1]])
      plt.xlim([0,1])
      x_set = MultipleLocator(0.2)
      y_set = MultipleLocator(0.05)
      ax=plt.gca()
      ax.xaxis.set_major_locator(x_set)  
      ax.yaxis.set_major_locator(y_set)
      plt.xlabel('Recall')
      plt.ylabel('Precision')

      if not os.path.exists(save_path):
          os.mkdir(save_path)
      plt.savefig(f'{save_path}/{dataset}.png',dpi=600)
    plt.close()
