from sklearn.feature_extraction.text import TfidfTransformer
import pickle
import re
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
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


def predict_personality_full(user_post="Hi, everyone!  I’m a San Francisco native who attended Caltech in Pasadena and has spent time all over the country.  My favorite cities are San Francisco, Boston, Raleigh, and Denver.  I am a bootcamp veteran, having acquired a skill set in web development, and where I, amazingly, met Josh Shaman who now works for Metis.  I bike, play piano, and dance in my spare time."):
    train_size = 0.8
    random_state = 56

    oversample_size = 1000
    vectorizer_max_features = 1500
    chosen_classifier = MultinomialNB

    myers_briggs = load_data_set()

    mb_df = pd.DataFrame(myers_briggs, columns=['type', 'posts'])

    X_nat, y_nat = mb_df['posts'], mb_df['type']
    X_train_val, X_holdback, y_train_val, y_holdback = train_test_split(
        X_nat, y_nat)
    sanitized_train_val = sanitize_posts(X_train_val)
    X_train, X_val, y_train, y_val = train_test_split(
        sanitized_train_val, y_train_val, train_size=train_size, random_state=random_state)

    ros = RandomOverSampler(sampling_strategy={"ENFJ": oversample_size, "ENTJ": oversample_size, "ESFJ": oversample_size, "ESFP": oversample_size, "ESTJ": oversample_size,
                                               "ESTP": oversample_size, 'ISFJ': oversample_size, 'ISFP': oversample_size, 'ISTJ': oversample_size, 'ISTP': oversample_size})
    X_train_ros, y_train_ros = ros.fit_sample(
        pd.DataFrame(X_train, columns=['posts']), y_train)

    vectorizer = CountVectorizer(max_features=vectorizer_max_features,
                                 min_df=5, max_df=0.7, stop_words=stopwords.words('english'))
    X_vectorized = vectorizer.fit_transform(X_train_ros['posts']).toarray()

    tfidfconverter = TfidfTransformer()
    X_tfidf = tfidfconverter.fit_transform(X_vectorized).toarray()

    classifier = chosen_classifier()
    classifier.fit(X_tfidf, y_train_ros)

    with open('text_vectorizer', 'wb') as picklefile:
        pickle.dump(vectorizer, picklefile)

    with open('text_tfidf', 'wb') as picklefile:
        pickle.dump(tfidfconverter, picklefile)

    with open('text_classifier', 'wb') as picklefile:
        pickle.dump(classifier, picklefile)

    with open('text_vectorizer', 'rb') as training_model:
        text_vectorizer = pickle.load(training_model)

    with open('text_tfidf', 'rb') as training_model:
        text_tfidf = pickle.load(training_model)

    with open('text_classifier', 'rb') as training_model:
        text_classifier = pickle.load(training_model)

    user_vectorized = text_vectorizer.transform([user_post]).toarray()
    user_tfidf = text_tfidf.fit_transform(user_vectorized).toarray()

    return text_classifier.predict(user_tfidf)[0]


def predict_personality(user_post="Hi, everyone!  I’m a San Francisco native who attended Caltech in Pasadena and has spent time all over the country.  My favorite cities are San Francisco, Boston, Raleigh, and Denver.  I am a bootcamp veteran, having acquired a skill set in web development, and where I, amazingly, met Josh Shaman who now works for Metis.  I bike, play piano, and dance in my spare time."):
    with open('text_vectorizer', 'rb') as training_vectorizer:
        vectorizer = pickle.load(training_vectorizer)
    with open('text_tfidf', 'rb') as training_tdidf:
        tfidfconverter = pickle.load(training_tdidf)
    with open('text_classifier', 'rb') as training_classifier:
        classifier = pickle.load(training_classifier)

    user_vectorized = vectorizer.transform([user_post]).toarray()
    user_tfidf = tfidfconverter.fit_transform(user_vectorized).toarray()

    return classifier.predict(user_tfidf)[0]
