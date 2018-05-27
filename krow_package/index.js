'use_strict'
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var utf8 = require('utf8');

var osvar = process.platform;
if (osvar == "win32") {
  var python = spawn('python', [__dirname + "\\search.py"], {detached: true, cwd: __dirname});
} else {
  var python = spawn('python', [__dirname + "/search.py"], {detached: true, cwd: __dirname});
}

// app.engine('html', require('ejs').renderFile);
// console.log(__dirname + '\\search.py')
exports.search = async function(query, page) {
  // console.log(query)
  // current_page += 1;
  return new Promise(function(resolve, reject){
    python.stdout.on('data', async (chunk) => {
      // console.log("ici")
      results = chunk.toString().split(" ");
      json_res = results;
      var data = ""
      var results_num = (page - 1) * 10
      // console.log(page)
      var input = results[results_num] + " "
      //console.time("loop")
      for (var i = results_num + 1; i <= results_num + 9; i++){
        // console.log()
        input += results[i] + " "
      }
      //console.timeEnd("loop")

      // console.log(input)
      //console.time("process")
      await process_ID(input)
        .then(function(result){
          // console.log(result)
          // python = spawn('python', [__dirname + "\\search.py"], {detached: true, cwd: __dirname});
          resolve(result.toString())
        })
        //console.timeEnd("process")
    })
    //console.time("write")
    python.stdin.write(query + os.EOL);
    //console.timeEnd("write")
  })

}



function process_ID(jobID) {
  // var send = results[i.toString()]
  //console.time('spawn')
  var python2 = spawn('python', [__dirname + '\\load_data_from_id.py'], {detached: true, cwd: __dirname});
  //console.timeEnd('spawn')
  return new Promise(function (resolve, reject){
    python2.stdout.on('data', async (chunk) =>{
      // console.log("here")
      resolve(chunk)
    })
    python2.stderr.on("data", async (chunk) => {
      console.log(chunk.toString())
    })
    python2.stdin.write(jobID);
    python2.stdin.write(os.EOL);
    python2.stdin.end();
  })

  // console.log(jobID)



}
// await search(req, res, page)
// .then(function (result, json_res){
//   result = utf8.encode(result)
//   res.render("index", {results: result, term: req.query.q})
//   full_json = json_res
//   res.end();
//   res = null;
//   req = null;
// })
