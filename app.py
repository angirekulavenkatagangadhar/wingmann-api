from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import re
import os
from datetime import datetime
from functools import wraps
from collections import OrderedDict

app = Flask(__name__)

# JSON file path
JSON_DATA_FILE = 'users_data.json'
DB_FILE = 'wingmann.db'

# Database initialization
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  gender TEXT NOT NULL,
                  phone TEXT NOT NULL,
                  answers TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def init_json_file():
    if not os.path.exists(JSON_DATA_FILE):
        with open(JSON_DATA_FILE, 'w') as f:
            json.dump([], f)

def save_to_json(user_data):
    """Save user data to JSON file"""
    if os.path.exists(JSON_DATA_FILE):
        with open(JSON_DATA_FILE, 'r') as f:
            users = json.load(f)
    else:
        users = []
    
    if 'answers' in user_data and isinstance(user_data['answers'], dict):
        sorted_items = sorted(user_data['answers'].items(), key=lambda x: int(x[0]))
        user_data['answers'] = OrderedDict(sorted_items)
    
    users.append(user_data)
    
    for user in users:
        if 'answers' in user and isinstance(user['answers'], dict):
            sorted_items = sorted(user['answers'].items(), key=lambda x: int(x[0]))
            user['answers'] = OrderedDict(sorted_items)
    
    with open(JSON_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

def get_all_users_from_json():
    """Get all users from JSON file"""
    if os.path.exists(JSON_DATA_FILE):
        with open(JSON_DATA_FILE, 'r') as f:
            users = json.load(f)
            for user in users:
                if 'answers' in user and isinstance(user['answers'], dict):
                    sorted_items = sorted(user['answers'].items(), key=lambda x: int(x[0]))
                    user['answers'] = OrderedDict(sorted_items)
            return users
    return []

init_db()
init_json_file()

# Question weights
QUESTION_WEIGHTS = {
    1: 3, 2: 5, 3: 4, 4: 4, 5: 5,
    6: 4, 7: 4, 8: 4, 9: 5, 10: 4,
    11: 5, 12: 4, 13: 4, 14: 2, 15: 4,
    16: 5, 17: 4, 18: 5, 19: 4, 20: 2,
    21: 5, 22: 5, 23: 3, 24: 3, 25: 3
}

# Matching rules for compatibility
MATCHING_RULES = {
    1: {
        "high": [(1,1),(2,2),(3,3),(4,4)],
        "moderate": [(1,4),(2,4),(3,4)],
        "low": [(1,2),(1,3),(2,3)]
    },
    2: {
        "high": [(1,1),(3,3),(1,3),(2,2)],
        "moderate": [(2,3),(2,1)],
        "low": [(1,4),(2,4),(3,4),(4,4)]
    },
    3: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    4: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    5: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
                 (1,2),(1,3),(1,4),(1,5),(1,7),(2,3),(4,3),(5,3),(7,3),(2,5),(2,7),(4,5),(5,7)],
        "moderate": [(2,4),(4,7)],
        "low": [(6,1),(6,2),(6,3),(6,4),(6,5),(6,7)]
    },
    6: {
        "high": [(1,1),(2,2),(2,4)],
        "moderate": [(1,3),(1,2)],
        "low": [(3,3),(3,4),(4,4),(2,3),(1,4)]
    },
    7: {
        "high": [(1,1),(2,2),(3,3),(4,4),(1,4)],
        "moderate": [(1,3),(2,4)],
        "low": [(1,2),(2,3),(3,4)]
    },
    8: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    9: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    10: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    11: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    12: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    13: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    14: {
        "high": [(1,1),(2,2)],
        "moderate": [(1,2),(1,3),(1,4)],
        "low": [(3,3),(2,4),(2,3),(4,4),(3,4)]
    },
    15: {
        "high": [(1,1)],
        "moderate": [(2,2),(1,2),(1,3),(1,4)],
        "low": [(3,3),(3,4),(4,3),(2,3),(3,2),(4,4),(2,4),(4,2)]
    },
    16: {
        "high": [(1,1),(2,2),(3,3),(4,4),(5,5),(1,2),(4,5)],
        "moderate": [(1,3),(2,3),(3,4),(3,5)],
        "low": [(1,4),(1,5),(2,4),(2,5)]
    },
    17: {
        "high": [(4,4),(5,5),(4,5)],
        "moderate": [(1,3),(2,3),(3,3),(3,4),(3,5)],
        "low": [(1,1),(2,2),(1,2),(1,4),(1,5),(2,4),(2,5)]
    },
    18: {
        "high": [(2,2),(3,3),(4,4)],
        "moderate": [(3,4),(2,3)],
        "low": [(1,1),(2,4),(1,2),(1,3),(1,4)]
    },
    19: {
        "high": [(1,1),(2,2),(1,2)],
        "moderate": [(1,3),(2,3),(3,3),(3,4),(3,5)],
        "low": [(4,4),(5,5),(4,5),(2,4),(2,5),(1,4),(1,5)]
    },
    20: {
        "high": [(1,1),(2,2),(1,2),(4,4),(5,5),(4,5)],
        "moderate": [(1,3),(2,3),(3,3),(2,4),(1,4)],
        "low": [(1,5),(2,5),(4,3),(5,3)]
    },
    21: {
        "high": [(4,4),(5,5),(4,5)],
        "moderate": [(3,3),(3,4),(3,5),(2,3),(1,3)],
        "low": [(1,1),(2,2),(1,2),(1,4),(1,5),(2,4),(2,5)]
    },
    22: {
        "high": [(4,4),(5,5),(4,5)],
        "moderate": [(3,3),(3,4),(3,5),(1,3)],
        "low": [(1,1),(2,2),(1,2),(2,3),(2,4),(2,5),(1,5),(1,4)]
    },
    23: {
        "high": [(1,1),(2,2),(1,3),(2,3),(1,2)],
        "moderate": [(3,4),(3,5),(3,3),(4,4)],
        "low": [(5,5),(1,5),(2,5),(1,4),(2,4),(4,5)]
    },
    24: {
        "high": [(1,1)],
        "moderate": [(1,2),(1,4),(2,2),(4,4),(3,3)],
        "low": [(2,4),(2,3),(3,4),(1,3)]
    },
    25: {
        "high": [(1,1),(3,3),(1,3)],
        "moderate": [(2,2),(1,2),(4,4),(2,3),(3,4)],
        "low": [(1,4),(2,4)]
    }
}

