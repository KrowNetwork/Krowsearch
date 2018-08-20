'use_strict'
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var utf8 = require('utf8');

var events = require('events');
var eventEmitter = new events.EventEmitter();
eventEmitter.setMaxListeners(1000)

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

exports.search = async function(query, location, sort) {

  return new Promise(function(resolve, reject){
    python.stdout.on('data', async (chunk) => {

      results = chunk

      await process_ID(results)
        .then(function (result){
          resolve(result)
        });
    })
    if (sort == "relevance" || sort === undefined) {
      var date = new Date();
      if (date.getMinutes() == 30) {
        python.stdin.write("\"" + query +  "\"" + " \"" + location + "\" " + "\"relevance\"" + "\"reset\"" + os.EOL);
      } else {
        python.stdin.write("\"" + query +  "\"" + " \"" + location + "\" " + "\"relevance\"" + os.EOL);
      }
      console.log("\"" + query +  "\"" + " \"" + location + "\" " + "\"relevance\"" + os.EOL)
      python.stdout.write('\033c');
    }
    else {
      python.stdin.write("\"" + query +  "\"" + " \"" + location + "\" " + "\"" + sort + "\"" + os.EOL);
      python.stdout.write('\033c');
    }
    
  })

}



function process_ID(jobID) {

  return new Promise(function (resolve, reject){
    python2.stdout.on('data', async (chunk) =>{
      ret = {}
      chunk = chunk.toString().split("~+/=")
      for (var i = 0; i < 10; i++){
        ret[i.toString()] = chunk[i]
      }
      resolve(ret)
    })
    python2.stderr.on("data", async (chunk) => {
      reject(chunk.toString())
    })
    if (new Date().getMinutes() == 30) {
      python2.stdin.write('"' + jobID + '"' + ' "reset"' + os.EOL);
    } else {
      python2.stdin.write('"' + jobID + '"' + os.EOL);
    }
    python2.stdout.write('\033c');

  })

}
