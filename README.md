# Cyberbullying Detection — NLP Text Classification

A machine learning system that automatically detects cyberbullying in text messages and social media posts using Natural Language Processing techniques.

## Problem Statement
Online harassment and cyberbullying affect millions of users. This project builds a classifier that can identify harmful content across different categories — helping platforms automate content moderation at scale.

## Approach
1. **Data Preprocessing** — text cleaning, tokenization, stopword removal
2. **Feature Engineering** — TF-IDF vectorization to convert text to numerical features
3. **Model Training** — Logistic Regression and Decision Tree classifiers
4. **Evaluation** — Precision, Recall, F1-score across all classes

## Tech Stack
- **Language:** Python 3
- **ML Library:** Scikit-learn
- **NLP:** TF-IDF, Bag of Words (NLTK)
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Tools:** Jupyter Notebook, Git

## Results
| Metric | Score |
|--------|-------|
| Accuracy | [add your score] |
| Precision | [add your score] |
| Recall | [add your score] |
| F1-Score | [add your score] |

## Project Structure
```
cyberbullying-detection/
├── data/                  # Dataset files
├── notebooks/             # Jupyter notebooks
│   └── cyberbullying_detection.ipynb
├── src/                   # Python modules
│   ├── preprocessing.py   # Text cleaning
│   ├── features.py        # TF-IDF feature extraction
│   └── model.py           # Model training and evaluation
├── requirements.txt
└── README.md
```

## Setup Instructions
```bash
git clone https://github.com/Monisha-1307/cyberbullying-detection.git
cd cyberbullying-detection
pip install -r requirements.txt
jupyter notebook notebooks/cyberbullying_detection.ipynb
```

## Key Learnings
- NLP text preprocessing and feature engineering
- Multi-class text classification with Scikit-learn
- Model evaluation and performance analysis
- Modular Python code with OOP architecture

## Author
**Monisha N** — MCA Graduate, Bangalore
[LinkedIn](https://linkedin.com/in/monisha-n-9a63912b6) | [GitHub](https://github.com/Monisha-1307)
