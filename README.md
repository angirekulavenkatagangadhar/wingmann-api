# Wingmann - Compatibility Assessment Application

A sleek dating compatibility assessment application built with Flask, HTML, CSS, and JavaScript. This application helps users find their perfect match based on psychological compatibility questions.

## Features

- **25 Psychological Questions**: Comprehensive assessment covering:
  - Lifestyle & Value Alignment
  - Emotional Communication
  - Attachment & Comfort Zone
  - Conflict & Repair Patterns
  - Growth, Readiness & Emotional Maturity

- **Smart Compatibility Scoring**: 
  - Weighted algorithm based on question importance
  - NLP-based categorization for descriptive answers
  - Gender-filtered results

- **Modern Dark Theme UI**: 
  - Sleek, modern design
  - Responsive layout
  - Smooth animations and transitions

## Installation

1. **Clone or download the repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Fill out the onboarding form**:
   - Enter your name, gender, and phone number
   - Answer all 25 compatibility questions

2. **Submit the form**:
   - The system will calculate your compatibility scores with all users of the opposite gender
   - Results are displayed sorted by compatibility percentage

3. **View results**:
   - See compatibility scores with all matched users
   - Scores are displayed as percentages with visual progress bars

## Question Types

- **MCQ (Multiple Choice Questions)**: Select one option from multiple choices
- **Scale Questions**: Rate on a scale of 1-5 (1 = Completely Disagree, 5 = Completely Agree)
- **Descriptive Questions**: Free-text answers analyzed using NLP

## Compatibility Algorithm

The compatibility score is calculated using:
- **Question Weights**: Each question has a specific weight (total = 200)
- **Matching Rules**: High (2x), Moderate (1x), or Low (0x) compatibility multipliers
- **Final Score**: `(Total Score / 200) × 100`

## Database

The application uses SQLite to store user responses. The database file (`wingmann.db`) will be created automatically on first run.

## Project Structure

```
wingmann/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── wingmann.db            # SQLite database (created automatically)
├── templates/
│   ├── index.html        # Main assessment form
│   └── results.html      # Results display page
└── static/
    ├── style.css         # Dark theme styling
    └── script.js         # Frontend JavaScript
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite
- **NLP**: Keyword-based text categorization

## Notes

- The application filters results by gender (male users see only female users and vice versa)
- Question 5 uses NLP to categorize descriptive answers into predefined categories
- All compatibility rules and weights are based on the provided specification

## License

This project is created for the Wingmann dating application compatibility assessment.

