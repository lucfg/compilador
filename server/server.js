var express = require('express');
var bodyParser = require('body-parser');
var logger = require('morgan');
var methodOverride = require('method-override')
var cors = require('cors');
var PythonShell = require('python-shell');
var pyshell = new PythonShell('mobprol.py');
//you can use error handling to see if there are any errors
 
var app = express();
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(methodOverride());
app.use(cors());

var queadruples = null;

pyshell.on('message', function (message) {
    console.log("Received qudaruples: " + message);
    quadruples = message;
});

app.post('/compile', function(req, res) {
    while (quadruples == null) {

    }
    res.json({"success": true, "quadruples":quadruples});
    quadruples = null;
});

app.listen(process.env.PORT || 8080);