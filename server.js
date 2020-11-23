const express = require('express');
const { spawn } = require('child_process');

const app = express();

app.get('/api', (req, res) => {
  console.log('waiting');
  const python = spawn('/bin/python3', ['./algo/main.py', 'david']);
  python.stdout.on('data', function (data) {
    console.log('Pipe data from python script ...');
    dataToSend = data.toString();
  });
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`);
  });
  while (typeof dataToSend == "undefined") {
    if (typeof dataToSend != "undefined") {
      break;
    }
  }
  res.send(dataToSend);
});

app.get('/', (req, res) => {
  res.send('Hello');
});

app.listen(8000, () => {
  console.log('Listening on port 8000');
});
