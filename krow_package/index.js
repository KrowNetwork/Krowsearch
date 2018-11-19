'use_strict'
var spawn = require("child_process").spawn;
var execFile  = require("child_process").execFileSync ;
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

exports.search = async function(query, location, sort) {

  return new Promise(function(resolve, reject){
    python.stdout.on('data', async (chunk) => {

      results = chunk
      // console.log(chunk)

      await process_ID(results)
        .then(function (result){
          console.log(result)
          resolve(result)
        });
    })
    
        python.stdin.write(query + os.EOL);
    
  })

}

exports.reset = async function() {
  if (osvar == "win32") {
    var python = spawn('python', [__dirname + "\\search.py"], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
  } else {
    var python = spawn('python', [__dirname + "/search.py"], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
  }
  
//   if (osvar == "win32") {
//     var python2 = spawn('python', [__dirname + '\\get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
//   } else {
//     var python2 = spawn('python', [__dirname + '/get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
//   }
}



function process_ID(jobID) {
  return new Promise(function (resolve, reject){
    arr = []
    jobID = jobID.toString().split('|').forEach(element => {
      arr.push(element.split(", "))
    });
    var obj = {}
    var c = 0
    console.log(arr)
    arr.forEach(element => {
      obj[c] = {
        "name": element[0],
        "id": element[1]
      }
      c += 1
    })
    console.log(obj)
    resolve(obj)
  })
  
  // return new Promise(function (resolve, reject){
  //   python2.stdout.on('data', async (chunk) =>{
  //     ret = {}
  //     // console.log(chunk)
  //     chunk = chunk.toString().split("~+/=")
  //     for (var i = 0; i < 10; i++){
  //       ret[i.toString()] = chunk[i]
  //     }
  //     resolve(ret)
  //   })
  //   python2.stderr.on("data", async (chunk) => {
  //     reject(chunk.toString())
  //   })
  //   if (new Date().getMinutes() == 30) {
  //     python2.stdin.write(jobID + os.EOL);
  //   } else {
  //     python2.stdin.write(jobID + os.EOL);
  //   }
  //   python2.stdout.write('\033c');

  // })

}

// exports.reset = function() {
//   console.log("process.py")
//   if (osvar == "win32") {
//     execFile('python', [__dirname + "\\process.py"], {cwd: __dirname}, (error, stdout, stderr) => {
//       if (error) {
//         console.error('process.py - stderr', stderr);
//         throw error;
//     }
//       console.log('process.py - complete');
//     });
     
//   } else {
//     execFile('python', [__dirname + "/process.py"], {cwd: __dirname}, (error, stdout, stderr) => {
//       if (error) {
//         console.error('process.py - stderr', stderr);
//         throw error;
//     }
//       console.log('process.py - complete');
//     });
//   }

//   console.log("create_w2v.py")
//   if (osvar == "win32") {
//     execFile('python', [__dirname + "\\create_w2v.py"], {cwd: __dirname}, (error, stdout, stderr) => {
//       if (error) {
//         console.error('create_w2v.py - stderr', stderr);
//         throw error;
//     }
//       console.log('create_w2v.py - complete');
//     });
     
//   } else {
//     execFile('python', [__dirname + "/create_w2v.py"], {cwd: __dirname}, (error, stdout, stderr) => {
//       if (error) {
//         console.error('create_w2v.py - stderr', stderr);
//         throw error;
//     }
//       console.log('create_w2v.py - complete');
//     });
//   }
//   console.log("search.py")
//   if (osvar == "win32") {
//     python = spawn('python', [__dirname + "\\search.py"], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
//   } else {
//     python = spawn('python', [__dirname + "/search.py"], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
//   }

//   console.log("get_data.py")
//   if (osvar == "win32") {
//     python2 = spawn('python', [__dirname + '\\get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
//   } else {
//     python2 = spawn('python', [__dirname + '/get_data.py'], {detached: true, cwd: __dirname, maxBuffer: 1024 * 200});
//   }

//   console.log("done")
// }
