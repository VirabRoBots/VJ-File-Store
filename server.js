const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static('public'));

const VOTES_FILE = path.join(__dirname, 'votes.json');
const REPORTS_FILE = path.join(__dirname, 'reports.json');

if (!fs.existsSync(VOTES_FILE)) fs.writeFileSync(VOTES_FILE, JSON.stringify({}));
if (!fs.existsSync(REPORTS_FILE)) fs.writeFileSync(REPORTS_FILE, JSON.stringify([]));

app.get('/votes/:file_id', (req, res) => {
  const data = JSON.parse(fs.readFileSync(VOTES_FILE));
  const fileId = req.params.file_id;
  
  if (!data[fileId]) {
    data[fileId] = {
      likes: Math.floor(Math.random() * 100) + 400,
      dislikes: Math.floor(Math.random() * 45) + 5
    };
    fs.writeFileSync(VOTES_FILE, JSON.stringify(data, null, 2));
  }
  
  res.json({
    likes: data[fileId].likes,
    dislikes: data[fileId].dislikes,
    user_vote: null
  });
});

app.post('/vote', (req, res) => {
  const { file_id, vote } = req.body;
  const data = JSON.parse(fs.readFileSync(VOTES_FILE));
  
  if (!data[file_id]) {
    data[file_id] = {
      likes: Math.floor(Math.random() * 100) + 400,
      dislikes: Math.floor(Math.random() * 45) + 5
    };
  }
  
  if (vote === 'like') data[file_id].likes++;
  else if (vote === 'dislike') data[file_id].dislikes++;
  
  fs.writeFileSync(VOTES_FILE, JSON.stringify(data, null, 2));
  
  res.json({
    likes: data[file_id].likes,
    dislikes: data[file_id].dislikes,
    user_vote: vote
  });
});

app.post('/report', (req, res) => {
  const reports = JSON.parse(fs.readFileSync(REPORTS_FILE));
  reports.push({
    ...req.body,
    timestamp: new Date().toISOString()
  });
  fs.writeFileSync(REPORTS_FILE, JSON.stringify(reports, null, 2));
  res.json({ success: true });
});

app.listen(PORT, () => {
  console.log(`✅ Server running on http://localhost:${PORT}`);
});
