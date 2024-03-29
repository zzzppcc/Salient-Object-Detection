import os
import cv2
import numpy as np
import evaluation
import xlsxwriter

GT_PATH = r'path to data       .../data'
other_data_path = r'path to other_data path  .../other_path'

datasets = ["ECSSD", "PASCAL-S", "DUTS-TE", "HKU-IS", "DUT-OMRON"]
model = {
    'ResNet': ['AFNet', 'BASNet', 'CPD-R', 'GateNet', 'GCPA', 'F3Net', 'LDF', 'MINet', 'ITSD', 'U2Net', 'PurNet',
               'MSFNet', 'PFSNet', 'CTDNet', 'DCN', 'ICON-R', 'EDNet', 'RCSB', 'GFINet', 'DSLRDNet', 'MENet', 'DCNet-R',
               'M3Net-R'],
    'Transformer': ['VST', 'ICON-S', 'SRformer', 'DCNet-S', 'M3Net-S']
}

for key, value in model.items():
    print(key)
    for model_name in value:
        print(model_name)
        for dataset in datasets:
            saliency_evaluation = evaluation.SaliencyEvaluation()
            saliency_evaluation.clear()
            with open(os.path.join(GT_PATH, dataset, "test.txt")) as f:
                for line in f:
                    gt_path = os.path.join(GT_PATH, dataset, 'mask', line.replace("\n", "") + ".png")
                    if model_name in ["RCSB", "SRformer"]:
                        pred_path = os.path.join(other_data_path, f'{model_name}/{model_name}', dataset,
                                                 line.replace("\n", "") + "_sal.png")
                    else:
                        pred_path = os.path.join(other_data_path, f'{model_name}/{model_name}', dataset,
                                                 line.replace("\n", "") + ".png")
                    gt = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)
                    pred = cv2.imread(pred_path, cv2.IMREAD_GRAYSCALE)
                    if pred is None:
                        print("&" * 100)
                    if pred is not None and gt.shape == pred.shape:
                        saliency_evaluation.add_one(
                            pred.astype(np.float), gt.astype(np.float)
                        )
            MAE, Precision, Recall, F_m, S_m, E_m = saliency_evaluation.get_evaluation()
            idx = np.argmax(F_m)
            best_F = F_m[idx]
            mean_F = np.mean(F_m)
            best_precison = Precision[idx]
            best_recall = Recall[idx]
            print('{} - MAE:{}, max F-Measure:{}, mean F-Measure:{}, Precision:{},'
                  ' Recall:{}, S-Measure: {}, E-Measure: {}'
                  .format(dataset, MAE, best_F, mean_F, best_precison, best_recall,
                          S_m, E_m))
            # record Precision、Recall and F-measure
            endfile = f'{other_data_path}/{model_name}/ECEL/{model_name}_{dataset}_f_p_r.xlsx'
            print(endfile)
            wb = xlsxwriter.Workbook(endfile)
            ws = wb.add_worksheet()
            ws.write(0, 0, 'Precision')
            ws.write(0, 1, 'Recall')
            ws.write(0, 2, 'F_Measure')
            for a in range(len(Precision)):
                ws.write(a + 1, 0, Precision[a])
                ws.write(a + 1, 1, Recall[a])
                ws.write(a + 1, 2, F_m[a])
            wb.close()
            print("文件合并完成")
