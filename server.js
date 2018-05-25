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

app.post("/search", function(req, res) {
  let body = req.body.data;
  console.log(body);
  res.send("search term: ${body}")
  let ret = "Fail"
  // fs.writeFile("data.txt", body, function(err) {
  //   console.log("The file was saved!");
  // });
  var python = spawn('python', ['search.py']);
  python.stdin.on('data', function(data){
    ret += data.toString();
  });
  python.stdout.on('data', function(chunk){
    var chunk = chunk.toString('utf8');
    console.log(chunk);
  });
  python.on('exit', function(code){
    console.log("Process quit with code : " + code);
  });

  python.stdin.write(body);
  python.stdin.end();
  // console.log(ret);

})

app.listen(port, function (err) {
  if (err) {
    throw err
  }
  console.log('Server started on port 3000')
})