# NLP categories for Question 5
Q5_CATEGORIES = {
    1: ["love", "care", "affection", "warmth", "emotional support", "kindness", "compassion", "maturity"],
    2: ["honesty", "loyalty", "transparency", "dependability", "faithfulness", "reliability"],
    3: ["openness", "communication", "listening", "understanding", "expressing emotions", "patience"],
    4: ["support", "respect", "equality", "appreciation", "independence", "space", "boundaries"],
    5: ["growth", "teamwork", "understanding", "adaptive", "flexible", "supporting goals", "solving"],
    6: ["sex", "sharing experiences", "adventure", "chemistry", "humour", "humor", "emotional connection"],
    7: ["commitment", "safety", "consistency", "partnership", "togetherness"]
}

QUESTION_OPTIONS = {
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
}


def get_answer_label(question_num: int, raw_value):
    """Return human-readable label for an answer, falling back to the raw value."""
    
    if question_num == 5:
        return str(raw_value)

    try:
        key = int(raw_value)
    except (TypeError, ValueError):
        return str(raw_value)

    options = QUESTION_OPTIONS.get(question_num)
    if options is None:
        return str(raw_value)

    return options.get(key, str(raw_value))

def categorize_q5_answer(text):
    """Categorize descriptive answer for Question 5 using semantic analysis
    
    Uses conceptual matching based on word meanings and relationships:
    1. Keyword matching for known terms
    2. Semantic concept matching for new/unseen words
    3. Word root analysis for better coverage
    """
    if not text or not isinstance(text, str):
        return 3  # Default to Communication category
    
    text_lower = text.lower().strip()
    words = text_lower.split()
    
    # Core keywords for each category (from original document)
    core_keywords = {
        1: ["love", "care", "affection", "warmth", "emotional support", "kindness", "compassion", "maturity"],
        2: ["honesty", "loyalty", "transparency", "dependability", "faithfulness", "reliability"],
        3: ["openness", "communication", "listening", "understanding", "expressing emotions", "patience"],
        4: ["support", "respect", "equality", "appreciation", "independence", "space", "boundaries"],
        5: ["growth", "teamwork", "understanding", "adaptive", "flexible", "supporting goals", "solving"],
        6: ["sex", "sharing experiences", "adventure", "chemistry", "humour", "humor", "emotional connection"],
        7: ["commitment", "safety", "consistency", "partnership", "togetherness"]
    }
    
    # Semantic concept mappings - maps concepts to categories
    semantic_concepts = {
        # Category 1: Emotional values - concepts related to feelings, emotions, care
        1: {
            "concepts": ["forgiveness", "forgive", "forgiving", "mercy", "compassion", "empathy", 
                        "emotional", "feelings", "heart", "soul", "warmth", "tenderness"],
            "word_roots": ["forgiv", "compass", "empath", "emot", "feel", "heart", "soul"]
        },
        # Category 2: Trust & Integrity - concepts related to honesty, reliability, responsibility
        2: {
            "concepts": ["accountability", "accountable", "responsibility", "responsible", "integrity",
                        "honest", "trust", "reliable", "dependable", "faithful", "loyal"],
            "word_roots": ["account", "responsib", "integrit", "honest", "trust", "reliab", "depend", "faith", "loyal"]
        },
        # Category 3: Communication - concepts related to talking, expressing, understanding
        3: {
            "concepts": ["communication", "talk", "discuss", "express", "listen", "understand", 
                        "dialogue", "conversation", "share", "open"],
            "word_roots": ["communicat", "talk", "discuss", "express", "listen", "understand", "dialogue", "share"]
        },
        # Category 4: Respect & Equality - concepts related to respect, boundaries, fairness
        4: {
            "concepts": ["respect", "equality", "equal", "fair", "fairness", "boundaries", 
                        "privacy", "independence", "autonomy", "freedom"],
            "word_roots": ["respect", "equal", "fair", "boundar", "privac", "independ", "autonom", "freedom"]
        },
        # Category 5: Growth & Companionship - concepts related to improvement, teamwork, development
        5: {
            "concepts": ["growth", "grow", "improve", "develop", "evolve", "learn", "progress",
                        "teamwork", "collaboration", "partnership", "together"],
            "word_roots": ["grow", "improv", "develop", "evolv", "learn", "progress", "team", "collabor", "partner"]
        },
        # Category 6: Fun & Connection - concepts related to enjoyment, excitement, intimacy
        6: {
            "concepts": ["fun", "enjoyment", "excitement", "adventure", "passion", "romance",
                        "intimacy", "chemistry", "humor", "laughter", "enjoy"],
            "word_roots": ["fun", "enjoy", "excit", "adventur", "passion", "romance", "intimac", "chemistr", "humor", "laugh"]
        },
        # Category 7: Stability - concepts related to commitment, security, consistency
        7: {
            "concepts": ["commitment", "commit", "stable", "stability", "consistent", "security",
                        "secure", "steady", "permanent", "long-term"],
            "word_roots": ["commit", "stabil", "consist", "secur", "steady", "perman", "long"]
        }
    }
    
    category_scores = {}
    category_positions = {}  
    
    for cat_id in range(1, 8):
        word_count = 0
        first_position = len(text_lower) 
        
        all_matches = set()
        
        for keyword in core_keywords[cat_id]:
            if keyword in text_lower:
                position = text_lower.find(keyword)
                if position < first_position:
                    first_position = position
                all_matches.add(keyword)
        
        concepts = semantic_concepts[cat_id]["concepts"]
        for concept in concepts:
            if concept in text_lower:
                position = text_lower.find(concept)
                if position < first_position:
                    first_position = position
                all_matches.add(concept)
        
        word_roots = semantic_concepts[cat_id]["word_roots"]
        for word in words:
            for root in word_roots:
                if word.startswith(root) or root in word:
                    position = text_lower.find(word)
                    if position < first_position:
                        first_position = position
                    all_matches.add(word)
                    break  
        word_count = len(all_matches)
        
        category_scores[cat_id] = word_count
        category_positions[cat_id] = first_position if word_count > 0 else len(text_lower)
    
   
    max_count = max(category_scores.values())
    
    if max_count > 0:
        top_categories = [cat_id for cat_id, count in category_scores.items() if count == max_count]
        
        if len(top_categories) > 1:
            
            best_category = min(top_categories, key=lambda cat_id: category_positions[cat_id])
        else:
            best_category = top_categories[0]
        
        return best_category
    
   
    if len(words) > 3:
        return 3  # Communication (most common for detailed answers)
    
    # Default to Category 3 (Communication) as it's most neutral/common
    return 3

