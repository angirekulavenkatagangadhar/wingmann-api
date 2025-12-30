// Global state
let allUsers = [];
let currentSection = 'discoverSection';

// Question texts (must match backend QUESTION_TEXTS)
const QUESTION_TEXTS = {
    1: "How do you usually like to spend your weekends?",
    2: "When it comes to managing money as a couple, I prefer:",
    3: "I feel most balanced when my partner and I have similar daily habits and energy levels.",
    4: "If I had to choose between spending time on my goals or my relationship, I'd usually choose my goals.",
    5: "What's one thing that really matters to you in a relationship?",
    6: "When I'm upset, I tend to:",
    7: "When you care about someone, you usually show it through:",
    8: "I pick up on changes in someone's mood quickly.",
    9: "I can express how I feel even when it might cause disagreement.",
    10: "When my partner withdraws during a disagreement, I usually want to reach out and reconnect.",
    11: "I sometimes worry that my partner might lose interest or drift away.",
    12: "I love emotional closeness, but too much of it can make me want space.",
    13: "Even with someone I trust, I sometimes hold back my true feelings.",
    14: "When I feel overwhelmed, I usually:",
    15: "If someone you're dating doesn't text back for hours, what's your first reaction?",
    16: "I feel safe sharing my feelings when I know I won't be judged.",
    17: "After a disagreement, I'm usually the one to take the first step toward making things right.",
    18: "When conflict arises, I tend to:",
    19: "I often focus more on being right than on being understood.",
    20: "I find it difficult to stay calm when I feel misunderstood.",
    21: "I believe relationships help both people grow.",
    22: "When I realize I've hurt someone, I try to take responsibility and reconnect.",
    23: "I rarely talk about my feelings and emotions.",
    24: "Which best describes how you feel about relationships right now?",
    25: "I've learned the most about relationships from:",
};

// Option labels (must match backend QUESTION_OPTIONS)
const QUESTION_OPTIONS = {
    1: {
        1: "Relaxing at home",
        2: "Going out with friends or exploring new places",
        3: "Doing something productive",
        4: "Mixing it up depending on my mood",
    },
    2: {
        1: "Putting it all together",
        2: "Keeping our own accounts but being open about stuff",
        3: "Splitting things in a way that feels fair for both",
        4: "Keeping finances totally separate",
    },
    3: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    4: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    6: {
        1: "Stay quiet and think",
        2: "Talk things through right away",
        3: "Distract myself until I feel calmer",
        4: "Wait for the other person to reach out first",
    },
    7: {
        1: "Spending quality time together",
        2: "Giving thoughtful gifts",
        3: "Checking in and making sure they are okay",
        4: "Doing things to help or support them",
    },
    8: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    9: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    10: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    11: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    12: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    13: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    14: {
        1: "Take some time alone to recharge and think",
        2: "Talk it out with someone I trust",
        3: "Distract myself with music, shows, or hobbies",
        4: "Try to stay busy and push through it",
    },
    15: {
        1: "Calm – they're probably busy",
        2: "Anxious – did I say something wrong?",
        3: "Unbothered – I'll reply later too",
        4: "Irritated – communication should be consistent",
    },
    16: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    17: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    18: {
        1: "Avoid it until things calm down",
        2: "Address it right away",
        3: "Compromise quickly to move on",
        4: "Reflect before bringing it up",
    },
    19: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    20: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    21: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    22: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    23: {
        1: "1 - Completely Disagree",
        2: "2",
        3: "3",
        4: "4",
        5: "5 - Completely Agree",
    },
    24: {
        1: "Ready to build something meaningful",
        2: "Open but cautious",
        3: "Still exploring what I really want",
        4: "Healing and taking things slow",
    },
    25: {
        1: "My past relationships",
        2: "Watching family or friends",
        3: "Personal growth and self reflection",
        4: "Movies, books, or social media",
    },
};

function getAnswerLabel(questionNum, rawValue) {
    // Q5 is descriptive free-text
    if (parseInt(questionNum, 10) === 5) {
        return String(rawValue);
    }
    const qNum = parseInt(questionNum, 10);
    const options = QUESTION_OPTIONS[qNum];
    if (!options) return String(rawValue);
    const key = parseInt(rawValue, 10);
    if (Number.isNaN(key)) return String(rawValue);
    return options[key] || String(rawValue);
}

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    loadAllUsers();
    showSection('discoverSection');
});

