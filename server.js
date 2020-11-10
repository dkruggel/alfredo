const express = require('express');

const app = express();

app.get('/api', (req, res) => {
  res.send('Hello');
})

app.get('/', (req, res) => {
  res.send('Hello');
})

app.listen(8000, () => {
  console.log('Listening on port 8000');
})