def get_compatibility_level(question_num, answer1, answer2):
    """Get compatibility level (high/moderate/low) for a question"""
    if question_num not in MATCHING_RULES:
        return "low"
    
    rules = MATCHING_RULES[question_num]
    pair = (answer1, answer2)
    reverse_pair = (answer2, answer1)
    
    if pair in rules["high"] or reverse_pair in rules["high"]:
        return "high"
    elif pair in rules["moderate"] or reverse_pair in rules["moderate"]:
        return "moderate"
    else:
        return "low"

def calculate_compatibility(user1_answers, user2_answers, detailed=False):
    """Calculate compatibility score between two users
    
    Args:
        user1_answers: Dictionary of user1's answers
        user2_answers: Dictionary of user2's answers
        detailed: If True, returns detailed breakdown by question
    
    Returns:
        If detailed=False: float (compatibility percentage)
        If detailed=True: dict with 'total_score', 'percentage', and 'breakdown' list
    """
    total_score = 0
    breakdown = []
    
    # Question texts for display
    QUESTION_TEXTS = {
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
        25: "I've learned the most about relationships from:"
    }
    
    for q_num in range(1, 26):
        weight = QUESTION_WEIGHTS[q_num]
        answer1 = user1_answers.get(str(q_num))
        answer2 = user2_answers.get(str(q_num))
        
        if answer1 is None or answer2 is None:
            continue
        
        # Keep raw answers for label lookup before any numeric conversion
        original_answer1 = answer1
        original_answer2 = answer2
        
        # Handle Question 5 (descriptive) - convert to category first
        if q_num == 5:
            if isinstance(answer1, str):
                answer1 = categorize_q5_answer(answer1)
            if isinstance(answer2, str):
                answer2 = categorize_q5_answer(answer2)
        
        # Convert to int for comparison
        try:
            answer1_int = int(answer1)
            answer2_int = int(answer2)
        except (ValueError, TypeError):
            continue
        
        level = get_compatibility_level(q_num, answer1_int, answer2_int)
        
        if level == "high":
            compatibility_value = 2
        elif level == "moderate":
            compatibility_value = 1
        else:
            compatibility_value = 0
        
        question_score = weight * compatibility_value
        total_score += question_score
        
        if detailed:
            display_answer1 = get_answer_label(q_num, original_answer1)
            display_answer2 = get_answer_label(q_num, original_answer2)

            breakdown.append({
                'question_num': q_num,
                'question_text': QUESTION_TEXTS.get(q_num, f"Question {q_num}"),
                'weight': weight,
                'user1_answer': display_answer1,
                'user2_answer': display_answer2,
                'compatibility_level': level,
                'compatibility_value': compatibility_value,
                'question_score': question_score,
                'max_possible_score': weight * 2  # Max is high compatibility (2)
            })
    
    percentage = (total_score / 200) * 100
    
    if detailed:
        return {
            'total_score': total_score,
            'max_possible_score': 200,
            'percentage': round(percentage, 2),
            'breakdown': breakdown
        }
    else:
        return round(percentage, 2)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400
        
        name = data.get('name')
        gender = data.get('gender')
        phone = data.get('phone')
        answers = data.get('answers', {})
        
        # Validate required fields
        if not name or not gender or not phone:
            return jsonify({'success': False, 'error': 'Missing required fields (name, gender, phone)'}), 400
        
        if not answers or len(answers) != 25:
            return jsonify({'success': False, 'error': f'Invalid number of answers. Expected 25, got {len(answers)}'}), 400
        
        # Prepare user data
        user_data = {
            'name': name,
            'gender': gender,
            'phone': phone,
            'answers': answers,
            'created_at': datetime.now().isoformat()
        }
        
        # Save user to SQLite database
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO users (name, gender, phone, answers) VALUES (?, ?, ?, ?)',
                  (name, gender, phone, json.dumps(answers)))
        user_id = c.lastrowid
        conn.commit()
        conn.close()
        
        # Add ID to user_data and save to JSON
        user_data['id'] = user_id
        # Sort answers by question number before saving
        sorted_answers = OrderedDict(sorted(answers.items(), key=lambda x: int(x[0])))
        user_data['answers'] = dict(sorted_answers)
        save_to_json(user_data)
        
        # Get all other users of opposite gender
        opposite_gender = 'Female' if gender == 'Male' else 'Male'
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('SELECT id, name, answers FROM users WHERE gender = ? AND id != ?',
                  (opposite_gender, user_id))
        other_users = c.fetchall()
        conn.close()
        
        # Calculate compatibility scores
        compatibility_scores = []
        for other_user in other_users:
            other_id, other_name, other_answers_json = other_user
            other_answers = json.loads(other_answers_json)
            score = calculate_compatibility(answers, other_answers)
            compatibility_scores.append({
                'id': other_id,
                'name': other_name,
                'score': score
            })
        
        # Sort by score descending
        compatibility_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'success': True,
            'scores': compatibility_scores
        })
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in submit endpoint: {error_trace}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/add-user')
def add_user():
    """Page to add a new user"""
    return render_template('add_user.html')

