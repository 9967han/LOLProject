// nodemon app.js로 서버 실행
var express = require('express')
var axios = require('axios');
var urlencode = require('urlencode')
const api_key = "" // 여기에 key 입력

var app = express() // express 함수 실행
app.listen(3000, function(){ 
    // 3000포트로 실행하고 대기, 비동기로 인해 나중에 실행됨
    console.log("start! express server port 3000")
});

//url : / route to main.html
app.get('/', function(req, res){
    res.sendFile(__dirname + "/public/main.html")
});

//url : /main route to main.html
app.get('/main', function(req, res){
    res.sendFile(__dirname + "/public/main.html")
});

//static file(.js) routing : public 디렉터리 내 파일들은 static으로 요청시 내려받을 수 있음.
app.use(express.static("public"))

/*app.post('/search', function(req, res){
    res.sendFile(__dirname + "/public/main.html")
});*/

app.get('/search',  async (req, res) => {
    console.log("id1 : " + req.query.id1)
    res.sendFile(__dirname + "/public/main.html")
    const { data } = await axios.get("https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + urlencode(req.query.id1) + "?api_key=" + api_key)
    console.log(data)
})

