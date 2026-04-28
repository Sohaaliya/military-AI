import numpy as np
from model import WordModel

# Example dataset (replace with your 100-word dataset)
sentences = [
    "15 ___ ready",
    "cpu ___ temperature high"
]

labels = [
    "corps",
    "core"
]

X = []
y = []

from embed import encode
from preprocess import make_context

for s, label in zip(sentences, labels):
    word = "___"
    vec = encode(s)
    X.append(vec)
    y.append(label)

X = np.array(X)

model = WordModel()
model.train(X, y)

import joblib
joblib.dump(model, "trained_model.pkl")