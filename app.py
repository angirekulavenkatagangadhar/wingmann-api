from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import os
from functools import lru_cache
from collections import OrderedDict

app = Flask(__name__)
# Enable CORS for all routes - allows external systems to call the API
CORS(app)

# Performance: Enable SQLite connection optimizations
sqlite3.enable_callback_tracebacks(False)

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
            breakdown.append({
                'question_num': q_num,
                'weight': weight,
                'user1_answer': str(original_answer1),
                'user2_answer': str(original_answer2),
                'compatibility_level': level,
                'compatibility_value': compatibility_value,
                'question_score': question_score,
                'max_possible_score': weight * 2
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

# API Routes

@app.route('/', methods=['GET'])
def index():
    """Root endpoint - API information"""
    return jsonify({
        'service': 'Wingmann Compatibility API',
        'version': '1.0',
        'endpoints': {
            'POST /api/compatibility/batch': 'Calculate compatibility scores between a user and multiple other users',
            'GET /health': 'Health check endpoint'
        },
        'documentation': 'See API_DOCUMENTATION.md for detailed usage'
    })

@app.route('/api/compatibility/batch', methods=['POST'])
def get_batch_compatibility():
    """Get compatibility scores between a user and multiple other users
    
    Request body (JSON):
    {
        "user_id": 1,
        "answers": {
            "1": "2",
            "2": "1",
            ...
            "25": "1"
        },
        "other_user_ids": [3, 5, 8]
    }
    
    Returns:
    {
        "user_id": 1,
        "compatibility_scores": [
            {"other_user_id": 3, "score": 75.5},
            {"other_user_id": 5, "score": 82.3},
            {"other_user_id": 8, "score": 68.2}
        ]
    }
    """
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        user_id = data.get('user_id')
        user_answers = data.get('answers')
        other_user_ids = data.get('other_user_ids', [])
        
        # Validate input
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        if not user_answers or not isinstance(user_answers, dict):
            return jsonify({'error': 'answers must be a dictionary with question numbers as keys'}), 400
        
        if not other_user_ids or not isinstance(other_user_ids, list):
            return jsonify({'error': 'other_user_ids must be a list of user IDs'}), 400
        
        if len(other_user_ids) == 0:
            return jsonify({'error': 'other_user_ids cannot be empty'}), 400
        
        # Connect to database with optimizations for speed
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        # Performance: Enable row factory for faster access
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Fetch other users from database - optimized single query
        placeholders = ','.join(['?'] * len(other_user_ids))
        c.execute(f'SELECT id, name, gender, answers FROM users WHERE id IN ({placeholders})', other_user_ids)
        other_users = c.fetchall()
        conn.close()
        
        # Check if all requested users were found
        found_user_ids = {user[0] for user in other_users}
        missing_user_ids = set(other_user_ids) - found_user_ids
        
        if missing_user_ids:
            return jsonify({
                'error': f'Users not found: {list(missing_user_ids)}'
            }), 404
        
        # Calculate compatibility scores - optimized for speed
        compatibility_scores = []
        
        # Pre-parse JSON answers once for all users
        for other_user in other_users:
            other_user_id = other_user[0]
            other_user_answers_json = other_user[3]
            
            # Fast JSON parsing
            try:
                other_user_answers = json.loads(other_user_answers_json)
            except json.JSONDecodeError:
                continue
            
            # Calculate compatibility score
            score = calculate_compatibility(user_answers, other_user_answers, detailed=False)
            
            compatibility_scores.append({
                'other_user_id': other_user_id,
                'score': score
            })
        
        # Sort by score (highest first) - in-place sort for speed
        compatibility_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'user_id': user_id,
            'compatibility_scores': compatibility_scores
        })
    
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON in request body'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Wingmann Compatibility API'})

if __name__ == '__main__':
    # For cloud deployment, use PORT from environment or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
