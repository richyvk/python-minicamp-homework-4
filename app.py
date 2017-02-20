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

        m_title = request.form.get('title').lower()
        m_year = request.form.get('year').lower()
        m_genre = request.form.get('genre').lower()
        m_description = request.form.get('description').lower()
        m_rating = request.form.get('rating').lower()
        print(m_title, m_year, m_genre, m_description, m_rating)

        try:
            print("Adding record")
            db = records.Database(DB)
            print("Connected to DB")
            query = ('INSERT INTO movies (title, year, genre, '
                     'description, rating) VALUES(:title, :year, '
                     ':genre, :description, :rating)')
            print(query)
            db.query(query, title=m_title, year=m_year, genre=m_genre,
                     description=m_description, rating=m_rating)
            print("Success: record added")
        except:
            db.rollback()
            print("Error adding record")
        finally:
            return redirect(url_for('index'))
    else:
        return render_template('add-movie.html')


@app.route('/movies/')
def movies_json():
    try:
        db = records.Database(DB)
        print("Connected to DB")
        rows = db.query('SELECT * FROM movies')
        print("Success: all rows selected")
    except:
        db.rollback()
        print("Error retreiving records")
    finally:
        movies = {'movies': rows.as_dict()}
        return jsonify(movies)


@app.route('/search/<title>')
def title_search(title):
    try:
        db = records.Database(DB)
        print("Connected to DB")
        query = 'SELECT * FROM movies WHERE title=:title'
        rows = db.query(query,
                        title=title.lower())
        print("Success: rows selected")
    except:
        db.rollback()
        print("Error retrieving records")
    finally:
        movies = {'movies': rows.as_dict()}
        return jsonify(movies)


@app.route('/api/')
def api_details():
    return render_template('api.html')


@app.route('/all-movies/')
def all_movies():
    try:
        db = records.Database(DB)
        print("Connected to DB")
        query = 'SELECT * FROM movies ORDER BY movies.rating DESC, movies.title'
        rows = db.query(query)
        print("Success: rows selected")
    except:
        db.rollback()
        print("Error retrieving records")
    finally:
        # row_list = []
        # for row in rows:
        #     row_list.append(row.title)
        return render_template('all-movies.html', movies=rows)
