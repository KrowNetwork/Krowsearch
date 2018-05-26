'use_strict'
var bodyParser = require('body-parser');
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var cluster = require("cluster")

var num_cpus = os.cpus().length;

var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000;

if (cluster.isMaster) {
  console.log(`Master ${process.pid} is running`);

  // Fork workers.
  for (let i = 0; i < num_cpus; i++) {
    cluster.fork();
  }

} else {

  app.engine('html', require('ejs').renderFile);
  app.use(bodyParser.urlencoded({ extended: false }))
  app.use(bodyParser.json());

  async function search(req, res, callback) {
    var python = spawn('python', ['search.py'], {detached: true});
    var query = req.query.q;
    return new Promise(function(resolve, reject){

      python.stdout.on('data', async (chunk) => {
        chunk = chunk.toString().split("'").join('"');
        results = JSON.parse(chunk);
        // console.log(results);
        var data = ""
        var input = results["10"] + " "
        for (var i = 9; i >= 0; i --){
          // console.log()
          input += results[i.toString()] + " "
        }
        // console.log(input)
         await process_ID(input)
          .then(function(result){
            resolve(result.toString())
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
    res.render("index.html")
  });
  app.get("/search", async (req, res, next) => {
    res.writeHead(200,{"Content-Type" : "text/html"});
    await search(req, res)
      .then(function (result){
        res.write(result)
        res.end()
      })
      return next()


    // res.end()



  });
  app.listen(port, function (err) {
    if (err) {
      throw err
    }
    console.log(`Worker ${process.pid} started`);

  })
}
