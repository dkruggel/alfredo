const express = require('express');
const { spawn } = require('child_process');

const app = express();

let runScript = function(user) {
  return new Promise(function (success, nosuccess) {
    const python = spawn('python', ['./algo/main.py', user]);

    python.stdout.on('data', function (data) {
      success(data);
    });

    python.stdout.on('data', (data) => {
      nosuccess(data);
    });
  });
}

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});

app.get('/api/:user', (req, res) => {
  user = req.params['user'];
  runScript(user).then(function (output) {
    res.send(output.toString().slice(107,-1));
  });
});

app.get('/', (req, res) => {
  res.send('Hello');
});

app.listen(8000, () => {
  console.log('Listening on port 8000');
});
