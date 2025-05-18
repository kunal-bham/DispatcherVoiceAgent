const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');
const app = express();
const port = 3000;

// MongoDB connection URL
const mongoUrl = 'mongodb://localhost:27017';
const dbName = 'CALL_SUMMARY';

// Middleware
app.use(express.json());

// Serve static files from the root directory
app.use(express.static(path.join(__dirname)));
// Serve static files from the dist directory
app.use('/dist', express.static(path.join(__dirname, 'dist')));
// Serve static files from the src directory
app.use('/src', express.static(path.join(__dirname, 'src')));

// Add CORS headers
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    next();
});

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
      timestamp: new Date(),
      type: 'test_entry'  // Add type to distinguish from other entries
    };
    console.log('Entry object:', entry);
    
    console.log('Attempting to insert into MongoDB...');
    const result = await db.collection('messages').insertOne(entry);
    console.log('MongoDB insert result:', result);
    
    // Format the response to match what frontend expects
    const response = { 
      success: true, 
      entry: { 
        _id: result.inserted_id,
        message: entry.message,
        timestamp: entry.timestamp,
        type: entry.type
      } 
    };
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
    const entries = await db.collection('messages')
      .find({})
      .sort({ created_at: -1, timestamp: -1 })
      .toArray();
    
    console.log(`Found ${entries.length} entries`);
    
    // Format entries to ensure consistent structure
    const formattedEntries = entries.map(entry => {
      // Handle voice agent entries (with raw_messages)
      if (entry.raw_messages) {
        return {
          _id: entry._id,
          message: entry.concise_summary || entry.raw_messages,
          timestamp: entry.created_at,
          type: 'emergency_call'
        };
      }
      // Handle test entries
      return {
        _id: entry._id,
        message: entry.message,
        timestamp: entry.timestamp,
        type: entry.type || 'test_entry'
      };
    });
    
    console.log('Formatted entries:', formattedEntries);
    res.json(formattedEntries);
  } catch (error) {
    console.error('Error fetching entries:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
}); 