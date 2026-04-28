from sklearn.linear_model import LogisticRegression

class WordModel:
    def __init__(self):
        self.model = LogisticRegression(max_iter=200)

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, x):
        return self.model.predict([x])[0]