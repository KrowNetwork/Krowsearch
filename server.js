'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var cluster = require("cluster")
var utf8 = require('utf8');
var num_cpus = os.cpus().length;
var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;

var current_page = 1
var full_res = ""

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);

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
    var python = spawn('python', ['search.py'], {detached: true});
    var query = req.query.q;
    // current_page += 1;
    return new Promise(function(resolve, reject){

      python.stdout.on('data', async (chunk) => {
        chunk = chunk.toString().split("'").join('"');
        results = JSON.parse(chunk);
        json_res = results;
        // console.log(results);
        var data = ""
        var results_num = page * 10 - 1
        // console.log(results_num)
        var input = results[results_num.toString()] + " "
        for (var i = results_num - 1; i >= results_num - 10; i --){
          // console.log()
          input += results[i.toString()] + " "
        }
        // console.log(input)
         await process_ID(input)
          .then(function(result){
            resolve(result.toString(), json_res)
          })

        // console.log(data);
      })
      python.stdin.write(query);
      python.stdin.write(os.EOL);

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
    res.render("index", {results: null})
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
      res.render("index", {results: result})
      full_json = json_res
      // res.end()
    })

    


      return next()

  });
  app.listen(port, function (err) {
    if (err) {
      throw err
    }
    console.log(`Worker ${process.pid} started`);

  })
}
