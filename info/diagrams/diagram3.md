%%{init: {"themeVariables": {"fontSize": "15px", "nodeSpacing": 40, "rankSpacing": 100}}}%%
graph LR
    A[Content Library] --> B[AI Engine]
    B --> C[Leitner Module]
    C --> D{Forgetfulness Forecast}
    D --> E[(Save Results)]
    B --> F[Sprint Planner]
    F --> G[Growth Curve Dashboard]
    G --> H[Progress Analytics]
    H --> I[Mobile App]
    H -->|Feedback| B
