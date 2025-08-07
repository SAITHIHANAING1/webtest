/**
 * SafeStep Chatbot Widget
 * Frontend JavaScript for the floating chat widget
 */

class SafeStepChatbot {
    constructor() {
        this.isOpen = false;
        this.isLoading = false;
        this.userRole = 'caregiver'; // Default role, will be updated based on user
        this.init();
    }

    init() {
        this.createWidget();
        this.bindEvents();
        this.detectUserRole();
    }

    createWidget() {
        // Create chatbot HTML
        const chatbotHTML = `
            <div id="chatbot-widget" class="chatbot-widget">
                <!-- Chat Button -->
                <div id="chatbot-button" class="chatbot-button">
                    <i class="fas fa-comments"></i>
                    <span class="chatbot-badge" id="chatbot-badge" style="display: none;">1</span>
                </div>
                
                <!-- Chat Window -->
                <div id="chatbot-window" class="chatbot-window" style="display: none;">
                    <!-- Header -->
                    <div class="chatbot-header">
                        <div class="chatbot-title">
                            <i class="fas fa-robot"></i>
                            <span>SafeStep Assistant</span>
                        </div>
                        <button id="chatbot-close" class="chatbot-close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <!-- Messages Container -->
                    <div id="chatbot-messages" class="chatbot-messages">
                        <div class="chatbot-message bot-message">
                            <div class="message-content">
                                <i class="fas fa-robot"></i>
                                <div class="message-text">
                                    Hello! I'm your SafeStep assistant. How can I help you today?
                                </div>
                            </div>
                            <div class="message-time">${this.getCurrentTime()}</div>
                        </div>
                    </div>
                    
                    <!-- Input Area -->
                    <div class="chatbot-input-area">
                        <div class="chatbot-input-container">
                            <input type="text" id="chatbot-input" placeholder="Type your question..." maxlength="500">
                            <button id="chatbot-send" class="chatbot-send">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                        <div class="chatbot-suggestions">
                            <button class="suggestion-btn" data-question="How do I set up a safety zone?">Safety Zones</button>
                            <button class="suggestion-btn" data-question="What should I do during a seizure?">Seizure Response</button>
                            <button class="suggestion-btn" data-question="How do I access training modules?">Training</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Add to page
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    bindEvents() {
        // Toggle chat window
        document.getElementById('chatbot-button').addEventListener('click', () => {
            this.toggleChat();
        });

        // Close chat window
        document.getElementById('chatbot-close').addEventListener('click', () => {
            this.closeChat();
        });

        // Send message
        document.getElementById('chatbot-send').addEventListener('click', () => {
            this.sendMessage();
        });

        // Enter key to send
        document.getElementById('chatbot-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Suggestion buttons
        document.querySelectorAll('.suggestion-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const question = e.target.dataset.question;
                document.getElementById('chatbot-input').value = question;
                this.sendMessage();
            });
        });

        // Close on outside click
        document.addEventListener('click', (e) => {
            const widget = document.getElementById('chatbot-widget');
            if (!widget.contains(e.target) && this.isOpen) {
                this.closeChat();
            }
        });
    }

    detectUserRole() {
        // Detect user role from page URL or user data
        const path = window.location.pathname;
        if (path.includes('/admin')) {
            this.userRole = 'admin';
        } else if (path.includes('/caregiver')) {
            this.userRole = 'caregiver';
        }
        
        // Update chatbot title based on role
        const titleElement = document.querySelector('.chatbot-title span');
        if (titleElement) {
            titleElement.textContent = `SafeStep Assistant (${this.userRole})`;
        }
    }

    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    openChat() {
        this.isOpen = true;
        document.getElementById('chatbot-window').style.display = 'block';
        document.getElementById('chatbot-button').classList.add('active');
        
        // Focus on input
        setTimeout(() => {
            document.getElementById('chatbot-input').focus();
        }, 100);
    }

    closeChat() {
        this.isOpen = false;
        document.getElementById('chatbot-window').style.display = 'none';
        document.getElementById('chatbot-button').classList.remove('active');
    }

    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        
        if (!message || this.isLoading) return;
        
        // Clear input
        input.value = '';
        
        // Add user message
        this.addMessage(message, 'user');
        
        // Show loading
        this.isLoading = true;
        this.showTypingIndicator();
        
        try {
            // Send to backend
            const response = await fetch('/api/chatbot/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message,
                    user_role: this.userRole
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // Add bot response
                this.addMessage(data.response, 'bot');
            } else {
                // Show error
                const errorMsg = data.error || 'Sorry, I encountered an error. Please try again.';
                this.addMessage(errorMsg, 'bot');
            }
            
        } catch (error) {
            console.error('Chatbot error:', error);
            this.addMessage('Sorry, I\'m having trouble connecting. Please check your internet connection.', 'bot');
        } finally {
            this.isLoading = false;
            this.hideTypingIndicator();
        }
    }

    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}-message`;
        
        const icon = sender === 'bot' ? 'fas fa-robot' : 'fas fa-user';
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <i class="${icon}"></i>
                <div class="message-text">${this.escapeHtml(text)}</div>
            </div>
            <div class="message-time">${this.getCurrentTime()}</div>
        `;
        
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom with smooth animation
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }

    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-message bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        
        typingDiv.innerHTML = `
            <div class="message-content">
                <i class="fas fa-robot"></i>
                <div class="message-text">
                    <span class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </span>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        
        // Scroll to bottom to show typing indicator
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 50);
    }

    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    getCurrentTime() {
        return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showNotification() {
        const badge = document.getElementById('chatbot-badge');
        badge.style.display = 'block';
        
        // Hide after 5 seconds
        setTimeout(() => {
            badge.style.display = 'none';
        }, 5000);
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.safeStepChatbot = new SafeStepChatbot();
});
