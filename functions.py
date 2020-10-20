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
    postgreSQL_select_Query = "SELECT * FROM raw_data;"

    try:
        cursor.execute(postgreSQL_select_Query)
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
