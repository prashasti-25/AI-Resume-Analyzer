# AI-Resume-Analyzer
An AI/ML based Resume Analyzer that evaluates resumes against job descriptions using NLP and Machine Learning.
## 📁 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│
├── models/
│
├── resume_parser/
│   ├── __init__.py
│   ├── pdf_parser.py
│   └── information_extractor.py
│
├── nlp/
│   ├── __init__.py
│   ├── preprocessing.py
│   └── similarity.py
│
├── ml/
│   ├── __init__.py
│   ├── train.py
│   ├── predict.py
│   └── evaluate.py
│
├── frontend/
│   └── components.py
│
├── utils/
│   └── helpers.py
│
└── tests/
```

### 📂 Folder Description

| File/Folder | Purpose |
|---|---|
| `app.py` | Main application entry point |
| `data/` | Datasets used for training and testing |
| `models/` | Trained ML models and saved model files |
| `resume_parser/` | Extracts text and information from resumes |
| `nlp/` | Text preprocessing and similarity calculations |
| `ml/` | Model training, prediction and evaluation |
| `frontend/` | User interface components |
| `utils/` | Helper functions |
| `tests/` | Testing files |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
