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

var API_KEY = "42fc1e42-5eb8-4a8f-8904-7c58529f0f58";

var current_page = 1
var full_res = ""
// var python = spawn('python', ['search.py'], {detached: true});

function log(message) {
  var date = new Date(Date.now()).toLocaleString({timeZone: "America/New_York"});
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
    res.render("index", {results: null, term: null, resTime: null})
  });

  app.get("/search", async (req, res, next) => {
    // res.writeHead(200,{"Content-Type" : "text/html"});
    var query = req.body.term;
    var key = req.query.key;
    if (key != API_KEY) {
      res.send("invalid api key")
    } else {
      // q = query.split(" ").join("+")
      // if (q.substring(q.length - 1) == "+") {
      //   q = q.substring(0, q.length - 1)
      // }
      // log("connection at /search?q=" + q)

        // page = 1
      var useID = true
      var start = Date.now()

// TODO: remove page

      await krow.search(query, 1, useID)
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
        // res.render("index", {results: result, term: req.query.q, resTime: t})
        //console.timeEnd('render')
        // full_json = json_res
        res.send(results);
        // res = null;
        // req = null;

        return next()
    });
    }
    // var page = req.query.page;


})
  app.listen(port, function (err) {
    if (err) {
      throw err
    }
    console.log(`worker ${process.pid} started`);

  })
}
