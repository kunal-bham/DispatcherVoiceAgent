class Notification {
    constructor() {
        console.log('Initializing Notification system');
        this.notificationContainer = null;
        this.createContainer();
    }

    createContainer() {
        console.log('Creating notification container');
        this.notificationContainer = document.createElement('div');
        this.notificationContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            max-width: 300px;
        `;
        document.body.appendChild(this.notificationContainer);
        console.log('Notification container created and added to body');
    }

    show(message) {
        console.log('\n=== SHOWING NOTIFICATION ===');
        console.log('Message:', message);
        
        try {
            const notification = document.createElement('div');
            notification.style.cssText = `
                background-color: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                animation: slideIn 0.3s ease-out;
            `;
            
            notification.textContent = message;
            console.log('Notification element created');
            
            this.notificationContainer.appendChild(notification);
            console.log('Notification added to container');
            
            // Add animation keyframes
            const style = document.createElement('style');
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
            console.log('Animation styles added');
            
            // Remove notification after 5 seconds
            setTimeout(() => {
                console.log('Removing notification');
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    this.notificationContainer.removeChild(notification);
                    console.log('Notification removed from DOM');
                }, 300);
            }, 5000);
        } catch (error) {
            console.error('Error showing notification:', error);
            console.error('Full error details:', {
                message: error.message,
                stack: error.stack,
                name: error.name
            });
        }
    }
}

export default new Notification(); 