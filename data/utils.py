import json
import requests

# Get Champoon INFO and store it
def champion_info():
    data = requests.get("http://ddragon.leagueoflegends.com/cdn/11.18.1/data/en_US/champion.json")
    data = data.text
    data = json.loads(data)
    data = data.get('data')
    
    write_data = {}
    for champ in data:
        parsed_data = {}
        champ_data = data[champ]
        parsed_data['championName'] = champ_data['id']
        parsed_data['championId'] = champ_data['key']
        parsed_data['championImage'] = champ_data['image']
        write_data[champ] = parsed_data
    with open('champion_data.json', 'w', encoding='utf-8') as make_file:
        json.dump(write_data, make_file, ensure_ascii=False, indent='\t')
    return write_data


# INIT User INFO data file by given filename
# Used before get User data by Tier
def init_userInfo(filename):
    write_data = {}
    write_data['puuid'] = {}
    write_data['encid'] = {}
    
    with open('champion_data.json', 'r') as f:
        champInfo = json.load(f)
    for champ in champInfo:
        data = champInfo[champ]
        write_data[data['championId']] = {}
    
    with open(filename, 'w', encoding='utf-8') as make_file:
        json.dump(write_data, make_file, ensure_ascii=False, indent='\t')

    return write_data


def init_matchInfo(filename):
    write_data = {}
    write_data['puuid'] = {}
    write_data['encid'] = {}
    store_data_type = ["largetsKillingSpree", "goldEarned", "timePlayed", "assists", "deaths", "kills", "detectorWardsPlaced", "killingSprees", "wardsKilled", "wardsPlaced", "win", "visionScore", "totalDamageDealtToChampions", "totalDamageTaken", "totalMinionsKilled", "neutralMinionsKilled", "lane"]
    for i in store_data_type:
        write_data[i] = {}

    with open(filename, 'w', encoding='utf-8') as make_file:
        json.dump(write_data, make_file, ensure_ascii=False, indent='\t')

    return write_data