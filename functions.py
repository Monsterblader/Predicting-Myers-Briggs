import re
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
