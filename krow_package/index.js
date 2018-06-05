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

if (osvar == "win32") {
  var python2 = spawn('python', [__dirname + '\\get_data.py'], {detached: true, cwd: __dirname});
} else {
  var python2 = spawn('python', [__dirname + '/get_data.py'], {detached: true, cwd: __dirname});
}

exports.reset_spawn = async function() {
  if (osvar == "win32") {
    var python = spawn('python', [__dirname + "\\search.py"], {detached: true, cwd: __dirname});
  } else {
    var python = spawn('python', [__dirname + "/search.py"], {detached: true, cwd: __dirname});
  }
}

exports.search = async function(query) {

  return new Promise(function(resolve, reject){
    python.stdout.on('data', async (chunk) => {
      // console.log(chunk.toString())
      // results = JSON.parse(chunk.toString().split("'").join('"'));
      results = chunk
      // json_res = results;
      arr = []
      // console.log(json_res)
      // console.log(json_res['0'])
      // console.time("t")
      await process_ID(results)
        .then(function (result){
          // console.timeEnd("t")

          resolve(result)
        });
      // console.log(arr)

    })
    python.stdin.write(query + os.EOL);
  //
  })

}



function process_ID(jobID) {

  return new Promise(function (resolve, reject){
    python2.stdout.on('data', async (chunk) =>{
      resolve(chunk)
    })
    python2.stderr.on("data", async (chunk) => {
      console.log(chunk.toString())
    })
    python2.stdin.write(jobID + os.EOL);
    // python2.stdin.write();
    // python2.stdin.end();
  })

}
