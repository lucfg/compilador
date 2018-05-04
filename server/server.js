var express = require('express');
var bodyParser = require('body-parser');
var logger = require('morgan');
var methodOverride = require('method-override')
var cors = require('cors');
var PythonShell = require('python-shell');
 
var app = express();
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(methodOverride());
app.use(cors());

var quadruples = null;

app.post('/compile', function(req, res) {
  console.log("Compiling program...")
  console.log("Code to compile: " + req.body.code);

  var options = {
    mode: 'text',
    pythonPath: '/Library/Frameworks/Python.framework/Versions/3.6/bin/python3',
    pythonOptions: ['-W', 'ignore'],
    args: [req.body.code]
  };
  
  PythonShell.run('mobprol.py', options, function (err, results) {
    if (err) throw err;

    console.log('results: %j', results[results.length-1]);
    console.log();
    let unprocessedData = results[results.length-1];
    
    // Clean data for json
    var data;
      // Unnecessary backslashes
    data = unprocessedData.replace("\\\"", "\"");
    console.log("Data after removing backslashes: ");
    console.log(data);
      // Change strings to constant notation
    data = data.replace(/\:\"\" ,/g, "\: \"\"\,"); // Modify empty data to not collide with strings
    data = data.replace(/\:\"\"\}/g, "\: \"\"\}"); // Modify empty data to not collide with strings

    data = data.replace(/\:\"\"/g, "\:\"/");        // Modify string start
    data = data.replace(/\"\" /g, "/\"");           // Modify string end

      // Change single quot marks for double
    data = data.replace(/[']/g, "\"");
    console.log("New data is " + data);

    res.json({data});
  });
  
});

app.listen(process.env.PORT || 8080);