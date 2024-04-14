import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

from Essentials import Package_Tag, Txt_package, Pipeline_Actor

class Text_Evaluator(Pipeline_Actor):
    def __init__(self, data_path: str):
        self.data = pd.read_csv(data_path)
        self.train, test = train_test_split(self.data, test_size=0.1, shuffle=True)
        self.train.reset_index(inplace=True)
        test.reset_index(inplace=True)

        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(self.train.offer)
        y = self.train.accepted.values

        self.clf_lr = LogisticRegression(max_iter=100000)
        self.clf_lr.fit(X, y)

    def evaluate_package(self, package: Txt_package):
        input_txt = package.txt
        series = pd.Series(input_txt)
        X_input = self.vectorizer.transform(series)
        score = self.clf_lr.predict_proba(X_input)[0][1]

        return Txt_package(package.txt, score, package.tag)

    def get_packages(self, packages: [Txt_package]):
        return_packages = []
        for package in packages:
            return_packages.append(self.evaluate_package(package))
        return return_packages
