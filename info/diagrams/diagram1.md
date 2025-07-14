%%{init: {"themeVariables": {"fontSize": "16px", "nodeSpacing": 50, "rankSpacing": 100}}}%%
graph TD
    A[Docsity Sprint Platform] --> B[Educational Scrum Framework]
    A --> C[Adaptive Leitner Engine]
    A --> D[Growth Analytics Dashboard]
    
    B --> B1[Weekly Study Sprints]
    B --> B2[Personal Kanban Board]
    B --> B3[Virtual Standups]
    B --> B4[Exam Retrospectives]
    
    C --> C1[Smart Flashcards]
    C --> C2[Spaced Repetition AI]
    C --> C3[Weakness Prediction]
    C --> C4[Auto-Review Alerts]
    
    D --> D1[Mastery Curve]
    D --> D2[Focus Time Metrics]
    D --> D3[Score Forecast]
    D --> D4[Adaptive Recommendations]
    
    E[User] -->|Interaction| B
    E -->|Usage Data| C
    E -->|Performance| D
    D -->|Feedback| C
    C -->|Optimization| B