// Load all users from API
async function loadAllUsers() {
    try {
        const response = await fetch('/api/users');
        allUsers = await response.json();
        
        // Populate all user selects
        populateUserSelect('discoverUserSelect', allUsers);
        populateUserSelect('profileUserSelect', allUsers);
        populateUserSelect('searchUserSelect', allUsers);
        populateUserSelect('messageUserSelect', allUsers);
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

// Populate user select dropdown
function populateUserSelect(selectId, users) {
    const select = document.getElementById(selectId);
    if (!select) return;
    
    select.innerHTML = '<option value="">Select User</option>';
    
    users.forEach(user => {
        const option = document.createElement('option');
        option.value = user.id;
        option.textContent = `${user.name} (${user.gender})`;
        select.appendChild(option);
    });
}

// Show specific section
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    document.getElementById(sectionId).classList.add('active');
    
    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Update active nav item
    const navItems = {
        'discoverSection': 0,
        'searchSection': 1,
        'messagingSection': 2,
        'profileSection': 3
    };
    if (navItems[sectionId] !== undefined) {
        document.querySelectorAll('.nav-item')[navItems[sectionId]].classList.add('active');
    }
    
    currentSection = sectionId;
    
    // Load section-specific content
    if (sectionId === 'discoverSection') {
        loadRecommendedProfiles();
    } else if (sectionId === 'profileSection') {
        loadProfile();
    } else if (sectionId === 'searchSection') {
        loadCompatibility();
    } else if (sectionId === 'messagingSection') {
        loadMessages();
    }
}

// Load Recommended Profiles (Discover Section)
async function loadRecommendedProfiles() {
    const userId = document.getElementById('discoverUserSelect').value;
    const discoverContent = document.getElementById('discoverContent');
    
    if (!userId) {
        discoverContent.innerHTML = '<div class="empty-state"><p>Select a user to see recommended profiles</p></div>';
        return;
    }
    
    const user = allUsers.find(u => u.id == userId);
    if (!user) return;
    
    discoverContent.innerHTML = '<div class="loading-message">Loading recommendations...</div>';
    
    try {
        // Get opposite gender users
        const oppositeGender = user.gender === 'Male' ? 'Female' : 'Male';
        const recommendedUsers = allUsers.filter(u => 
            u.id != userId && u.gender === oppositeGender
        );
        
        if (recommendedUsers.length === 0) {
            discoverContent.innerHTML = '<div class="empty-state"><p>No profiles available yet. Add more users!</p></div>';
            return;
        }
        
        // Get compatibility scores for recommended users
        const response = await fetch(`/api/compatibility/all?user_id=${userId}`);
        const matches = await response.json();
        
        // Create a map of user IDs to scores
        const scoreMap = {};
        matches.forEach(match => {
            const matchUser = match.user1.id == userId ? match.user2 : match.user1;
            scoreMap[matchUser.id] = match.score;
        });
        
        // Sort recommended users by compatibility score (highest first)
        recommendedUsers.sort((a, b) => {
            const scoreA = scoreMap[a.id] || 0;
            const scoreB = scoreMap[b.id] || 0;
            return scoreB - scoreA;
        });
        
        let html = '<div class="recommended-profiles">';
        
        recommendedUsers.forEach((recommendedUser) => {
            const score = scoreMap[recommendedUser.id] || 0;
            const scoreColor = score >= 70 ? 'var(--success)' : 
                              score >= 50 ? 'var(--warning)' : 
                              'var(--text-secondary)';
            
            html += `
                <div class="profile-card-recommended" onclick="viewProfileDetail(${recommendedUser.id})">
                    <div class="profile-card-header">
                        <div class="profile-avatar-large">${recommendedUser.name.charAt(0).toUpperCase()}</div>
                        <div class="profile-card-info">
                            <h3>${recommendedUser.name}</h3>
                            <p class="profile-card-gender">${recommendedUser.gender}</p>
                            <div class="profile-card-score" style="color: ${scoreColor}">
                                ${score}% Match
                            </div>
                        </div>
                    </div>
                    <div class="profile-card-actions">
                        <button class="action-btn like-btn" onclick="event.stopPropagation(); likeProfile(${recommendedUser.id})">👍 Like</button>
                        <button class="action-btn view-btn" onclick="event.stopPropagation(); viewProfileDetail(${recommendedUser.id})">View Profile</button>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        discoverContent.innerHTML = html;
    } catch (error) {
        console.error('Error loading recommendations:', error);
        discoverContent.innerHTML = '<div class="empty-state"><p>Error loading recommendations. Please try again.</p></div>';
    }
}

// View profile detail
function viewProfileDetail(userId) {
    // Switch to profile section and select the user
    document.getElementById('profileUserSelect').value = userId;
    showSection('profileSection');
    loadProfile();
}

// Like profile (placeholder)
function likeProfile(userId) {
    alert(`Liked profile! (User ID: ${userId})`);
}

// Load Profile Section
async function loadProfile() {
    const userId = document.getElementById('profileUserSelect').value;
    const profileContent = document.getElementById('profileContent');
    
    if (!userId) {
        profileContent.innerHTML = '<div class="empty-state"><p>Select a user to view their profile</p></div>';
        return;
    }
    
    const user = allUsers.find(u => u.id == userId);
    if (!user) return;

    // Build detailed answers with question text + readable answer
    const answersHtml = Object.entries(user.answers)
        .sort((a, b) => parseInt(a[0]) - parseInt(b[0]))
        .map(([qNum, answer]) => {
            const qNumber = parseInt(qNum, 10);
            const questionText = QUESTION_TEXTS[qNumber] || `Question ${qNum}`;
            const answerLabel = getAnswerLabel(qNum, answer);
            return `
                <div class="answer-item">
                    <div class="answer-question-block">
                        <span class="answer-question-num">Q${qNum}</span>
                        <span class="answer-question-text">${questionText}</span>
                    </div>
                    <div class="answer-value-block">
                        <span class="answer-label-title">Answer:</span>
                        <span class="answer-value">${answerLabel}</span>
                    </div>
                </div>
            `;
        }).join('');

    profileContent.innerHTML = `
        <div class="profile-card">
            <div class="profile-header">
                <div class="profile-avatar">${user.name.charAt(0).toUpperCase()}</div>
                <div class="profile-info">
                    <h3>${user.name}</h3>
                    <p class="profile-gender">${user.gender}</p>
                    <p class="profile-phone">📱 ${user.phone}</p>
                </div>
            </div>
            
            <div class="profile-answers">
                <h4>Compatibility Answers</h4>
                <div class="answers-list">
                    ${answersHtml}
                </div>
            </div>
        </div>
    `;
}

// Load Compatibility/Search Section
async function loadCompatibility() {
    const userId = document.getElementById('searchUserSelect').value;
    const compatibilityContent = document.getElementById('compatibilityContent');
    
    if (!userId) {
        compatibilityContent.innerHTML = '<div class="empty-state"><p>Select a user to find their compatibility matches</p></div>';
        return;
    }
    
    compatibilityContent.innerHTML = '<div class="loading-message">Loading matches...</div>';
    
    try {
        const response = await fetch(`/api/compatibility/all?user_id=${userId}`);
        const data = await response.json();
        
        if (data.length === 0) {
            compatibilityContent.innerHTML = '<div class="empty-state"><p>No matches found for this user.</p></div>';
            return;
        }
        
        let html = '<div class="matches-list">';
        
        data.forEach((item, index) => {
            const scoreColor = item.score >= 70 ? 'var(--success)' : 
                              item.score >= 50 ? 'var(--warning)' : 
                              'var(--text-secondary)';
            
            // Determine which user is the match (opposite of selected user)
            const matchUser = item.user1.id == userId ? item.user2 : item.user1;
            
            html += `
                <div class="match-card" onclick="showDetailedAnalysis(${item.user1.id}, ${item.user2.id})">
                    <div class="match-avatar">${matchUser.name.charAt(0).toUpperCase()}</div>
                    <div class="match-info">
                        <h3>${matchUser.name}</h3>
                        <p class="match-gender">${matchUser.gender}</p>
                        <div class="match-score" style="color: ${scoreColor}">
                            ${item.score}% Match
                        </div>
                    </div>
                    <div class="match-action">
                        <span class="match-arrow">→</span>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        compatibilityContent.innerHTML = html;
    } catch (error) {
        console.error('Error loading compatibility:', error);
        compatibilityContent.innerHTML = '<div class="empty-state"><p>Error loading matches. Please try again.</p></div>';
    }
}

// Global chat state
let currentChatUserId = null;
let currentChatMatchId = null;
let chatMessages = {}; // Store messages in memory (not persisted)

// Load Messages Section
async function loadMessages() {
    const userId = document.getElementById('messageUserSelect').value;
    const messagesContent = document.getElementById('messagesContent');
    
    if (!userId) {
        messagesContent.innerHTML = '<div class="empty-state"><p>Select a user to view their messages</p></div>';
        currentChatUserId = null;
        return;
    }
    
    const user = allUsers.find(u => u.id == userId);
    if (!user) return;
    
    currentChatUserId = userId;
    
    // Get all opposite gender users
    const oppositeGender = user.gender === 'Male' ? 'Female' : 'Male';
    const oppositeUsers = allUsers.filter(u => 
        u.id != userId && u.gender === oppositeGender
    );
    
    if (oppositeUsers.length === 0) {
        messagesContent.innerHTML = '<div class="empty-state"><p>No users available to message yet.</p></div>';
        return;
    }
    
    // Get compatibility scores for display
    try {
        const response = await fetch(`/api/compatibility/all?user_id=${userId}`);
        const matches = await response.json();
        
        // Create score map
        const scoreMap = {};
        matches.forEach(match => {
            const matchUser = match.user1.id == userId ? match.user2 : match.user1;
            scoreMap[matchUser.id] = match.score;
        });
        
        let html = '<div class="conversations-list">';
        
        oppositeUsers.forEach(oppositeUser => {
            const score = scoreMap[oppositeUser.id] || 0;
            const scoreColor = score >= 70 ? 'var(--success)' : 
                              score >= 50 ? 'var(--warning)' : 
                              'var(--text-secondary)';
            
            html += `
                <div class="conversation-item" onclick="openChat(${userId}, ${oppositeUser.id}, '${oppositeUser.name}')">
                    <div class="conversation-avatar">${oppositeUser.name.charAt(0).toUpperCase()}</div>
                    <div class="conversation-info">
                        <h4>${oppositeUser.name}</h4>
                        <p class="conversation-preview">${score > 0 ? score + '% Match' : 'New conversation'}</p>
                    </div>
                    ${score > 0 ? `<div class="conversation-badge" style="background: ${scoreColor}">${score}%</div>` : ''}
                </div>
            `;
        });
        
        html += '</div>';
        messagesContent.innerHTML = html;
    } catch (error) {
        console.error('Error loading messages:', error);
        messagesContent.innerHTML = '<div class="empty-state"><p>Error loading conversations.</p></div>';
    }
}

// Show detailed analysis (reuse from all_compatibility.html)
async function showDetailedAnalysis(user1Id, user2Id) {
    // Create modal dynamically
    const modal = document.createElement('div');
    modal.id = 'analysisModal';
    modal.className = 'modal';
    modal.style.display = 'block';
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <h2>Detailed Compatibility Analysis</h2>
                <span class="close-modal" onclick="this.closest('.modal').remove()">&times;</span>
            </div>
            <div class="modal-body" id="modalBody">
                <div class="loading-message">Loading analysis...</div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    
    const modalBody = document.getElementById('modalBody');
    
    try {
        const response = await fetch(`/api/compatibility/detailed?user1_id=${user1Id}&user2_id=${user2Id}`);
        const data = await response.json();
        
        if (data.error) {
            modalBody.innerHTML = `<div class="error-message">${data.error}</div>`;
            return;
        }
        
        const { user1, user2, analysis } = data;
        
        let html = `
            <div class="analysis-header">
                <div class="analysis-users">
                    <div class="analysis-user">
                        <h3>${user1.name}</h3>
                        <span class="user-gender">${user1.gender}</span>
                    </div>
                    <div class="vs-divider">vs</div>
                    <div class="analysis-user">
                        <h3>${user2.name}</h3>
                        <span class="user-gender">${user2.gender}</span>
                    </div>
                </div>
                <div class="overall-score">
                    <div class="score-large">${analysis.percentage}%</div>
                    <div class="score-details">${analysis.total_score} / ${analysis.max_possible_score} points</div>
                </div>
            </div>
            
            <div class="breakdown-section">
                <h3>Question-by-Question Breakdown</h3>
                <div class="breakdown-list">
        `;
        
        analysis.breakdown.forEach((item) => {
            const levelColors = {
                'high': 'var(--success)',
                'moderate': 'var(--warning)',
                'low': 'var(--error)'
            };
            
            const levelLabels = {
                'high': 'High Compatibility',
                'moderate': 'Moderate Compatibility',
                'low': 'Low Compatibility'
            };
            
            const color = levelColors[item.compatibility_level];
            const percentage = ((item.question_score / item.max_possible_score) * 100).toFixed(0);
            
            html += `
                <div class="breakdown-item">
                    <div class="breakdown-question">
                        <span class="question-num">Q${item.question_num}</span>
                        <span class="question-text">${item.question_text}</span>
                    </div>
                    <div class="breakdown-details">
                        <div class="breakdown-answers">
                            <span class="answer-label">User 1:</span> <span class="answer-value">${item.user1_answer}</span>
                            <span class="answer-separator">|</span>
                            <span class="answer-label">User 2:</span> <span class="answer-value">${item.user2_answer}</span>
                        </div>
                        <div class="breakdown-score">
                            <span class="compatibility-level" style="color: ${color}">
                                ${levelLabels[item.compatibility_level]}
                            </span>
                            <span class="score-info">
                                ${item.question_score} / ${item.max_possible_score} points 
                                (Weight: ${item.weight}, Multiplier: ${item.compatibility_value}x)
                            </span>
                        </div>
                        <div class="breakdown-bar">
                            <div class="breakdown-bar-fill" style="width: ${percentage}%; background: ${color};"></div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `
                </div>
            </div>
        `;
        
        modalBody.innerHTML = html;
    } catch (error) {
        console.error('Error loading detailed analysis:', error);
        modalBody.innerHTML = '<div class="error-message">Error loading detailed analysis. Please try again.</div>';
    }
    
    // Close modal when clicking outside
    modal.onclick = function(event) {
        if (event.target == modal) {
            modal.remove();
        }
    };
}

// Open chat interface
function openChat(userId, matchId, matchName) {
    currentChatUserId = userId;
    currentChatMatchId = matchId;
    
    const messagesContent = document.getElementById('messagesContent');
    const matchUser = allUsers.find(u => u.id == matchId);
    
    // Initialize chat if doesn't exist
    const chatKey = `${userId}_${matchId}`;
    if (!chatMessages[chatKey]) {
        chatMessages[chatKey] = [];
    }
    
    const messages = chatMessages[chatKey];
    
    let html = `
        <div class="chat-container">
            <div class="chat-header">
                <button class="back-btn-chat" onclick="loadMessages()">← Back</button>
                <div class="chat-header-info">
                    <div class="chat-header-avatar">${matchName.charAt(0).toUpperCase()}</div>
                    <div>
                        <h3>${matchName}</h3>
                        <p class="chat-status">${matchUser ? matchUser.gender : ''}</p>
                    </div>
                </div>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                ${messages.length === 0 ? '<div class="chat-empty">No messages yet. Start the conversation!</div>' : ''}
                ${messages.map(msg => `
                    <div class="chat-message ${msg.senderId == userId ? 'sent' : 'received'}">
                        <div class="message-content">${escapeHtml(msg.text)}</div>
                        <div class="message-time">${msg.time}</div>
                    </div>
                `).join('')}
            </div>
            
            <div class="chat-input-container">
                <input type="text" 
                       id="chatInput" 
                       class="chat-input" 
                       placeholder="Type a message..."
                       onkeypress="handleChatKeyPress(event)">
                <button class="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>
    `;
    
    messagesContent.innerHTML = html;
    
    // Scroll to bottom
    setTimeout(() => {
        const chatMessagesEl = document.getElementById('chatMessages');
        if (chatMessagesEl) {
            chatMessagesEl.scrollTop = chatMessagesEl.scrollHeight;
        }
        document.getElementById('chatInput').focus();
    }, 100);
}

// Handle Enter key in chat input
function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Send message
function sendMessage() {
    const input = document.getElementById('chatInput');
    const messageText = input.value.trim();
    
    if (!messageText || !currentChatUserId || !currentChatMatchId) return;
    
    const chatKey = `${currentChatUserId}_${currentChatMatchId}`;
    if (!chatMessages[chatKey]) {
        chatMessages[chatKey] = [];
    }
    
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    
    // Add sent message
    chatMessages[chatKey].push({
        senderId: currentChatUserId,
        text: messageText,
        time: timeString
    });
    
    // Clear input
    input.value = '';
    
    // Refresh chat display
    openChat(currentChatUserId, currentChatMatchId, allUsers.find(u => u.id == currentChatMatchId).name);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show add user modal
function showAddUserModal() {
    document.getElementById('addUserModal').style.display = 'block';
}

// Close add user modal
function closeAddUserModal() {
    document.getElementById('addUserModal').style.display = 'none';
    // Reload users after adding
    loadAllUsers();
}

// Listen for messages from iframe
window.addEventListener('message', function(event) {
    if (event.data === 'userAdded') {
        closeAddUserModal();
        loadAllUsers();
    }
});

window.onclick = function(event) {
    const modal = document.getElementById('addUserModal');
    if (event.target == modal) {
        closeAddUserModal();
    }
}

