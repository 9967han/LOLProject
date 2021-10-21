import numpy as np

from data import dataset

import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.nn as nn

if __name__ == "__main__":

    test_batch = 128

    model_path = './models/'
    model_name = 'LOLproject.p'
    model = nn.Sequential(
        nn.Linear(11, 50),
        nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        nn.Linear(50, 30),
        nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        nn.Linear(30, 20),
        nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        nn.Linear(20, 10),
        nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        nn.Linear(10, 1),
        nn.Sigmoid()
    )

    model.load_state_dict(torch.load(model_path+model_name))
    test = dataset.Dataset("./data", mode = "test", match_filename = 'MatchInfo_SILVER1.json', user_filename = "UserInfo_SILVER1.json")
    test_x, test_y = test.data, test.target
    test_x_tensor = torch.tensor(test_x).float()
    test_y_tensor = torch.tensor(test_y).float()
    test_dataset = TensorDataset(test_x_tensor, test_y_tensor)
    test_loader = DataLoader(test_dataset, batch_size=test_batch)

    correct = 0
    TP_num = 0
    FP_num = 0
    FN_num = 0

    for _, batch_data in enumerate(test_loader):
        batch_x, batch_y = batch_data

        hypothesis = model(batch_x)

        prediction = hypothesis >= torch.FloatTensor([0.5])
        correct_prediction = prediction.float() == batch_y
        correct += correct_prediction.sum().item()

        for b, p in zip(batch_y, prediction):
            if b == torch.FloatTensor([1.0]) and p == torch.FloatTensor([1.0]):
                TP_num += 1
            elif b == torch.FloatTensor([0.0]) and p == torch.FloatTensor([1.0]):
                FP_num += 1
            elif b == torch.FloatTensor([1.0]) and p == torch.FloatTensor([0.0]):
                FN_num += 1

    accuracy = correct/len(test_dataset)

    print("Accuracy is {:2.2f}%".format(accuracy * 100))
    recall = TP_num / (TP_num + FN_num)
    precision = TP_num / (TP_num + FP_num)
    f1_score = (2*precision*recall) / (precision + recall)
    print("Precision is {:.2f}".format(precision))
    print("Recall is {:.2f}".format(recall))
    print("F1-Score is {:.2f}".format(f1_score))
