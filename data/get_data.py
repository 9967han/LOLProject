import requests
import json
import time
import pandas as pd
import numpy as np
import utils

API_KEY = "RGAPI-24680870-7ece-4b42-9918-aa9dd19bcc87"

url_SummonerName = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}"
url_LeagueTier = "https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{}/{}?page={}"
url_SummonerChamp = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}"


class Request_Info:
    def __init__(self, method, param):
        self._method = method
        self._param = param
        self._headers = {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": API_KEY,
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    def get_SummonerName(self):
        url = url_SummonerName.format(self._param)
        res_SummonerName = requests.get(url = url, headers = self._headers)
        return res_SummonerName.json()

    def get_LeagueTier(self):
        url = url_LeagueTier.format(self._param[0], self._param[1], self._param[2])
        res_LeagueTier = requests.get(url = url, headers = self._headers)
        return res_LeagueTier.json()

    def get_SummonerChamp(self):
        url = url_SummonerChamp.format(self._param)
        res_SummonerChamp = requests.get(url = url, headers = self._headers)
        return res_SummonerChamp.json()


def init_data():
    utils.champion_info()
    utils.init_userInfo('UserInfo_GOLD4.json')


if __name__=="__main__":
    init_data()
    print("Step 0 : Get Summoners list by tier")
    param = ["GOLD", "IV", 1]
    request_info = Request_Info(method = "None", param = param)
    data = request_info.get_LeagueTier()

    summonerName_list = []
    for i in data:
        summonerName_list.append(i['summonerName'])
    summoner_puuid = {}
    summoner_encid = {}
    print("Step 1 : Get Summoers puuid...")
    for name in summonerName_list:
        data = Request_Info(method = "None", param = name)
        data_name = data.get_SummonerName()
        # sleep 100 for gather data properly
        time.sleep(1)
        if 'puuid' in data_name:
            summoner_puuid[name] = data_name['puuid']
            summoner_encid[name] = data_name['id']
        if len(summoner_puuid) >= 10:
            break
    
    print("Step 2 : Get Summoers info and store....")
    print(len(summonerName_list), len(summoner_puuid), len(summoner_encid))

    #UserInfo store filename 
    filename = "UserInfo_GOLD4.json"
    with open(filename, 'r') as f:
        file_data = json.load(f)
    
    summoner_Champ = {}
    cnt = 1
    for name in summoner_encid:
        encid = summoner_encid[name]
        puuid = summoner_puuid[name]
        print(encid, puuid)
        file_data["puuid"][cnt] = puuid
        file_data["encid"][cnt] = encid
        summonerChamp = Request_Info(method = "None", param = encid)
        summonerChamp_data = summonerChamp.get_SummonerChamp()
        for info in summonerChamp_data:
            champ_id = str(info["championId"])
            champ_points = info["championPoints"]
            #champ_level = info["championLevel"]
            file_data[champ_id][cnt] = champ_points
        
        for champ_id in file_data:
            if champ_id != "puuid" and champ_id != 'encid':
                if cnt not in file_data[champ_id]:
                    file_data[champ_id][cnt] = 0

        summoner_Champ[name] = summonerChamp_data
        time.sleep(1)
        cnt += 1
    
    with open(filename, 'w', encoding='utf-8') as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, indent='\t')

    Tiers = ["PLATINUM", "GOLD", "SILVER"]
    Ranks = ["I", "II", "III", "IV"]

    