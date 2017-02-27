from flask import Flask, jsonify, render_template, request, redirect, url_for
import records

app = Flask(__name__)

DB = 'sqlite:///database.db'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie/', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':
        # get form data
        m_title = request.form.get('title').lower()
        m_year = request.form.get('year').lower()
        m_genre = request.form.get('genre').lower()
        m_description = request.form.get('description').lower()
        m_rating = request.form.get('rating').lower()
        print(m_title, m_year, m_genre, m_description, m_rating)

        db = records.Database(DB)  # connecting to database
        print("Connected to DB")
        tx = db.transaction()  # init db transaction
        try:
            print("Adding record")
            query = ('INSERT INTO movies (title, year, genre, '
                     'description, rating) VALUES(:title, :year, '
                     ':genre, :description, :rating)')
            print(query)
            db.query(query, title=m_title, year=m_year, genre=m_genre,
                     description=m_description, rating=m_rating)
            tx.commit()  # commit changes
            print("Success: record added")
        except:
            tx.rollback()  # rollback if error adding data
            print("Error adding record")
        finally:
            return redirect(url_for('index'))
    else:
        return render_template('add-movie.html')


@app.route('/movies/')
def movies_json():
    db = records.Database(DB)  # connecting to database
    print("Connected to DB")
    try:
        rows = db.query('SELECT * FROM movies')
        print("Success: all rows selected")
    except:
        print("Error retreiving records")
        pass
    finally:
        movies = {'movies': rows.as_dict()}
        return jsonify(movies)


@app.route('/search/<title>')
def title_search(title):
    db = records.Database(DB)  # connecting to database
    print("Connected to DB")
    try:
        query = 'SELECT * FROM movies WHERE title=:title'
        rows = db.query(query, title=title.lower())
        print("Success: rows selected")
    except:
        print("Error retrieving records")
        pass
    finally:
        movies = {'movies': rows.as_dict()}
        return jsonify(movies)


@app.route('/api/')
def api_details():
    return render_template('api.html')


@app.route('/all-movies/')
def all_movies():
    db = records.Database(DB)  # connecting to database
    print("Connected to DB")
    try:
        query = 'SELECT * FROM movies ORDER BY \
                 movies.rating DESC, movies.title'
        rows = db.query(query)
        print("Success: rows selected")
    except:
        pass
        print("Error retrieving records")
    finally:
        return render_template('all-movies.html', movies=rows)
