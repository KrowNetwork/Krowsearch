'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var cluster = require("cluster")
var utf8 = require('utf8');
var num_cpus = Math.floor(os.cpus().length / 2);
var events = require('events');
var eventEmitter = new events.EventEmitter();
eventEmitter.setMaxListeners(1000)
var osvar = process.platform;
// emitter.setMaxListeners(20)

// if (osvar != "win32") {
//   cluster.schedulingPolicy = cluster.SCHED_RR
// }
var krow = require("krow_package/index.js")

var API_KEY = "42fc1e42-5eb8-4a8f-8904-7c58529f0f58";

var KEYS = {
  "42fc1e42-5eb8-4a8f-8904-7c58529f0f58": "nik/frontend",
  "dgf463d4-4fg5-55la-3z0f-7c78ft9s9z64": "tucker"
}                                    

var current_page = 1
var full_res = ""

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


  app.set('view engine', 'ejs')
  app.use(bodyParser.urlencoded({ extended: false }))
  app.use(bodyParser.json());
  app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header("Content-Length", "262144");
    next();
  });

  app.get("/search", async (req, res, next) => {

    var query = req.query.term;
    var key = req.query.key;

    if (KEYS[key] === undefined) {
      throw new Error("API Key " + key + " is invalid. Contact Tucker to clear the issue")
      res.end()
    } else {
      log(key + "[" + KEYS[key] + "]: " + query)
      await krow.search(query)

      .then(function (result){
        // console.log(result.toString())
        res.header("Content-Length", result.toString().length*2+'')
        res.write(result)//.toString().trim());
        res.end()
        return next()
    });

    }


})
  app.listen(port, function (err) {
    if (err) {
      throw err
    }
    console.log(`worker ${process.pid} started`);

  })
}
