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
    console.log('Using database:', dbName);
  })
  .catch(err => {
    console.error('MongoDB connection error:', err);
  });

// API endpoint to add a new entry
app.post('/api/entries', async (req, res) => {
  console.log('\n=== RECEIVED NEW ENTRY REQUEST ===');
  console.log('Request body:', req.body);
  
  try {
    const { message } = req.body;
    console.log('Message to store:', message);
    
    const entry = {
      message,
      timestamp: new Date()
    };
    console.log('Entry object:', entry);
    
    console.log('Attempting to insert into MongoDB...');
    const result = await db.collection('messages').insertOne(entry);
    console.log('MongoDB insert result:', result);
    
    const response = { success: true, entry: { ...entry, _id: result.insertedId } };
    console.log('Sending response:', response);
    res.json(response);
  } catch (error) {
    console.error('Error adding entry:', error);
    console.error('Full error details:', {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    res.status(500).json({ success: false, error: error.message });
  }
});

// API endpoint to get all entries
app.get('/api/entries', async (req, res) => {
  console.log('\n=== FETCHING ALL ENTRIES ===');
  try {
    console.log('Querying MongoDB for all entries...');
    const entries = await db.collection('messages')
      .find({})
      .sort({ timestamp: -1 })
      .toArray();
    console.log(`Found ${entries.length} entries`);
    console.log('Entries:', entries);  // Log the actual entries
    res.json(entries);
  } catch (error) {
    console.error('Error fetching entries:', error);
    console.error('Full error details:', {
      message: error.message,
      stack: error.stack,
      name: error.name
    });
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
}); 