@app.route('/all-compatibility')
def all_compatibility():
    """Page showing compatibility scores between all users"""
    return render_template('all_compatibility.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users from database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, gender, phone, answers, created_at FROM users ORDER BY created_at DESC')
    users = []
    for row in c.fetchall():
        users.append({
            'id': row[0],
            'name': row[1],
            'gender': row[2],
            'phone': row[3],
            'answers': json.loads(row[4]),
            'created_at': row[5]
        })
    conn.close()
    return jsonify(users)

@app.route('/api/compatibility/all', methods=['GET'])
def get_all_compatibility():
    """Get compatibility scores between all users (only opposite genders)"""
    user_id = request.args.get('user_id', type=int)
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, gender, answers FROM users')
    all_users = c.fetchall()
    conn.close()
    
    compatibility_matrix = []
    
    # If user_id is provided, only show compatibility for that user
    if user_id:
        # Find the selected user
        selected_user = None
        for user in all_users:
            if user[0] == user_id:
                selected_user = user
                break
        
        if not selected_user:
            return jsonify({'error': 'User not found'}), 404
        
        user1_id, user1_name, user1_gender, user1_answers_json = selected_user
        user1_answers = json.loads(user1_answers_json)
        
        # Calculate compatibility with all other users of opposite gender
        for user2 in all_users:
            user2_id, user2_name, user2_gender, user2_answers_json = user2
            
            # Skip same user and same gender
            if user2_id != user1_id and user1_gender != user2_gender:
                user2_answers = json.loads(user2_answers_json)
                score = calculate_compatibility(user1_answers, user2_answers)
                
                compatibility_matrix.append({
                    'user1': {
                        'id': user1_id,
                        'name': user1_name,
                        'gender': user1_gender
                    },
                    'user2': {
                        'id': user2_id,
                        'name': user2_name,
                        'gender': user2_gender
                    },
                    'score': score
                })
    else:
        # Show all compatibility pairs
        for i, user1 in enumerate(all_users):
            user1_id, user1_name, user1_gender, user1_answers_json = user1
            user1_answers = json.loads(user1_answers_json)
            
            for j, user2 in enumerate(all_users):
                if i < j:  # Only calculate once for each pair
                    user2_id, user2_name, user2_gender, user2_answers_json = user2
                    user2_answers = json.loads(user2_answers_json)
                    
                    # Only calculate compatibility for opposite genders
                    if user1_gender != user2_gender:
                        score = calculate_compatibility(user1_answers, user2_answers)
                        
                        compatibility_matrix.append({
                            'user1': {
                                'id': user1_id,
                                'name': user1_name,
                                'gender': user1_gender
                            },
                            'user2': {
                                'id': user2_id,
                                'name': user2_name,
                                'gender': user2_gender
                            },
                            'score': score
                        })
    
    # Sort by score descending
    compatibility_matrix.sort(key=lambda x: x['score'], reverse=True)
    
    return jsonify(compatibility_matrix)

