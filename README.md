# Resume Screening System

An AI/ML-powered web application that analyzes resumes against job descriptions using Natural Language Processing (NLP), machine learning techniques, and skill matching to help candidates understand how well their profiles align with job opportunities.

## Overview

The **AI Resume Analyzer & Job Matcher** is designed to simplify the initial resume screening process. It extracts relevant information from resumes, identifies skills, and compares candidate profiles with job descriptions to generate a matching score.

The project combines resume parsing, text preprocessing, similarity analysis, database integration, and a web-based interface in one application.

## Key Features

- **Resume Parsing:** Extracts text and relevant information from PDF resumes.
- **Skill Extraction:** Identifies skills from resume content using a skills dataset.
- **Job Description Matching:** Compares resume content against a given job description.
- **NLP-Based Analysis:** Uses text preprocessing and TF-IDF-based text representation.
- **Similarity Scoring:** Uses cosine similarity and skill overlap to calculate a resume-job match score.
- **User Authentication:** Provides registration and login interfaces.
- **Analysis History:** Includes an interface for viewing previous analyses.
- **Machine Learning Pipeline:** Includes scripts for model training, prediction, and evaluation.
- **Web Interface:** Provides pages for resume analysis, results, registration, and login.
- **Database Integration:** Stores application data through a dedicated database layer.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Machine Learning | Scikit-learn |
| NLP & Text Processing | TF-IDF, text preprocessing, cosine similarity |
| Resume Processing | PDF text extraction and information extraction |
| Database | Configured through the project's database module |
| Frontend | HTML, CSS, JavaScript |
| Data Processing | Pandas, NumPy |
| Testing | Pytest |
| Version Control | Git and GitHub |

## How It Works

1. **Resume Upload:** The user provides a resume in PDF format.
2. **Text Extraction:** The resume parser extracts readable text and relevant information.
3. **Preprocessing:** The extracted text and job description are processed for analysis.
4. **Skill Identification:** Relevant skills are extracted and compared.
5. **Similarity Analysis:** TF-IDF representations and cosine similarity are used to compare resume content with the job description.
6. **Match Score Calculation:** Text similarity and skill overlap contribute to the final matching score.
7. **Results Display:** The application presents the analysis results through its web interface.

## Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── config.py
├── init_db.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── models.py
│
├── resume_parser/
│   ├── __init__.py
│   ├── pdf_parser.py
│   ├── information_extractor.py
│   └── skill_extractor.py
│
├── ml/
│   ├── __init__.py
│   ├── preprocess.py
│   ├── predict.py
│   ├── train.py
│   └── evaluate.py
│
├── data/
│   ├── skills_master.csv
│   └── README.md
│
├── models/
│   └── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── analyzer.html
│   ├── results.html
│   └── history.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── tests/
    ├── __init__.py
    ├── test_parser.py
    ├── test_backend.py
    ├── test_ml.py
    └── fixtures/
        └── sample_resume.pdf
```

### Folder and File Descriptions

| File or Folder | Purpose |
|---|---|
| `app.py` | Main Flask application and application routes |
| `config.py` | Application configuration |
| `init_db.py` | Database initialization script |
| `database/` | Database connection and data models |
| `resume_parser/` | PDF parsing, information extraction, and skill extraction |
| `ml/` | Text preprocessing, prediction, model training, and evaluation |
| `data/` | Skill dataset and related documentation |
| `models/` | Directory for trained model artifacts and documentation |
| `templates/` | HTML pages for the application |
| `static/` | CSS stylesheets and JavaScript files |
| `tests/` | Automated tests for the parser, backend, and ML components |
| `requirements.txt` | Python package dependencies |
| `README.md` | Project documentation |

## Installation and Setup

### Prerequisites

- Python installed on your system
- Git
- A terminal or IDE such as Visual Studio Code

### 1. Clone the repository

```bash
git clone https://github.com/prashasti-25/Resume-Screening-System.git
```

### 2. Navigate to the project directory

```bash
cd Resume-Screening-System
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure the application

Review `config.py` and the database configuration in `database/database.py`. Set any required environment variables or database settings before running the application.

Keep credentials and secrets out of the repository. Do not commit your `.env` file or other private configuration files.

### 6. Initialize the database

```bash
python init_db.py
```

### 7. Run the application

```bash
python app.py
```

Open the local address displayed in your terminal, typically:

```text
http://127.0.0.1:5000
```

## Machine Learning Pipeline

The project includes a dedicated `ml/` module for the machine learning workflow.

- **Preprocessing:** Prepares text for downstream analysis.
- **Prediction:** Performs resume-job matching and score calculation.
- **Training:** Provides a script for training the project's classification model.
- **Evaluation:** Evaluates the trained classifier using available evaluation data.

Run the following commands from the project root when the required dependencies and data are available:

```bash
python -m ml.train
```

```bash
python -m ml.evaluate
```

The application's primary matching score uses text similarity and skill overlap. The training and evaluation scripts provide an additional classification workflow.

## Testing

Run the automated test suite from the project root:

```bash
pytest tests/ -v
```

Ensure that the required dependencies, test fixtures, and database configuration are available before running the tests.

## Current Scope and Future Enhancements

Potential future improvements include:

- More detailed skill-gap analysis
- Resume improvement suggestions
- Keyword coverage and missing-skill reports
- Support for additional resume formats
- Expanded datasets and model evaluation
- Improved authentication and account security
- More comprehensive test coverage
- Deployment to a production hosting platform

These are possible enhancements rather than claims about features already implemented.

## Team Collaboration

This project is developed collaboratively using Git and GitHub. Development work is organized into feature branches, allowing team members to work on separate components before integrating their changes into the `main` branch.

Contributions should be tested and reviewed before being merged.

## Disclaimer

The matching score is an estimate of similarity between a resume and a job description. It should not be treated as a guarantee of employability or as the sole basis for recruitment decisions.

## Author

**Prashasti Bhatt**

AI Resume Analyzer & Job Matcher — a collaborative project exploring NLP, machine learning, resume parsing, and web application development.

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.
g files |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
