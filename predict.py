import numpy as np

import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.nn as nn

import sys
import json

PERFECT = 50

def parse_data(data_list):
    dataIdx = {}
    for i, idx in enumerate(["largestKillingSpree", "goldEarned", "timePlayed", "assists", "deaths", "kills", "detectorWardsPlaced", "killingSprees", "wardsKilled", "wardsPlaced", "visionScore", "totalDamageDealtToChampions", "totalDamageTaken", "totalMinionsKilled", "neutralMinionsKilled"]):
        dataIdx[idx] = i
    parsed_data = []
    #print(dataIdx)
    for data in data_list:
        one_of_data = []
        data = data.split(",")
        data = list(map(float, data))
        if data[dataIdx["deaths"]] != 0:        
            kda_of_user = (data[dataIdx["kills"]] + data[dataIdx["assists"]]) / data[dataIdx["deaths"]]
        else:
            kda_of_user = PERFECT
        gold_per_minute = data[dataIdx["goldEarned"]] / (data[dataIdx["timePlayed"]] // 60)
        damage_dealt_per_minute = data[dataIdx["totalDamageDealtToChampions"]] / (data[dataIdx["timePlayed"]] // 60)
        damage_taken_per_minute = data[dataIdx["totalDamageTaken"]] / (data[dataIdx["timePlayed"]] // 60)
        minions_per_minute = (data[dataIdx["totalMinionsKilled"]] + data[dataIdx["neutralMinionsKilled"]]) / (data[dataIdx["timePlayed"]] // 60)

        one_of_data.append(data[dataIdx["largestKillingSpree"]])
        one_of_data.append(gold_per_minute/100)
        one_of_data.append(kda_of_user)
        one_of_data.append(damage_dealt_per_minute/100)
        one_of_data.append(damage_taken_per_minute/100)
        one_of_data.append(data[dataIdx["detectorWardsPlaced"]])
        one_of_data.append(data[dataIdx["killingSprees"]])
        one_of_data.append(data[dataIdx["wardsKilled"]])
        one_of_data.append(data[dataIdx["wardsPlaced"]])
        one_of_data.append(data[dataIdx["visionScore"]])
        one_of_data.append(minions_per_minute)

        one_of_data = np.array(one_of_data)
        one_of_data = (one_of_data - one_of_data.mean())/one_of_data.std()
        one_of_data = list(one_of_data)

        parsed_data.append(one_of_data)

    parsed_data = np.array(parsed_data)
    return parsed_data


if __name__ == "__main__":
    
    parsed_data = parse_data(sys.argv[1:])
    x_tensor = torch.tensor(parsed_data).float()

    test_batch = 1

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
    
    hypothesis = 0

    for i in x_tensor:
        hypothesis += model(i)
    hypothesis /= 5

    #print("Prediction Winning Rate is {:2.2f}%".format(hypothesis * 100))

    print(str(round(hypothesis.item()*100, 2)))
