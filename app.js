// nodemon app.js로 서버 실행
var express = require("express");
var axios = require("axios");
var urlencode = require("urlencode");
const api_key = ""; // 여기에 key 입력

var app = express(); // express 함수 실행
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
  console.log("id2 : " + req.query.id2);
  res.sendFile(__dirname + "/public/form.html");
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
  );
  const summoner1ChampionMastery = await axios.get(
    "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
      summoner1.id +
      "?api_key=" +
      api_key
  );
  const summoner2ChampionMastery = await axios.get(
    "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
      summoner2.id +
      "?api_key=" +
      api_key
  );
  const summoner3ChampionMastery = await axios.get(
    "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
      summoner3.id +
      "?api_key=" +
      api_key
  );
  const summoner4championMastery = await axios.get(
    "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
      summoner4.id +
      "?api_key=" +
      api_key
  );
  const summoner5ChampionMastery = await axios.get(
    "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" +
      summoner5.id +
      "?api_key=" +
      api_key
  );
  const { data: summoner1MatchList } = await axios.get(
    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
      summoner1.puuid +
      "/ids" +
      "?api_key=" +
      api_key
  );
  const { data: summoner2MatchList } = await axios.get(
    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
      summoner2.puuid +
      "/ids" +
      "?api_key=" +
      api_key
  );
  const { data: summoner3MatchList } = await axios.get(
    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
      summoner3.puuid +
      "/ids" +
      "?api_key=" +
      api_key
  );
  const { data: summoner4MatchList } = await axios.get(
    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
      summoner4.puuid +
      "/ids" +
      "?api_key=" +
      api_key
  );
  const { data: summoner5MatchList } = await axios.get(
    "https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/" +
      summoner5.puuid +
      "/ids" +
      "?api_key=" +
      api_key
  );
});
