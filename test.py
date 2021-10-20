import numpy as np

from data import dataset

import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn

if __name__ == "__main__":

    test_batch = 128

    model_path = './models/'
    model_name = 'LOLproject.p'
    model = nn.Sequential(
        nn.Linear(12, 50),
        nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        #nn.ReLU(),
        nn.Linear(50, 100),
        nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        #nn.ReLU(),
        #nn.Linear(40, 50),
        #nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        #nn.ReLU(),
        #nn.Linear(50, 40),
        #nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        # #nn.ReLU(),
        #nn.Linear(40, 30),
        #nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        # nn.ReLU(),
        #nn.Linear(30, 20),
        #nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        nn.Linear(100, 10),
        nn.LeakyReLU(negative_slope = 0.01, inplace = False),
        # nn.ReLU(),
        nn.Linear(10, 1),
        nn.Sigmoid()
    )

    model.load_state_dict(torch.load(model_path+model_name))
    test = dataset.Dataset("./data", mode = "test", match_filename = 'MatchInfo_SILVER3.json', user_filename = "UserInfo_SILVER3.json")
    test_x, test_y = test.data, test.target
    test_x_tensor = torch.tensor(test_x).float()
    test_y_tensor = torch.tensor(test_y).float()
    test_dataset = TensorDataset(test_x_tensor, test_y_tensor)
    test_loader = DataLoader(test_dataset, batch_size=test_batch)

    correct = 0

    for b, batch_data in enumerate(test_loader):
        batch_x, batch_y = batch_data

        hypothesis = model(batch_x)

        prediction = hypothesis >= torch.FloatTensor([0.5])
        correct_prediction = prediction.float() == batch_y
        correct += correct_prediction.sum().item()
    accuracy = correct/len(test_dataset)

    print("Accuracy is {:2.2f}%".format(accuracy * 100))
