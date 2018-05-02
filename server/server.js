var express = require('express');
var bodyParser = require('body-parser');
var logger = require('morgan');
var methodOverride = require('method-override')
var cors = require('cors');
var PythonShell = require('python-shell');
//var pyshell = new PythonShell('test.py');
//you can use error handling to see if there are any errors
 
var app = express();
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(methodOverride());
app.use(cors());

var quadruples = null;

//pyshell.send('hello');
 
/*pyshell.on('message', function (message) {
  // received a message sent from the Python script (a simple "print" statement)
  console.log(message);
});
*/

var options = {
  mode: 'text',
  pythonPath: '/Library/Frameworks/Python.framework/Versions/3.6/bin/python3',
  pythonOptions: ['-W', 'ignore'],
  args: ["program myProgram { main() {}}"]
};

PythonShell.run('mobprol.py', options, function (err, results) {
  if (err) throw err;
  // results is an array consisting of messages collected during execution
  console.log('results: %j', results);
});

app.post('/compile', function(req, res) {
  var options = {
    mode: 'text',
    pythonPath: '/usr/bin/env python3',
    args: ['program myProgram { main() {}}']
  };
  
      console.log("Sending input to compiler");
      PythonShell.run('mobprol.py', function (err) {
    if (err) throw err;
    console.log('finished');
  });
    });

app.listen(process.env.PORT || 8080);