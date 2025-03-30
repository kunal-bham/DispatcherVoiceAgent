// Dummy MongoDB connection and notification system
class DatabaseManager {
    constructor() {
        this.listeners = [];
        this.apiUrl = 'http://localhost:3000/api';
        this.lastEntryId = null;
        this.startPolling();
    }

    // Add a new entry to MongoDB
    async addEntry(entry) {
        try {
            const response = await fetch(`${this.apiUrl}/entries`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(entry)
            });
            
            if (!response.ok) {
                throw new Error('Failed to add entry');
            }
            
            const result = await response.json();
            return result.entry;
        } catch (error) {
            console.error('Error adding entry:', error);
            throw error;
        }
    }

    // Get all entries from MongoDB
    async getEntries() {
        try {
            const response = await fetch(`${this.apiUrl}/entries`);
            if (!response.ok) {
                throw new Error('Failed to fetch entries');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching entries:', error);
            throw error;
        }
    }

    // Add a listener for new entries
    addListener(callback) {
        this.listeners.push(callback);
    }

    // Start polling for new entries
    async startPolling() {
        // Get initial entries
        const entries = await this.getEntries();
        if (entries.length > 0) {
            this.lastEntryId = entries[0]._id;
        }

        // Poll every 2 seconds
        setInterval(async () => {
            try {
                const entries = await this.getEntries();
                if (entries.length > 0) {
                    const latestEntry = entries[0];
                    if (this.lastEntryId !== latestEntry._id) {
                        this.lastEntryId = latestEntry._id;
                        this.notifyListeners(latestEntry);
                    }
                }
            } catch (error) {
                console.error('Error polling for new entries:', error);
            }
        }, 2000);
    }

    // Notify all listeners of a new entry
    notifyListeners(entry) {
        this.listeners.forEach(callback => callback(entry));
    }
}

// Create a singleton instance
const dbManager = new DatabaseManager();
export default dbManager; 