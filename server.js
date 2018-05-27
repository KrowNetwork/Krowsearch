'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var cluster = require("cluster")
var utf8 = require('utf8');
var num_cpus = Math.floor(os.cpus().length / 2);

var express = require('express'),
  app = express(),
  port = process.env.PORT || 4200;

var current_page = 1
var full_res = ""
var python = spawn('python', ['search.py'], {detached: true});

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
  for (let i = 0; i < num_cpus; i++) {
    cluster.fork();
  }

} else {

  // app.engine('html', require('ejs').renderFile);
  app.set('view engine', 'ejs')
  app.use(bodyParser.urlencoded({ extended: false }))
  app.use(bodyParser.json());

  async function search(req, res, page, callback) {
    var query = req.query.q;
    // current_page += 1;
    return new Promise(function(resolve, reject){

      python.stdout.on('data', async (chunk) => {
        results = chunk.toString().split(" ");
        // results = JSON.parse(chunk)//JSON.stringify(chunk));
        // console.log("recieved results")
        // console.log(process)
        // log("recieved results for term \"" + query + "\"")

        // console.log(results)
        json_res = results;
        var data = ""
        var results_num = (page - 1) * 10
        // console.log(page)
        var input = results[results_num] + " "
        for (var i = results_num + 1; i <= results_num + 9; i++){
          // console.log()
          input += results[i] + " "
        }
        // console.log(input)
         await process_ID(input)
          .then(function(result){
            resolve(result.toString(), json_res)
            // log("processed results for term \"" + query + "\"")
          })

        // console.log(data);
      })
      // log("recieved search term \"" + query + "\"")
      python.stdin.write(query + os.EOL);
      // python.stdin.write(os.EOL);

    })

  }



  function process_ID(jobID) {
    // var send = results[i.toString()]
    var python2 = spawn('python', ['load_data_from_id.py']);
    return new Promise(function (resolve, reject){
      python2.stdout.on('data', async (chunk) =>{
        resolve(chunk)
      })
      python2.stdin.write(jobID);
      python2.stdin.write(os.EOL);
      python2.stdin.end();
    })

    // console.log(jobID)



  }

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
    await search(req, res, page)
    .then(function (result, json_res){
      result = utf8.encode(result)
      res.render("index", {results: result, term: req.query.q})
      full_json = json_res
      res.end();
      res = null;
      req = null;
    })




      return next()

  });
  app.listen(port, function (err) {
    if (err) {
      throw err
    }
    console.log(`worker ${process.pid} started`);

  })
}
