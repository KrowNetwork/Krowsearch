'use_strict'
var spawn = require("child_process").spawn;
var fs = require('fs');
var os = require("os")
var path = require("path")
var utf8 = require('utf8');

var python = spawn('python', [__dirname + '\\search.py'], {detached: true});

// app.engine('html', require('ejs').renderFile);
console.log(__dirname + '\\search.py')
exports.search = async function(query, page) {
  // console.log(query)
  // current_page += 1;
  return new Promise(function(resolve, reject){
    console.log("1");
    python.stdout.on('data', async (chunk) => {
      results = chunk.toString().split(" ");
      console.log("2")
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
          resolve(result.toString())
          // log("processed results for term \"" + query + "\"")
        })

      // console.log(data);
    })
    python.stdin.write(query + os.EOL);
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
// await search(req, res, page)
// .then(function (result, json_res){
//   result = utf8.encode(result)
//   res.render("index", {results: result, term: req.query.q})
//   full_json = json_res
//   res.end();
//   res = null;
//   req = null;
// })
