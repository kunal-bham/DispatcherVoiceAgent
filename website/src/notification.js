class Notification {
    constructor() {
        this.createNotificationElement();
    }

    createNotificationElement() {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 20px 40px;
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            font-size: 1.5rem;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
            pointer-events: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        `;
        this.element = notification;
        document.body.appendChild(notification);
    }

    show(message) {
        this.element.textContent = message;
        this.element.style.opacity = '1';
        
        setTimeout(() => {
            this.element.style.opacity = '0';
        }, 60000); // Changed to 60 seconds (1 minute)
    }
}

export default new Notification(); 