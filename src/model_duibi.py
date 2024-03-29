# 对比其他模型的代码 将其他模型的predict map画到一张画布上
import os
import cv2
import matplotlib.pyplot as plt
GT_PATH = r'path to data       .../data'
other_data_path = r'path to other_data path  .../other_path'
save_path = r'path to save   .../out'

model = ['F3Net','LDF']
datasets = ["ECSSD","PASCAL-S","DUTS-TE","HKU-IS","DUT-OMRON"]
for dataset in  datasets:
    file_name = []
    with open(os.path.join(GT_PATH,dataset,"test.txt")) as f:
        for line in f:
            file_name.append(line.replace("\n","")+".png")
        index = 1
        for item in file_name:
            print(dataset,f'[{index}/',len(file_name),']')
            index+=1
            image = cv2.imread(os.path.join(GT_PATH,dataset,'image',item.replace('.png','.jpg')))
            mask = cv2.imread(os.path.join(GT_PATH,dataset,'mask',item))
            plt.subplot(4,4,1)
            plt.imshow(image)
            plt.subplot(4,4,2)
            plt.imshow(mask)
            i = 1
            for model_name in model:
                if model_name in ['RCSB','SRformer']:
                    model_mask = cv2.imread(os.path.join(other_data_path,f'{model_name}/{model_name}',dataset,item.replace('.png','_sal.png')))
                else: 
                    model_mask = cv2.imread(os.path.join(other_data_path,f'{model_name}/{model_name}',dataset,item))
                if model_mask is None:
                    continue
                plt.subplot(4,4,2+i)
                i+=1
                plt.imshow(model_mask)
                plt.title(model_name)
            savePath = f'{save_path}/{dataset}/'
            if not os.path.exists(savePath):
                os.mkdir(savePath)
            plt.savefig(os.path.join(savePath, item))
            plt.close()
            



                
             
    