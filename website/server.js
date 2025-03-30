const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');
const app = express();
const port = 3000;

// MongoDB connection URL
const mongoUrl = 'mongodb://localhost:27017';
const dbName = 'dispatcher_db';

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname)));

// MongoDB connection
let db;
MongoClient.connect(mongoUrl)
  .then(client => {
    console.log('Connected to MongoDB');
    db = client.db(dbName);
  })
  .catch(err => {
    console.error('MongoDB connection error:', err);
  });

// API endpoint to add a new entry
app.post('/api/entries', async (req, res) => {
  try {
    const { message } = req.body;
    const entry = {
      message,
      timestamp: new Date()
    };
    
    const result = await db.collection('messages').insertOne(entry);
    res.json({ success: true, entry: { ...entry, _id: result.insertedId } });
  } catch (error) {
    console.error('Error adding entry:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to get all entries
app.get('/api/entries', async (req, res) => {
  try {
    const entries = await db.collection('messages')
      .find({})
      .sort({ timestamp: -1 })
      .toArray();
    res.json(entries);
  } catch (error) {
    console.error('Error fetching entries:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
}); 