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
  //console.log("Compiling program...")
  //console.log("Code to compile: " + req.body.code);

  var options = {
    mode: 'text',
    //pythonPath: '/Library/Frameworks/Python.framework/Versions/3.6/bin/python3', // uncommment for localhost running (must adapt ionic app too)
    pythonOptions: ['-W', 'ignore'],
    args: [req.body.code]
  };
  
  PythonShell.run('mobprol.py', options, function (err, results) {
    var errorData;
    if (err) { // Cancel execution to avoid pointless processing of data
      console.log("REAL ERROR: " + err.message);
      let errorData = cleanErrorMessage(err.message);
      console.log("BEAUTIFIED ERROR: " + errorData);
      res.json({errorData});
      return;
    }

    console.log('results: %j', results[results.length-1]);
    console.log();
    let unprocessedData = results[results.length-1];
    
    // Clean data for json
    var data;
      // Unnecessary backslashes
    data = unprocessedData.replace("\\\"", "\"");
    //console.log("Data after removing backslashes: ");
    //console.log(data);
      // Change strings to constant notation
    data = data.replace(/\:\"\" ,/g, "\: \"\"\,"); // Modify empty data to not collide with strings
    data = data.replace(/\:\"\"\}/g, "\: \"\"\}"); // Modify empty data to not collide with strings

    data = data.replace(/\:\"\"/g, "\:\"/");        // Modify string start
    data = data.replace(/\"\" /g, "/\"");           // Modify string end

      // Change single quot marks for double
    data = data.replace(/[']/g, "\"");

    console.log("Data to send is:")
    console.log(data);

    res.json({data});
  });
  
});

app.listen(process.env.PORT || 8080);

function cleanErrorMessage(msg) {
  let cleanMsg = "";

  let syntaxError = "Syntax error.";
  let nonDeclaredVariable = "Variable has not been declared.";

  if (msg.indexOf("AttributeError")) { // This also happens with the same message when var lacks init
    cleanMsg = syntaxError;
  }
  else if (msg.indexOf("KeyError")) {
    cleanMsg = nonDeclaredVariable;
  }
  else if (msg.indexOf("ply.lex.LexError")) {
    cleanMsg = syntaxError;
  }
  else if (msg.indexOf(Exception)) {
    cleanMsg = msg.replace(/Exception: /g, "");
  }

  return cleanMsg;
}