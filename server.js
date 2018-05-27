'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var cluster = require("cluster")
var utf8 = require('utf8');
var num_cpus = Math.floor(os.cpus().length / 2);

var osvar = process.platform;
if (osvar != "win32") {
  cluster.schedulingPolicy = 'rr'
}

var current_page = 1
var full_res = ""
// var python = spawn('python', ['search.py'], {detached: true});

function log(message) {
  console.log("worker " + process.pid + ": " + message)
}

if (cluster.isMaster) {
  console.log(`master ${process.pid} is running`);

  if (num_cpus < 4) {
    console.warn("worker count too low, attempting to increase worker count")
    if (os.cpus().length >= 4) {
      num_cpus = 4
    } else {
      num_cpus = os.cpus().length
    }
  }
  // Fork workers.
  for (let i = 0; i < 4; i++) {
    cluster.fork();
  }

} else {

  var express = require('express'),
    app = express(),
    port = process.env.PORT || 4200;

  var krow = require("krow_package/index.js")

  // app.engine('html', require('ejs').renderFile);
  app.set('view engine', 'ejs')
  app.use(bodyParser.urlencoded({ extended: false }))
  app.use(bodyParser.json());


  app.get("/", function(req, res) {
    log("new connection at /")
    res.render("index", {results: null, term: null})
  });
  app.get("/search", async (req, res, next) => {
    // res.writeHead(200,{"Content-Type" : "text/html"});
    var page = req.query.page;
    if (page === undefined) {
      page = 1
    }

      // page = 1
    console.time("run time");
    await krow.search(req.query.q, page)
    .then(function (result){
      // console.log(result)
      //console.time("encode time")
      result = utf8.encode(result)
      //console.timeEnd("encode time")
      // console.log("x")
      //console.time("render")
      res.render("index", {results: result, term: req.query.q})
      //console.timeEnd('render')
      // full_json = json_res
      res.end();
      // res = null;
      // req = null;
      return next()

    })
    console.log(process.pid)
    console.timeEnd("run time")
    // console.log(process.memoryUsage())

      // return next()

  });
  app.listen(port, function (err) {
    if (err) {
      throw err
    }
    console.log(`worker ${process.pid} started`);

  })
}
