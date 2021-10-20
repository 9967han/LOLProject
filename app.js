// nodemon app.js로 서버 실행
var express = require("express");
var axios = require("axios");
var urlencode = require("urlencode");
var PythonShell = require('python-shell');
const ejs = require("ejs");
const api_key = ""; // 여기에 key 입력

var app = express(); // express 함수 실행
app.set("view engine", "ejs");

app.listen(3000, function () {
  // 3000포트로 실행하고 대기, 비동기로 인해 나중에 실행됨
  console.log("start! express server port 3000");
});

//url : / route to main.html
app.get("/", function (req, res) {
  res.sendFile(__dirname + "/public/main.html");
});

//url : /main route to main.html
app.get("/main", function (req, res) {
  res.sendFile(__dirname + "/public/main.html");
});

//static file(.js) routing : public 디렉터리 내 파일들은 static으로 요청시 내려받을 수 있음.
app.use(express.static("public"));

app.get("/search", async (req, res) => {
  // console.log("id2 : " + req.query.id2);
  // res.sendFile(__dirname + "/public/form.html");
  const sleep = (ms) => {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    });
  };
  try {
    const { data: summoner1 } = await axios.get(
      "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        urlencode(req.query.id1) +
        "?api_key=" +
        api_key
    );
    const { data: summoner2 } = await axios.get(
      "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        urlencode(req.query.id2) +
        "?api_key=" +
        api_key
    );
    const { data: summoner3 } = await axios.get(
      "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        urlencode(req.query.id3) +
        "?api_key=" +
        api_key
    );
    const { data: summoner4 } = await axios.get(
      "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        urlencode(req.query.id4) +
        "?api_key=" +
        api_key
    );
    const { data: summoner5 } = await axios.get(
      "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        urlencode(req.query.id5) +
        "?api_key=" +
        api_key
    );/*
    const summoner1ChampionMastery = await axios.get(
      "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
        urlencode(summoner1.id) +
        "?api_key=" +
        api_key
    );
    const summoner2ChampionMastery = await axios.get(
      "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
        urlencode(summoner2.id) +
        "?api_key=" +
        api_key
    );
    const summoner3ChampionMastery = await axios.get(
      "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
        urlencode(summoner3.id) +
        "?api_key=" +
        api_key
    );
    const summoner4championMastery = await axios.get(
      "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
        urlencode(summoner4.id) +
        "?api_key=" +
        api_key
    );
    const summoner5ChampionMastery = await axios.get(
      "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
        urlencode(summoner5.id) +
        "?api_key=" +
        api_key
    );*/
    await sleep(1000);
    const { data: summoner1MatchList } = await axios.get(
      "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        urlencode(summoner1.puuid) +
        "/ids?start=0&count=10" +
        "&api_key=" +
        api_key
    );
    const { data: summoner2MatchList } = await axios.get(
      "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        urlencode(summoner2.puuid) +
        "/ids?start=0&count=10" +
        "&api_key=" +
        api_key
    );

    const { data: summoner3MatchList } = await axios.get(
      "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        urlencode(summoner3.puuid) +
        "/ids?start=0&count=10" +
        "&api_key=" +
        api_key
    );
    const { data: summoner4MatchList } = await axios.get(
      "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        urlencode(summoner4.puuid) +
        "/ids?start=0&count=10" +
        "&api_key=" +
        api_key
    );
    const { data: summoner5MatchList } = await axios.get(
      "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        urlencode(summoner5.puuid) +
        "/ids?start=0&count=10" +
        "&api_key=" +
        api_key
    );
    await sleep(1000);
    const summoner1Match = [], summoner2Match = [], summoner3Match = [], summoner4Match = [], summoner5Match = [];
    const player1Data = Array.from({length:16}, ()=>0);
    const player2Data = Array.from({length:16}, ()=>0);
    const player3Data = Array.from({length:16}, ()=>0);
    const player4Data = Array.from({length:16}, ()=>0);
    const player5Data = Array.from({length:16}, ()=>0);

    async function makeSummonerMatch() {
      for (const matchId of summoner1MatchList) {
        let { data: result } = await axios.get(
          "https://asia.api.riotgames.com/lol/match/v5/matches/" +
            urlencode(matchId) +
            "?api_key=" +
            api_key
        );
        if (result.info.queueId == 420 || result.info.queueId == 440) {
          resultIdx = result.metadata.participants.indexOf(summoner1.puuid);
          result = result.info.participants[resultIdx];
          summoner1Match.push(result);
        }
      }
      await sleep(1000);
      for (const matchId of summoner2MatchList) {
        let { data: result } = await axios.get(
          "https://asia.api.riotgames.com/lol/match/v5/matches/" +
            urlencode(matchId) +
            "?api_key=" +
            api_key
        );
        if (result.info.queueId == 420 || result.info.queueId == 440) {
          resultIdx = result.metadata.participants.indexOf(summoner2.puuid);
          result = result.info.participants[resultIdx];
          summoner2Match.push(result);
        }
      }
      await sleep(2000);
      for (const matchId of summoner3MatchList) {
        let { data: result } = await axios.get(
          "https://asia.api.riotgames.com/lol/match/v5/matches/" +
            urlencode(matchId) +
            "?api_key=" +
            api_key
        );
        if (result.info.queueId == 420 || result.info.queueId == 440) {
          resultIdx = result.metadata.participants.indexOf(summoner3.puuid);
          result = result.info.participants[resultIdx];
          summoner3Match.push(result);
        }
      }
      await sleep(1000);
      for (const matchId of summoner4MatchList) {
        let { data: result } = await axios.get(
          "https://asia.api.riotgames.com/lol/match/v5/matches/" +
            urlencode(matchId) +
            "?api_key=" +
            api_key
        );
        if (result.info.queueId == 420 || result.info.queueId == 440) {
          resultIdx = result.metadata.participants.indexOf(summoner4.puuid);
          result = result.info.participants[resultIdx];
          summoner4Match.push(result);
        }
      }
      await sleep(1000);
      for (const matchId of summoner5MatchList) {
        let { data: result } = await axios.get(
          "https://asia.api.riotgames.com/lol/match/v5/matches/" +
            urlencode(matchId) +
            "?api_key=" +
            api_key
        );
        if (result.info.queueId == 420 || result.info.queueId == 440) {
          resultIdx = result.metadata.participants.indexOf(summoner5.puuid);
          result = result.info.participants[resultIdx];
          summoner5Match.push(result);
        }
      }
    }
    await makeSummonerMatch();

    var infoArr = ["largestKillingSpree", "goldEarned", "timePlayed", "assists", "deaths", "kills", "detectorWardsPlaced", "killingSprees", "wardsKilled", "wardsPlaced", "visionScore", "totalDamageDealtToChampions", "totalDamageTaken", "totalMinionsKilled", "neutralMinionsKilled"];
    var player1Idx = 0, player2Idx = 0, player3Idx = 0, player4Idx = 0, player5Idx = 0;
    var player1Cnt = 0, player2Cnt = 0, player3Cnt = 0, player4Cnt = 0, player5Cnt = 0;
    for(var match of summoner1Match){
      player1Idx = 0;
      player1Cnt++;
      for(var info of infoArr){
        player1Data[player1Idx++] += parseInt(match[info]);
      }
    }
    for(var match of summoner2Match){
      player2Idx = 0;
      player2Cnt++;
      for(var info of infoArr){
        player2Data[player2Idx++] += parseInt(match[info]);
      }
    }
    for(var match of summoner3Match){
      player3Idx = 0;
      player3Cnt++;
      for(var info of infoArr){
        player3Data[player3Idx++] += parseInt(match[info]);
      }
    }
    for(var match of summoner4Match){
      player4Idx = 0;
      player4Cnt++;
      for(var info of infoArr){
        player4Data[player4Idx++] += parseInt(match[info]);
      }
    }
    for(var match of summoner5Match){
      player5Idx = 0;
      player5Cnt++;
      for(var info of infoArr){
        player5Data[player5Idx++] += parseInt(match[info]);
      }
    }
    console.log(player2Data)
    for(var i=0; i<infoArr.length; i++){
      player1Data[i] /= player1Cnt;
      player2Data[i] /= player2Cnt;
      player3Data[i] /= player3Cnt;
      player4Data[i] /= player4Cnt;
      player5Data[i] /= player5Cnt;
    }

    var options = {
      mode: 'text',
      pythonPath: '',
      pythonOptions: ['-u'],
      scriptPath: '',
      args: [player1Data, player2Data, player3Data, player4Data, player5Data]
    };

    PythonShell.PythonShell.run('predict.py', options, function (err, results) {
      if (err) throw err;
      console.log('results: %j', results);
      const data = {
        id1: req.query.id1,
        id2: req.query.id2,
        id3: req.query.id3,
        id4: req.query.id4,
        id5: req.query.id5,
        result: results
      };
      res.render("form.ejs", data);
    });

  } catch (error) {
    console.log(error);
  }
});