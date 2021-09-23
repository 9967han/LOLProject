import codecs
import os

import numpy as np
import torch
from torch import distributions as dist
from torch import nn
from torch.nn import functional as F
from torch.utils import data

import json

PERFECT = 50

class Dataset(data.Dataset):
	def __init__(
		self,
		root,
		mode,
		transform = None,
		**kwargs
	):

		super().__init__()
		self.root = root
		self.transform = transform
		self.mode = mode

		if self.mode in ["training"]:
			self.data, self.targets = self.load_data()

	def __len__(self):
		return len(self.data)

	def __getitem__(self, index):

		if self.mode in ["training"]:
			data, target = self.data[index], self.targets[index]

			if self.transform is not None:
				data = self.transform(data)
			return data, target

		return

	def load_data(self):
		data = []
		target = []
		idx = []

		Each_Match_of_User = {}

		MatchInfo_file = self.root + '/MatchInfo_GOLD4.json'
		UserInfo_file = self.root + '/UserInfo_GOLD4.json'

		with open(MatchInfo_file, 'r') as mf:
			Match_data = json.load(mf)
			for match_name in Match_data["encid"]:
				user_name = Match_data["encid"][match_name]
				if user_name in Each_Match_of_User:
					Each_Match_of_User[user_name].append(match_name)
				else:
					Each_Match_of_User[user_name] = [match_name]

			user_index = {}
			with open(UserInfo_file, 'r') as uf:
				User_proficiency_data = json.load(uf)
				for index in User_proficiency_data["encid"]:
					user_index[User_proficiency_data["encid"][index]] = index
				

				for user_name in Each_Match_of_User:
					for match in Each_Match_of_User[user_name]:
						#print(user_name, match)

						one_of_data = []
						if Match_data["deaths"][match] != 0:
							kda_of_user = (Match_data["kills"][match] + Match_data["assists"][match]) / Match_data["deaths"][match]
						else:
							kda_of_user = PERFECT

						gold_per_minute = Match_data["goldEarned"][match] / (Match_data["timePlayed"][match] // 60)
						damage_dealt_per_minute = Match_data["totalDamageDealtToChampions"][match] / (Match_data["timePlayed"][match] // 60)
						damage_taken_per_minute = Match_data["totalDamageTaken"][match] / (Match_data["timePlayed"][match] // 60)
						minions_per_minute = (Match_data["totalMinionsKilled"][match] + Match_data["neutralMinionsKilled"][match]) / (Match_data["timePlayed"][match] // 60)
						
						champion = str(Match_data["championId"][match])

						champion_proficiency = User_proficiency_data[champion][user_index[user_name]]

						one_of_data.append(Match_data["largestKillingSpree"][match])
						one_of_data.append(gold_per_minute)
						one_of_data.append(kda_of_user)
						one_of_data.append(Match_data["detectorWardsPlaced"][match])
						one_of_data.append(Match_data["killingSprees"][match])
						one_of_data.append(Match_data["wardsKilled"][match])
						one_of_data.append(Match_data["wardsPlaced"][match])
						one_of_data.append(Match_data["visionScore"][match])
						one_of_data.append(minions_per_minute)
						one_of_data.append(champion_proficiency)

						data.append(one_of_data)
						target.append(Match_data["win"][match])

			target = torch.BoolTensor(target)
			return data, target