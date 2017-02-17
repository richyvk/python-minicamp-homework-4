import records


db = records.Database('sqlite:///database.db')
print('Database created')
QUERY = ('CREATE TABLE movies (title TEXT, year INTEGER, genre TEXT, '
         'description TEXT, rating INTEGER)')
db.query(QUERY)
print('Table created')
db.close()
print('Database closed')
