'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');

var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;

// var routes = require('./routes.js'); //importing route
// routes(app);
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json());

app.get("/search", function(req, res) {
  var python = spawn('python', ['search.py']);

  let body = req.body.data;
  console.log(body);

  let ret = "Fail"
  let results = "";
  // fs.writeFile("data.txt", body, function(err) {
  //   console.log("The file was saved!");
  // });
  python.stdin.on('data', function(data){
    ret += data.toString();
  });
  python.stdout.on('data', function(chunk){
    chunk = chunk.toString().split("'").join('"');
    results = JSON.parse(chunk);
    res.send(results)
  });
  python.on('exit', function(code){
    console.log("Process quit with code : " + code);
  });

  python.stdin.write(body);
  python.stdin.end();
  // console.log(ret);
  // console.log(results);

})

app.listen(port, function (err) {
  if (err) {
    throw err
  }
  console.log('Server started on port 3000')
})
