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
  cluster.schedulingPolicy = cluster.SCHED_RR
}

var current_page = 1
var full_res = ""
// var python = spawn('python', ['search.py'], {detached: true});

function log(message) {
  var date = new Date(Date.now()).toLocaleString();
  console.log(date.toString() + " - worker " + process.pid + ": " + message)
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
  for (let i = 0; i < num_cpus; i++) {
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
    log("connection at /")
    // res.render("index", {results: null, term: null, resTime: null})
    res.send("test")
  });
  app.get("/search", async (req, res, next) => {
    // res.writeHead(200,{"Content-Type" : "text/html"});
    var page = req.query.page;
    if (page === undefined) {
      page = 1
    }
    q = req.query.q.split(" ").join("+")
    if (q.substring(q.length - 1) == "+") {
      q = q.substring(0, q.length - 1)
    }
    log("connection at /search?q=" + q)

      // page = 1
    var useID = false
    var start = Date.now()
    await krow.search(req.query.q, page, useID)
    .then(function (result){
      // console.log(result)
      //console.time("encode time")
      if (!useID) {
        result = utf8.encode(result)
      } else {
        result = result.toString()
      }
      //console.timeEnd("encode time")
      // console.log("x")
      //console.time("render")
      var t = Date.now() - start
      res.render("index", {results: result, term: req.query.q, resTime: t})
      //console.timeEnd('render')
      // full_json = json_res
      res.end();
      // res = null;
      // req = null;
      return next()

    })
    // console.log(process.pid)
    // console.timeEnd("run time")
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
