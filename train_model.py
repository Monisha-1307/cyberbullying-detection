from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Sample training data
texts = [
    "You are so stupid",
    "I hate you",
    "You look ugly",
    "Have a great day",
    "You are amazing",
    "That was a nice post"
]
labels = [1, 1, 1, 0, 0, 0]  # 1 = bullying, 0 = safe

# Train model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
clf = LogisticRegression()
clf.fit(X, labels)

# Save model + vectorizer into model.pkl
with open('model.pkl', 'wb') as f:
    pickle.dump((vectorizer, clf), f)

print("✅ model.pkl created successfully!")
