'use_strict'
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var utf8 = require('utf8');

var osvar = process.platform;
if (osvar == "win32") {
  var python = spawn('python', [__dirname + "\\search.py"], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
} else {
  var python = spawn('python', [__dirname + "/search.py"], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
}

if (osvar == "win32") {
  var python2 = spawn('python', [__dirname + '\\get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
} else {
  var python2 = spawn('python', [__dirname + '/get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
}

exports.reset_spawn = async function() {
  if (osvar == "win32") {
    var python2 = spawn('python', [__dirname + '\\get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
  } else {
    var python2 = spawn('python', [__dirname + '/get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
  }
}

exports.search = async function(query) {

  return new Promise(function(resolve, reject){
    python.stdout.on('data', async (chunk) => {

      results = chunk

      await process_ID(results)
        .then(function (result){
          resolve(result)
        });
    })
    python.stdin.write(query + os.EOL);
  })

}



function process_ID(jobID) {

  return new Promise(function (resolve, reject){
    python2.stdout.on('data', async (chunk) =>{
      if (osvar == "win32") {
        chunk = chunk.toString().substring(0, chunk.length - 4)
      } else {
        chunk = chunk.toString().substring(0, chunk.length)
      } 
      // console.log(chunk.toString())
      resolve(chunk)
    })
    python2.stderr.on("data", async (chunk) => {
      reject(chunk.toString())
    })
    python2.stdin.write(jobID + os.EOL);

  })

}
