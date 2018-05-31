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

exports.reset_spawn = async function() {
  if (osvar == "win32") {
    var python = spawn('python', [__dirname + "\\search.py"], {detached: true, cwd: __dirname});
  } else {
    var python = spawn('python', [__dirname + "/search.py"], {detached: true, cwd: __dirname});
  }
}

exports.search = async function(query, page, useID) {

  return new Promise(function(resolve, reject){
    python.stdout.on('data', async (chunk) => {
      console.log(results)
      results = chunk.toString().split(" ");
      json_res = results;
      resolve(json_res)
      // var data = ""
      // var results_num = (page - 1) * 10


  //     if (useID == true) {
  //       var input = [results[results_num]]
  //
  //       for (var i = results_num + 1; i <= results_num + 9; i++){
  //         input.push(results[i])
  //       }
  //       resolve(input)
  //
  //     } else {
  //
  //       var input = results[results_num] + " "
  //
  //       for (var i = results_num + 1; i <= results_num + 9; i++){
  //         input += results[i] + " "
  //       }
  //       await process_ID(input, useID)
  //         .then(function(result){
  //           resolve(result.toString())
  //         })
  //     }
    })
    python.stdin.write(query + os.EOL);
  //
  })

}



function process_ID(jobID) {
  if (osvar == "win32") {
    var python2 = spawn('python', [__dirname + '\\load_data_from_id.py'], {detached: true, cwd: __dirname});
  } else {
    var python2 = spawn('python', [__dirname + '/load_data_from_id.py'], {detached: true, cwd: __dirname});
  }
  return new Promise(function (resolve, reject){
    python2.stdout.on('data', async (chunk) =>{
      resolve(chunk)
    })
    python2.stderr.on("data", async (chunk) => {
      console.log(chunk.toString())
    })
    python2.stdin.write(jobID);
    python2.stdin.write(os.EOL);
    python2.stdin.end();
  })

}
