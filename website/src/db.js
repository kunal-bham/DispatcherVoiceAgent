// Dummy MongoDB connection and notification system
class DatabaseManager {
    constructor() {
        console.log('Initializing DatabaseManager');
        this.listeners = [];
        this.apiUrl = 'http://localhost:3000/api';
        this.lastEntryId = null;
        console.log('Starting polling for updates...');
        this.startPolling();
    }

    // Add a new entry to MongoDB
    async addEntry(entry) {
        console.log('\n=== ADDING NEW ENTRY ===');
        console.log('Entry to add:', entry);
        
        try {
            console.log('Sending POST request to:', `${this.apiUrl}/entries`);
            const response = await fetch(`${this.apiUrl}/entries`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(entry)
            });
            
            console.log('Response status:', response.status);
            if (!response.ok) {
                throw new Error(`Failed to add entry: ${response.status}`);
            }
            
            const result = await response.json();
            console.log('Server response:', result);
            
            if (result.success && result.entry) {
                console.log('Entry added successfully:', result.entry);
                return result.entry;
            } else {
                throw new Error('Invalid response format from server');
            }
        } catch (error) {
            console.error('Error adding entry:', error);
            console.error('Full error details:', {
                message: error.message,
                stack: error.stack,
                name: error.name
            });
            throw error;
        }
    }

    // Get all entries from MongoDB
    async getEntries() {
        console.log('\n=== FETCHING ALL ENTRIES ===');
        try {
            console.log('Sending GET request to:', `${this.apiUrl}/entries`);
            const response = await fetch(`${this.apiUrl}/entries`);
            console.log('Response status:', response.status);
            
            if (!response.ok) {
                throw new Error(`Failed to fetch entries: ${response.status}`);
            }
            
            const entries = await response.json();
            console.log(`Received ${entries.length} entries`);
            
            // Validate entries structure
            const validEntries = entries.filter(entry => 
                entry && 
                entry._id && 
                entry.message && 
                entry.timestamp
            );
            
            console.log('Valid entries:', validEntries);
            return validEntries;
        } catch (error) {
            console.error('Error fetching entries:', error);
            console.error('Full error details:', {
                message: error.message,
                stack: error.stack,
                name: error.name
            });
            throw error;
        }
    }

    // Add a listener for new entries
    addListener(callback) {
        console.log('Adding new listener');
        this.listeners.push(callback);
        console.log(`Total listeners: ${this.listeners.length}`);
    }

    // Start polling for new entries
    async startPolling() {
        console.log('Starting polling mechanism');
        // Get initial entries
        try {
            const entries = await this.getEntries();
            if (entries.length > 0) {
                this.lastEntryId = entries[0]._id;
                console.log('Initial lastEntryId:', this.lastEntryId);
            }
        } catch (error) {
            console.error('Error getting initial entries:', error);
        }

        // Poll every 2 seconds
        setInterval(async () => {
            try {
                console.log('\n=== POLLING CYCLE ===');
                const entries = await this.getEntries();
                if (entries.length > 0) {
                    const latestEntry = entries[0];
                    console.log('Latest entry:', latestEntry);
                    console.log('Latest entry ID:', latestEntry._id);
                    console.log('Current lastEntryId:', this.lastEntryId);
                    
                    // Convert both IDs to strings for comparison
                    const latestId = latestEntry._id.toString();
                    const lastId = this.lastEntryId ? this.lastEntryId.toString() : null;
                    
                    console.log('Comparing IDs:', {
                        latestId,
                        lastId,
                        areEqual: latestId === lastId
                    });
                    
                    if (latestId !== lastId) {
                        console.log('New entry detected!');
                        console.log('Entry details:', latestEntry);
                        this.lastEntryId = latestEntry._id;
                        console.log('Notifying listeners...');
                        this.notifyListeners(latestEntry);
                    } else {
                        console.log('No new entries detected');
                    }
                } else {
                    console.log('No entries found in database');
                }
            } catch (error) {
                console.error('Error polling for new entries:', error);
                console.error('Full error details:', {
                    message: error.message,
                    stack: error.stack,
                    name: error.name
                });
            }
        }, 2000);
    }

    // Notify all listeners of a new entry
    notifyListeners(entry) {
        console.log(`\n=== NOTIFYING LISTENERS ===`);
        console.log(`Number of listeners: ${this.listeners.length}`);
        console.log('Entry to notify:', entry);
        this.listeners.forEach((callback, index) => {
            console.log(`Calling listener ${index + 1}`);
            try {
                callback(entry);
                console.log(`Successfully notified listener ${index + 1}`);
            } catch (error) {
                console.error(`Error notifying listener ${index + 1}:`, error);
            }
        });
    }
}

// Create a singleton instance
console.log('Creating DatabaseManager instance');
const dbManager = new DatabaseManager();
export default dbManager; 