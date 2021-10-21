import numpy as np

from data import dataset

import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn

def main():

	#-------------------- Hyperparameter --------------------

	random_seed=1

	weight_decay = 5e-4
	learning_rate = 0.00001

	epochs = 2000
	train_batch = 128
	test_batch = 128
	valid_ratio = 0.1

	model_path = './models/'
	model_name = 'LOLproject.p'

	#--------------------------------------------------------

	np.random.seed(random_seed)
	torch.manual_seed(random_seed)

	if torch.cuda.is_available():
	    device = 'cuda' 
	    torch.cuda.manual_seed_all(random_seed) 
	    torch.backends.cudnn.deterministic = True
	else :
	    device = 'cpu'

	match_filenames = ['MatchInfo_GOLD4.json', 'MatchInfo_GOLD3.json', 'MatchInfo_GOLD2.json', 'MatchInfo_GOLD1.json',
					   'MatchInfo_PLATINUM4.json', 'MatchInfo_PLATINUM3.json', 'MatchInfo_PLATINUM2.json', 'MatchInfo_PLATINUM1.json',
                       'MatchInfo_SILVER4.json', 'MatchInfo_SILVER3.json', 'MatchInfo_SILVER2.json', 'MatchInfo_SILVER1.json']
	user_filenames = ["UserInfo_GOLD4.json", "UserInfo_GOLD3.json", "UserInfo_GOLD2.json", "UserInfo_GOLD1.json",
					  "UserInfo_PLATINUM4.json", "UserInfo_PLATINUM3.json", "UserInfo_PLATINUM2.json", "UserInfo_PLATINUM1.json",
                      "UserInfo_SILVER4.json", "UserInfo_SILVER3.json", "UserInfo_SILVER2.json", "UserInfo_SILVER1.json"]
	train_x = []
	train_y = []
	valid_x = []
	valid_y = []
	for i in range(0, len(match_filenames), 1):
		train_tmp = dataset.Dataset("./data", mode = "training", valid_ratio = valid_ratio, match_filename = match_filenames[i], user_filename = user_filenames[i], shuffle = True)
		if len(train_x) == 0:
			train_x, train_y, valid_x, valid_y = train_tmp.train_x, train_tmp.train_y, train_tmp.valid_x, train_tmp.valid_y
		else:
			train_x = np.append(train_x, train_tmp.train_x, axis = 0)
			train_y = np.append(train_y, train_tmp.train_y, axis = 0)
			valid_x = np.append(valid_x, train_tmp.valid_x, axis = 0)
			valid_y = np.append(valid_y, train_tmp.valid_y, axis = 0)
			
	print("Train length:", len(train_x), "Valid length:", len(valid_x), "\n")

	x_tensor = torch.tensor(train_x).float()
	y_tensor = torch.tensor(train_y).float()
	vx_tensor = torch.tensor(valid_x).float()
	vy_tensor = torch.tensor(valid_y).float()
	train_dataset = TensorDataset(x_tensor, y_tensor)
	valid_dataset = TensorDataset(vx_tensor, vy_tensor)
	train_loader = DataLoader(train_dataset, batch_size=train_batch)
	valid_loader = DataLoader(valid_dataset, batch_size=train_batch)

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
	optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay = weight_decay)

	early_stop = 0
	best_accuracy = 0

	for epoch in range(epochs):
		model.train()
		correct = 0
		for b, batch_data in enumerate(train_loader):
			batch_x, batch_y = batch_data

			hypothesis = model(batch_x)

			loss = F.binary_cross_entropy(hypothesis, batch_y)
			optimizer.zero_grad()
			loss.backward()
			optimizer.step()

			prediction = hypothesis >= torch.FloatTensor([0.5])
			correct_prediction = prediction.float() == batch_y
			correct += correct_prediction.sum().item()
		accuracy = correct/len(train_dataset)

		if epoch % 10 == 0:
			correct = 0
			model.eval()
			print('Epoch {:4d}/{} Cost: {:.6f} Train Accuracy: {:2.2f}%'.format(epoch, epochs, loss.item(), accuracy * 100), end = " ")

			for v, batch_data in enumerate(valid_loader):
				batch_x, batch_y = batch_data
				hypothesis = model(batch_x)

				prediction = hypothesis >= torch.FloatTensor([0.5])
				correct_prediction = prediction.float() == batch_y
				correct += correct_prediction.sum().item()
			accuracy = correct/len(valid_dataset)
			print("Valid Accuracy: {:2.2f}%".format(accuracy * 100))

			if accuracy > best_accuracy:
				print("Best valid accuracy is updated!", best_accuracy*100, "->", accuracy*100, "\n")
				torch.save(model.state_dict(), model_path+model_name)
				best_accuracy = accuracy
				early_stop = 0
			else:
				early_stop += 1
				print("Early stop: ", early_stop, "\n")
				if early_stop == 16:
					print("Early stop")
					break 
	print("Best accuracy is {:2.2f}%".format(best_accuracy * 100))
			

if __name__ == "__main__":
    main()