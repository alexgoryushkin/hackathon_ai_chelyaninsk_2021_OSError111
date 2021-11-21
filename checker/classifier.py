import os.path
import pickle

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

from operator import itemgetter

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score, accuracy_score
import regex
from transliterate import translit, detect_language

vectorizer = None
ovrc = None
data = None
mlb = None

def normalize(name):
    try:
        if regex.search(r'\p{IsLatin}', name):
            name = translit(name, language_code='ru')
    except TypeError:
        print(name)
    return regex.sub('[^А-Яа-я]+', ' ', name).strip()


def init(path_to_dataset : str):
    global vectorizer
    global ovrc
    global data
    global mlb

    if os.path.exists('vectorizer.pk') and os.path.exists('ovrc.pk'):
        try:
            with open('vectorizer.pk', 'rb') as fin:
                vectorizer = pickle.load(fin)
        except Exception as e:
            print(e)
        try:
            with open('ovrc.pk', 'rb') as fin:
                ovrc = pickle.load(fin)
        except Exception as e:
            print(e)
        try:
            with open('mlb.pk', 'rb') as fin:
                mlb = pickle.load(fin)
        except Exception as e:
            print(e)
        print('ok, load models')
        return

    print("Start clearing errors")
    data_p = pd.read_csv(path_to_dataset, sep='	').rename(columns={'c_name':'cat', 'c_id': 'id'})
    data_p['name'] = data_p['name'].map(lambda x: normalize(x))
    data_temp = data_p[data_p.duplicated() == True]

    for i in data_temp['name'].unique():
        new_id = data_temp[data_temp['name'] == i]['id'].value_counts().index[0]
        data_temp.loc[data_temp['name'] == i, 'id'] = data_temp.loc[data_temp['name'] == i, 'id'].map(lambda x: new_id)

    data = pd.concat([data_p[data_p.duplicated() == False], data_temp])
    # data = pd.read_csv(path_to_dataset,encoding='utf-8', sep=',')
    # data['name'] = data['name'].values.astype('U')
    vectorizer = TfidfVectorizer(min_df=5)
    vectorizer.fit(data['name'])
    mlb = MultiLabelBinarizer()

    # создаем объект pandas DataFrame: данные - результат преобразования MultiLabelBinarizer, названия столбцов - жанры
    y = pd.DataFrame(mlb.fit_transform([[i] for i in data.cat]), columns=mlb.classes_)
    X_train, X_test, y_train, y_test = train_test_split(data['name'], y, test_size=0.33, random_state=42)
    X_train_encoded = vectorizer.transform(X_train)
    X_test_encoded = vectorizer.transform(X_test)
    ovrc = OneVsRestClassifier(LogisticRegression(C=10), n_jobs=-1)
    ovrc.fit(X_train_encoded, y_train)
    preds = ovrc.predict(X_test_encoded)

    print(f1_score(y_test, preds, average='samples'), accuracy_score(y_test, preds))
    try:
        with open('vectorizer.pk', 'wb') as fin:
            pickle.dump(vectorizer, fin)
    except Exception as e:
        print(e)
    try:
        with open('ovrc.pk', 'wb') as fin:
            pickle.dump(ovrc, fin)
    except Exception as e:
        print(e)
    try:
        with open('mlb.pk', 'wb') as fin:
            pickle.dump(mlb, fin)
    except Exception as e:
        print(e)

def predict(description : str, threshold = 0.6):
    global vectorizer
    global ovrc
    global mlb

    vectorized = vectorizer.transform([description])

    preds_multi = ovrc.predict_proba(vectorized)
    preds_multi_labels = preds_multi.argpartition(-3, axis=1)[:,-3:]
    preds_multi_proba = [preds_multi[i][preds_multi_labels[i]] for i in range(len(preds_multi))]
    out_df = pd.DataFrame(data=[[description], [mlb.classes_[i] for i in preds_multi_labels], preds_multi_proba], index=['name', 'cat', 'proba']).T
    cats = out_df["cat"][0]
    probas = out_df["proba"][0]
    result = []
    for i in range(len(cats)):
        # if probas[i]<threshold:
        #     continue
        result.append((cats[i], probas[i]))
    result = sorted(result, key=itemgetter(1), reverse=True)
    result = [x for x, y in result]
    return result[0] if result else []