@app.route('/api/json-data', methods=['GET'])
def get_json_data():
    """Get all users from JSON file"""
    users = get_all_users_from_json()
    # Re-save with sorted answers to fix any existing data
    if users:
        with open(JSON_DATA_FILE, 'w') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    return jsonify(users)

@app.route('/api/compatibility/detailed', methods=['GET'])
def get_detailed_compatibility():
    """Get detailed compatibility analysis between two users"""
    user1_id = request.args.get('user1_id', type=int)
    user2_id = request.args.get('user2_id', type=int)
    
    if not user1_id or not user2_id:
        return jsonify({'error': 'Both user1_id and user2_id are required'}), 400
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Get user1 data
    c.execute('SELECT id, name, gender, answers FROM users WHERE id = ?', (user1_id,))
    user1_data = c.fetchone()
    
    # Get user2 data
    c.execute('SELECT id, name, gender, answers FROM users WHERE id = ?', (user2_id,))
    user2_data = c.fetchone()
    
    conn.close()
    
    if not user1_data or not user2_data:
        return jsonify({'error': 'One or both users not found'}), 404
    
    user1_id_db, user1_name, user1_gender, user1_answers_json = user1_data
    user2_id_db, user2_name, user2_gender, user2_answers_json = user2_data
    
    user1_answers = json.loads(user1_answers_json)
    user2_answers = json.loads(user2_answers_json)
    
    detailed_analysis = calculate_compatibility(user1_answers, user2_answers, detailed=True)
    
    return jsonify({
        'user1': {
            'id': user1_id_db,
            'name': user1_name,
            'gender': user1_gender
        },
        'user2': {
            'id': user2_id_db,
            'name': user2_name,
            'gender': user2_gender
        },
        'analysis': detailed_analysis
    })

if __name__ == '__main__':
    app.run(debug=True)

