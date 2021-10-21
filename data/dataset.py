import numpy as np
import json

PERFECT = 50

class Dataset():
	def __init__(
		self,
		root,
		mode,
		match_filename,
		user_filename,
		valid_ratio = 0,
		shuffle = False,
		**kwargs
	):

		super().__init__()
		self.root = root
		self.mode = mode
		self.valid_ratio = valid_ratio
		self.shuffle = shuffle
		self.match_filename = match_filename
		self.user_filename = user_filename

		if self.mode in ["training"]:
			self.train_x, self.train_y, self.valid_x, self.valid_y = self.load_data(self.mode)
		if self.mode in ["test"]:
			self.data, self.target = self.load_data(self.mode)

	def load_data(self, mode):
		data = []
		target = []
		idx = []

		Each_Match_of_User = {}

		MatchInfo_file = self.root + '/' + self.match_filename
		UserInfo_file = self.root + '/' + self.user_filename

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
						
						lane = Match_data["teamPosition"][match]
						if lane != "BOTTOM" and lane != "TOP" and lane != "JUNGLE" and lane != "MIDDLE" and lane != "UTILITY":
							continue


						champion = int(Match_data["championId"][match])
						#print(champion, type(champion))
						if champion > 300000:
							continue
						champion = str(champion)
						champion_proficiency = User_proficiency_data[champion][user_index[user_name]]

						one_of_data.append(Match_data["largestKillingSpree"][match])
						#one_of_data.append(gold_per_minute)
						one_of_data.append(gold_per_minute/100)
						one_of_data.append(kda_of_user)
						#one_of_data.append(damage_dealt_per_minute)
						one_of_data.append(damage_dealt_per_minute/100)
						#one_of_data.append(damage_taken_per_minute)
						one_of_data.append(damage_taken_per_minute/100)
						one_of_data.append(Match_data["detectorWardsPlaced"][match])
						one_of_data.append(Match_data["killingSprees"][match])
						one_of_data.append(Match_data["wardsKilled"][match])
						one_of_data.append(Match_data["wardsPlaced"][match])
						one_of_data.append(Match_data["visionScore"][match])
						one_of_data.append(minions_per_minute)
						#one_of_data.append(champion_proficiency)
						#one_of_data.append(champion_proficiency/10000)

						#print(one_of_data)
						one_of_data = np.array(one_of_data)
						one_of_data = (one_of_data - one_of_data.mean())/one_of_data.std()
						one_of_data = list(one_of_data)

						data.append(one_of_data)
						if Match_data["win"][match]:
							target.append([1])
						else:
							target.append([0])

			num_data = len(data)

			data = np.array(data)
			#data = (data - data.mean())/data.std()
			target = np.array(target)

			if mode == "training":
				if self.shuffle:
					perm = np.random.permutation(num_data)
					data = data[perm]
					target = target[perm]

				valid_data = int(num_data*self.valid_ratio)
				split_idx = num_data - valid_data
				train_x, valid_x = data[:split_idx], data[split_idx:]
				train_y, valid_y = target[:split_idx], target[split_idx:]

				return train_x, train_y, valid_x, valid_y
			else:
				return data, target