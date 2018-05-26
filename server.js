'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")

var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;
app.engine('html', require('ejs').renderFile);
app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json());

var python = spawn('python', ['search.py']);


// app.get("/search", function(req, res){
//   res.render("index.html")
// })

app.get("/", function(req, res, next) {
  res.render("index.html")
});
app.get("/search", function(req, res) {
  res.writeHead(200,{"Content-Type" : "text/html"});
  var body = req.query.q;
  var ret = ""
  var results = "";
  console.log(body);
  python.stdout.on('data', function(chunk){
    chunk = chunk.toString().split("'").join('"');
    results = JSON.parse(chunk);
    var returns = ""
    // res.write("<form method=\"get\" action=\"/\">")
    // res.write("<input type=\"submit\" value=\"Search\" class=\"submitButton\">")
    // res.write("</form>")
    res.write('<script type="text/javascript"></script>'+
      '<form method="get" action="/search">'+
      '<input class="q tt-query" spellcheck="false" autocomplete="off" name="q" type="text" />'+
      '<input type="submit" value="Search" class="submitButton">'+
     '</form>')
    // res.write("<form></form>")

    for (var i = 0; i < 10; i ++) {
      var send = results[i.toString()]
      var python2 = spawn('python', ['load_data_from_id.py']);
      python2.stdout.on('data', function(chunk){
        // ret += "<p>\n"
        // ret += chunk.toString()
        // ret += "</p>\n"
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
  python.stdin.write(os.EOL);
  // console.log(ret);
  // res.end();
  // return false
});
app.listen(port, function (err) {
  if (err) {
    throw err
  }
  console.log('Server started on port 3000')
})
