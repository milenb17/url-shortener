
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="milenbelanger",
        user="milenbelanger",
        password="")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS books;')
cur.execute('CREATE TABLE urls (id serial PRIMARY KEY,'
                                 'url varchar (150) NOT NULL,'
                                 'key varchar (10) NOT NULL);'
                                 )


# Insert data into the table

"""
cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('Anna Karenina',
             'Leo Tolstoy',
             864,
             'Another great classic!')
            )
"""


conn.commit()

cur.close()
conn.close()