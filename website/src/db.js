// Dummy MongoDB connection and notification system
class DatabaseManager {
    constructor() {
        this.entries = [];
        this.listeners = [];
    }

    // Simulate adding a new entry
    addEntry(entry) {
        this.entries.push(entry);
        this.notifyListeners(entry);
    }

    // Add a listener for new entries
    addListener(callback) {
        this.listeners.push(callback);
    }

    // Notify all listeners of a new entry
    notifyListeners(entry) {
        this.listeners.forEach(callback => callback(entry));
    }
}

// Create a singleton instance
const dbManager = new DatabaseManager();
export default dbManager; 