'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');

var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;
app.engine('html', require('ejs').renderFile);


app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json());

// app.get("/search", function(req, res){
//   res.render("index.html")
// })

app.get("/", function(req, res) {
  res.render("index.html")
});

app.get("/search", function(req, res) {
  var python = spawn('python', ['search.py']);
  var body = req.query.q;
  var ret = "Fail"
  var results = "";
  console.log(body);
  python.stdout.on('data', function(chunk){
    chunk = chunk.toString().split("'").join('"');
    results = JSON.parse(chunk);
    var returns = ""
    for (var i = 0; i < 10; i ++) {
      var send = results[i.toString()]
      var python2 = spawn('python', ['load_data_from_id.py']);
      python2.stdout.on('data', function(chunk){
        res.write("<p>")
        res.write(chunk.toString())
        res.write("</p>")
      });
      python2.stdin.write(send);
      python2.stdin.end();
    }

  });
  python.on('exit', function(code){
    console.log("Process quit with code : " + code);
  });

  python.stdin.write(body);
  python.stdin.end();

});

app.listen(port, function (err) {
  if (err) {
    throw err
  }
  console.log('Server started on port 3000')
})
