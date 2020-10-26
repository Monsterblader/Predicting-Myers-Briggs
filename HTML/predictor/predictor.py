from sklearn.feature_extraction.text import TfidfTransformer
import nltk
import pickle
import re
import time
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from nltk.stem import WordNetLemmatizer
import psycopg2 as pg


def load_data_set():
    """Opens the MyersBriggs database and returns its contents.

    Returns:
        DataFrame: 'type', 'posts'
    """
    connection_args = {
        'host': 'localhost',  # We are connecting to our _local_ version of psql
        'dbname': 'myersbriggs',    # DB that we are connecting to
        'port': 5432          # port we opened on AWS
    }
    connection = pg.connect(**connection_args)  # What is that "**" there??
    cursor = connection.cursor()
    postgreSQL_select_query = "SELECT * FROM raw_data;"

    try:
        cursor.execute(postgreSQL_select_query)
        connection.commit()
        contents = cursor.fetchall()
    except (Exception, pg.DatabaseError) as error:
        print("Error: %s" % error)
        connection.rollback()
        cursor.close()
        contents = 1

    cursor.close()
    connection.close()

    return contents


def sanitize_posts(source):
    """Strips punctuation, numbers from posts, otherwise cleans, and lemmatizes text.

    Args:
        source (list-like): text
    """
    documents = []
    stemmer = WordNetLemmatizer()

    for sen in range(0, len(source)):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(source.iloc[sen]))

        # remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Converting to Lowercase
        document = document.lower()

        # Lemmatization
        document = document.split()

        document = [stemmer.lemmatize(word) for word in document]
        document = ' '.join(document)

        documents.append(document)

    return documents


def predict_personality(user_post="Hi, everyone!  I’m a San Francisco native who attended Caltech in Pasadena and has spent time all over the country.  My favorite cities are San Francisco, Boston, Raleigh, and Denver.  I am a bootcamp veteran, having acquired a skill set in web development, and where I, amazingly, met Josh Shaman who now works for Metis.  I bike, play piano, and dance in my spare time."):

    train_size = 0.8
    vectorizer_max_features = 1500
    chosen_classifier = MultinomialNB

    myers_briggs = load_data_set()

    mb_df = pd.DataFrame(myers_briggs, columns=['type', 'posts'])
    types = sorted(mb_df['type'].unique())

    post_list = [re.split('\|\|\|+', post) for post in mb_df['posts']]
    post_df = pd.DataFrame(post_list)
    post_df.insert(loc=0, column='type', value=mb_df['type'])

    posts_by_type = {typ: mb_df[mb_df['type'] == typ] for typ in types}

    vertical_post_df = pd.read_csv(
        '../analysis/vertical_posts.csv', index_col=0)

    X, y = mb_df['posts'], mb_df['type']

    X_train_val, X_holdback, y_train_val, y_holdback = train_test_split(X, y)

    X_train_val, X_holdback, y_train_val, y_holdback = train_test_split(X, y)

    documents = sanitize_posts(X_train_val)

    vectorizer = CountVectorizer(max_features=vectorizer_max_features,
                                 min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
    X = vectorizer.fit_transform(X_train_val).toarray()

    tfidfconverter = TfidfTransformer()
    X = tfidfconverter.fit_transform(X).toarray()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_train_val, train_size=train_size, random_state=0)

    classifier = chosen_classifier()
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    with open('text_classifier', 'wb') as picklefile:
        pickle.dump(classifier, picklefile)

    with open('text_classifier', 'rb') as training_model:
        model = pickle.load(training_model)

    holdback_df = pd.DataFrame(
        zip(y_holdback, X_holdback), columns=('type', 'posts'))

    holdback_post_list = [re.split('\|\|\|+', post)
                          for post in holdback_df['posts']]
    holdback_post_df = pd.DataFrame(holdback_post_list)
    holdback_post_df.insert(loc=0, column='type', value=holdback_df['type'])

    def compress_posts(df):
        result = []
        df_length = range(len(df))

        for i in df_length:
            for j in range(57):
                if df.iloc[i][j] != None:
                    result.append([df['type'][i], df.iloc[i][j]])

        return pd.DataFrame(result, columns=('type', 'post'))

    vertical_holdback = compress_posts(holdback_post_df)

    documents = sanitize_posts(vertical_holdback['post'])

    vertical_X_holdback = vectorizer.transform(documents).toarray()
    vertical_X_holdback = tfidfconverter.fit_transform(
        vertical_X_holdback).toarray()
    pred_holdback = classifier.predict(vertical_X_holdback)

    classifier.predict_proba(vertical_X_holdback)

    trans_user = vectorizer.transform([user_post]).toarray()
    trans_user = tfidfconverter.fit_transform(trans_user).toarray()

    return classifier.predict(trans_user)[0]
