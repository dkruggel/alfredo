const express = require('express');
const { spawn } = require('child_process');

const app = express();

let runScript = function (user, measAcc) {
  return new Promise(function (success, nosuccess) {
    const python = spawn('/usr/bin/python3', ['./algo/main.py', user, measAcc]);

    python.stdout.on('data', function (data) {
      success(data);
    });

    python.stdout.on('data', (data) => {
      nosuccess(data);
    });
  });
};

app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  next();
});

app.get('/search/', (req, res) => {
  runScript('ofKDkJKXSKZXu5xJNGiiBQ', false).then(function (output) {
    out = output.toString();
    res.send(out);
  });
});

app.get('/accuracy/', (req, res) => {
  runScript('ofKDkJKXSKZXu5xJNGiiBQ', 'True').then(function (output) {
    out = output.toString();
    res.send(out);
  });
});

app.get('/', (req, res) => {
  res.send('Hello');
});

app.listen(7000, () => {
  console.log('Listening on port 7000');
});
